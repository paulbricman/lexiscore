from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
sample_style_sheet = getSampleStyleSheet()

doc = SimpleDocTemplate('mealprep.pdf')

components = []

a = Paragraph('Credo', sample_style_sheet['h2'])
b = Paragraph(
    'I am become death, destroyer of worlds.',
    sample_style_sheet['BodyText']
)
c = Paragraph('4 min', sample_style_sheet['h6'])

components.append(a)
components.append(c)
components.append(b)

doc.build(components)