import json
import os
from datetime import datetime
# date format
# 2021-01-03T15:37:40.035+00:00
s = "%Y-%m-%dT%H:%M:%S"
start_date = datetime.strptime("0001-01-01T01:01:01", s)

def addfile(filename):
    with open(filename, "r") as f:
        js = json.load(f)
    with open(f"txt/{filename}.txt", "w") as f:
        for m in js["messages"]:
            if len(m['content']) > 0:
                f.write(m["content"].replace("\n", " ") + '\n')

with open("lines.txt", "w") as f:
    for fn in [fn for fn in os.listdir() if fn.endswith(".json")]:
        with open(fn, "r") as j:
            js = json.load(j)

        author = None
        msg = ""
        time_prev = start_date
        for m in js["messages"]:
            time_cur = datetime.strptime(m["timestamp"].split('.')[0].split("+")[0], s)
            if author == m["author"]["id"] and (time_cur - time_prev).total_seconds() < 60:
                msg += " " + m['content'].replace("\n", " ").replace("  ", " ").replace("||", "").replace("*", "")
            else:
                if msg:
                    f.write(msg + "\n")
                author = m["author"]["id"]
                msg = m["content"].replace("\n", " ").replace("  ", " ").replace("||", "").replace("*", "")
            time_prev = time_cur




