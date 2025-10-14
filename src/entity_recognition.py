import spacy
import logging,os

from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
from logging import getLogger,ERROR


getLogger("tokenizers").setLevel(ERROR)


class Entity:
    def __init__(self, mention, label, context, start, end):
        self.mention = mention
        self.label = label
        self.context = context
        self.start = start
        self.end = end
        self.wikipedia_link = ""
        self.kb_id = ""
        self.wiki_first_para = ""

    def __str__(self):
        return f"{self.mention} : {self.label} {self.start}:{self.end}\n{self.context}\n{self.wikipedia_link}\n{self.kb_id}\n"

    def __repr__(self):
        return self.__str__()

    def get_wikipedia_page(self):
        if self.wikipedia_link:
            return self.wikipedia_link
        else:
            return "unknown"


class NER:
    def __init__(self, context_diameter:int,cache_dir=os.getenv('MODELS_CACHE','./models_cache/hub')):
        # in number of tokens, will extract 2*context_diameter tokens around the entity
        self.context_diameter = context_diameter
        self.nlp = spacy.load("en_core_web_sm")
        self.tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER", cache_dir=cache_dir)
        self.model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER",cache_dir=cache_dir)
        

    
    def double_check(self, entity:Entity)->list[Entity]:
        """
        Double check if the entity can be divided into two entities
        """
        
        nlp = pipeline('ner', model=self.model,tokenizer=self.tokenizer, aggregation_strategy = 'simple')
        result = nlp(entity.mention)
        if len(result) <= 1:
            return [entity]
        ret = []
        for i in result:
            e = Entity(i['word'], i['entity_group'], entity.context, i['start'], i['end'])
            ret.append(e)
        return ret


    # discarded luke because
    # 1) false-positive "Yes" in
    #       "Yes, the monarch of England is also the monarch of Canada. surely you know that. 
    #       but what you probably don’t know is that the monarch of England is also the monarch of Australia, 
    #       New Zealand, Antigua, Barbuda, Bahamas, Barbados, Belize, Grenada, Jamaica"
    # 2) can't recongize anything in 
    #       "The largest company in the world by revenue is Wal-Mart B: 
    #       The largest company in the world by revenue is Samsung C: 
    #       The largest company in the world by revenue is Microsoft D: 
    #       The largest company in the world by revenue is Google Answer: C"
    def recognize(self, text):
        """
        Recognizes entities in the provided text.

        Args:
        text (str): The input text to recognize entities in.

        Returns:
        list: A list of recognized entities with their labels and context.
        """

        ret = {}
        doc = self.nlp(text)
        for i in doc.ents:
            label = i.label_
            if label in ["MONEY","DATE","QUANTITY","ORDINAL","CARDINAL","PERCENT","TIME",]:
                continue

            context_start_token = max(i.start - self.context_diameter, 0)
            context_end_token = min(i.end + self.context_diameter, len(doc))
            mention = i.text
            sp = mention.split("(")
            mention = mention.strip()
            if len(sp) > 1 and len(sp[0]) > 1: # avoid corner case like "U.K. (United Kingdom)"
                mention = sp[0]
            if mention.startswith("the "):
                mention = mention[4:]

            # if mention not in ret:
            #     ret[mention] = Entity(mention, label,
            #                            doc[context_start_token:context_end_token].text,
            #                            i.start_char,i.end_char)
            new_entity = Entity(mention, label,
                                       doc[context_start_token:context_end_token].text,
                                       i.start_char,i.end_char)
            checked_entities = self.double_check(new_entity)
            for e in checked_entities:
                if e.mention not in ret:
                    ret[e.mention] = e
        
        for e in ret.values():
            logging.info(e)

        return list(ret.values())



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    ner = NER(1)
    text = """Apple’s all-new Mac mini is more mighty, more mini, and built for Apple Intelligence Apple’s all-new Mac mini is more mighty, more mini, and built for Apple Intelligence"""

    # ret = ner.recognize(text)
    # for (_, _,(start, end), label, context) in ret:
    #     print(f"{text[start:end]} : {label}\n{context}\n")


    # text = """U.K. is a country. Yes, Managua is the capital city of Nicaragua. It is located in the southwestern part of the country and is home to many important government buildings and institutions, including the President's office and the National Assembly."""
    # ret = ner.recognize(text)
    # ret = sorted(ret, key=lambda x: x[0])
    # ret = [x[0] for x in ret]
    # assert ret == ['Apple', 'Atlantic Ocean', 'Earth', 'U.K.']

