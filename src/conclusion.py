import os, torch, logging

from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer, AutoModelForQuestionAnswering
from transformers.utils import logging
from src.entity_recognition import Entity, NER
from src.utils import longest_common_substring

logging.get_logger("transformers").setLevel(logging.ERROR)

class Conclusion():
    def __init__(self, cache_dir=os.getenv('MODELS_CACHE','./models_cache/hub')) -> None:
        self.ec = NER(50)
        self.boolq_tokenizer = AutoTokenizer.from_pretrained("nfliu/deberta-v3-large_boolq", 
                                                             cache_dir=cache_dir)
        self.boolq_model = AutoModelForSequenceClassification.from_pretrained("nfliu/deberta-v3-large_boolq", 
                                                                              cache_dir=cache_dir)
        self.entity_pipeline = pipeline('question-answering', model="deepset/deberta-v3-base-squad2", 
                       tokenizer="deepset/deberta-v3-base-squad2",
                       cache_dir=os.getenv('MODELS_CACHE','./models_cache/hub'))
        # self.entityq_tokenizer = AutoTokenizer.from_pretrained("deepset/deberta-v3-base-squad2",
        #                                                        cache_dir=cache_dir)
        # self.entityq_model = AutoModelForQuestionAnswering.from_pretrained("deepset/deberta-v3-base-squad2",
        #                                                                    cache_dir=cache_dir)
        
    def conclude_yn(self, question, answer) -> str:
        """
        for boolean question and statement question, conclude yes or no
        """
        encoded_input = self.boolq_tokenizer([(question,answer)], padding=True, truncation=True, return_tensors="pt")

        with torch.no_grad():
            model_output = self.boolq_model(**encoded_input)
            probabilities = torch.softmax(model_output.logits, dim=-1).cpu().tolist()
        prob_no = [round(prob[0], 2) for prob in probabilities][0]
        prob_yes = [round(prob[1], 2) for prob in probabilities][0]
        if prob_no > prob_yes:
            return "no"
        else:
            return "yes"
        
    def conclude_entity(self, question, answer, entities: list[Entity]):
        '''
        Return entity if possible, string if no match.
        '''
        nlp = self.entity_pipeline
        
        ret = nlp(question=question, context=answer)['answer']
        
        e_in_ret = self.ec.recognize(ret)
        if len(e_in_ret)==0:
            for e in entities:
                if e.mention in question:
                    return e
            return ret
        
        entities = [e for e in entities if e.wikipedia_link!=""]
        e_with_score = [(e, longest_common_substring(e.mention, ret)[0]) for e in entities]
        e_with_score.sort(key=lambda x: x[1], reverse=True)

        if len(e_with_score)>0:
            return e_with_score[0][0]

        return ret
    





if __name__ == "__main__":
    a = "ABCDABC"
    b = "AB AB DAB AC DAB"
    # print(longest_common_substring(a, b))
    # conclusion = Conclusion()
    # qa = ("Is the sky blue?", "The sky is red.")
    # assert conclusion.conclude_yn(*qa) == "no"
    # qa = ("Is the sky blue?", "The sky is azure.")
    # assert conclusion.conclude_yn(*qa) == "yes"
    # qa = ("Apple is the largest company by revenue", "In the fiscal year 2021, Apple was the largest company by revenue.")
    # assert conclusion.conclude_yn(*qa) == "yes"
    # qa = ("Apple is the largest company by revenue", "That's not entirely accurate. According to the latest available data (2022), the largest company in the world by revenue is actually Amazon.  As of 2022, Amazon's market capitalization was over $1 trillion, and its annual revenue was over $478 billion. Apple's market capitalization was around $2")
    # assert conclusion.conclude_yn(*qa) == "no"

    # qa = ("What is the capital of France?", "Paris is the capital of France.",[])
    # assert conclusion.conclude_entity(*qa) == "Paris"
    