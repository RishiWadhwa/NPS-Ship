import cv2
import pytesseract
from pdf2image import convert_from_path
import string
import re
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

pdf_path = 'essay.pdf'
images = convert_from_path(pdf_path)

for i, image in enumerate(images):
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) # PIL ot OpenCV

    img_cv = cv2.resize(img_cv, (800, 1000)) # resizing
    # TODO: Denoise, etc.

    ocr_scan = pytesseract.image_to_string(img_cv)

    cv2.imwrite('preprocessed_page_' + str(i) + '.jpg', img_cv) # preprocess img overriding

# NLTK Library processing
ocr_scan = ocr_scan.lower() # lowercased
cleaned_scan = re.sub('[' + string.punctuation + ']', '', ocr_scan) # remove punc

# stopword removal
nltk.download('stopwords')
stopwords = set(stopwords.words('english'))
tokens = word_tokenize(cleaned_scan)
filtered_scan_list = [token for token in tokens if token.lower() not in stopwords]

# lemmatize / frequency distribuition
lemmatize_dict = {}

lemmatizer = WordNetLemmatizer()
for word in filtered_scan_list:
	lemmatize_dict[word] = lemmatizer.lemmatize(word)

print(lemmatize_dict)
