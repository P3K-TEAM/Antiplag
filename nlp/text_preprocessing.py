import nltk
from bs4 import BeautifulSoup
import unidecode
import gensim.downloader as api
from nltk.corpus import stopwords
from word2number import w2n
import inflect
import re
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk import pos_tag, ne_chunk
import spacy
import majka
import string
from pycontractions import Contractions
from textblob import TextBlob
import textract
import os
import shutil


def text_extraction(path_to_file):
    file_name, file_extension = os.path.splitext(path_to_file)

    if file_extension == '.srt' or file_extension == '.md':
        file_extension = '.txt'
        path_to_file_old = path_to_file
        path_to_file = file_name + file_extension
        shutil.copyfile(path_to_file_old, path_to_file)

    text_string = textract.process(path_to_file).decode()
    return text_string

def preprocess_text(text, strip_html_tags=True, remove_extra_whitespace=True, remove_accented_chars=False,
                    expand_contractions=False, remove_punctuation=True, lowercase_text=True, words_to_numbers=False,
                    numbers_to_words=False, remove_numbers=True, remove_stopwords=False, language="sk",
                    tokenize_words=True, tokenize_sentences=False, stem=False, lemmatize=True):
    processed_text = text
    tokenized_text = []

    if strip_html_tags:
        processed_text = strip_html_tags_func(processed_text)

    if remove_extra_whitespace:
        processed_text = remove_whitespaces_func(processed_text)

    if remove_accented_chars:
        processed_text = remove_accented_chars_func(processed_text)

    if expand_contractions:
        processed_text = expand_contractions_func(processed_text)

    if remove_punctuation:
        processed_text = remove_punctuation_func(processed_text)

    if lowercase_text:
        processed_text = lowercase_text_func(processed_text)

    if words_to_numbers:
        processed_text = words_to_numbers_func(processed_text)

    if numbers_to_words:
        processed_text = numbers_to_words_func(processed_text)

    if remove_numbers:
        processed_text = remove_numbers_func(processed_text)

    if remove_stopwords:
        processed_text = remove_stopwords_func(processed_text, language)

    if tokenize_words:
        tokenized_text = tokenize_words_func(processed_text)

    if tokenize_sentences:
        tokenized_text = tokenize_words_func(processed_text)

    if stem:
        tokenized_text = stem_func(tokenized_text)

    if lemmatize:
        tokenized_text = lemmatize_func(tokenized_text)

    return tokenized_text


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
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)


def lowercase_text_func(text):
    return text.lower()


def words_to_numbers_func(text):
    text = text.split()
    new_text = []
    for word in text:
        try:
            new_text.append(w2n.word_to_num(word))
        except ValueError:
            new_text.append(word)

    text = ' '.join(map(str, new_text))
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
    temp_str = ' '.join(new_string)

    return temp_str


def remove_numbers_func(text):
    result = re.sub(r'\d+', '', text)

    return result


