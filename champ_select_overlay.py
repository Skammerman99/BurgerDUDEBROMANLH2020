import requests
import shutil
import cv2



def fullCSTest():
    id = 266
    # somewhere here relate champ id to champ name, in this case Nami
    champions = ["Shen", "Graves", "Syndra", "Samira", "Leona", "Ornn", "Hecarim", "Galio", "Ezreal", "Yuumi"]
    num = 0
    cs_slot_num = 1


    for champion in champions:
        addChampPick(champion, 0, cs_slot_num)
        cs_slot_num += 1

def addChampPick(champion, skinID, slot):
    print('attempting to update with ' + champion)
    image_url = "http://ddragon.leagueoflegends.com/cdn/img/champion/loading/{}_{}.jpg".format(champion, 0)
    print(image_url)
    # filename = image_url.split("/")[-1]
    filename = "champ" + str(slot) + ".png"
    print(filename)

    r = requests.get(image_url, stream=True)

    if r.status_code == 200:
        r.raw.decode_content = True
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        print('Image successfully downloaded: {}'.format(filename))
    else:
        print("Image could\n't be retrieved")

    image = cv2.imread(filename)
    resized_image = cv2.resize(image, (160, 291))
    cv2.imwrite(filename, resized_image)
    cv2.waitKey(0)

def addChampBan(champion, slot):
    #print('attempting to update with ' + champion)
    image_url = "http://ddragon.leagueoflegends.com/cdn/10.22.1/img/champion/{}.png".format(champion)
    #print(image_url)
    # filename = image_url.split("/")[-1]
    filename = "ban" + str(slot) + ".png"
    #print(filename)

    r = requests.get(image_url, stream=True)

    if r.status_code == 200:
        r.raw.decode_content = True
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        #print('Image successfully downloaded: {}'.format(filename))
    else:
        print("Image could\n't be retrieved")

    image = cv2.imread(filename)
    resized_image = cv2.resize(image, (80, 80))
    cv2.imwrite(filename, resized_image)
    cv2.waitKey(0)

if __name__ == '__main__':
    fullCSTest()
