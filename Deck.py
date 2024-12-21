# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 12:41:06 2024

@author: amude
"""

from Card import Card
import random


class Deck:
    
    def __init__(self, deckList):
        
        self.deckList = deckList
        
        self.drawPile = []
        self.discardPile = []
        
        self.deck = []
        
        for cardName in deckList:
            self.deck.append(Card(cardName))
            
        self.drawPile = self.deck
        
            
    def Shuffle(self):
        random.shuffle(self.deck)
        
    
    def TopDeck(self):
        
        if len(self.drawPile) == 0:
            self.drawPile = self.discardPile
            self.Shuffle()
        
        topCard = self.drawPile.pop(0)
        
        return topCard
    
    
    def Discard(self, card):
        
        self.discardPile.append(card)
    
            