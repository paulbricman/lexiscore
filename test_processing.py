import util
import processing
import connectors

import torch
from transformers import AutoTokenizer, AutoModelWithLMHead
from tqdm import tqdm


def test_skill():
    model = processing.init_model()

    conceptarium = util.fetch_conceptarium()
    conceptarium = [e['content'] for e in conceptarium if e['modality'] == 'language']
    conceptarium_embeddings = processing.get_embeddings(model, conceptarium)

    content = connectors.fetch_from_opml('data/subscriptions.xml', 100)
    content = list(content.values())[0]
    content_paragraphs = processing.get_paragraphs(content)
    content_embeddings = processing.get_embeddings(model, content_paragraphs)

    results = processing.get_closest_thoughts(conceptarium_embeddings, content_embeddings)
    skill = processing.get_skill(results)
    print(skill, results)


def test_perplexity():
    tokenizer = AutoTokenizer.from_pretrained('distilgpt2')
    model = AutoModelWithLMHead.from_pretrained('distilgpt2')

    content = connectors.fetch_from_opml('data/subscriptions.xml', 14)
    content = list(content.values())[0]
    print(content)
    encodings = tokenizer(content, return_tensors='pt')
    print(encodings['input_ids'].size(0))
    
    max_length = model.config.n_positions
    stride = max_length

    nlls = []
    for i in tqdm(range(0, encodings.input_ids.size(1), stride)):
        begin_loc = max(i + stride - max_length, 0)
        end_loc = min(i + stride, encodings.input_ids.size(1))
        trg_len = end_loc - i    # may be different from stride on last loop
        input_ids = encodings.input_ids[:,begin_loc:end_loc]
        target_ids = input_ids.clone()
        target_ids[:,:-trg_len] = -100

        with torch.no_grad():
            outputs = model(input_ids, labels=target_ids)
            neg_log_likelihood = outputs[0] * trg_len

        nlls.append(neg_log_likelihood)

    ppl = torch.exp(torch.stack(nlls).sum() / end_loc)

    print(ppl, nlls)



test_perplexity()