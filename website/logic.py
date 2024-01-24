import logging
import requests

# from datetime import datetime

#This are hardcoded region name and tagline of my account feal free to change it
region = 'europe'
name = 'Porsze'
tag_line = 'EUNE'
API_KEY_FILE_PATH = './API_KEY' #change path to pointing to your coresponding API_key
# API_KEY_FILE_PATH = './API_KEY_OLD' #old key
# API key you can get from https://developer.riotgames.com/ in your account dashboard


# function reused later to request all API endpints
def standard_get(path=''):
    r = requests.get(f'https://{region}.api.riotgames.com{path}?api_key={api_key}')
    if r.status_code == 200:
        return r.json()
    if r.status_code != 200:
        logging.log(msg = f'main() func - status: {r.status_code}', level = 50)
        return r.json() #Here should be backup or database.


def get_api_key():
    try:
        with open(API_KEY_FILE_PATH, 'r') as file:
            api_key = file.read().strip()
            return api_key
    except FileNotFoundError:
        print(f"Error: apikey file path not found.")
        return None





# function get out user puuid, after we have imidiatly call this func to store puuid in variable
def puuid_get():
    # r = requests.get('https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/121512511/EUNE?api_key=RGAPI-4a07bcfa-a6ee-46ad-b676-ab0efd1c710a')
    r = standard_get(path=f'/riot/account/v1/accounts/by-riot-id/{name}/{tag_line}')
    try:
        return r['puuid']
    except Exception as e:
        logging.log(msg=f'puuid_get() func - response: {r}', level = 40)
        logging.log(msg={e}, level = 50)
        return None


def lol_history():
    try:
        r = standard_get(path =f'/lol/match/v5/matches/by-puuid/{puuid}/ids')
        return r
    except Exception as e:
        logging.log(msg=f'error {e} ocurre', level=50)


def match_details(match_id):
    try:
        idx = match_history[match_id]['metadata']['participants'].index(puuid)
        kills = match_history[match_id]['info']['participants'][idx]['kills']
        deaths = match_history[match_id]['info']['participants'][idx]['deaths']
        assists = match_history[match_id]['info']['participants'][idx]['assists']
        # game_end_timestamp = datetime.fromtimestamp((match_history[match_id]['info']['gameEndTimestamp'])/1000)
        # champion_name = match_history[match_id]['info']['participants'][idx]['championName']
        # champion_ID = match_history[match_id]['info']['participants'][idx]['championId']

        if match_history[match_id]['info']['participants'][idx]['win']:
            temp_str = 'Win'
        else:
            temp_str = 'Lose'

        if deaths == 0:
            return_str = f'{kills}/{deaths}/{assists} KDA: PERFECT \t{temp_str}'
        else:
            return_str = f'{kills}/{deaths}/{assists} KDA: {round(kills + assists / deaths, 2)} \t{temp_str}'
            # f'{champion_name}: {champion_ID} \t{game_end_timestamp}'
        return print(return_str)
    except Exception as e:
        logging.log(msg=f'error in match_details() func - {e}', level=50)


if __name__ == "__main__":
    api_key = get_api_key()
    puuid = puuid_get()
    match_history = {} #to powinna byc baza danych


# Store all detail information about our games in 'mat ch_history' variable
    for i in lol_history():
        r = standard_get(path=f'/lol/match/v5/matches/{i}')
        match_history.update({i: r})

    for i in match_history:
        match_details(i)

