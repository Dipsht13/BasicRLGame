# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 13:59:50 2024

@author: amude
"""

from Deck import Deck


class Player:
    
    def __init__(self):
        
        #initialize player
        self.name = 'Player'
        self.image  = 'images\\player.jpg'
        
        self.deck = Deck(['Strike']*5 + ['Block']*5) #always default to 5 strikes & 5 blocks
        self.deck.Shuffle()
        self.hand = []
        self.drawCount = 5
        
        self.path = None
        self.subpath = None
        
        self.relics = []
        
        self.mana = 0
        
        self.health = 50
        self.fullHealth = 50
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
                
    
    def Block(self, block):
        if self.frail:
            block = round(0.75*block)
            
        self.armor += block
        
    
    def TakeDamage(self, dmg):
        
        if self.vulnerable:
            dmg = round(1.25*dmg)
        
        if self.armor > dmg:
            self.armor -= dmg
        
        else:
            dmg -= self.armor
            self.armor = 0
            self.health = max(self.health - dmg, 0)
            
            
    def ProcessBuffDebuff(self, listTuple):
        
        attr = listTuple[0].lower(); val = listTuple[1]
        
        setattr(self, attr, getattr(self, attr) + val)
            
        
    def CanPlay(self, hand_ix):
        
        if hand_ix == -1:
            return True
        
        else:
            return self.hand[hand_ix].mana <= self.mana
        
            
    def PlayCard(self, hand_ix):
        
        card = self.hand.pop(hand_ix)
        self.mana -= card.mana
        
        return card
            
            
    def TurnEnd(self):
        
        self.mana = 3
        
        self.armor = 0
        
        self.health -= self.poison
        self.poison -= 1
        
        self.health -= self.burn
        self.burn -= 1