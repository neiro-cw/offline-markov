import re
import sys

if not len(sys.argv) > 1:
    exit()

rep = re.compile(r"[^\s](,|\?|!|\.)")
url = re.compile(r"[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)")
filename = sys.argv[1]
with open(filename, "r") as r, open("fixed_" + filename, "w") as w:
    for line in r.readlines():
        newline = []
        for word in line.split():
            if len(word) > 2 and word[0] == ':' and word[-1] == ':':
                newline.append(word)
                continue
            elif url.match(word):
                newline.append(word)
                continue

            newline.append(rep.sub(r" \1", word))

        w.write(" ".join(newline) + "\n")
