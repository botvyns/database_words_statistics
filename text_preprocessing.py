from collections import defaultdict
import pymorphy2
import string
import tokenize_uk


def text_preprocess(file_name: str):
    """:returns: dictionary where key is lemmatized word and values are list [pos, [inflections]]
    :rtype: dict"""

    lemma_info = defaultdict(list)

    morph = pymorphy2.MorphAnalyzer(lang="uk")

    with open(file_name, "r", encoding="utf-8") as f:
        text = f.read()

    # tokenize text to words creating list obly of unique words

    tokenized_words = list(
        set(
            [
                word.lower()
                for word in tokenize_uk.tokenize_words(text)
                if word.isalpha()
            ]
        )
    )

    # fill lemma_info where key is lemmatized word and values are list [pos, [inflections]]

    for w in tokenized_words:
        lemma_info[morph.parse(w)[0].normal_form] = (
            morph.parse(w)[0].tag.POS,
            [inf[0] for inf in morph.parse(w)[0].lexeme],
        )

    return lemma_info

    # uncomment lines below to see keys and values of lemma_info

    # for k, v in lemma_info.items():
    #     print(k, '----->', v)
    