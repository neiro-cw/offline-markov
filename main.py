import os

import asyncio
import discord
import markovify
from random import randrange
import re
from collections import defaultdict
from config import TOKEN

def load_markov():
    global markov2, markov3
    with open("history.txt", "r") as f:
        text = f.read()
    with open("new_messages.txt", "r") as f:
        text += f.read()

    markov3 = markovify.NewlineText(text, state_size = 3)
    markov2 = markovify.NewlineText(text, state_size = 2)

def load_emotes(guilds):
    global emotes
    emotes = {}
    for guild in guilds:
        emotes[guild.id] = {":"+e.name+":": e for e in guild.emojis if not e.animated}


def format_message(text):
    return rem.sub(r":\1:", text.replace("\n", " ").replace("  ", " ").replace("||", ""))

def sentence_with_start(model, start, tries = 10):
    for i in range(tries):
        sentence = model.make_sentence_with_start(start, strict=False)
        if sentence:
            return sentence

    return None

def markov_say(words):
    if not words:
        return None

    for n in range(3, 1, -1):
        sentence = sentence_with_start(markov3, " ".join(words[:n]))
        if sentence:
            return sentence
        sentence = sentence_with_start(markov2, " ".join(words[:n]))
        if sentence:
            return sentence

    return None

def markov_random():
    sentence = markov3.make_sentence(tries=10)
    if sentence:
        return sentence
    return markov2.make_sentence(tries=10)

def format_emotes(message, guild_id):
    if guild_id not in emotes:
        return message

    for name, emote in emotes[guild_id].items():
        message = message.replace(name, str(emote))

    return message

async def greetings(guilds, message):
    for guild in guilds:
        if not guild.id in main_channels:
            continue

        await guild.get_channel(main_channels[guild.id]).send(message)


rem = re.compile(r"<:([\w\d]+)(~\d+)?:\d+>")
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

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = format_message(message.content)

    with open("new_messages.txt", "a") as f:
        f.write(content + "\n")

    react_if_fail = True
    if content.lower().startswith("markov say"):
        sentence_start = content.split()[2:]
        try:
            response = markov_say(sentence_start)
        except Exception:
            print(f"Failed to find an answer to \"{content}\"")
            await message.add_reaction("❓")
            return
    elif "markov" in content.lower(): # or client.user.mentioned_in(message):
        response = markov_random()
    elif randrange(0, 100) == 0:
        react_if_fail = False
        await asyncio.sleep(3)
        response = markov_random()
    else:
        return

    if response:
        response = format_emotes(response, message.guild.id)
        await message.channel.send(response)
    elif react_if_fail:
        await message.add_reaction("❌")

client.run(TOKEN)
