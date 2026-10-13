with open('src/agentos/db/connection.py') as f: lines=f.read().splitlines()
for i,l in enumerate(lines):
    if 'class Connection' in l:
        print(i+1, l)
        for j in range(i, min(i+20,len(lines))):
            print(j+1, lines[j])
