# temp - testin spaCyLayout library for use with
# ADS report PDF docs


import spacy
from spacy_layout import spaCyLayout
import regex

def normalize_whitespace(text: str, preserve_line_breaks: bool=True) -> str:
    if preserve_line_breaks: # normalize only spaces, not line or paragraph breaks
        return regex.sub(pattern=r"\p{Separator}+", repl=" ", string=text).strip()
    else:
        return " ".join(text.split())


nlp = spacy.blank("en")
layout = spaCyLayout(nlp)

# Process a document and create a spaCy Doc object
#doc = layout("./data/078_047_054.pdf")
doc = layout("./data/001_142_151.pdf")
spacer = "\n=============================================================\n"
# The text-based contents of the document
#print(f"{spacer}doc.text:\n{doc.text}")
normalized = normalize_whitespace(doc.text)
print(f"{spacer}normalized:\n{normalized}")

# Document layout including pages and page sizes
print(f"{spacer}doc._.layout:\n{doc._.layout}")
# Tables in the document and their extracted data
print(f"{spacer}doc._.tables:\n{doc._.tables}")
# Markdown representation of the document
print(f"{spacer}doc._.markdown:\n{doc._.markdown}")
print(doc._.markdown)

# Layout spans for different sections
print(f"{spacer}doc.spans[\"layout\"]:")
for span in doc.spans["layout"]:
    # Document section and token and character offsets into the text
    print(span.text, span.start, span.end, span.start_char, span.end_char)
    # Section type, e.g. "text", "title", "section_header" etc.
    print(span.label_)
    # Layout features of the section, including bounding box
    print(span._.layout)
    # Closest heading to the span (accuracy depends on document structure)
    print(span._.heading)
