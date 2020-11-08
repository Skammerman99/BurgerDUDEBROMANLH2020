from lcuapi import LCU, Event, EventProcessor
from config import RG_API_KEY
from collections import defaultdict
import requests
import champ_select_overlay
import sums

players_dict = defaultdict(dict)

champ_name_exceptions = {"Kog'Maw" : "KogMaw",
                         "Nunu & Willump" : "Nunu",
                         "Rek'Sai" : "RekSai"
                        }

sum_exception = {"/lol-game-data/assets/DATA/Spells/Icons2D/SummonerIgnite.png" : "SummonerDot",
                 "/lol-game-data/assets/DATA/Spells/Icons2D/SummonerBarrier.png" : "SummonerBarrier"}


players_dict = defaultdict(dict)

def playerDictHelper(summonerName):
    summoner_name = str(summonerName)
    url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-account/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": RG_API_KEY
    }

    response = requests.request("GET", url + summoner_name, headers=headers)
    print(response.json()['id'])

class PrintChampSelectInfo(EventProcessor):
    global players_dict

    # Returns True if the event handler can handle the event, False otherwise.
    def can_handle(self, event: Event):
        if issubclass(event.__class__, Event):
            return True
        return False

    # event.uri, event.created, event.data
    """def handle(self, event: Event):
        if event.uri.startswith("/lol-champ-select/v1/grid-champions"):
            print(event.data['data']['name'])"""

    def handle(self, event: Event):
        event_json = event.data['data']
        if event.uri.startswith("/lol-champ-select/v1/grid-champions"):
            # If a champ has been banned
            if event_json['selectionStatus']['isBanned']:
                print(event_json['name'] + " has been banned.")
            # If a champ is not banned but has "pickedByOtherOrBanned" set to True, it has been picked
            #elif not event_json['selectionStatus']['isBanned'] and event_json['selectionStatus'][
            #    'pickedByOtherOrBanned']:
                #if event_json['name'] in champ_name_exceptions.keys():
                    #champ_name = champ_name_exceptions[event_json['name']]
                #else:
                    #champ_name = event_json['name'].replace(" ", "")
                    #if "'" in champ_name:
                     #   champ_name = champ_name[0] + champ_name[1:].replace("'", "").lower()
                #print(champ_name + " has been picked.")
                #champ_select_overlay.addChampPick(champ_name, 0, 1)
        if event.uri.startswith("/lol-champ-select/v1/summoners"):
            print(event_json)
            summonerSlotID = event_json['slotId']
            temp = {
                "summonerId": event_json['summonerId'],
                "skinId": event_json['skinId'],
                "spell1": event_json['spell1IconPath'],
                # FIX-ME - Integrate better with DataDragon, use actual spell name?
                "spell2": event_json['spell2IconPath'],
            }
            players_dict[summonerSlotID] = temp

            champ_name = event_json['championName']
            print(champ_name + " has been picked.")
            if champ_name != "":
                champ_select_overlay.addChampPick(champ_name, 0, summonerSlotID+1)
            #
            # print(event_json['spell1IconPath'])
            # if event_json['spell1IconPath'] in sum_exception.keys():
            #     spell1 = sum_exception[event_json['spell1IconPath']]
            #     print(spell1temp)
            # else:
            #     spell1temp = event_json['spell1IconPath'].split("/")[-1][:-4].split("_")
            #     spell1 = spell1temp[0] + spell1temp[1][0].upper() + spell1temp[1][1:]
            # sums.addSummonerSpell(spell1, 1)
            #
            # if event_json['spell2IconPath'] in sum_exception.keys():
            #     spell2 = sum_exception[event_json['spell2IconPath']]
            # else:
            #     spell2temp = event_json['spell2IconPath'].split("/")[-1][:-4].split("_")
            #     print(spell2temp)
            #     spell2 = spell2temp[0] + spell2temp[1][0].upper() + spell2temp[1][1:]
            # sums.addSummonerSpell(spell2, 2)

        if event.uri.startswith("/lol-summoner/v1/current-summoner"):
            print()
            print("TEST JSON LOOK HERE JAMEL LOOK")
            print(event_json)



class InGameStats(EventProcessor):
    # Returns True if the event handler can handle the event, False otherwise.
    def can_handle(self, event: Event):
        if issubclass(event.__class__, Event):
            return True
        return False


def main():
    lcu = LCU()
    lcu.attach_event_processor(PrintChampSelectInfo())
    lcu.wait_for_client_to_open()
    lcu.wait_for_login()
    lcu.process_event_stream()
    lcu.wait()


if __name__ == '__main__':
    main()
