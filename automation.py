# -*- coding: utf-8 -*-
"""automation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JwZkC9pgOPfrQ7zoV8jNV5lHm9dO4ut4
"""

!apt install tesseract-ocr
!apt install libtesseract-dev
!pip install pytesseract pillow

import pytesseract
from PIL import Image
import re
import os
import pandas as pd

from google.colab import drive
drive.mount('/content/drive')

def process_image(image_path):
    img = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(img)

    def extract_info_from_text(text):
        word, part_of_speech, definition, example, level = None, None, None, None, None

        word_pos_pattern = r'WORD OF THE DAY\s*([^\n(]+)\s*\(([^)]+)\)'
        definition_pattern = r'(?<=\(noun\)\s)(.*?)(?=(Eg:|WORD OF THE DAY FOR))'
        example_pattern = r'Eg:(.*?)(?=WORD OF THE DAY FOR)'

        word_pos_match = re.search(word_pos_pattern, text)
        if word_pos_match:
            word = word_pos_match.group(1).strip()
            part_of_speech = word_pos_match.group(2).strip()

        definition_match = re.search(definition_pattern, text, re.DOTALL)
        if definition_match:
            definition = definition_match.group(1).strip()

        example_match = re.search(example_pattern, text, re.DOTALL)
        if example_match:
            example = example_match.group(1).strip()

        if "BEGINNER" in text.upper():
            level = "Beginner"
        elif "ADVANCE" in text.upper():
            level = "Advance"
        elif "INTERMEDIATE" in text.upper():
            level = "Intermediate"

        return word, part_of_speech, definition, example, level

    word, part_of_speech, definition, example, level = extract_info_from_text(extracted_text)

    definition = " ".join(definition.split())
    example = " ".join(example.split())

    return word, part_of_speech, definition, example, level

images_directory = '/content/drive/MyDrive/Ed-Tech Automation'

words, parts_of_speech, definitions, examples, levels = [], [], [], [], []

for filename in os.listdir(images_directory):
    if filename.lower().endswith('.png'):
        image_path = os.path.join(images_directory, filename)
        word, pos, definition, example, level = process_image(image_path)
        words.append(word)
        parts_of_speech.append(pos)
        definitions.append(definition)
        examples.append(example)
        levels.append(level)

data = {
    'Word': words,
    'Part of Speech (POS)': parts_of_speech,
    'Definition': definitions,
    'Example': examples,
    'Level': levels
}

df = pd.DataFrame(data)

output_excel_file = '/content/drive/MyDrive/Ed-Tech Automation/output.xlsx'
df.to_excel(output_excel_file, index=False)

print("Data saved to Excel successfully.")

