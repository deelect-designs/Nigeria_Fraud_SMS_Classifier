import re
import string

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# Download required resources (safe to call multiple times)
for resource in ["punkt", "punkt_tab", "stopwords"]:
    try:
        nltk.data.find(resource)
    except LookupError:
        nltk.download(resource)

stemmer = PorterStemmer()
stop_words = set(stopwords.words("english"))


def preprocess_text(text: str) -> str:
    """
    Clean and preprocess SMS text for prediction.
    """

    if text is None:
        return ""

    text = str(text).lower()

    text = re.sub(r"http\S+|www\S+|https\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"\d+", " ", text)

    translator = str.maketrans("", "", string.punctuation)
    text = text.translate(translator)

    text = " ".join(text.split())

    tokens = word_tokenize(text)

    tokens = [
        stemmer.stem(word)
        for word in tokens
        if word not in stop_words
    ]

    return " ".join(tokens)