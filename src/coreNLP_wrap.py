from stanza.server import CoreNLPClient
import logging
logging.getLogger('stanza').setLevel(logging.ERROR)
import src.utils as utils

class RelationTriple:
        def __init__(self):
                """
                Stanford CoreNLP's OpenIE
                """
                self.client = CoreNLPClient(
                        annotators=['openie'],
                        timeout=30000,
                        memory='2G',
                        be_quiet=True)
                # self.triple = []
                # self.subject = None
                # self.object = None


        def generate_triples(self, text):
                """
                Generate triple using Stanford CoreNLP's OpenIE.

                Parameters:
                text (str): input text.

                Returns:
                list: [{subject, relation, object}].
                """
                document = self.client.annotate(text, output_format='json')
                triples = []
                for sentence in document['sentences']:
                        for triple in sentence['openie']:
                                triples.append({
                                'subject': triple['subject'],
                                'relation': triple['relation'],
                                'object': triple['object']
                                })
                return triples
        
        def replace_entity_id(self, triples, entities):
                """
                match subject and object with entity name in entites, and generate entity id
                """
                for i in range(len(triples)):
                        triple = triples[i]
                        sub_length = 0
                        sub_entity_id = ''
                        obj_length = 0
                        obj_entity_id = ''
                        for entity in entities:
                                name = entity.mention
                                entity_id = entity.kb_id
                                # calculate similarity of subject
                                sub_cur_length, sub_lcs = utils.longest_common_substring(triple['subject'], name)
                                if sub_cur_length > sub_length and sub_cur_length >2:
                                        sub_length = sub_cur_length
                                        sub_entity_id = entity_id
                                # calculate similarity of object
                                obj_cur_length, obj_lcs = utils.longest_common_substring(triple['object'], name)
                                if obj_cur_length > obj_length and obj_cur_length > 2:
                                        obj_length = obj_cur_length
                                        obj_entity_id = entity_id
                        triples[i]['subject'] = sub_entity_id
                        triples[i]['object'] = obj_entity_id

                # remove None
                triples = [t for t in triples if t.get('subject') != '' and t.get('object') != '']
                return triples
        
        def choose_final_triple(self, triples):
                """
                choose final triple as the one with longest sentence
                """
                if not triples:
                        return
                max_len = 0
                for triple in triples:
                        cur_len = len(triple['subject'])+len(triple['relation'])+len(triple['object'])
                        if cur_len > max_len:
                                max_len = cur_len
                                final_triple = triple
                return final_triple
        
        def get_triples(self, text, entities):
                """
                genrate triple from text and match with entity id
                """
                subject = None
                obj = None
                triple = []
                # remove None entity id in entity
                entities = [ent for ent in entities if ent.kb_id != ""]
                # generate triples, match entity id, select longest triple
                ori_triples = self.generate_triples(text)
                triples = self.replace_entity_id(ori_triples, entities)
                if not triples:
                        return triple, subject, obj
                final_tri = self.choose_final_triple(triples)
                triple = [final_tri['subject'],final_tri['relation'],final_tri['object']]
                for entity in entities:
                        if entity.kb_id == final_tri['subject']:
                                subject = entity
                        if entity.kb_id == final_tri['object']:
                                obj = entity
                return triple, subject, obj
                



        


        
if __name__ == "__main__":
        relation_tri = RelationTriple()
        # text = 'Is it true that Q123 is the country with most people in the world?'
        # triples = [{'subject': 'that country', 'relation': 'is with', 'object': 'most people in world'}, \
        #            {'subject': 'most people', 'relation': 'is in', 'object': 'world'}, \
        #            {'subject': 'China', 'relation': 'is country with', 'object': 'people in world'}, \
        #            {'subject': 'it', 'relation': 'Is', 'object': 'true'}, \
        #            {'subject': 'China', 'relation': 'is country with', 'object': 'most people in world'}]

        # text = 'The largest company in the world by revenue is Apple'
        # triples = [{'subject': 'largest company', 'relation': 'is in', 'object': 'world'}, \
        #            {'subject': 'largest company', 'relation': 'is', 'object': 'Apple'}, \
        #            {'subject': 'company', 'relation': 'is', 'object': 'Apple'}]




        



