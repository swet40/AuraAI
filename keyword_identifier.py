import os
from collections import defaultdict
import spacy
from datetime import datetime

nlp = spacy.load('en_core_web_sm')

def extract_image_prompts(story):
    uninformative_words = {'can', 'to', 'which', 'you', 'your', 'that', 'their', 'they'}
    doc = nlp(story)
    sentences = [sent.text.strip() for sent in doc.sents]
    num_sentences = len(sentences)

    print(f"\nThe story has {num_sentences} sentences.")
    user_choice = input("Do you want to generate one image prompt per sentence? (y/n): ").lower()

    if user_choice == 'y':
        num_prompts = num_sentences
    else:
        num_prompts = int(input("How many image prompts would you like to generate? "))

    main_subjects = []
    sentence_docs = []

    for sentence in sentences:
        sent_doc = nlp(sentence.lower())
        sentence_docs.append(sent_doc)
        for chunk in sent_doc.noun_chunks:
            if chunk.root.dep_ == 'nsubj' and chunk.root.head.text.lower() != 'that':
                main_subjects.append(chunk.text)

    main_subject = main_subjects[0] if main_subjects else None

    related_words = defaultdict(list)
    for sent_doc, sentence in zip(sentence_docs, sentences):
        for tok in sent_doc:
            if tok.text in uninformative_words or not tok.text.isalnum():
                continue
            if (tok.pos_ == 'NOUN') and (main_subject is None or tok.text != main_subject):
                related_words[sentence].append(tok.text)

    image_prompts = []
    for sentence, related in related_words.items():
        if main_subject:
            prompt = f"{main_subject} {' '.join(related)} photorealistic" if related else f"{main_subject} photorealistic"
        else:
            prompt = f"{sentence} photorealistic"
        image_prompts.append(prompt)

    # Adjust prompt list length based on num_prompts
    if len(image_prompts) < num_prompts:
        print(f"Could only generate {len(image_prompts)} unique prompts. Duplicating...")
        i = 0
        while len(image_prompts) < num_prompts:
            image_prompts.append(image_prompts[i])
            i = (i + 1) % len(image_prompts)
    elif len(image_prompts) > num_prompts:
        image_prompts = image_prompts[:num_prompts]

    print("\nGenerated Image Prompts:")
    for idx, prompt in enumerate(image_prompts, start=1):
        print(f"{idx}: {prompt}")

    while True:
        user_input = input("\nProceed with these prompts? (y/n): ").lower()
        if user_input == 'y':
            break
        elif user_input == 'n':
            user_prompts = []
            print("\nEnter your own image prompts:")
            for i in range(num_prompts):
                user_prompt = input(f"Prompt {i+1}: ")
                user_prompts.append(user_prompt)
            image_prompts = user_prompts
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

    # Save prompts to file
    os.makedirs('outputs', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    with open(f"outputs/image_prompts_{timestamp}.txt", "w") as f:
        for prompt in image_prompts:
            f.write(prompt + "\n")

    return image_prompts
