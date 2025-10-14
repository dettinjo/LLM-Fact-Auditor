"""
note: I haven't use the Stanford Open IE success. So I try another method but it cannot adapt to more complex statements. Welcome to try a clever method to generate triple. 
generate triple from statement
input: statement
output: ['subject','relation','object']
example:
input: "Quentin Tarantino is the director of Pulp Fiction."
output: [{'subject': 'Quentin Tarantino', 'relation': 'is the director of', 'object': 'Pulp Fiction'}]
"""
import spacy
nlp = spacy.load('en_core_web_sm')
from spacy.matcher import Matcher 

class Triplet:
    def __init__(self):
        self.subject = ""
        self.relation = ""
        self.object = ""

class Triple:
    def __init__(self):
        self.subject = ''
        self.object = ''
        self.relation = ''
        
    def get_triple(self,sent):
        #
        ent1 = ""
        ent2 = ""
        relation = ""
        triple = {}

        prv_tok_dep = ""    # dependency tag of previous token in the sentence
        prv_tok_text = ""   # previous token in the sentence

        prefix = ""
        modifier = ""

        predicate_flag = False

        doc = nlp(sent)
        # relation
        relation = self.get_relation(doc)


        for tok in doc:

            # if token is a punctuation mark then move on to the next token
            if tok.dep_ == "punct":
                continue

            if tok.pos_ == "VERB" or tok.pos_ == "AUX":
                predicate_flag = True

            # check: token is a compound word or not
            if tok.dep_ == "compound":
                prefix = tok.text
                # if the previous word was also a 'compound' then add the current word to it
                if prv_tok_dep == "compound":
                    prefix = prv_tok_text + " "+ tok.text
            
            # mod修饰词
            # check: token is a modifier or not
            if tok.dep_.endswith("mod") == True:
                modifier = tok.text
                # if the previous word was also a 'compound' then add the current word to it
                if prv_tok_dep == "compound":
                    modifier = prv_tok_text + " "+ tok.text
                
            # subject
            if tok.dep_.find("subj") == True:
                ent1 = modifier + prefix + " "+ tok.text
                prefix = ""
                modifier = ""
                prv_tok_dep = ""
                prv_tok_text = ""      

            # object
            if (tok.dep_== "pobj" or tok.dep_== "attr") and predicate_flag:
                ent2 = prefix +" "+ tok.text
            

            # update variables
            prv_tok_dep = tok.dep_
            prv_tok_text = tok.text

        self.subject = ent1.strip()
        self.relation = relation
        self.object = ent2.strip()

        return

    def get_relation(self,doc):
        # extract relation
        matcher = Matcher(nlp.vocab)

        # Define the pattern
        pattern = [{'DEP': 'ROOT'}, 
            {'DEP': 'neg', 'OP': "*"},
            {'DEP': 'det', 'OP': "*"},
            {'DEP': 'amod', 'OP': "*"},
            {'DEP': 'dobj', 'OP': "*"},
            {'DEP': 'attr', 'OP': "*"},
            {'DEP': 'prep', 'OP': "*"}
            
        ]
        matcher.add("matching_1", [pattern])

        matches = matcher(doc)

        k = len(matches) - 1

        span = doc[matches[k][1]:matches[k][2]] 
        
        return span.text

if __name__ == "__main__":
    triple = Triple()

    sentences = ["Quentin Tarantino is the director of Pulp Fiction.",
    "Managua is the capital of nicaragua",
    "Beijing is not the capital of nicaragua",
    "The largest company in the world by revenue is not Apple",
    "China has the most population in the world."]

    for sent in sentences:
        result = triple.get_triple(sent)