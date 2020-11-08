from lcuapi import LCU, Event, EventProcessor
from config import RG_API_KEY
from collections import defaultdict
import requests
import champ_select_overlay
import sums
import time
import text_files
import tweet_stream

REGION = "na1"
patch_json = requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()
latest_patch = patch_json[0]

# players_dict is constantly updating to check for summoner spell changes & champion changes.
# name_dict is created at the start of champ select and is not updated
players_dict = defaultdict(dict)
name_dict = defaultdict(str)
bans_dict = defaultdict(lambda: defaultdict(str))

sum_exception = {"/lol-game-data/assets/DATA/Spells/Icons2D/SummonerIgnite.png": "SummonerDot",
                 "/lol-game-data/assets/DATA/Spells/Icons2D/SummonerBarrier.png": "SummonerBarrier"}

champ_name_exceptions = {"Kog'Maw": "KogMaw",
                         "Nunu & Willump": "Nunu",
                         "Rek'Sai": "RekSai",
                         "Dr. Mundo": "DrMundo",
                         "LeBlanc": "Leblanc"
                         }



def targetedBanHelper():
    for side, ban_list in bans_dict.items():
        for banned_id, champ_name in ban_list.items():
            for player in name_dict.values():
                print(player)
                if banned_id in player['mains']:
                    print("Target Ban: " + player['username'] + " mains " + champ_name)


class PrintChampSelectInfo(EventProcessor):
    global players_dict
    global bans_dict

    # Returns True if the event handler can handle the event, False otherwise.
    def can_handle(self, event: Event):
        if issubclass(event.__class__, Event):
            return True
        return False

    def handle(self, event: Event):
        event_json = event.data['data']
        # if event.uri.startswith("/lol-champ-select/v1/session"):
        #     print("BANS HERE PLS WORG " + str(event_json['bans']))
            # for ban in event_json['bans']['myTeamBans']:
            #     bans_dict["blue_side"] =
            # bans_dict["blue_side"] = event_json['bans']['myTeamBans']
            # bans_dict["red_side"] = event_json['bans']['theirTeamBans']
            # print(bans_dict)

        if event.uri.startswith("/lol-champ-select/v1/grid-champions"):
            # If a champ has been banned
            if event_json['selectionStatus']['isBanned']:
                print(event_json['name'] + " has been banned.")
                champ_name =  event_json['name']
                if champ_name in champ_name_exceptions.keys():
                    champ_name = champ_name_exceptions[champ_name]
                else:
                    champ_name = champ_name.replace(" ", "")
                    if "'" in champ_name:
                        champ_name = champ_name[0] + champ_name[1:].replace("'", "").lower()

                if len(bans_dict["blue_side"]) == len(bans_dict["red_side"]):
                    bans_dict["blue_side"][event_json['id']] = champ_name
                    champ_select_overlay.addChampBan(champ_name, len(bans_dict["blue_side"]))
                else:
                    bans_dict["red_side"][event_json['id']] = champ_name
                    champ_select_overlay.addChampBan(champ_name, len(bans_dict["red_side"]) + 5)
                # print(bans_dict)
                targetedBanHelper()

        if event.uri.startswith("/lol-champ-select/v1/summoners"):
            if not event_json['isPlaceholder']:
                # print(event_json)
                summonerSlotID = event_json['slotId']
                temp = {
                    "summonerId": event_json['summonerId'],
                    "skinId": event_json['skinId'],
                    "spell1": event_json['spell1IconPath'],
                    "spell2": event_json['spell2IconPath'],
                }
                players_dict[summonerSlotID] = temp

                champ_name = event_json['championName']

                if champ_name != "" and event_json['activeActionType'] == "pick":
                    if champ_name in champ_name_exceptions.keys():
                        champ_name = champ_name_exceptions[champ_name]
                    else:
                        champ_name = champ_name.replace(" ", "")
                        if "'" in champ_name:
                          champ_name = champ_name[0] + champ_name[1:].replace("'", "").lower()
                    print(champ_name + " has been picked.")
                    champ_select_overlay.addChampPick(champ_name, 0, summonerSlotID+1)

                if not event_json['spell1IconPath'] == '' and not event_json['spell1IconPath'] == '':
                    #print(event_json['spell1IconPath'])
                    if event_json['spell1IconPath'] in sum_exception.keys():
                        spell1 = sum_exception[event_json['spell1IconPath']]
                    else:
                        spell1temp = event_json['spell1IconPath'].split("/")[-1][:-4].split("_")
                        spell1 = spell1temp[0] + spell1temp[1][0].upper() + spell1temp[1][1:]
                    sums.addSummonerSpell(spell1, 2 * summonerSlotID + 1)

                    if event_json['spell2IconPath'] in sum_exception.keys():
                        spell2 = sum_exception[event_json['spell2IconPath']]
                    else:
                        spell2temp = event_json['spell2IconPath'].split("/")[-1][:-4].split("_")
                        #print("spell2temp = " + str(spell2temp))
                        # print("spell2temp = " + str(spell2temp))
                        spell2 = spell2temp[0] + spell2temp[1][0].upper() + spell2temp[1][1:]
                    sums.addSummonerSpell(spell2, 2*summonerSlotID + 2)

