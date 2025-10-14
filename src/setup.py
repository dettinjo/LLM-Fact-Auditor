# Run this once to download the necessary models

import os, subprocess

# Read the cache dir environment variable
cache_dir = os.getenv('MODELS_CACHE','./models_cache/hub') 
os.makedirs(cache_dir, exist_ok=True)
subprocess.run(["sudo", "apt", "update"], check=True)
subprocess.run(["sudo", "apt", "install", "-y", "default-jre"], check=True)

import stanza
stanza.install_corenlp()

from transformers import DistilBertTokenizer, DistilBertModel
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased', cache_dir=cache_dir)
model = DistilBertModel.from_pretrained('distilbert-base-uncased', cache_dir=cache_dir)


from llama_cpp import Llama
llm = Llama.from_pretrained(
	repo_id="bartowski/Llama-3.2-1B-Instruct-GGUF",
	filename="Llama-3.2-1B-Instruct-Q6_K_L.gguf",
    verbose=False,
    cache_dir=cache_dir
)


from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForTokenClassification
AutoTokenizer.from_pretrained("shahrukhx01/question-vs-statement-classifier", cache_dir=cache_dir)
AutoModelForSequenceClassification.from_pretrained("shahrukhx01/question-vs-statement-classifier", cache_dir=cache_dir)

AutoTokenizer.from_pretrained("PrimeQA/tydiqa-boolean-question-classifier", cache_dir=cache_dir)
AutoModelForSequenceClassification.from_pretrained("PrimeQA/tydiqa-boolean-question-classifier", cache_dir=cache_dir)
    
AutoTokenizer.from_pretrained("nfliu/deberta-v3-large_boolq", cache_dir=cache_dir)
AutoModelForSequenceClassification.from_pretrained("nfliu/deberta-v3-large_boolq",cache_dir=cache_dir)

AutoTokenizer.from_pretrained("dslim/bert-base-NER", cache_dir=cache_dir)
AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER",cache_dir=cache_dir)