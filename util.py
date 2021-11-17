import json
import fitz
import os


def fetch_conceptarium():
    conceptarium = json.load(open('data/dummy.json'))
    return conceptarium


def pdf_to_images(path):
    doc = fitz.open(path)
    filename = os.path.splitext(os.path.basename(path))[0]
    pix_paths = []

    for page_idx, page in enumerate(doc.pages()):
        pix = page.get_pixmap(matrix=fitz.Matrix(150/72,150/72))
        pix_path = os.path.abspath('./tmp/' + filename + str(page_idx) + '.png')
        pix_paths += [pix_path]
        pix.save(pix_path)

    return pix_paths