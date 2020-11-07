from PIL import Image
num =1
name = 'champ{}.png'.format(num)
while name != "champ11.png":
    img= Image.open("transparent.png")
    img.save(name)
    num += 1
    name = 'champ{}.png'.format(num)