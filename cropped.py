import requests
import shutil
import cv2

champion = "Talon"
num = 0
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
    print("Image could\n't be retrieved")

image = cv2.imread(filename)
y=20
x=100
h=300
w=250
crop_image= image[x:w, y:h]
cv2.imwrite("Champ1.png", crop_image)
cv2.waitKey(0)
