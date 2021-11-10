from nltk.tokenize import sent_tokenize, word_tokenize
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import semantic_search
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


def get_paragraphs(text):
    lines = text.split('\n')
    paragraphs = []

    for line in lines:
        sents = len(sent_tokenize(line))
        if sents >= 2 and sents <= 8:
            paragraphs += [line]

    return paragraphs


def init_encoder():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model


def init_autoregressive():
    model = AutoModelForCausalLM.from_pretrained('distilgpt2')
    tokenizer = AutoTokenizer.from_pretrained('distilgpt2')
    return model, tokenizer 


def get_embeddings(model, paragraphs):
    return model.encode(paragraphs)


def get_closest_thoughts(conceptarium_embeddings, content_embeddings):
    return semantic_search(content_embeddings, conceptarium_embeddings, top_k=3)


def get_skill(results): 
    scores = [e[0]['score'] for e in results]
    return np.mean(scores)


def get_challenge(conceptarium, results, content_paragraphs, model, tokenizer):
    ppls = []
    lengths = []
    
    for result_idx, result in enumerate(results):
        context = 'Main Points:\n\n- ' + '\n- '.join([conceptarium[e] for e in reversed([f['corpus_id'] for f in result])]) + '\n\nSummary\n\n'
        target = content_paragraphs[result_idx]
        full = context + target

        print(full)
        
        target_len = tokenizer(target, return_tensors='pt').input_ids.size(1)
        full_ids = tokenizer(full, return_tensors='pt').input_ids
        
        target_ids = full_ids.clone()
        target_ids[:,:-target_len] = -100
        
        with torch.no_grad():
            outputs = model(full_ids, labels=target_ids)
            neg_log_likelihood = outputs[0] * target_len

        ppl = torch.exp(neg_log_likelihood / target_len)
        ppls += [ppl.numpy()]
        lengths += [len(word_tokenize(target))]

    return np.average(ppls, weights=lengths)

