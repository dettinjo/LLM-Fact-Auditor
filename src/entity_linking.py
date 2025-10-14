from src.disambiguation import *
from src.entity_recognition import *
from src.candidate_generation import *
"""
This module links the entity to the related Wikipedia page.
"""

class EntityLinking:
    def __init__(self,context_diameter:int, disam_linkage:bool = True):
        """
        Constructs all the necessary attributes for the EntityLinking object.

        Args:
        context_diameter (int): The diameter of the context to consider for entity recognition.
        disam_linkage (bool): Whether to use linkage to facilitate disambiguation (default is True).
        """
        self.ner = NER(context_diameter)
        self.cg = CandidateGeneration()
        self.disambiguation = Disambiguation()
        self.disam_linkage = disam_linkage # whether to use linkage to facilitate disambiguation
        return
    
    def link(self,text:str) -> list[Entity]:
        """
        Links entities in the provided text to their corresponding Wikipedia articles.

        Args:
        text (str): The text in which to recognize and link entities.

        Returns:
        list: A list of all entities, linked, for further processing.
        """
        entities = self.ner.recognize(text)

        identified_entities = []
        to_revisit = []
        for entity in entities:
            original_mention = entity.mention
            context = entity.context
            candidates = self.cg.query_wikidata(original_mention)
            if len(candidates) == 0:
                # for "the Caribbean Sea" wikidata only knows "Caribbean Sea"
                # give it one last chance
                if original_mention.startswith("the"):
                    alternated = original_mention[4:].strip()
                    candidates = self.cg.query_wikidata(alternated)
                    if len(candidates) == 0:
                        logging.info(f"For {original_mention}, no candidates found.")
                        # no candidates found
                        continue
                    else:
                        original_mention = alternated
                else:
                    # no candidates found
                    continue

            ranked_candidates_and_weight = self.disambiguation.disambiguate(original_mention, context,candidates)
            if len(ranked_candidates_and_weight) > 1 and self.disam_linkage:
                first_confidence = ranked_candidates_and_weight[0][1]
                second_confidence = ranked_candidates_and_weight[1][1]
                if first_confidence - second_confidence < 0.025:
                    logging.info(f"For {original_mention}, confidence difference between top two candidates is less than 0.05.")
                    logging.info(f"For {original_mention}, skipping for now.")
                    to_revisit.append([entity, ranked_candidates_and_weight])
                    continue
            result_candidate = ranked_candidates_and_weight[0][0]
            identified_entities.append(result_candidate)
            result_wikipedia_link = result_candidate.wiki_article
        
            entity.wikipedia_link = result_wikipedia_link
            entity.kb_id = result_candidate.kb_link.split("/")[-1]
            entity.wiki_first_para = result_candidate.get_wiki_first_para()

        for (entity, unsure_ranking) in to_revisit:
            original_mention = entity.mention
            # TODO : support other KBs like yago 
            correlation_ranked = self.cg.query_correlation_wikidata(original_mention, identified_entities)
            first_candidate = correlation_ranked[0]
            if first_candidate.link_count > 0:
                identified_entities.append(first_candidate)
                entity.wikipedia_link = first_candidate.wiki_article
                entity.kb_id = first_candidate.kb_link.split("/")[-1]
                entity.wiki_first_para = first_candidate.get_wiki_first_para()
            else:
                min_cred = unsure_ranking[0][1] - 0.025
                unsure_ranking = [x for x in unsure_ranking if x[1] > min_cred][:5]
                # choose the one with the most links (most popular)
                unsure_ranking = sorted(unsure_ranking, key=lambda x: x[0].link_count, reverse=True)
                entity.wikipedia_link = unsure_ranking[0][0].wiki_article
                entity.kb_id = unsure_ranking[0][0].kb_link.split("/")[-1]
                entity.wiki_first_para = unsure_ranking[0][0].get_wiki_first_para()

        return entities

if __name__ == "__main__":

    import logging
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s]   %(message)s')
    el = EntityLinking(50)

    # showcase of why exact matching should be enforced all the time
    # otherwise Apple will give Mac Pro instead of Apple Inc. (no other heuristics deployed)
    text = "Apple’s all-new Mac mini is more mighty, more mini, and built for Apple Intelligence"
    linked = el.link(text)
    for l in linked:
        print(l)

    # fun fact: yago doesn't know China
    # fun fact2: AIDA can't link China properly
    text = "The capital of China is Beijing."
    linked = el.link(text)
    for l in linked:
        print(l)

    # a good showcase of how linkage facilitates disambiguation
    # also at least on par with AIDA
    text = "Yes, Mars is a god in Roman mythology. He is the god of war, often associated with military power, aggression, and valor. Mars was one of the most important gods in the Roman pantheon, second only to Jupiter, and he was also seen as a protector of Rome. The Romans identified Mars with the Greek god Ares, though Mars had a more respected role in Roman culture compared to Ares in Greek mythology."
    el_no_linkage_heuristics = EntityLinking(50, disam_linkage=False)
    linked = el.link(text)
    for l in linked:
        print(l)
    linked = el_no_linkage_heuristics.link(text)
    for l in linked:
        print(l)

    text = "Yes, Managua is the capital city of Nicaragua. It is located in the southwestern part of the country and is home to many important government buildings and institutions, including the President's office and the National Assembly. The city has a population of over one million people and is known for its vibrant cultural scene, historic landmarks, and beautiful natural surroundings."
    
    # spacy doesn't do better than luke
    #
    # nlp = spacy.load("en_core_web_sm")
    # doc = nlp(text)
    # for i in doc.ents:
    #     print(i.text, i.label_)

    linked = el.link(text)
    for l in linked:
        print(l)
