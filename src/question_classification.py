import os,torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

QUESTION_TYPE_STATEMENT = 'statement' # Cayde-6 is the best vanguard.
QUESTION_TYPE_BOOLEAN = 'boolean' # Is Cayde-6 the best vanguard?
QUESTION_TYPE_ENTITY = 'entity' # Who is the best vanguard?

class QuestionClassifier():
    def __init__(self, cache_dir=os.getenv('MODELS_CACHE','./models_cache/hub')):
        # tell question from statement
        self.question_tokenizer = AutoTokenizer.from_pretrained("shahrukhx01/question-vs-statement-classifier",
                                                                 cache_dir=cache_dir)
        self.question_model = AutoModelForSequenceClassification.from_pretrained("shahrukhx01/question-vs-statement-classifier"
                                                                                 , cache_dir=cache_dir)

        # tell boolean question from entity question
        self.boolq_tokenizer = AutoTokenizer.from_pretrained("PrimeQA/tydiqa-boolean-question-classifier"
                                                             , cache_dir=cache_dir)
        self.boolq_model = AutoModelForSequenceClassification.from_pretrained("PrimeQA/tydiqa-boolean-question-classifier"
                                                                              , cache_dir=cache_dir)
    
    def classify(self, question:str):
        inputs = self.question_tokenizer(question, return_tensors="pt")

        with torch.no_grad():
            logits = self.question_model(**inputs).logits

        predicted_class_id = logits.argmax().item()
        if predicted_class_id == 0:
            return QUESTION_TYPE_STATEMENT


        inputs = self.boolq_tokenizer(question, return_tensors="pt")
        with torch.no_grad():
            logits = self.boolq_model(**inputs).logits

        predicted_class_id = logits.argmax().item()
        if predicted_class_id == 0:
            return QUESTION_TYPE_ENTITY
        else:
            return QUESTION_TYPE_BOOLEAN

if __name__ == '__main__':
    qc = QuestionClassifier()
    assert qc.classify("Is the sky blue?") == QUESTION_TYPE_BOOLEAN
    assert qc.classify("Sky is blue.") == QUESTION_TYPE_STATEMENT
    assert qc.classify("What is the color of the sky") == QUESTION_TYPE_ENTITY

    assert qc.classify("What is the capital of France?") == QUESTION_TYPE_ENTITY
    assert qc.classify("Who is the president of the United States?") == QUESTION_TYPE_ENTITY
    
    assert qc.classify("The best vanguard is Cayde-6.") == QUESTION_TYPE_STATEMENT
    assert qc.classify("Who is the best vanguard") == QUESTION_TYPE_ENTITY
    assert qc.classify("Igneous Hammer is the best 120 hand cannon") == QUESTION_TYPE_STATEMENT
    assert qc.classify("What is the best 120 hand cannon") == QUESTION_TYPE_ENTITY