import util
import processing
import connectors

import torch
from transformers import AutoTokenizer, AutoModelWithLMHead
from tqdm import tqdm


def test_skill():
    encoder_model = processing.init_model()

    conceptarium = util.fetch_conceptarium()
    conceptarium = [e['content'] for e in conceptarium if e['modality'] == 'language']
    conceptarium_embeddings = processing.get_embeddings(encoder_model, conceptarium)

    content = connectors.fetch_from_opml('data/subscriptions.xml', 100)
    content = list(content.values())[0]
    content_paragraphs = processing.get_paragraphs(content)
    content_embeddings = processing.get_embeddings(encoder_model, content_paragraphs)

    results = processing.get_closest_thoughts(conceptarium_embeddings, content_embeddings)
    skill = processing.get_skill(results)
    print(skill, results)


def test_perplexity():
    encoder_model = processing.init_encoder()

    conceptarium = util.fetch_conceptarium()
    conceptarium = [e['content'] for e in conceptarium if e['modality'] == 'language']
    conceptarium_embeddings = processing.get_embeddings(encoder_model, conceptarium)

    content = connectors.fetch_from_opml('data/subscriptions.xml', 100)
    content = list(content.values())[0]
    content_paragraphs = processing.get_paragraphs(content)
    content_embeddings = processing.get_embeddings(encoder_model, content_paragraphs)

    results = processing.get_closest_thoughts(conceptarium_embeddings, content_embeddings)
    autoregressive_model, tokenizer = processing.init_autoregressive()

    challenge = processing.get_challenge(conceptarium, results, content_paragraphs, autoregressive_model, tokenizer)
    print('Challenge:', challenge)

test_perplexity()