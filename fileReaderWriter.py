def readFile (fileName, seekInfo): #looks in the file (fileName) and returns info from the info u request (seekInfo)
    with open (fileName, 'r') as file:
        for line in file:
            if seekInfo in line:
                information = line[(len(seekInfo.strip()) + 1):(len(line.strip()))]
                break
    return int(information)


def writeFile (fileName, valueName, writeValue):
    with open (fileName, 'r+') as file:
        list_of_lines = file.readlines()
        file.seek(0)
        i = 0
        for line in file:
            i += 1
            if valueName in line:
                list_of_lines[i-1] = f"{valueName}:{writeValue}\n"
                file.seek(0)
                file.writelines (list_of_lines)
                break