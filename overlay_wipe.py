from PIL import Image
num =1
name = 'champ{}.png'.format(num)
for num in range (0,11):
    img= Image.open("transparent.png")
    img.save(name)
    num += 1
    name = 'champ{}.png'.format(num)