def remove_stopwords_func(text, language):
    stop_words_en = set(stopwords.words("english"))
    stop_words_sk = ["a", "aby", "aj", "ak", "aká", "akáže", "aké", "akéže", "akého", "akéhože", "akej", "akejže",
                     "akému", "akémuže", "ako", "akože", "akom", "akomže", "akou", "akouže", "akú", "akúže", "akých",
                     "akýchže", "akým", "akýmže", "akými", "akýmiže", "ale", "alebo", "ani", "áno", "asi", "až", "ba",
                     "bez", "bezo", "bol", "bola", "boli", "bolo", "bude", "budem", "budeme", "budeš", "budete", "budú",
                     "by", "byť", "cez", "cezo", "čej", "či", "čí", "čia", "čie", "čieho", "čiemu", "čím", "čími",
                     "čiu", "čo", "čoho", "čom", "čomu", "čou", "ďalšia", "ďalšie", "ďalšieho", "ďalšiemu", "ďalšiu",
                     "ďalší", "ďalších", "ďalším", "ďalšími", "ďalšou", "dnes", "do", "ho", "ešte", "i", "iba", "ich",
                     "im", "iná", "inej", "iné", "iného", "inému", "iní", "inom", "inú", "iný", "iných", "inými", "ja",
                     "je", "jeho", "jej", "jemu", "ju", "k", "ká", "káže", "kam", "kamže", "každá", "každé", "každému",
                     "každí", "každou", "každú", "každý", "každých", "každým", "každými", "kde", "keď", "kej", "kejže",
                     "ké", "kéže", "kie", "kieho", "kiehože", "kiemu", "kiemuže", "kieže", "koho", "kom", "komu", "kou",
                     "kouže", "kto", "ktorá", "ktorej", "ktoré", "ktorí", "ktorou", "ktorú", "ktorý", "ktorých",
                     "ktorým", "ktorými", "ku", "kú", "kúže", "ký", "kýho", "kýhože", "kým", "kýmu", "kýmuže", "kýže",
                     "lebo", "leda", "ledaže", "len", "ma", "má", "majú", "mám", "máme", "máš", "máte", "mať", "medzi",
                     "mi", "mne", "mnou", "mňa", "moj", "moje", "mojej", "mojich", "mojim", "mojimi", "mojou", "moju",
                     "môcť", "môj", "môjho", "môže", "môžem", "môžeme", "môžeš", "môžete", "môžu", "mu", "musieť",
                     "musí", "musia", "musím", "musíme", "musíte", "musíš", "my", "na", "nad", "nado", "nám", "nami",
                     "nás", "náš", "naša", "naše", "našej", "nášho", "naši", "našich", "našim", "našimi", "našou", "ne",
                     "neho", "nech", "nej", "nejaká", "nejaké", "nejakého", "nejakej", "nejakému", "nejakom", "nejakou",
                     "nejakú", "nejakých", "nejakým", "nejakými", "nemu", "než", "nich", "nič", "ničím", "ničoho",
                     "ničom", "ničomu", "nie", "niektorá", "niektoré", "niektorého", "niektorej", "niektorému",
                     "niektorom", "niektorou", "niektorú", "niektorý", "niektorých", "niektorým", "niektorými", "nim",
                     "nimi", "ním", "ňom", "ňou", "ňu", "o", "od", "odo", "on", "ona", "oni", "ono", "ony", "oň",
                     "oňho", "po", "pod", "podo", "podľa", "pokiaľ", "potom", "popod", "popri", "poza", "práve", "pre",
                     "prečo", "preto", "pretože", "pred", "predo", "pri", "s", "sa", "si", "sme", "so", "som", "ste",
                     "sú", "svoj", "svoja", "svoje", "svojho", "svojich", "svojim", "svojím", "svojimi", "svojou",
                     "svoju", "ta", "tá", "tam", "tak", "takže", "táto", "teda", "tej", "ten", "tento", "tiež", "tí",
                     "tie", "tieto", "títo", "to", "toho", "tohto", "tom", "tomto", "tomu", "tomuto", "toto", "tou",
                     "touto", "tu", "tú", "túto", "tvoj", "tvoja", "tvoje", "tvojej", "tvojho", "tvoji", "tvojich",
                     "tvojím", "tvojimi", "ty", "tých", "tým", "tými", "týmto", "už", "v", "vám", "vami", "vás", "váš",
                     "vaša", "vaše", "vašej", "vášho", "vaši", "vašich", "vašim", "vaším", "viac", "vo", "však",
                     "všetci", "všetka", "všetko", "všetky", "všetok", "vy", "z", "za", "začo", "začože", "zo", "že"]
    stop_words_cz = ["a", "aby", "aj", "ale", "anebo", "ani", "aniz", "ano", "asi", "avska", "az", "ba", "bez", "bude",
                     "budem", "budes", "by", "byl", "byla", "byli", "bylo", "byt", "ci", "clanek", "clanku", "clanky",
                     "co", "com", "coz", "cz", "dalsi", "design", "dnes", "do", "email", "ho", "i", "jak", "jake",
                     "jako", "je", "jeho", "jej", "jeji", "jejich", "jen", "jeste", "jenz", "ji", "jine", "jiz", "jsem",
                     "jses", "jsi", "jsme", "jsou", "jste", "k", "kam", "kde", "kdo", "kdyz", "ke", "ktera", "ktere",
                     "kteri", "kterou", "ktery", "ku", "ma", "mate", "me", "mezi", "mi", "mit", "mne", "mnou", "muj",
                     "muze", "my", "na", "nad", "nam", "napiste", "nas", "nasi", "ne", "nebo", "nebot", "necht",
                     "nejsou", "není", "neni", "net", "nez", "ni", "nic", "nove", "novy", "nybrz", "o", "od", "ode",
                     "on", "org", "pak", "po", "pod", "podle", "pokud", "pouze", "prave", "pred", "pres", "pri", "pro",
                     "proc", "proto", "protoze", "prvni", "pta", "re", "s", "se", "si", "sice", "spol", "strana", "sve",
                     "svuj", "svych", "svym", "svymi", "ta", "tak", "take", "takze", "tamhle", "tato", "tedy", "tema",
                     "te", "ten", "tedy", "tento", "teto", "tim", "timto", "tipy", "to", "tohle", "toho", "tohoto",
                     "tom", "tomto", "tomuto", "totiz", "tu", "tudiz", "tuto", "tvuj", "ty", "tyto", "u", "uz", "v",
                     "vam", "vas", "vas", "vase", "ve", "vedle", "vice", "vsak", "vsechen", "vy", "vzdyt", "z", "za",
                     "zda", "zde", "ze", "zpet", "zpravy"]
    word_tokens = word_tokenize(text)

    if language == "en":
        text = [word for word in word_tokens if word not in stop_words_en]
    elif language == "sk":
        text = [word for word in word_tokens if word not in stop_words_sk]
    elif language == "cz":
        text = [word for word in word_tokens if word not in stop_words_cz]
    else:
        print("invalid language code")

    return text


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
    morph = majka.Majka('wordlists/lemmas.sk.fsa')
    if language == "sk":
        morph = majka.Majka('wordlists/lemmas.sk.fsa')
    elif language == "cz":
        morph = majka.Majka('wordlists/lemmas.cz.fsa')

    lemmas = [morph.find(token) for token in word_tokens]

    return lemmas


