import os
from collections import defaultdict
from datetime import datetime
import spacy
from collections import defaultdict

nlp = spacy.load('en_core_web_sm')

def extract_image_prompts(story, max_prompts=5):
    uninformative_words = {'can', 'to', 'which', 'you', 'your', 'that', 'their', 'they'}
    doc = nlp(story)
    sentences = [sent.text.strip() for sent in doc.sents]

    image_prompts = []
    added_prompts = set()

    for sentence in sentences:
        sent_doc = nlp(sentence.lower())
        nouns = [tok.text for tok in sent_doc if tok.pos_ == "NOUN" and tok.text not in uninformative_words]

        if nouns:
            prompt_text = f"{' '.join(set(nouns))} photorealistic"
            if prompt_text not in added_prompts:
                image_prompts.append(prompt_text)
                added_prompts.add(prompt_text)

        if len(image_prompts) >= max_prompts:
            break

    return image_prompts