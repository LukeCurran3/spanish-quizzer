import json
import random
import os

def get_word_list():
    try:
        with open ("words_storage.json", 'r') as file:
            word_list = json.load(file)
    except FileNotFoundError:
        word_list = {}
    return word_list
def save_word(word_list):
    with open ("words_storage.json", 'w') as file:
        json.dump(word_list, file, indent = 1)
def add_word(word_list):
    word_span = input("Que es la palabara en Espanol?").strip().lower()
    word_eng = input("Que es la palabra en ingles?").strip().lower()
    word_list[word_span] = {"Spanish:": word_span, "English:": word_eng}
    save_word(word_list)
    print("Tu palabra ha sido anadida!")


def quiz(word_list):
    if not word_list:
        print("Necasitas poner palabras para aprender primero!")
        return
    quiz_words = list(word_list.keys())
    random.shuffle(quiz_words)
    response = ""
    count = 0
    print('La hora de examen! Escribi "Para" para parar la programa')
    while response != "para" and count <= len(word_list):
        span_word = quiz_words[count]
        eng_word = quiz_words[span_word]["English:"]
        print(eng_word + "/n")
        response = input("Tranduction: ")
        
        if response == span_word:
            print("Correcto! Usala en una phrase!")
            input()
            print("Muy Bien!")
        else:
            print("Incorrecto")
    count+=1


        
