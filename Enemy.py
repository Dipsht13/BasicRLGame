# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 12:28:08 2024

@author: amude
"""

import json
from random import randint as rng


def RNGesus(aList):
    
    randix = rng(0, len(aList)-1)    
    
    return aList[randix]


class Enemy:
    
    def __init__(self, name):
        
        if name == 'rando':
            with open('enemies.json', 'r') as f:
                temp = json.load(f)
                enemyList = list(temp.keys())
                del temp
            self.name = RNGesus(enemyList)
        else:
            self.name = name
        
        self.image = ''
        self.currentTurn = [0, 0, [], []]
        
        self.health = 0
        self.fullHealth = 0
        self.dead = False
        self.armor = 0
        
        self.strength = 0
        self.steel = 0
                
        self.weak = 0
        self.frail = 0
        self.vulnerable = 0
        self.poison = 0
        self.burn = 0
        
        self.attrList = ['strength', 'steel', 'weak', 'frail', 'vulnerable',
                         'poison', 'burn']
        
        self.attack = []
        self.block = []
        
        self.buffs = []
        self.debuffs = []
        
        self.possibleActions = []
        
        
        with open('enemies.json', 'r') as f:
            db_entry = json.load(f)[self.name]
        
        self.image = db_entry['image']
        self.health = db_entry['health']
        self.fullHealth = db_entry['health']
        self.possibleActions = db_entry['possibleActions']
        
        if 'attack' in db_entry:
            self.attack = db_entry['attack']
            
        if 'block' in db_entry:
            self.block = db_entry['block']
            
        if 'buffs' in db_entry:
            self.buffs = db_entry['buffs']
            
        if 'debuffs' in db_entry:
            self.debuffs = db_entry['debuffs']
            
            
    def UpdateCurrentTurn(self, action):
        # returns [int attack, int block, list buff, list debuff
        
        if action == "attack":
            dmg = RNGesus(self.attack)
            dmg = dmg + self.strength
            if self.weak:
                dmg = round(dmg*.75)
    
            self.currentTurn[0] += dmg
        
        elif action == "block":
            block = RNGesus(self.block) 
            block = block + self.steel
            if self.frail:
                block = round(block * .75)
            
            self.currentTurn[1] += block
        
        elif action == "buff":
            newBuff = RNGesus(self.buffs)
            
            self.currentTurn[2].append(newBuff)
            
        elif action == "debuff":
            newDebuff = RNGesus(self.debuffs)
            
            self.currentTurn[3].append(newDebuff)
                       
        
    def ProcessBuffDebuff(self, listTuple):
        
        attr = listTuple[0].lower(); val = listTuple[1]
        
        setattr(self, attr, getattr(self, attr) + val)
        
            
    def Block(self, block):
        if self.frail:
            block = round(0.75*block)
        
        self.armor += block
        
        
    def TakeDamage(self, dmg):
        
        if self.vulnerable:
            dmg = round(dmg*1.25)
        
        if self.armor > dmg:
            self.armor -= dmg
        
        else:
            dmg -= self.armor
            self.armor = 0
            self.health = max(self.health - dmg, 0)  
            
            
    def TurnEnd(self):
        
        self.armor = 0
        
        self.health -= self.poison
        self.poison -= 1
        
        self.health -= self.burn
        self.burn -= 1
        