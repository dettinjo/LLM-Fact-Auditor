from transformers import DistilBertTokenizer, DistilBertModel
from src.candidate_generation import Candidate
import torch
import logging
import os
import torch.nn.functional as F

class Disambiguation():
    def __init__(self, cache_dir=os.getenv('MODELS_CACHE','./models_cache/hub')) -> None:
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased',cache_dir=cache_dir)
        self.model = DistilBertModel.from_pretrained('distilbert-base-uncased',cache_dir=cache_dir)

    def get_embedding(self, text):
        """
        Generates an embedding for the given text using DistilBERT.

        Args:
        text (str): The text to generate an embedding for.

        Returns:
        torch.Tensor: The generated embedding.
        """
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        # Mean pooling
        embedding = outputs.last_hidden_state.mean(dim=1)
        return embedding.squeeze(0)
    
    def attempt_exact_matching(self, entity_in_question:str, candidates:list[Candidate])->list[Candidate]:
        """
        Attempts to find exact matches for the entity in question among the candidates.

        Args:
        entity_in_question (str): The entity to find exact matches for.
        candidates (list[Candidate]): The list of candidate entities.

        Returns:
        list[Candidate]: The list of exact match candidates or the original list if no exact matches are found.
        """
        exact_matches = []
        for c in candidates:
            # here we have a tradeoff
            #
            # if we allow vague matching like entity in entity_name
            # then BERT will be more easily confused by more candidates (e.g. Beijing -> Beijing Intl. Airport)
            #
            # if we enforce exact matching, then we may miss out cases like
            #   expected "Roman mythology" for "Roman"
            #   but exact match only returns "Roman" (city in Romania)
            if entity_in_question.lower() in c.entity_name.lower():
                exact_matches.append(c)
        if len(exact_matches) == 0:
            return candidates
        
        logging.info(f"Exact matches found: {[c.entity_name for c in exact_matches]}")

        return exact_matches
    
    def disambiguate(self, entity_in_question:str, context:str, candidates:list[Candidate])->list[tuple[Candidate,float]]:
        """
        Disambiguates the entity in question based on the context and ranks the candidates by similarity.

        Args:
        entity_in_question (str): The entity to disambiguate.
        context (str): The context in which the entity appears.
        candidates (list[Candidate]): The list of candidate entities.

        Returns:
        list[tuple[Candidate, float]]: The list of candidates ranked by similarity.
        """
        # first we see if there are exact matches
        # if there are exact matches, discard the rest
        # this is to address the case where BERT deems Mac Pro is closer to "apple" than Apple Inc.
        candidates = self.attempt_exact_matching(entity_in_question, candidates)

        context_embedding = self.get_embedding(context)
        candidate_embeddings = {}
        for c in candidates:
            candidate_embeddings[c] = self.get_embedding(c.get_wiki_first_para())

        similarities = {}
        for c, embedding in candidate_embeddings.items():
            similarity = F.cosine_similarity(context_embedding, embedding, dim=0)
            similarities[c] = similarity.item()

        ranked_candidates = sorted(similarities.items(), key=lambda item: item[1], reverse=True)
        
        return ranked_candidates
    
if __name__ == '__main__':
    from candidate_generation import CandidateGeneration
    disambiguation = Disambiguation()
    context = "Cayde was an Exo Guardian and the Vanguard for the Hunter class. He was the best."
    cg = CandidateGeneration()
    candidates = cg.query_wikidata("cayde")
    ranked_candidates = disambiguation.disambiguate(context, "cayde", candidates)
    for i in ranked_candidates[:3]:
        print(i[0], "\n" ,i[1],"\n",sep="")