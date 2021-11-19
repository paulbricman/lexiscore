from os import replace
from nltk.tokenize import sent_tokenize, word_tokenize
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import semantic_search
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import streamlit as st
import random


def get_paragraphs(text):
    lines = text.split('\n')
    paragraphs = []

    max_sents = 10

    for line in lines:
        sents = sent_tokenize(line)
        if len(sents) > max_sents:
            left = 0
            max_right = len(sents)

            while left < max_right:
                right = left + 1
                while right < max_right and right - left < max_sents and len(' '.join(sents[left:right]).split()) < 400:
                    right += 1
                paragraphs += [' '.join(sents[left:right])]
                left = right

        elif len(sents) >= 2:
            paragraphs += [line]

    if len(paragraphs) > 100:
        paragraphs = random.sample(paragraphs, k=100)

    return paragraphs


@st.cache(allow_output_mutation=True)
def init_encoder():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model


@st.cache(allow_output_mutation=True)
def init_autoregressive():
    model = AutoModelForCausalLM.from_pretrained('distilgpt2')
    return model


def init_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained('distilgpt2')
    return tokenizer


@st.cache(allow_output_mutation=True)
def get_embeddings(paragraphs):
    return st.session_state['encoder_model'].encode(paragraphs)


def get_closest_thoughts(content_embeddings):
    return semantic_search(content_embeddings, st.session_state['conceptarium_embeddings'], top_k=3)


def get_skill(results): 
    scores = [e[0]['score'] for e in results]
    return np.mean(scores)


def get_challenge(results, content_paragraphs):
    ppls = []
    lengths = []
    
    for result_idx, result in enumerate(results):
        context = 'Main Points:\n\n- ' + '\n- '.join([st.session_state['conceptarium'][e] for e in reversed([f['corpus_id'] for f in result])]) + '\n\nSummary\n\n'
        target = content_paragraphs[result_idx]
        full = context + target
        
        target_len = st.session_state['tokenizer'](target, return_tensors='pt').input_ids.size(1)
        full_ids = st.session_state['tokenizer'](full, return_tensors='pt').input_ids
        
        target_ids = full_ids.clone()
        target_ids[:,:-target_len] = -100
        
        with torch.no_grad():
            outputs = st.session_state['autoregressive_model'](full_ids, labels=target_ids)
            neg_log_likelihood = outputs[0] * target_len

        ppl = torch.exp(neg_log_likelihood / target_len)
        ppls += [ppl.numpy()]
        lengths += [len(word_tokenize(target))]

    return np.average(ppls, weights=lengths)


def get_raw_challenge(content_paragraphs):
    ppls = []
    lengths = []
    
    for content_paragraph_idx, content_paragraph in enumerate(content_paragraphs):
        target = content_paragraph
        
        target_len = st.session_state['tokenizer'](target, return_tensors='pt').input_ids.size(1)
        target_ids = st.session_state['tokenizer'](target, return_tensors='pt').input_ids
        
        with torch.no_grad():
            outputs = st.session_state['autoregressive_model'](target_ids, labels=target_ids)
            neg_log_likelihood = outputs[0] * target_len

        ppl = torch.exp(neg_log_likelihood / target_len)
        ppls += [ppl.numpy()]
        lengths += [len(word_tokenize(target))]

    return np.average(ppls, weights=lengths)