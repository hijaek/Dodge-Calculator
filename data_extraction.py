#### I need to write a function to extract and gather data from API
####
#### Steps of the function
####  1) Extract list of objects of games I've played
####  2) Loop to partition list of games, to prevent data loss due to random api errors 
####  3) creating a list of stats of each participant(i)
####  4) writing csv files of 15 games of 150 participants for how many ever loops


from cassiopeia import riotapi
from cassiopeia.core import *
from cassiopeia.dto import *
from cassiopeia.type.core.common import *
from cassiopeia.type.api.exception import APIError
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

####setting parameters
riotapi.set_load_policy(LoadPolicy.eager)
riotapi.set_load_policy(LoadPolicy.lazy)
key="1306e669-7f7a-4122-8938-7c60cf7d656f"
riotapi.set_region("NA")
riotapi.set_api_key(key)
riotapi.set_rate_limits((9, 10), (499, 600))



def extract_participant(sum_name, gamecount):
    ##parameters
    quetype=Queue.ranked_solo
    myseason=Season.season_5
    summoner = riotapi.get_summoner_by_name(sum_name)
    #################################### 1 #################################
    #extracting list of objects games
    mygamelist=riotapi.get_match_list(summoner, num_matches=gamecount, ranked_queues=quetype, seasons=myseason)
    #################################### 2 #################################
    #need to partition list of games, to prevent data loss due to random api errors 
    for file in range(0, gamecount, 15):
        yolo_two=[]
        print("i'm starting...", file)
        a=1
        for game in mygamelist[file:file+15]:
            print("for game", a)
            a=a+1
            for i in range(0,10):
                participant=game.match().participants[i] ## +1 api call
                print("1 loop: ",i, "-", cassiopeia.riotapi.get_requests_count())
                #### Random API errors often occur for champstat
                #### This is an algo to re-request to API after an error instead of killing the entire job
                try:
                    champstat = participant.summoner.ranked_stats(season=myseason)[participant.champion] ##+2 api call
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
                ############################  3 #############################
                #creating a list of stats of each participant(i)
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
                yolo_two.append(participant_list)
                print("3 loop: ",i, "-", cassiopeia.riotapi.get_requests_count())
                #time.sleep(2)
                print("next up is participant:", i+1)
            if i < 15:
                print("waiting 5 sec for the next game")
                time.sleep(5)
        ########################## 4 ################################
        ##writing csv files of 15 games of 150 participants
        with open(str(file)+'testyolo.csv', 'w', encoding='UTF-8', newline='') as testfile:
            a = csv.writer(testfile, delimiter=',')
            a.writerows(yolo_two)
            print("i just did ",file)
            print("Here comes next round of csvfile")
        ## pause for api call limit
        print("waiting 10sec...")
        time.sleep(10)


#extract_participant('mufasakim', 400)
#takes about 40min for 400 games. 
#print(cassiopeia.riotapi.get_requests_count())



############################## don't mind. test ####################################
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
