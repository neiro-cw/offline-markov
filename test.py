import os

import asyncio
import discord
import markovify
from random import randrange
import re
from config import TOKEN

def load_markov():
    global markov3
    with open("fixed_history.txt", "r") as f:
        text = f.read()

    markov3 = markovify.NewlineText(text, state_size = 2)

def load_emotes(guilds):
    global emotes
    emotes = {}
    for guild in guilds:
        emotes[guild.id] = {":"+e.name+":": e for e in guild.emojis if not e.animated}


def format_message(text):
    tmp = rem.sub(r":\1:", text.replace("\n", " ").replace("  ", " ").replace("||", ""))
    return rec.sub(r"\1 \2", tmp)

def sentence_with_start(model, start, tries = 25):
    for i in range(tries):
        sentence = model.make_sentence_with_start(start, strict=False)
        if sentence:
            return sentence

    return None

def markov_say(words):
    if not words:
        return None

    l = len(words)
    for n in range(min(2, l)):
        try:
            sentence = sentence_with_start(markov3, " ".join(words[n:]))
        except Exception:
            if n == min(2, l) - 1:
                raise
            else:
                continue
        if sentence:
            return " ".join(words[:n]) + (" " if n != 0 else "") + sentence

    return None

def markov_random():
    sentence = markov3.make_sentence(tries=25)
    return sentence

def format_emotes(message, guild_id):
    return rep.sub(r"\1 ", message + " ").strip()

async def greetings(guilds, message):
    for guild in guilds:
        if not guild.id in main_channels:
            continue

        await guild.get_channel(main_channels[guild.id]).send(message)


rem = re.compile(r"<:([\w\d]+)(~\d+)?:\d+>")
rep = re.compile(r" (,|\.|!|\?) ")
rec = re.compile(r"([^\s])(,|\?|!|\.)")
load_markov()
client = discord.Client(intents=discord.Intents.all())
main_channels = {
    # Offline chat    : #markov
    794516395895291914: 1017147127559897089,
}


@client.event
async def on_ready():
    print(f'Markov up and running')
    print(f"Servers: {[guild.name for guild in client.guilds]}")
    load_emotes(client.guilds)
    await greetings(client.guilds, "markov online")

def on_message(message):
    content = format_message(message)
    print(content)

    react_if_fail = True
    if content.lower().startswith("markov say"):
        sentence_start = content.split()[2:][-2:]
        try:
            response = markov_say(sentence_start)
        except Exception:
            print(f"Failed to find an answer to \"{content}\"")
            return
        response = " ".join(content.split()[2:-2]) + " " + response
    elif "markov" in content.lower(): # or client.user.mentioned_in(message):
        response = markov_random()
    elif randrange(0, 100) == 0:
        react_if_fail = False
        response = markov_random()
    else:
        return

    if response:
        response = format_emotes(response.strip(), 0)
        print(response)
    elif react_if_fail:
        pass


on_message("markov say sissy")
on_message("markov say sissy,")
on_message("markov say sissy ,")
