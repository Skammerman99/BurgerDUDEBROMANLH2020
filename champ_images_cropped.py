import requests
import shutil
import cv2

id = 266
# somewhere here relate champ id to champ name, in this case Nami
champion = "Nami"
num = 3
image_url= "http://ddragon.leagueoflegends.com/cdn/img/champion/loading/{}_{}.jpg".format(champion, num)
filename = image_url.split("/")[-1]
print(filename)

r= requests.get(image_url, stream =True)

if r.status_code ==200:
    r.raw.decode_content = True
    with open(filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    print('Image successfully downloaded: {}'.format(filename))
else:
    print("Image couldn't be retrieved")

image = cv2.imread(filename)
y=0
x=0
h=308
w=308
crop_image= image[x:w, y:h]
cv2.imwrite("Champ1.png", crop_image)
cv2.waitKey(0)



# img = Image.open(filename)
# width, height = img.size
# print(width, height)
# img = img.crop((0,50,510,292))
img.show()