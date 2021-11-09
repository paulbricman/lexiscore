import util
import processing
import connectors


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

test_skill()