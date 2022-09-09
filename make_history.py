import json
import os
from datetime import datetime
import re


# date format
# 2021-01-03T15:37:40.035+00:00
s = "%Y-%m-%dT%H:%M:%S"
start_date = datetime.strptime("0001-01-01T01:01:01", s)

with open("history.txt", "w") as f:
    for fn in [fn for fn in os.listdir() if fn.endswith(".json")]:
        with open(fn, "r") as j:
            js = json.load(j)

        author = None
        msg = ""
        time_prev = start_date
        for m in js["messages"]:
            time_cur = datetime.strptime(m["timestamp"].split('.')[0].split("+")[0], s)
            if author == m["author"]["id"] and (time_cur - time_prev).total_seconds() < 60:
                if not m['content']:
                    continue
                if not m['content'].startswith("I "):
                    m['content'] = m['content'][0].lower() + m['content'][1:]
                msg += " " + m['content'].replace("\n", " ").replace("  ", " ").replace("||", "").replace("*", "")
            else:
                if msg:
                    f.write(msg + "\n")
                author = m["author"]["id"]
                msg = m["content"].replace("\n", " ").replace("  ", " ").replace("||", "").replace("*", "")
            time_prev = time_cur




