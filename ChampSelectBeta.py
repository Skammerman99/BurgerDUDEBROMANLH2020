from lcuapi import LCU, Event, EventProcessor
from config import RG_API_KEY
from collections import defaultdict
import requests
import champ_select_overlay
import sums

# players_dict is constantly updating to check for summoner spell changes & champion changes.
# name_dict is created at the start of champ select and is not updated
players_dict = defaultdict(dict)
name_dict = defaultdict(str)
bans_dict = defaultdict(list)

sum_exception = {"/lol-game-data/assets/DATA/Spells/Icons2D/SummonerIgnite.png" : "SummonerDot",
                 "/lol-game-data/assets/DATA/Spells/Icons2D/SummonerBarrier.png" : "SummonerBarrier"}

champ_name_exceptions = {"Kog'Maw" : "KogMaw",
                         "Nunu & Willump" : "Nunu",
                         "Rek'Sai" : "RekSai",
                         "Dr. Mundo" : "DrMundo",
                         "LeBlanc" : "Leblanc"
                        }



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
        if event.uri.startswith("/lol-champ-select/v1/session"):
            print("BANS HERE PLS WORG " + str(event_json['bans']))
            bans_dict["blue_side_ids"] = event_json['bans']['myTeamBans']
            bans_dict["red_side_ids"] = event_json['bans']['theirTeamBans']
            print(bans_dict)

        if event.uri.startswith("/lol-champ-select/v1/grid-champions"):
            # If a champ has been banned
            if event_json['selectionStatus']['isBanned']:
                print(event_json['name'] + " has been banned.")
                if len(bans_dict["blue_side_names"]) == len(bans_dict["red_side_names"]):
                    bans_dict["blue_side_names"].append(event_json['name'])
                    champ_select_overlay.addChampBan(event_json['name'], len(bans_dict["blue_side_names"]))
                else:
                    bans_dict["red_side_names"].append(event_json['name'])
                    champ_select_overlay.addChampBan(event_json['name'], len(bans_dict["red_side_names"]) + 5)
                print(bans_dict)

        if event.uri.startswith("/lol-champ-select/v1/summoners"):
            if not event_json['isPlaceholder']:
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
                        #print("spell1temp = " + str(spell1temp))
                        spell1 = spell1temp[0] + spell1temp[1][0].upper() + spell1temp[1][1:]
                    sums.addSummonerSpell(spell1, 2 * summonerSlotID + 1)

                    if event_json['spell2IconPath'] in sum_exception.keys():
                        spell2 = sum_exception[event_json['spell2IconPath']]
                    else:
                        spell2temp = event_json['spell2IconPath'].split("/")[-1][:-4].split("_")
                        #print("spell2temp = " + str(spell2temp))
                        spell2 = spell2temp[0] + spell2temp[1][0].upper() + spell2temp[1][1:]
                    sums.addSummonerSpell(spell2, 2*summonerSlotID + 2)


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
            import time
            time.sleep(2)
            print("Awaiting start of Champ Select")
        else:
            print("Champ Select detected, players present:")
            for k, v in players_dict.items():
                url = '/lol-summoner/v1/summoners/' + str(players_dict[k]['summonerId'])
                summoner_json = lcu.get(url)
                name_dict[k] = summoner_json['displayName']
                print(summoner_json['displayName'])
            temp = False
    lcu.wait()


if __name__ == '__main__':
    main()
