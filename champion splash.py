import requests
import shutil

id = 266
# somewhere here relate champ id to champ name, in this case Nami
champions = ["Shen", "Graves", "Syndra", "Samira", "Leona", "Ornn", "Hecarim", "Galio", "Ezreal", "Yuumi"]
num = 0
cs_slot_num = 1

for champion in champions:
    image_url= "http://ddragon.leagueoflegends.com/cdn/img/champion/loading/{}_{}.jpg".format(champion, num)
    #filename = image_url.split("/")[-1]
    filename = "champ" + str(cs_slot_num) + ".png"
    print(filename)

    r= requests.get(image_url, stream =True)

    if r.status_code ==200:
        r.raw.decode_content = True
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        print('Image successfully downloaded: {}'.format(filename))
    else:
        print("Image could\n't be retrieved")

    cs_slot_num += 1
