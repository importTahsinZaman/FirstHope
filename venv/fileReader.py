def readFile (fileName, seekInfo):
    with open (fileName, 'r') as file:
        for line in file:
            if seekInfo in line:
                information = line.strip("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " ")

    return int(information)