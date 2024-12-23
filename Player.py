# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 13:59:50 2024

@author: amude
"""

from Deck import Deck
from random import randint as rng


class Player:
    
    def __init__(self):
        
        #initialize player
        self.name = 'Player'
        self.image  = 'images\\player.jpg'
        
        self.deck = Deck(['Strike']*3 + ['Block']*5 + ['Heal']*2 + ['Bite']*2) #always default to 5 strikes & 5 blocks
        self.deck.Shuffle()
        self.hand = []
        self.drawCount = 5
        self.savingRoll = 6 #25% chance for burn or poison to apply additional effects
        
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
        self.anointed = 0
        
        self.weak = 0
        self.frail = 0
        self.vulnerable = 0
        self.bleed = 0
        
        self.attrList = ['strength', 'steel', 'anointed', 'weak', 'frail', 
                         'vulnerable', 'bleed']
                
    def D20(self):
        
        roll = rng(1, 20)
        
        return roll >= self.savingRoll
    
    
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
        
        #need to worry about over-healing
        self.health = min(self.health, self.fullHealth)
        #might as well do this too
        self.health = max(self.health, 0)
            
    def PlayCard(self, hand_ix):
        
        card = self.hand.pop(hand_ix)
        self.mana -= card.mana
        
        return card
    
    
    def EndTurn(self):
        
        #first apply anointed, poison, & burn effects
        self.health += self.anointed
        self.health = min(self.health, self.fullHealth)
        self.health -= self.bleed
        self.health = max(self.health, 0)
        
        #then decrement all the necessary attributes
        if self.anointed:
            self.anointed -= 1
        
        if self.weak > 0:
            self.weak -= 1
            
        if self.frail > 0:
            self.frail -= 1
            
        if self.vulnerable:
            self.vulnerable -= 1
        
        if self.bleed > 0:
            self.bleed -= 1
        
        #lastly, need to discard anything remaining in your hand
        for ix in range(len(self.hand)-1, -1, -1):
            card = self.hand.pop(ix)
            self.deck.Discard(card)
    
            
    def NewTurn(self):
        
        self.mana = 3
        
        self.armor = 0
                
        #now draw our hand
        for ix in range(self.drawCount):
            drawnCard = self.deck.TopDeck()
            self.hand.append(drawnCard)
        
        
    def CheckPulse(self):
        if self.health <= 0:
            self.dead = True
            
        