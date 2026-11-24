#!/usr/bin/env python3
"""Write the dashboard as one self-contained HTML file: data, labs and the logic graph inlined.

    python3 map/build.py && python3 map/bundle.py [output.html]

The default output is map/dashboard-single.html (not tracked by git). The file needs no server and
no network: attach it to a message or open it from disk. The pages under map/ stay the source."""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
read = lambda name: open(os.path.join(HERE, name), encoding="utf8").read()
# "<" never appears raw inside an inlined script, so no "</script>" or "<!--" can end or confuse it.
js = lambda x: json.dumps(x, ensure_ascii=False).replace("<", "\\u003c")

graph = json.loads(read("graph.json"))
card = read("card.js")
assert "</script" not in card and "<!--" not in card

def sub(page, tag, body):
    assert page.count(tag) == 1, tag
    return page.replace(tag, body)
def inline(page, data_script):
    page = sub(page, '<script src="graph.js"></script>', "<script>" + data_script + "</script>")
    return sub(page, '<script src="card.js"></script>', "<script>" + card + "</script>")

labs = {name: read(name) for name in sorted({n["vis"]["file"] for n in graph["nodes"] if n.get("vis")} | {"labs/views.html"})}
# The graph page gets its data from the dashboard when it is shown: index.html fills in /*BOOT*/.
pages = {"graph.html": inline(read("graph.html"), "/*BOOT*/")}
data = "window.GRAPH = " + js(graph) + ";\nwindow.LABS = " + js(labs) + ";\nwindow.PAGES = " + js(pages) + ";\n"
out = inline(read("index.html"), data)
assert not re.search(r'<script[^>]+src=|<link[^>]+href=', out), "something is still loaded from another file"

path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "dashboard-single.html")
open(path, "w", encoding="utf8").write(out)
print(path, f"{len(out.encode('utf8')) / 1e6:.2f} MB,", len(labs), "labs inlined")
