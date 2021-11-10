from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import semantic_search
import numpy as np


def get_paragraphs(text):
    lines = text.split('\n')
    paragraphs = []

    for line in lines:
        sents = len(sent_tokenize(line))
        if sents >= 2 and sents <= 8:
            paragraphs += [line]

    return paragraphs


def init_model():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model


def get_embeddings(model, paragraphs):
    return model.encode(paragraphs)


def get_closest_thoughts(conceptarium_embeddings, content_embeddings):
    return semantic_search(content_embeddings, conceptarium_embeddings, top_k=3)


def get_skill(results): 
    scores = [e[0]['score'] for e in results]
    return np.mean(scores)


