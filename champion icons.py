import requests
import shutil

champion = "Yasuo"

image_url= "http://ddragon.leagueoflegends.com/cdn/10.22.1/img/champion/{}.png".format(champion)
filename = image_url.split("/")[-1]
# print(filename)

r= requests.get(image_url, stream =True)

if r.status_code ==200:
    r.raw.decode_content = True
    with open(filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    print('Image successfully downloaded: {}'.format(filename))
else:
    print("Image could\n't be retrieved")