def csFinder():
    gaming = True
    while gaming:
        try:
            print("I'm looking for in game data.")
            jamel = requests.request("GET", "​https://127.0.0.1:2999/liveclientdata/playersummonerspells?summonerName=MrFrostByt3")
            print(jamel)
            # if jamel['creepScore'] > 6:
            # print("Jamel is a god at CSing: ", jamel['creepScore'])
            time.sleep(5)
        except KeyError as error:
            # print("Either we're not in game, or something is wrong. Either way, we'll try again in one minute!")
            # print("Error message: ", error)
            time.sleep(5)  # FIX-ME - make me 60 seconds or something on release
        except Exception as e:
            print(e)
            time.sleep(30)

def main():
    global name_dict
    global players_dict
    lcu = LCU()
    lcu.attach_event_processor(PrintChampSelectInfo())
    lcu.wait_for_client_to_open()
    lcu.wait_for_login()
    lcu.process_event_stream()
    temp = True
    while temp:
        if players_dict[0] == {}:
            time.sleep(3)
            print("Awaiting start of Champ Select... (Retrying in 3 seconds)")
        else:
            print("Champ Select detected, players present:")
            time.sleep(0.2)
            for k, v in players_dict.items():
                lcu_url = '/lol-summoner/v1/summoners/' + str(players_dict[k]['summonerId'])
                summoner_json = lcu.get(lcu_url)
                temp = {
                    'username': "",
                    'encryptedId': 0,
                    'mains': [],  # NOTE: MAIN CHAMPS GET SAVED AS CHAMPION IDs
                }
                temp['username'] = summoner_json['displayName']
                text_files.addSummonerNameFile(temp['username'], k)
                # Code to grab encrypted ID.
                summ_url = "https://" + REGION + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_json['displayName']

                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Origin": "https://developer.riotgames.com",
                    "X-Riot-Token": RG_API_KEY
                }

                summ4json = requests.request("GET", summ_url, headers=headers).json()
                temp['encrpytedId'] = summ4json['id']
                print("Hi Jamel I got your encrypted id right here: ", summ4json['id'])

                # Code to grab top 3 characters played
                mains_url = "https://" + REGION + ".api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" + summ4json['id']
                {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Origin": "https://developer.riotgames.com",
                    "X-Riot-Token": RG_API_KEY
                }

                mains_json = requests.request("GET", mains_url, headers=headers).json()
                temp['mains'] = [mains_json[0]['championId'], mains_json[1]['championId'], mains_json[2]['championId']]
                name_dict[k] = temp
                # print(name_dict)
                print(summoner_json['displayName'])


            temp = False
            print("I set champ select loop to false. It's done.")
        #print("calling csFinder")
        #csFinder()
    lcu.wait()


def genTeamNames(name, num):
    fname = "Team{}.txt".format(num)
    f = open(fname, "w+")
    f.write(name)

if __name__ == '__main__':
    answer = input("\nWould you like to enter team names? (Y/N)")
    if answer == "Y":
        name = input("\nEnter Team 1 Name: ")
        genTeamNames(name,1)
        name = input("\nEnter Team 2 Name: ")
        genTeamNames(name,2)

    main()