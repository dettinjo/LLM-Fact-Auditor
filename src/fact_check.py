
from SPARQLWrapper import SPARQLWrapper, JSON
from src.entity_linking import Entity
from src.disambiguation import Disambiguation
from src.conclusion import Conclusion
from torch.nn import functional as F

class FactCheck:
    def __init__(self):
        self.sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="OlafJanssen from PAWS")
        self.disambiguation = Disambiguation()
        self.concluder = Conclusion()

    def query_subject_object(self, subject_id, object_id)->list[str]:
        """
        Query the subject and object from the Wikidata.
        
        Args:
        subject (str): The subject of the question.
        object (str): The object of the question.
        
        Returns:
        list: The list of descriptions of relations between the subject and object.
        """

        sparql = SPARQLWrapper(
            "https://query.wikidata.org/sparql", agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        )
        
        query = (
            """
            SELECT ?p ?propertyLabel WHERE {
                wd:%s ?p ?statement .
                ?property wikibase:claim ?p.
                ?property wikibase:statementProperty ?ps.
                ?statement ?ps wd:%s .
                SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            }
            GROUP BY ?p ?propertyLabel
            """
            % (subject_id, object_id)
        )

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)

        resp = sparql.query().convert()


        result = resp["results"]["bindings"]
        ret = []
        for r in result:
            ret.append(r["propertyLabel"]["value"])


        return ret
    
    def if_triple_exists(self, triple:list[str], subject:Entity, object:Entity)->bool:
        """
        Check if the triple exists in the Wikidata.
        
        Args:
        triple (list): The list of descriptions of relations between the subject and object.
        subject (Entity): The subject entity.
        object (Entity): The object entity.
        
        Returns:
        bool: True if the triple exists, False otherwise.
        """
        candidate_relations = self.query_subject_object(subject.kb_id, object.kb_id)
        if len(candidate_relations) == 0:
            # try other way around
            subject, object = object, subject
            triple[0], triple[2] = triple[2], triple[0]
            candidate_relations = self.query_subject_object(subject.kb_id, object.kb_id)
            if len(candidate_relations) == 0:
                return False
        
        og_relation = triple[1]
        # fast path: exact matching
        for relation in candidate_relations:
            shorter = relation
            longer = og_relation
            if len(shorter) > len(longer):
                shorter, longer = longer, shorter
            if shorter in longer:
                return True

        # (candidate, similarity)
        relation_similarity = []
        for relation in candidate_relations:
            og_embedding = self.disambiguation.get_embedding(og_relation)
            this_embedding = self.disambiguation.get_embedding(relation)
            similarity = F.cosine_similarity(og_embedding, this_embedding, dim=0)
            relation_similarity.append((relation, similarity))
        relation_similarity.sort(key=lambda x: x[1], reverse=True)

        top_relation_pair = relation_similarity[0]
        if top_relation_pair[1] > 0.8:
            return True
        else:
            return False
        
    def fact_check_yn_using_concluder(self,q:str, a:str, concluded_answer:str, entities:list[Entity])->bool:
        # for statement & y/n questions
        # if no entity can be concluded, return False
        
        answer_e = self.concluder.conclude_entity(q,a,entities)
        if type(answer_e) != Entity:
            return False 
        wiki_first_para = answer_e.wiki_first_para

        checker_answer = self.concluder.conclude_yn(q, wiki_first_para)
        return checker_answer==concluded_answer

    def fact_check_entity_using_concluder(self,q:str, a:str, statement: str, concluded_entity:Entity)->bool:
        # for statement & y/n questions
        # if no entity can be concluded, return False
        if concluded_entity.wiki_first_para == "":
            return True
        checker_answer = self.concluder.conclude_yn(statement, concluded_entity.wiki_first_para)
        return checker_answer
        