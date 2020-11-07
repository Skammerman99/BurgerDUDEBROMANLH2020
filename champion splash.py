import requests
import shutil

id = 266
# somewhere here relate champ id to champ name, in this case Nami
champion = "Vi"
num = 1

image_url= "http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{}_{}.jpg".format(champion, num)
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
