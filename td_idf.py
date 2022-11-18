import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from warnings import simplefilter


def calc_td_idf(docs: list):
    """:returns: dataframe of words significance in floats per document
    :rtype: 2-dimensional labeled data structure"""

    # ignore all future warnings
    simplefilter(action="ignore", category=FutureWarning)

    corpus = []

    for doc in docs:
        with open(doc, encoding="utf-8") as f:
            corpus.append(f.read())

    tr_idf_model = TfidfVectorizer()
    tf_idf_vector = tr_idf_model.fit_transform(corpus)

    print(type(tf_idf_vector), tf_idf_vector.shape)

    words_set = tr_idf_model.get_feature_names()

    tf_idf_array = tf_idf_vector.toarray()

    df_tf_idf = pd.DataFrame(tf_idf_array, columns=words_set)

    return df_tf_idf
