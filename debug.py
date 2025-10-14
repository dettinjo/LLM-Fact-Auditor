from src.entity_linking import EntityLinking

# Q = "Which is the largest country in the world?"
# A = "The largest country in the world is Russia, covering approximately 17.1 million square kilometers (6.6 million square miles)."
# el = EntityLinking(50)
# ret = el.link(Q+" "+A)
# print(ret)

# from src.conclusion import Conclusion
# c = Conclusion()
# c.conclude_entity(Q,Q+" "+A,ret)

# Q = "Is Beijing the capital of the U.K.?"
# A = "London is the capital of the United Kingdom."
# el = EntityLinking(50)
# ret = el.link(Q+" "+A)
# print(ret)


# from main import generate_entity
# generate_entity("Is Beijing the capital of the U.K.?","London is the capital of the United Kingdom.")


# from src.fact_check import FactCheck
# from src.entity_linking import Entity
# factCheck = FactCheck()
# factCheck.query_subject_object("Q956", "Q148")
# subject = Entity("Beijing", "L" ,"",0,0)
# subject.kb_id = "Q956"
# obj = Entity("China", "L" ,"",0,0)
# obj.kb_id = "Q148"
# triple = ["Beijing", "is the capital of", "China"]
# print(triple, factCheck.if_triple_exists(triple, subject, obj))



# subject = Entity("Chongqing", "L" ,"",0,0)
# subject.kb_id = "Q11725"
# obj = Entity("China", "L" ,"",0,0)
# obj.kb_id = "Q148"
# triple = ["Chongqing", "is the capital of", "China"]
# factCheck.if_triple_exists(triple, subject, obj)
# print(triple, factCheck.if_triple_exists(triple, subject, obj))

# subject = Entity("Quentin Tarantino", "L" ,"",0,0)
# subject.kb_id = "Q3772"
# obj = Entity("Pulp Fiction", "L" ,"",0,0)
# obj.kb_id = "Q104123"
# triple = ["Quentin Tarantino", "is the director of", "Pulp Fiction"]
# factCheck.if_triple_exists(triple, subject, obj)
# print(triple, factCheck.if_triple_exists(triple, subject, obj))

# subject = Entity("Bruce Willis", "L" ,"",0,0)
# subject.kb_id = "Q2680"
# obj = Entity("Pulp Fiction", "L" ,"",0,0)
# obj.kb_id = "Q104123"
# triple = ["Bruce Willis", "is the director of", "Pulp Fiction"]
# factCheck.if_triple_exists(triple, subject, obj)
# print(triple, factCheck.if_triple_exists(triple, subject, obj))

# q = "Is Mars the god of War?"
# a = "In Roman mythology, Mars was indeed the god of war, but he was not the same as the Greek god of war Ares. While both gods were associated with violence and conflict, they had distinct roles and characteristics.  Mars, also known as Ares in Greek mythology, was the Roman god of war, violence."
# from src.conclusion import Conclusion
# from src.entity_linking import EntityLinking
# el = EntityLinking(50)
# entities = el.link(q+" "+a)
# c = Conclusion()
# answer = c.conclude_entity(q,q+" "+a,entities)

input_text = open("./test_data/input.txt", "r").read()
from main import main_task
from src.llama_wrap import LlamaWrapper, MODEL_LLAMA_3
main_task(input_text, LlamaWrapper(MODEL_LLAMA_3))