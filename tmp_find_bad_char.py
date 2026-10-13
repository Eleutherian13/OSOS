with open("src/agentos/evaluation_harness.py","r",encoding="utf-8",errors="replace") as f:
    lines = f.read().splitlines()
for i,l in enumerate(lines,1):
    for ch in l:
        o = ord(ch)
        if o > 127 and ch not in "éèêëàùûüçâôîï":
            print("line", i, "char U+%04X" % o, "context:", repr(l[:120]))
