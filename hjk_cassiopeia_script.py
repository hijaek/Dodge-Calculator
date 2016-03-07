import random

from cassiopeia import riotapi
from cassiopeia.core import *
from cassiopeia.dto import *
from cassiopeia.type import *
from cassiopeia.type.core.common import *

import cassiopeia.riotapi
import cassiopeia.dto.statsapi
import cassiopeia.core.requests
import cassiopeia.type.core.common
import cassiopeia.type.core.stats
import time




key="6d5b2d52-bbb2-4540-aab8-cdf82e1e2c13"
riotapi.set_region("NA")
riotapi.set_api_key(key)

##
##def extract_participant(matchid):
##    return riotapi.get_matches(matchid)

start_time= time.time()

def extract_participant(sum_name):  #games):  ##extracts match list and the list of participant objects
    summoner = riotapi.get_summoner_by_name(sum_name)  ##extracts a summoner object
    mylist=riotapi.get_match_list(summoner, num_matches=2, ranked_queues=Queue.ranked_solo, seasons=Season.season_5) #extracts my matchlist
    
    matchlist_id=[]

    for i in range(0, len(mylist)): #extracting the matchlist_id of of sum_name
        matchlist_id.append(mylist[i].id) #returns [match_id1, match_id2]
 
    participant_list=[]
    
    for i in range(0, len(matchlist_id)):   
        participant_list.append(riotapi.get_matches(matchlist_id)[i].participants) #appending each participant
    return participant_list ##[[part1, part2 ... part10], []...]







first_time = time.time() ##시간잰다
print("first time=", first_time - start_time)

hijaename=extract_participant('mufasakim')[0][3].summoner_name

hijae = extract_participant('mufasakim')[0][3].champion  ### [game#][participant#]
#https://github.com/robrua/cassiopeia/blob/27448aea42cbd5a751a87ce3bcfa8583bf15191c/cassiopeia/type/core/match.py
#여기 138줄에 보면 클라스 다나옴

hijae_stat = extract_participant('mufasakim')[0][3].summoner.ranked_stats(season=Season.season_5)[hijae]

#hijae_stat has <class 'cassiopeia.type.core.stats.AggregatedStats'>
#자세히 알려면 아래로 가세요
#http://cassiopeia.readthedocs.org/en/latest/cassiopeia.type.core.html?highlight=aggregatedstats#cassiopeia.type.core.stats.AggregatedStats

#print(hijae)
#print(hijae_stat)
#print(type(hijae_stat))
name=   hijaename
kda=    hijae_stat.kda
kill=   hijae_stat.kills
death=  hijae_stat.deaths
dmg=    hijae_stat.damage_dealt
dmg_tkn=hijae_stat.damage_taken
gm_amt= hijae_stat.games_played


yolo=[hijaename,kda,kill,death,dmg,dmg_tkn,gm_amt]

print(yolo)


first=time.time()##시간잰다
print("first participant took ",first - first_time) ##시간잰다




exit()




##def extract_participant_stat(participant_list):
##    participant_stat=[]
##    for match in range(0, len(participant_list)):  ##
##        for participant in range(0, 10):
##            summoner_stat=riotapi.get_ranked_stats(summoner=participant_list[match][participant], season=Season.season_5)
##            participant_stat.append(summoner_stat)
##    return participant_stat


##
##
##                       
##match in zip(participant_listrange(0, len(participant_list))
##        riotapi.get_summoner_by_id(participant_list[match][participant])
##
##
##    for match, i in zip(participant_list, range(0, len(participant_list))):
##        dictionary = {
##            i: match
##        }
    

print(extract_games("mufasakim"))
            


    

        

#extract_games("mufasakim")


def extract_participant(matchid):
    return riotapi.get_matches(matchid)

#print (extract_participant([2005044165, 2005044165, 2005044165])[1].participants)
    



stats=cassiopeia.dto.statsapi.get_ranked_stats(28396810, season='SEASON2015') #내가 2015년에 해왔던 챔프들(오브젝트)
stat=stats.champions[0]
print(stat.id) #111


hijae = riotapi.get_summoner_by_name("mufasakim")
hjstat=riotapi.get_ranked_stats(summoner=hijae, season=Season.season_5)

print(hjstat[riotapi.get_champion_by_id(36)].kda)




##print('[]:', cassiopeia.riotapi.get_champions_by_id([36]))#[<cassiopeia.type.core.staticdata.Champion object at 0x048F7E70>]
##print('[][0]:', cassiopeia.riotapi.get_champions_by_id([36])[0]) #dr mundo
##print("['36']", cassiopeia.riotapi.get_champions_by_id(['36']))
##print('():', cassiopeia.riotapi.get_champions_by_id(36)) #dr mundo



#print(riotapi.get_champion_by_id)





#stats=cassiopeia.dto.statsapi.get_ranked_stats(28396810)
######stat=stats.champions[0] #stats.champions는 리스트임
########print(stat.id) #prints 111(integer) first item of my champ list
######champion=list(stats.champion_ids) #list of champions i played
#print(cassiopeia.riotapi.get_champions_by_id(list(stats.champion_ids))) #<-요건 list of objects(챔프오브젝트).
######champions = {champion.id: champion for champion in cassiopeia.riotapi.get_champions_by_id(list(stats.champion_ids))}
######champion은 각챔프의 오브젝트. 즉, "champions"라는 딕셔너리는 {챔프id(int): 챔프오브젝트}를 매핑함. 
########print(champions[111])

#def extract_participant(matchid):


##    
##    
##print(hjstat[champions[111]].kda)
##print(hjstat[champions[111]].assists,
##      hjstat[champions[111]].kills,
##      hjstat[champions[111]].deaths,
##      hjstat[champions[111]].gold_earned)
      
#print(champions)
#champions = {#champions는 딕셔너리



##[ChampionStats(
##    {'stats':
##     aggregatedStats(
##        {'avg blahblahblah: 0,
##         'avg blahblah: 0
##         }
##        )
##     }),
##    'id': 111
## ]
##
##[오브젝트( 



##{ "id": 33,
##  "stats": {avg:0, avgkills:0...}
##}

#print(cassiopeia.dto.statsapi.get_ranked_stats(28396810).[36][33])






##num_matches = 5
###print(enumerate(mylist[0:num_matches]))
##for i, match_reference in enumerate(mylist[0:num_matches]):
##    print("i:", i)
##    print("match", match_reference)
##    match = riotapi.get_match(match_reference)
##    for participant in match.participants:
##        print(match.participants.




#champions = riotapi.get_champions()
#random_champion = random.choice(champions)
#print(random_champion)
#print("He enjoys playing LoL on all different champions, like {name}.".format(name=random_champion.name))
