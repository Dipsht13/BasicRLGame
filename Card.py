# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 12:44:00 2024

@author: amude
"""

import json


class Card:
    
    def __init__(self, name):
        
        self.name = name
        self.mana = 10
        self.displayStr = 'default'
        
        self.damage = 0
        self.armor = 0
        
        self.strength = 0
        self.steel = 0
        
        self.weak = 0
        self.frail = 0
        self.vulnerable = 0
        
        self.poison = 0
        self.burn = 0
                
        
        with open('cards.json', 'r') as f:
            db_entry = json.load(f)[name]
            
        self.mana = db_entry['mana']
            
        if 'damage' in db_entry:
            self.damage = db_entry['damage']
        
        if 'armor' in db_entry:
            self.armor = db_entry['armor']
            
        if 'strength' in db_entry:
            self.strength = db_entry['strength']
            
        if 'steel' in db_entry:
            self.steel = db_entry['steel']
            
        if 'weak' in db_entry:
            self.weak = db_entry['weak']
            
        if 'frail' in db_entry:
            self.frail = db_entry['frail']
            
        if 'vulnerable' in db_entry:
            self.vulnerable = db_entry['vulnerable']
            
        if 'poison' in db_entry:
            self.poison = db_entry['poison']
                        
        if 'burn' in db_entry:
            self.burn = db_entry['burn']
            
        self.UpdateText()
        
            
    def PlayState(self):
        #return [dmg, block, buffs, debuffs]
        all_buffs = [['strength', self.strength], ['steel', self.steel]]
        all_debuffs = [['weak', self.weak], ['frail', self.frail], ['vulnerable', self.vulnerable],
                       ['poison', self.poison], ['burn', self.burn]]
        
        return [self.damage, self.armor, all_buffs, all_debuffs]
    
    
    def UpdateText(self, playerStrength= 0, playerSteel= 0, 
                   playerWeak= False, playerFrail= False, enemyVulnerable= False):
        self.displayStr = self.name + ';'
        
        if self.damage > 0:
            dmgDealt = self.damage + playerStrength
            dmgMultiplier = 1
            if playerWeak:
                dmgMultiplier = dmgMultiplier * .75
            if enemyVulnerable:
                dmgMultiplier = dmgMultiplier * 1.5
            self.displayStr += ' Deal ' + str(round(dmgDealt*dmgMultiplier)) + ' dmg.'
            
        if self.armor > 0:
            armApplied = self.armor + playerSteel
            armMultiplier = 1
            if playerFrail:
                armMultiplier = armMultiplier * .75
            self.displayStr += ' Gain ' + str(round(armApplied*armMultiplier)) + ' armor.'
            
        if self.strength > 0:
            self.displayStr += ' Gain ' + str(self.strength) + ' str.'
            
        if self.steel > 0:
            self.displayStr += ' Gain ' + str(self.steel) + ' stl.'
            
        if self.weak > 0:
            self.displayStr += ' Apply ' + str(self.weak) + ' weak.'
            
        if self.frail > 0:
            self.displayStr += ' Apply ' + str(self.weak) + ' frl.'
            
        if self.vulnerable > 0:
            self.displayStr += ' Apply ' + str(self.vulnerable) + ' vuln.'
            
        if self.poison > 0:
            self.displayStr += ' Apply ' + str(self.poison) + ' psn.'
            
        if self.burn > 0:
            self.displayStr += ' Apply ' + str(self.burn) + ' brn.'
        