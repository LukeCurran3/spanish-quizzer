from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import json
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

with open("spanish-quizzer/data/redditdata.json", "r", encoding="utf-8") as f:
    all_docs = json.load(f)

labels = list(all_docs.keys())
docs = list(all_docs.values())



vectorizer = TfidfVectorizer (min_df=1,max_df=0.4, ngram_range=(1,1))
X_tfidf = vectorizer.fit_transform(docs)
feature_names = vectorizer.get_feature_names_out()
top_n = 40

regional_slang = []

for i, label in enumerate(labels):
    row = X_tfidf[i].toarray().ravel()
    top_idx = np.argsort(row)[-top_n:]
    top_words = [feature_names[j] for j in reversed(top_idx)]
    regional_slang.append({"region": label, "slang": top_words})



base = declarative_base()
class SlangWord(base):
    __tablename__ = 'slang_words'

    id = Column(Integer, primary_key=True)
    region = Column(String)
    word = Column(String)
    score = Column(Float)


engine = create_engine("sqlite:///slang.db")
base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

for i, label in enumerate(labels):
    row = X_tfidf[i].toarray().ravel()
    top_idx = np.argsort(row)[-top_n:]
    top_words = [feature_names[j] for j in reversed(top_idx)]
    
    for j in reversed(top_idx):
        word = feature_names[j]
        score = row[j]
        slang_entry = SlangWord(region=label, word=word, score=score)
        session.add(slang_entry)

session.commit()