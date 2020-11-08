num = 1
sumname = "Summoner{}.txt".format(num)

for i in range(10):
    f = open(sumname, "w+")
    f.write("potato")
    num += 1
    sumname = "Summoner{}.txt".format(num)