def part_of_speech_tagging_func(text):
    result = TextBlob(text)

    return result.tags


def chunking_func(tags):
    reg_exp = "NP: { < DT >? < JJ > * < NN >}"
    rp = nltk.RegexpParser(reg_exp)
    result = rp.parse(tags)

    # Draw the sentence tree structure
    # result.draw()

    return result


def chunking_with_post_func(text):
    result = TextBlob(text)

    reg_exp = "NP: { < DT >? < JJ > * < NN >}"
    rp = nltk.RegexpParser(reg_exp)
    result = rp.parse(result.tags)

    return result


def named_entity_recognition_func(word_tokens):
    # part of speech tagging of words
    word_pos = pos_tag(word_tokens)
    # tree of word entities

    return ne_chunk(word_pos)


def coreference_resolution_func(text):
    nlp = spacy.load('en_coref_lg')
    doc = nlp(text)
    if doc._.has_coref:
        print("Given text: " + text)
        print_mentions_func(doc)
        print_pronoun_references_func(doc)


def print_mentions_func(doc):
    print("\nAll the mentions in the given text:")
    for cluster in doc._.coref_clusters:
        print(cluster.mentions)


def print_pronoun_references_func(doc):
    print("\nPronouns and their references:")
    for token in doc:
        if token.pos_ == 'PRON' and token._.in_coref:
            for cluster in token._.coref_clusters:
                print(token.text + " => " + cluster.main.text)
