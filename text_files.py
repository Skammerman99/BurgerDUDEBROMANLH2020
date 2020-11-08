# num = 1
# sumname = "Summoner{}.txt".format(num)

def addSummonerNameFile(name, slot):
    for i in range(10):
        sumname = "Summoner{}.txt".format(slot+1)
        f = open(sumname, "w+")
        f.write(name)


