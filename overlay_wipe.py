from PIL import Image

f = open("Tweets.txt", "w+")
f.write("")
f.close()

f = open("Team1.txt", "w+")
f.write("")
f.close()
f = open("Team2.txt", "w+")
f.write("")
f.close()

for num in range (0,10):
    img= Image.open("transparent.png")
    img.save('champ{}.png'.format(num + 1))
    img.save('spell{}.png'.format(2*num + 1))
    img.save('spell{}.png'.format(2*num + 2))
    img.save('ban{}.png'.format(num+1))
    sumname = "Summoner{}.txt".format(num + 1)
    f = open(sumname, "w+")
    f.write("")
    f.close()


