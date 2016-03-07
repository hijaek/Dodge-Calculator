from riotwatcher import RiotWatcher
key = '6d5b2d52-bbb2-4540-aab8-cdf82e1e2c13'
w = RiotWatcher(key)


import pandas as pd
from pandas import *


#summoner_name = 'mufasakim'
##print(w.can_make_request())
#me = w.get_summoner(name='mufasakim')
##my_ranked_stats = w.get_ranked_stats(me['id'])


##### que types: 'RANKED_SOLO_5x5'
##### NORTH_AMERICA = 'na'


def extract_matchid(summoner_name):
    sumid = w.get_summoner(name=summoner_name)['id']
    matchlist = []
    for key in w.get_match_list(sumid, season='SEASON2015', ranked_queues='RANKED_SOLO_5x5', begin_time=1421896854200, end_time=1442171857013)['matches']:
        matchlist.append(key['matchId'])
    return matchlist

matchlist_mufasa = extract_matchid('mufasakim')

def extract_participant(matchid):
    part_id = []
    idinfo = {}
    y=w.get_match(matchid)
    for x in range(0,10):
#        print x
        summonerid=y['participantIdentities'][x]['player']['summonerId']
        champid= y['participants'][x]['championId']
        idinfo = {
            "matchid": matchid,
            "partcipantid": y['participants'][x]['participantId'],
            "summonerid": summonerid,
            "champid":champid,
            "summonername": y['participantIdentities'][x]['player']['summonerName'],
            "lane":  y['participants'][x]["timeline"]["lane"]
        }
        part_id.append(idinfo)
    return part_id

#print extract_participant('1704783361')[0]['summonerid']

def extract_stats(summonerid, champid):
    statlist = []
    statdic  = {}
    stat=w.get_ranked_stats(summonerid, region='NA')['champions']
    for x in range(0,int(len(stat))):
#        print x
        if str(stat[x]['id'])==champid:
            game=stat[x]['stats']['totalSessionsPlayed']
            statdic = {
                "summonerid": summonerid,
                "champid":champid,
                "dmg":stat[x]['stats']['totalPhysicalDamageDealt']/game,
                "game_played":game,
                "death":stat[x]['stats']['totalDeathsPerSession']/game,
                "kill":stat[x]['stats']['totalChampionKills']/game,
                "assist":stat[x]['stats']['totalAssists']/game,
                "winrate":stat[x]['stats']['totalSessionsWon']/game,
                "gold":stat[x]['stats']['totalGoldEarned']/game,
                "turrentkill":stat[x]['stats']['totalTurretsKilled']/game,
                "totalMinionKills":stat[x]['stats']['totalMinionKills']/game
            }
            print statdic
            statlist.append(statdic)
            break
    return statlist

def join_part_stat(matchid):
    partlist = extract_participant('1704783361')
    for x in range(0, len(extract_participant(matchid))):
        extract_stats partlist[x]['summonerid']
        


#join_part_stat('1704783361')
#print extract_participant('1704783361')

def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z



def innerjoin(d1,d2,k):
    return { k : d1[k] + d2[k] for k in d1 if k in d2 }






get_summoners(



    

#for key in w.get_match('1704783361')['participants']:
#    print key['participantId']

     #for key in w.get_match('1704783361')['participants']:
#    print key['championId']

