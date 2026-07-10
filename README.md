<!-- portfolio:date=2024-10-14 -->

[English](README.md) · [Deutsch](README.de.md)

# LLM Fact Auditor

A post-processing pipeline to fact-check, entity-link, and verify answers from Large Language Models, built for the Web Data Processing Systems course at Vrije Universiteit Amsterdam.

<p align="center">
  <img src="docs/pytorch.svg" alt="Pytorch" width="170" />
</p>

### The Challenge

LLMs are prone to hallucination — generating plausible-sounding but factually incorrect statements. This project addresses the verification problem by building an automated auditing layer that sits downstream of any LLM, cross-referencing its claims against authoritative knowledge sources.

### Pipeline Architecture

1. **Entity Recognition**: Uses spaCy and Stanza to identify named entities (people, places, organisations, dates) within LLM-generated answers.
2. **Entity Linking**: Maps recognized entities to Wikidata entries, resolving ambiguity using contextual scoring.
3. **Claim Extraction**: Identifies factual claims in the text using dependency parsing and semantic role labelling.
4. **Fact Verification**: Cross-references extracted claims against the Wikidata knowledge graph via SPARQL queries, assigning a confidence score to each claim.
5. **LLM Re-ranking**: Uses a Meta Llama model to re-rank candidate answers based on factual accuracy scores, selecting the most reliable response.

### Key Technologies

- **PyTorch + Hugging Face Transformers**: For LLM inference and semantic similarity scoring
- **spaCy & Stanza**: Multi-framework NLP for robust entity recognition across languages
- **Wikidata API**: The primary knowledge base for fact verification
- **Docker**: Containerized pipeline ensuring reproducible execution environments
