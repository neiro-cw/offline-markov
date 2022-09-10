import re

ref = re.compile(r"(\s|^)(forsenE|fors|forsen|forsens|forsen's|nina|nani|@[\w\d_-]+)(\s|\.|,|;|:|!|\?|$)")
rep = re.compile(r"(u/|r/|reddit|upvot|pedo|vadikus|weebikus|downvot|baj|peppah|forsa+n|hitler|mong|asylum)")
rem = re.compile(r"\[(.+?)\]\(((?:\/|https?:\/\/)[\w\d./?=#]+)\)")
ree = re.compile(r"(\s|^)(OMEGALUL|forsenLevel|AYAYA|COPIUM|forsenSmug|forsenCD|Clueless|Susge|LOLW|LULE|PagMan|Bedge|ResidentSleeper|KEKW|KEKL|flushE|pepeW|monkaLaugh|Dogege|Catge|FeelsBirthdayMan|FeelsWeirdMan|Pepege|Pepega|Okayge|FeelsOkayMan|WeirdChamp|KKonaW|3Head|PepeHands|gachiGASM|POGGERS|WTFF|Pog|EZ|peepoHappy|OMEGALULiguess|Sadge|PepeLaugh)(\s|\.|,|;|:|!|\?|$)")

with open('baj_full.txt', "r") as r, open('baj.txt', 'w') as w:
    for l in r.readlines():
        if not ref.search(l.lower()) and not rep.search(l.lower()):
            tmp = ree.sub(r"\1:\2:\3", l)
            w.write(rem.sub(r"\1", tmp).strip() + "\n")


