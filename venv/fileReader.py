def readFile (fileName, seekInfo):
    with open (fileName, 'r') as file:
        for line in file:
            if seekInfo in line:
                information = line[(len(seekInfo.strip()) + 1):(len(line.strip()))]

    return int(information)