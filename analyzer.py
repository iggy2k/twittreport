from __future__ import annotations, unicode_literals, print_function
import spacy
from spacy.lang.en import English

# Translate spacy abbreviations to readable english
# https://universaldependencies.org/u/pos/
UPOS = {
    'ADJ': 'adjective',
    'ADP': 'adposition',
    'ADV': 'adverb',
    'AUX': 'auxiliary verb',
    'CONJ': 'coordinating conjunction',
    'DET': 'determiner',
    'INTJ': 'interjection',
    'NOUN': 'noun',
    'NUM': 'numeral',
    'PART': 'particle',
    'PRON': 'pronoun',
    'PROPN': 'proper noun',
    'PUNCT': 'punctuation',
    'SCONJ': 'subordinating conjunction',
    'SYM': 'symbol',
    'VERB': 'verb',
    'X': 'other',
}

# Return sorted dict of nouns


def organizeNouns(noun_arr) -> dict:
    print("Organizing nouns...")
    nouns = {}
    for noun in noun_arr:
        if not noun in nouns:
            nouns[noun] = 1
        else:
            nouns[noun] += 1
    return dict(sorted(nouns.items(), key=lambda item: item[1], reverse=True))

# Return sorted dict of verbs


def organizeVerbs(verb_arr) -> dict:
    print("Organizing verbs...")
    verbs = {}
    for verb in verb_arr:
        if not verb in verbs:
            verbs[verb] = 1
        else:
            verbs[verb] += 1
    return dict(sorted(verbs.items(), key=lambda item: item[1], reverse=True))

# Build structures based on the UPOS values, return
# a sorted dictionary.


def getStructures(sentences):
    print("Bulding structures...")
    structures = {}
    STRUCT_MAX_LEN = 5
    nlp = spacy.load("en_core_web_sm")
    for sentence in sentences:
        struct = ''
        nlp_sent = nlp(sentence)
        for token in nlp_sent[:min(STRUCT_MAX_LEN, len(nlp_sent))]:
            if token.pos_ in UPOS:
                struct += UPOS[token.pos_] + ' + '
            else:
                struct += UPOS['X'] + ' + '
        if not struct in structures:
            structures[struct] = 1
        else:
            structures[struct] += 1
    return dict(sorted(structures.items(), key=lambda item: item[1], reverse=True))

# Returns a list of ALL sentences


def getSentences(full_text):
    print("Extracting sentences...")
    nlp = English()
    nlp.add_pipe('sentencizer')
    # Set max length to avoid exception
    doc = nlp(full_text[:1000000])
    return [sent.text.strip() for sent in doc.sents]

# Get average sentence length


def aveSentLen(sentences):
    return sum(len(sentence) for sentence in sentences) // len(sentences)

# Get average words


def aveSentWords(sentences):
    words = 0
    for sentence in sentences:
        for _ in sentence.split():
            words += 1
    return words // len(sentences)


print("Hang tight! Analyzing may take a while.")

# Load English tokenizer, tagger, parser and NER
with open('clean.txt', encoding="utf8") as file:
    full_text = file.read()

# Boilerplate
sentences = getSentences(full_text)
nlp = spacy.load("en_core_web_sm")
# Set max length to avoid exception
doc = nlp(full_text[: 1000000])


# Analyze syntax (boilerplate)
noun_arr = [chunk.text for chunk in doc.noun_chunks]
verb_arr = [token.lemma_ for token in doc if token.pos_ == "VERB"]

nouns = organizeNouns(noun_arr)
verbs = organizeVerbs(verb_arr)
structures = getStructures(sentences)

out = open('analyzed.csv', 'w')

out.write("Total tweets,{}\n".format(
    str(sum(1 for line in open('clean.txt', encoding="utf8")))))

out.write("Total sentences,{}\n".format(str(len(sentences))))

out.write("Average sentence length <chars> <words>,{},{}\n".format(
    str(aveSentLen(sentences)), str(aveSentWords(sentences))))

out.write("Most used verbs\n")
for top_verb in list(verbs)[:10]:
    out.write("{},{}\n".format(
        top_verb, verbs[top_verb]))

out.write("Most used nouns\n")
for top_noun in list(nouns)[:10]:
    out.write("{},{}\n".format(
        top_noun, nouns[top_noun]))

out.write("Most used sentence structures\n")
for struct in list(structures)[:10]:
    out.write("{},{}\n".format(
        struct, structures[struct]))