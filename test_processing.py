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
    encoder_model = processing.init_model()

    conceptarium = util.fetch_conceptarium()
    conceptarium = [e['content'] for e in conceptarium if e['modality'] == 'language']
    conceptarium_embeddings = processing.get_embeddings(encoder_model, conceptarium)

    content = connectors.fetch_from_opml('data/subscriptions.xml', 100)
    content = list(content.values())[0]
    content_paragraphs = processing.get_paragraphs(content)
    content_embeddings = processing.get_embeddings(encoder_model, content_paragraphs)

    results = processing.get_closest_thoughts(conceptarium_embeddings, content_embeddings)

    tokenizer = AutoTokenizer.from_pretrained('distilgpt2')
    model = AutoModelWithLMHead.from_pretrained('distilgpt2')
    
    for result_idx, result in enumerate(results):
        context = '\n\n'.join([conceptarium[e] for e in [f['corpus_id'] for f in result]]) + '\n\n---\n\n'
        target = content_paragraphs[result_idx]
        full = context + target

        print(full)
        
        target_len = tokenizer(target, return_tensors='pt').input_ids.size(1)
        full_ids = tokenizer(full, return_tensors='pt').input_ids
        
        target_ids = full_ids.clone()
        target_ids[:,:-target_len] = -100

        print(target_ids)
        
        with torch.no_grad():
            outputs = model(full_ids, labels=target_ids)
            neg_log_likelihood = outputs[0] * target_len

        print('neg_log_likelihood:', neg_log_likelihood)
        ppl = torch.exp(neg_log_likelihood / target_len)
        print(ppl)


test_perplexity()