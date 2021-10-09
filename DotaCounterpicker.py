# this code works as of 9/28
import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd
from IPython.display import display
headers = {'User-Agent': 'Mozilla/5.0'}

def main():
    enemyComp = userInput()
    counterpicks = team_matchup(enemyComp)
    counterpicks = team_matchup_percentage(counterpicks)
    display(counterpicks)

def hero_matchup(hero):
    hero = hero.lower()
    heroHyphen = hero.replace(' ','-')
    url = "https://www.dotabuff.com/heroes/" + heroHyphen + "/counters"
    response = rq.get(url, headers=headers)
    if response.status_code != 200:
        print("Request unsuccessful: " + str(response.status_code))
        return []
    page = bs(response.content, 'lxml')
    table = page.find('table', class_='sortable').find('tbody').findAll('tr')
    counters = []
    for i in table:
        counter = i.find('a', class_='link-type-hero').get_text()
        advantage = float(i.findNext('td').findNext('td').findNext('td').get('data-value')) / 100
        winrate = float(i.findNext('td').findNext('td').findNext('td').findNext('td').get('data-value')) / 100
        counters.append([counter, advantage])
    countersDataFrame = pd.DataFrame(counters, columns=["Counter", hero.title()]).sort_values('Counter')
    return countersDataFrame

def team_matchup(enemyComp):
    matchupData = hero_matchup(enemyComp[0])
    for pick in enemyComp[1:]:
        newData = hero_matchup(pick)
        matchupData = pd.merge(matchupData, newData, on='Counter', how='inner')
    matchupData['Average'] = matchupData.mean(axis=1)
    matchupData = matchupData.sort_values('Average', ascending=0)
    return matchupData

def team_matchup_percentage(counterpicks):
    for pick in counterpicks.columns[1:]:
        counterpicks[pick] = counterpicks[pick].map("{:.2%}".format)
    return counterpicks

def userInput():
    enemyTeam = []
    while (len(enemyTeam)<5):
        if(not enemyTeam):
            print('Enter in enemy heroes:')
            hero=input()
            hero=checkName(hero)
            if(hero!='none'):
                enemyTeam.append(hero)
        else:
            print('Current enemy team: '+', '.join(enemyTeam).title())
            print('Enter in enemy heroes. Enter blank if finished.')
            hero=input()
            if(hero==''):
                break;
            hero=checkName(hero)
            if(hero!='none'):
                enemyTeam.append(hero)
    return enemyTeam

def checkName(hero):
    hero=hero.lower()
    if(hero in allHeroes.keys()):
        return hero
    else:
        for name in allHeroes:
            if hero in allHeroes[name]:
                return name
    print('Not recognized as a hero, try again')
    return"none"

allHeroes={
    "abaddon": ["avernus"],
    "alchemist": ["razzil"],
    "ancient apparition": ["kaldr", "aa",'ancient'],
    "anti-mage": ["am",'anti mage','antimage'],
    "arc warden": {"aw",'zet','arc'},
    "axe": [],
    "bane": ["atropos"],
    "batrider": [],
    "beastmaster": ["karroch", "rexxar", "bm"],
    "bloodseeker": ["strygwyr", "bs"],
    "bounty hunter": ["gondar", "bh"],
    "brewmaster": ["mangix", "bm"],
    "bristleback": ["rigwarl", "bb"],
    "broodmother": ["bm"],
    "centaur warrunner": ["bradwarden", "cw"],
    "chaos knight": ["ck"],
    "chen": [],
    "clinkz": ["bone"],
    "clockwerk": ["rattletrap", "cw"],
    "crystal maiden": ["rylai", "cm"],
    "dark seer": ["ish", "ds"],
    "dark willow": ['dw','mireska'],
    'dawnbreaker':[],
    "dazzle": [],
    "death prophet": ["krobelus", "grobulus", "dp"],
    "disruptor": [],
    "doom": [],
    "dragon knight": ["davion", "dk"],
    "drow ranger": ["traxex", "dr"],
    "earthshaker": ["raigor", "es"],
    "earth spirit": ["kaolin"],
    "elder titan": ["et"],
    "ember spirit": ["xin", "es"],
    "enchantress": ["aiushtha"],
    "enigma": [],
    "faceless void": ["darkterror"],
    "grimstroke": ['gs'],
    "gyrocopter": ["aurel"],
    'hoodwink': ['hw'],
    "huskar": [],
    "invoker": ["kael", "karl", "carl"],
    "io": ["wisp"],
    "jakiro": ["thd",'jak'],
    "juggernaut": ["yurnero"],
    "keeper of the light": ["ezalor", "kotl"],
    "kunkka": [],
    "legion commander": ["tresdin", "lc"],
    "leshrac": ['lesh'],
    "lich": ["ethreain"],
    "lifestealer": ["naix"],
    "lina": [],
    "lion": [],
    "lone druid": ["sylla", "ld"],
    "luna": [],
    "lycan": ["banehallow"],
    "magnus": [],
    'mars':['ares'],
    "medusa": ["gorgon"],
    "meepo": ["geomancer"],
    "mirana": ["potm"],
    'monkey king':['mk','wukong','sun wukong'],
    "morphling": [],
    "naga siren": ["slithice", "ns",'naga'],
    "natures prophet": ["furion", "np"],
    "necrophos": ['necro'],
    "night stalker": ["ns", "balanar"],
    "nyx assassin": ["na"'nyx'],
    "ogre magi": ["aggron", "om",'ogre'],
    "omniknight": ["ok",'omni'],
    'oracle':['nerif'],
    "outworld devourer": ["od", "harbinger",'outhouse'],
    'pangolier':['pango'],
    "phantom assassin": ["pa", "mortred"],
    "phantom lancer": ["azwraith", "pl"],
    "phoenix": [],
    "puck": [],
    "pudge": ["butcher"],
    "pugna": [],
    "queen of pain": ["akasha", "qop"],
    "razor": [],
    "riki": [],
    "rubick": [],
    "sand king": ["crixalis", "sk"],
    "shadow demon": ["sd"],
    "shadow fiend": ["nevermore", "sf"],
    "shadow shaman": ["rhasta", "ss"],
    "silencer": ["nortrom"],
    "skywrath mage": ["dragonus", "sm"],
    "slardar": [],
    'slark':[],
    'snapfire':['snap'],
    "sniper": ["kardel"],
    "spectre": ["mercurial"],
    "spirit breaker": ["barathrum", "sb"],
    "storm spirit": ["raijin", "storm"],
    "sven": [],
    "techies": ["goblin", "gt", "sqee", "spleen", "spoon"],
    "templar assassin": ["lanaya", "ta"],
    "terrorblade": ["tb"],
    "tidehunter": ["leviathan",'tide'],
    "timbersaw": ["rizzrack"],
    "tinker": ["boush"],
    "tiny": [],
    "treant protector": ["rooftrellen",'treant','tp'],
    "troll warlord": ["tw",'troll'],
    "tusk": ["ymir"],
    'underlord':[],
    "undying": ["dirge"],
    'ursa':[],
    "vengeful spirit": ["shendelzare", "vs"],
    "venomancer": ["lesale"],
    'viper':[],
    "visage": [],
    "void spirit":['void'],
    "warlock": ["demnok", "wl"],
    "weaver": ["skitskurr"],
    "windranger": ["lyralei", "wr"],
    'winter wyvern':['winter','ww'],
    "witch doctor": ["zharvakko", "wd"],
    "wraith king": ["ostarion", "skeleton king", "wk", "sk"],
    "zeus": []
}

if __name__ == "__main__":
    main()
