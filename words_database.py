from text_preprocessing import text_preprocess
from td_idf import calc_td_idf
import sqlite3


def fill_and_query_db(file_name: str):
    conn = sqlite3.connect("words.db")

    c = conn.cursor()

    c.execute("""DROP TABLE IF EXISTS words""")
    c.execute("""DROP TABLE IF EXISTS pos""")
    c.execute("""DROP TABLE IF EXISTS inflections""")

    c.execute(
        """CREATE TABLE IF NOT EXISTS words (
     			word_id integer primary key,
    			pos_type varchar(50),
     			spelling varchar(50))
     	"""
    )

    c.execute(
        """CREATE TABLE IF NOT EXISTS pos (
     			pos_type varchar(50))

     	"""
    )

    c.execute(
        """CREATE TABLE IF NOT EXISTS inflections (
     			word_id integer,
     			inflected_form varchar(50),
     			FOREIGN KEY (word_id) REFERENCES words(word_id))
    	"""
    )

    conn.commit()

    lemma_info = text_preprocess(file_name)

    # define part of speech tags set

    pos = set([v[0] for v in lemma_info.values() if v[0] is not None])

    for i in pos:
        c.execute("INSERT INTO pos VALUES (?)", (i,))
        conn.commit()

    i = 1
    for k, v in lemma_info.items():
        c.execute("INSERT INTO words VALUES (?, ?, ?)", (i, v[0], k))
        for inf in v[1]:
            c.execute("INSERT INTO inflections VALUES (?, ?)", (i, inf))
        i += 1
        conn.commit()

    # calculate POS

    calc_pos = c.execute(
        "SELECT pos_type,COUNT(pos_type) FROM words GROUP BY pos_type ORDER BY COUNT(pos_type) DESC"
    ).fetchall()

    # calculates all inflections per POS type

    calc_inf = c.execute(
        "SELECT pos_type, COUNT(inflected_form) FROM words INNER JOIN inflections ON words.word_id = inflections.word_id GROUP BY pos_type ORDER BY COUNT(inflected_form) DESC"
    ).fetchall()

    print(f"Кількість частин мови: {calc_pos}")
    print(f"Кількість відмінювань на кожну з частин мови: {calc_inf}")
    conn.close()


docs = ["poetry.txt", "state_theory.txt", "tales.txt", "narys_istorii.txt"]

for doc in docs:
    print(f"\nТекст: {doc}")
    fill_and_query_db(doc)

print(f"\nDataframe of td_idf: {calc_td_idf(docs)}")
