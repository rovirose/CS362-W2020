# -*- coding: utf-8 -*-
"""
Created on Jan 18 2020

@author: Emmanuel Rovirosa
"""

import Dominion
import random
import testUtility
from collections import defaultdict

#Get player names
player_names = ["Annie","*Ben","*Carla"]

#number of victory cards, player and curses
nP = len(player_names)
if nP > 2:
    nV = 12
else:
    nV = 8
nC = -10 + 10 * nP

#define box
box = testUtility.getBoxes(nV)

#The supply always has these cards
supply_order = testUtility.getSupplyOrder()

#Pick 10 cards from box to be in the supply.
boxlist = [k for k in box]
random.shuffle(boxlist)
random10 = boxlist[:10]
supply = defaultdict(list,[(k,box[k]) for k in random10])

testUtility.setupSupply(nV, nC, nP, supply)
supply["Gold"]=[Dominion.Gold()]*3

#initialize the trash
trash = []

#Costruct the Player objects
players = []
for name in player_names:
    if name[0]=="*":
        players.append(Dominion.ComputerPlayer(name[1:]))
    elif name[0]=="^":
        players.append(Dominion.TablePlayer(name[1:]))
    else:
        players.append(Dominion.Player(name))

#Play the game
turn  = 0
while not Dominion.gameover(supply):
    turn += 1    
    print("\r")    
    for value in supply_order:
        print (value)
        for stack in supply_order[value]:
            if stack in supply:
                print (stack, len(supply[stack]))
    print("\r")
    for player in players:
        print (player.name,player.calcpoints())
    print ("\rStart of turn " + str(turn))    
    for player in players:
        if not Dominion.gameover(supply):
            print("\r")
            player.turn(players,supply,trash)
            

#Final score
dcs=Dominion.cardsummaries(players)
vp=dcs.loc['VICTORY POINTS']
vpmax=vp.max()
winners=[]
for i in vp.index:
    if vp.loc[i]==vpmax:
        winners.append(i)
if len(winners)>1:
    winstring= ' and '.join(winners) + ' win!'
else:
    winstring = ' '.join([winners[0],'wins!'])

print("\nGAME OVER!!!\n"+winstring+"\n")
print(dcs)
