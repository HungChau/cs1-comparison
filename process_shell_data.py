with open("shell.day6.txt") as f:
    for line in f:
        if line[:4] in ['>>> ', '... ']:
            print(line[4:].rstrip())