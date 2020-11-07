from lcuapi import LCU, Event, EventProcessor
import champ_select_overlay



class PrintChampSelectInfo(EventProcessor):
    summoner_spell_dict = {

    }

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
            elif not event_json['selectionStatus']['isBanned'] and event_json['selectionStatus'][
                'pickedByOtherOrBanned']:
                print(event_json['name'] + " has been picked.")
                champ_select_overlay.addChampPick(event_json['name'], 0, 1) #FIX-ME - Issue with space in champ name
        if event.uri.startswith("/lol-champ-select/v1/summoners"):
            summonerId = event_json['summonerId']
            summonerSlotID = event.uri[-1]
            skinId = event_json['skinId']
            spell1= event_json['spell1IconPath']
            spell2 = event_json['spell2IconPath']



def main():
    lcu = LCU()
    lcu.attach_event_processor(PrintChampSelectInfo())
    lcu.wait_for_client_to_open()
    lcu.wait_for_login()
    lcu.process_event_stream()
    lcu.wait()


if __name__ == '__main__':
    main()
