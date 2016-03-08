from cassiopeia import riotapi
from cassiopeia.core import *
from cassiopeia.dto import *
from cassiopeia.type import *
from cassiopeia.type.core.common import *
from cassiopeia.type.core.common import LoadPolicy
from cassiopeia.type.api.exception import APIError
from cassiopeia.type.core.common import LoadPolicy
from cassiopeia.type.api.store import SQLAlchemyDB
from cassiopeia import baseriotapi

import random
import cassiopeia.riotapi
import cassiopeia.dto.statsapi
import cassiopeia.core.requests
import cassiopeia.type.core.common
import cassiopeia.type.core.stats
import time


import numpy as np
import pandas as pd
import csv

d=[['Misleading', 42, 3.8461538461538463, 0.75, 26, 13, 24, 'Side.blue'], ['Alfíe', 53, 4.271186440677966, 0.5714285714285714, 58, 59, 194, 'Side.blue']]

print('Side.blue'[5:])
length = len(d[0])


riotapi.set_load_policy(LoadPolicy.eager)
riotapi.set_load_policy(LoadPolicy.lazy)
key="1306e669-7f7a-4122-8938-7c60cf7d656f"
riotapi.set_region("NA")
riotapi.set_api_key(key)
riotapi.set_rate_limits((9, 10), (450, 600))

# i=0
# quetype=Queue.ranked_solo
# myseason=Season.season_5
# me=riotapi.get_summoner_by_name('mufasakim')
# print("1 loop: ",i, "-", cassiopeia.riotapi.get_requests_count())
# mygamelist=riotapi.get_match_list(me, num_matches=1, ranked_queues=quetype, seasons=myseason)
# game=mygamelist[0]
# print("2 loop: ",i, "-", cassiopeia.riotapi.get_requests_count())
# participant=game.match().participants[i]
# hm=participant.summoner.id
# champ=participant.champion.id
# print("3 loop: ",i, "-", cassiopeia.riotapi.get_requests_count())
# sumstat=baseriotapi.get_ranked_stats(hm, season='SEASON2015')
# print("4 loop: ",i, "-", cassiopeia.riotapi.get_requests_count())




riotapi.set_load_policy(LoadPolicy.eager)
riotapi.set_load_policy(LoadPolicy.lazy)
key="1306e669-7f7a-4122-8938-7c60cf7d656f"
riotapi.set_region("NA")
riotapi.set_api_key(key)
#riotapi.set_rate_limits((10, 10), (500, 600))

def extract_participant(sum_name):
    quetype=Queue.ranked_solo
    myseason=Season.season_5
    summoner = riotapi.get_summoner_by_name(sum_name)
    mygamelist=riotapi.get_match_list(summoner, num_matches=2, ranked_queues=quetype, seasons=myseason) #matchlist objects
    mydict= dict()
    yolo=[]
#    for i in range(0, 500, 50):
    for game in mygamelist:
        #mydict[game.id]=[]
        for i in range(0,10):
            participant=game.match().participants[i]
            champstat=participant.summoner.ranked_stats(season=myseason)[participant.champion]
            participant_list=[]
            #participant_list.append(game.id)
            participant_list.append(participant.summoner_name)
            participant_list.append(participant.champion.id)
            participant_list.append(champstat.kda)
            participant_list.append(champstat.wins/champstat.games_played)
            participant_list.append(champstat.kills)
            participant_list.append(champstat.deaths)
            participant_list.append(champstat.assists)
            participant_list.append(str(participant.side)[5:])
            yolo.append(participant_list)
            #mydict[game.id]=participant_list
    return yolo

riotapi.set_rate_limits((9, 10), (499, 600))


def extract_participant_two(sum_name):
    quetype=Queue.ranked_solo
    myseason=Season.season_5
    summoner = riotapi.get_summoner_by_name(sum_name)
    mygamelist=riotapi.get_match_list(summoner, num_matches=400, ranked_queues=quetype, seasons=myseason) #matchlist objects
    for file in range(0, 400, 15):
        yolo_two=[]
        print("i'm starting...", file)
        a=1
        for game in mygamelist[file:file+15]:
            print("for game", a)
            a=a+1
            for i in range(0,10):
                participant=game.match().participants[i] ## +1 api call
                print("1 loop: ",i, "-", cassiopeia.riotapi.get_requests_count())
                #### champstat.tojson?
                try:
                    champstat = participant.summoner.ranked_stats(season=myseason)[participant.champion] ##+3 api call
                except APIError as error:
                    # Try Again Once
                    if error.error_code in [500]:
                        try:
                            print("Got a 500. retrying after 30sec...")
                            time.sleep(30)
                            champstat=participant.summoner.ranked_stats(season=myseason)[participant.champion] ##+3 api call
                        except APIError as another_error:
                            if another_error.error_code in [500, 400, 404]:
                                try:
                                    print ("got another 500, retrying after 60sec...")
                                    time.sleep(60)
                                    champstat=participant.summoner.ranked_stats(season=myseason)[participant.champion] ##+3 api call
                                except APIError as another_another_error:
                                    if another_error.error_code in [500, 400, 404]:
                                        print("failed on THIRD attempt. just passing")
                                        pass
                                    else:
                                        print("error man...")
                                        raise another_another_error
                            else:
                                print("error man...")
                                raise another_error
                    elif error.error_code in [400, 404]:
                        print("Got a 400 or 404")
                        pass
                    # Fatal
                    else:
                        print("some random error occured")
                        raise error

                print("2 loop: ",i, "-", cassiopeia.riotapi.get_requests_count())
                participant_list=[]
                pergame=champstat.games_played
                participant_list.append(i)
                participant_list.append(game.id)
                participant_list.append(participant.stats.win)
                participant_list.append(participant.side.name)
                participant_list.append(participant.timeline.role)
                participant_list.append(pergame)
                participant_list.append(champstat.wins)
                participant_list.append(champstat.losses)
                participant_list.append(champstat.wins/pergame)
                participant_list.append(champstat.kda)
                participant_list.append(champstat.kills/pergame)
                participant_list.append(champstat.deaths/pergame)
                participant_list.append(champstat.assists/pergame)
                participant_list.append(champstat.gold_earned/pergame)
                participant_list.append(champstat.damage_dealt/pergame)
                participant_list.append(champstat.damage_taken/pergame)
                participant_list.append(champstat.turrets_killed/pergame)
                participant_list.append(champstat.minions_killed/pergame)
                if i > 5:
                    participant_list.append("red")
                else:
                    participant_list.append("blue")
                yolo_two.append(participant_list)
                print("3 loop: ",i, "-", cassiopeia.riotapi.get_requests_count())
                #time.sleep(2)
                print("next up is participant:", i+1)
            if i < 15:
                print("waiting 5 sec for the next game")
                time.sleep(5)

        with open(str(file)+'testyolo.csv', 'w', encoding='UTF-8', newline='') as testfile:
            a = csv.writer(testfile, delimiter=',')
            a.writerows(yolo_two)
            print("i just did ",file)
        print("waiting 20sec...")
        time.sleep(20)


#print(extract_participant('mufasakim'))
extract_participant_two('mufasakim')
print(cassiopeia.riotapi.get_requests_count())
