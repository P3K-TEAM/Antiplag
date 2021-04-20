import nltk
from bs4 import BeautifulSoup
import unidecode
import gensim.downloader as api
from nltk.corpus import stopwords
from word2numberi18n import w2n
import inflect
import re
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
import majka
import string
from pycontractions import Contractions
import textract
import pytesseract
from PIL import Image, UnidentifiedImageError
from django.conf import settings

from .constants import stop_words_cz, stop_words_sk, DEFAULT_LANG

try:
    nltk.data.find("stopwords")
except LookupError:
    nltk.download("stopwords")


def extract_text_from_file(filepath):
    try:
        Image.open(filepath).verify()
        text_string = extract_text_from_image(filepath)
    except UnidentifiedImageError:
        text_string = textract.process(filepath).decode()

    return text_string


def extract_text_from_image(filepath):
    pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_PATH
    image = Image.open(filepath)
    return pytesseract.image_to_string(image)


def preprocess_text(
    text,
    strip_html_tags=True,
    remove_extra_whitespace=True,
    remove_accented_chars=True,
    expand_contractions=False,
    remove_punctuation=True,
    lowercase_text=True,
    words_to_numbers=False,
    numbers_to_words=False,
    remove_numbers=True,
    remove_stopwords=False,
    language=DEFAULT_LANG,
    tokenize_words=True,
    tokenize_sentences=False,
    stem=False,
    lemmatize=True,
):
    processed_text = text
    tokenized_text = []

    if strip_html_tags:
        processed_text = strip_html_tags_func(processed_text)

    if remove_stopwords:
        processed_text = remove_stopwords_func(processed_text, language)

    if words_to_numbers:
        processed_text = words_to_numbers(processed_text, language)

    if numbers_to_words:
        processed_text = numbers_to_words_func(processed_text)

    if remove_numbers:
        processed_text = remove_numbers_func(processed_text)

    if remove_accented_chars:
        processed_text = remove_accented_chars_func(processed_text)

    if expand_contractions:
        processed_text = expand_contractions_func(processed_text)

    if remove_punctuation:
        processed_text = remove_punctuation_func(processed_text)

    if lowercase_text:
        processed_text = lowercase_text_func(processed_text)

    if remove_extra_whitespace:
        processed_text = remove_whitespaces_func(processed_text)

    if tokenize_words:
        tokenized_text = tokenize_words_func(processed_text)

    if tokenize_sentences:
        tokenized_text = tokenize_words_func(processed_text)

    if stem:
        tokenized_text = stem_func(tokenized_text)

    if lemmatize:
        tokenized_text = lemmatize_func(tokenized_text)

    return tokenized_text, processed_text


def strip_html_tags_func(text):
    """remove html tags from text"""
    soup = BeautifulSoup(text, "html.parser")
    stripped_text = soup.get_text(separator=" ")

    return stripped_text


def remove_whitespaces_func(text):
    """remove extra whitespaces from text"""
    text = text.strip()

    return " ".join(text.split())


def remove_accented_chars_func(text):
    """remove accented characters from text, e.g. café"""
    text = unidecode.unidecode(text)

    return text


def expand_contractions_func(text):
    """expand shortened words, e.g. don't to do not"""
    model = api.load("glove-twitter-25")
    cont = Contractions(kv_model=model)
    cont.load_models()
    text = list(cont.expand_texts([text], precise=True))[0]

    return text


def remove_punctuation_func(text):
    translator = str.maketrans("", "", string.punctuation)
    return text.translate(translator)


def lowercase_text_func(text):
    return text.lower()


def words_to_numbers(text, language=DEFAULT_LANG):
    try:
        w2n_instance = w2n.W2N(lang_param=language)
    except FileNotFoundError:  # FileNotFoundError is thrown when w2n tries to locate data for unsupported lang
        return text

    text = text.split()
    new_text = []
    for word in text:
        try:
            word_as_number = str(w2n_instance.word_to_num(word))
            new_text.append(word_as_number)
        except ValueError:
            new_text.append(word)

    text = " ".join(new_text)
    return text


def numbers_to_words_func(text):
    # convert number into words
    p = inflect.engine()
    # split string into list of words
    temp_str = text.split()
    # initialise empty list
    new_string = []
    for word in temp_str:
        # if word is a digit, convert the digit
        # to numbers and append into the new_string list
        if word.isdigit():
            temp = p.number_to_words(word)
            new_string.append(temp)
        # append the word as it is
        else:
            new_string.append(word)
    # join the words of new_string to form a string
    temp_str = " ".join(new_string)

    return temp_str


def remove_numbers_func(text):
    result = re.sub(r"\d+", "", text)

    return result


def remove_stopwords_func(text, language):
    stop_words_en = set(stopwords.words("english"))
    word_tokens = word_tokenize(text)

    if language == "en":
        text = [word for word in word_tokens if word not in stop_words_en]
    elif language == "sk":
        text = [word for word in word_tokens if word not in stop_words_sk]
    elif language == "cz":
        text = [word for word in word_tokens if word not in stop_words_cz]
    else:
        print("invalid language code")

    return " ".join(text)


def tokenize_words_func(text):
    word_tokens = word_tokenize(text)
    return word_tokens


def tokenize_sentences_func(text):
    sentence_tokens = nltk.sent_tokenize(text)
    return sentence_tokens


def stem_func(word_tokens):
    stemmer = PorterStemmer()
    # stem words in the list of tokenized words
    stems = [stemmer.stem(word) for word in word_tokens]

    return stems


def lemmatize_func(word_tokens, language="sk"):
    morph = majka.Majka("wordlists/lemmas.sk.fsa")
    if language == "sk":
        morph = majka.Majka("wordlists/lemmas.sk.fsa")
    elif language == "cz":
        morph = majka.Majka("wordlists/lemmas.cz.fsa")

    lemmas = [morph.find(token) for token in word_tokens]

    return lemmas
