import praw
import pandas as pd
import spacy
import re
import json
import os
from langdetect import detect, LangDetectException

def is_spanish(text):
    try:
        return detect(text) == 'es'  
    except (LangDetectException, TypeError):
        return False  
    
reddit = praw.Reddit(
    client_id='Wh7pFn0kTz3kDNdUK6j4iQ',
    client_secret='wh18QDMMe6phYR2_nvrzwPH7RQ_aCQ',
    user_agent='SlangTrainer',
    username='Redit-scroller',
    password='412812'
)

nlp = spacy.load("es_core_news_sm")


subreddits = ["buenosaires","mexico","ecuador", "peru","chile","guatemala"]
docs = {}

def clean(text):
    text = re.sub(r'http\S+', '', text)  
    text = re.sub(r'@\S+', '', text)   
    text = re.sub(r'[^a-zA-ZáéíóúüñÁÉÍÓÚÜÑ\s]', '', text)  
    text= re.sub(r'\n','',text)
    doc = nlp(text.lower())  
    cleaned_text = ' '.join([token.lemma_ for token in doc if not token.is_stop])
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text

for sub in subreddits:
    posts = reddit.subreddit(sub).hot(limit=300)
    region_text = []
    for post in posts:
        if is_spanish(post.title):
            region_text.append(clean(post.title))
        if is_spanish(post.selftext):
            region_text.append(clean(post.selftext))
        post.comments.replace_more(limit=0)
        for comment in post.comments.list():
            if is_spanish(comment.body):
                region_text.append(clean(comment.body))

    # --- NEW posts ---
    new_posts = reddit.subreddit(sub).new(limit=300)
    for post in new_posts:
        if is_spanish(post.title):
            region_text.append(clean(post.title))
        if is_spanish(post.selftext):
            region_text.append(clean(post.selftext))
        post.comments.replace_more(limit=0)
        for comment in post.comments.list():
            if is_spanish(comment.body):
                region_text.append(clean(comment.body))

    joined = " ".join(region_text)
    docs[sub] = joined



os.makedirs("data", exist_ok=True)
with open("data/redditdata.json", "w", encoding="utf-8") as f:
    json.dump(docs, f, ensure_ascii=False, indent=2)
    


