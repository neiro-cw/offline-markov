import os

import asyncio
import markovify
from random import randrange
import re

def load_markov():
    global markov3
    with open("history.txt", "r") as f:
        text = f.read()
    with open("new_messages.txt", "r") as f:
        text += f.read()

    markov3 = markovify.NewlineText(text, state_size = 3)

def sentence_with_start(model, start, tries = 25):
    print(f"start = {start}")
    for i in range(tries):
        sentence = model.make_sentence_with_start(start, strict=False)
        if sentence:
            return sentence

    return None

def markov_say(words):
    if not words:
        return None

    for n in range(3):
        try:
            sentence = sentence_with_start(markov3, " ".join(words[n:]))
        except Exception:
            continue
        if sentence:
            print(f"n = {n}")
            return " ".join(words[:n]) + (" " if n != 0 else "") + sentence

    return None

def markov_random():
    sentence = markov3.make_sentence(tries=25)
    return sentence

load_markov()

response = None
content = "markov say I think I am a"
if content.lower().startswith("markov say"):
    sentence_start = content.split()[-3:]
    response = markov_say(sentence_start)
    response = " ".join(content.split()[2:-3]) + " " + response

if response:
    print(response)

