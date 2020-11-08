from PIL import Image

for num in range (0,10):
    img= Image.open("transparent.png")
    img.save('champ{}.png'.format(num + 1))
    img.save('spell{}.png'.format(2*num + 1))
    img.save('spell{}.png'.format(2*num + 2))
    img.save('ban{}.png'.format(num+1))

