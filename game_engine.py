# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 10:52:52 2024

@author: amude
"""

import json
from random import randint as rng
from Enemy import Enemy
from Player import Player


def D20(mustRoll = 11):
    
    roll = rng(1, 20)
    
    return roll >= mustRoll
    

def RNGesus(aList):
    
    randix = rng(0, len(aList)-1)    
    
    return aList[randix]


def Initialize():
    #start game
    #initialize player
    player = Player()
    
    #pick a random enemy
    enemy = Enemy('rando')
    
    return player, enemy

   
def PlayCard(player, enemy, cardix):
    # returns isPlayable boolean, errorMsg string
    
    #first check the mana cost
    if player.hand[cardix].mana > player.mana:
        return False, "Not enough mana."
    
    #if we have the mana, play it
    card = player.hand.pop(cardix)
    player.mana -= card.mana
    
    #and do all the other game state updates
    dmg, block, buffs, debuffs = card.PlayState()
    
    #first apply any damage the card may have
    if dmg > 0:
        enemy.TakeDamage(dmg + player.strength)
    
    #then apply any block the card may have
    if block > 0:
        player.Block(block + player.steel)
        
    #next apply any buffs to the player
    for buff in buffs:
        player.ProcessBuffDebuff(buff)
        
    #finally apply debuffs to the enemy
    for debuff in debuffs:
        enemy.ProcessBuffDebuff(debuff)
        
    player.deck.Discard(card)
    
    return True, ""
        

def StatusReport(person):
    
    status_str = person.name + ' Health: ' + str(person.health) + '/' + str(person.fullHealth) + '\n'
    status_str += person.name + ' Armor: ' + str(person.armor) + '\n'
    
    for attr in person.attrList:
        if getattr(person, attr) > 0:
            proper_name = attr[0].upper() + attr[1:]
            status_str += person.name + ' ' + proper_name + ': ' + str(getattr(person, attr)) + '\n'
    
    return status_str


def UpdateGameState(player, enemy):
    
    if player.dead and enemy.dead:
        return "Not sure I'd count death as a win but you do you I guess."
    
    elif player.dead:
        return "You are dead."
    
    elif enemy.dead:
        return "Oh my god, you killed " + enemy.name + "!\n You Bastard!"
    
    #first update card text if needed
    for card in player.hand:
        card.UpdateText(playerStrength= player.strength, playerSteel= player.steel, 
                       playerWeak= player.weak, playerFrail= player.frail, 
                       enemyVulnerable= enemy.vulnerable)
    
    dmg, _, buffs, debuffs = enemy.currentTurn

    game_str = ''
    if dmg == 0 and len(buffs) == 0 and len(debuffs) == 0:
        game_str += 'The enemy is blocking this turn.\n'
    
    else:
        dmgMultiplier = 1
        if enemy.weak:
            dmgMultiplier = dmgMultiplier * .75
        if player.vulnerable:
            dmgMultiplier = dmgMultiplier * 1.5
            
        game_str += 'You are facing ' + str(round(dmg*dmgMultiplier)) + ' damage.\n'
        if len(buffs) > 0:
            for buff in buffs:
                game_str += 'The enemy is buffing their ' + buff[0] + ' by ' + str(buff[1]) + '.\n'
        if len(debuffs) > 0:
            for debuff in debuffs:
                game_str += 'The enemy is applying ' + str(debuff[1]) + ' ' + debuff[0] + ' to you.\n'
    game_str += '\n'
    game_str += '\n'
    game_str += 'You have ' + str(player.mana) + ' mana.\n'
    
    return game_str


def EndTurnDecrements(person):
    
    if person.weak > 0:
        person.weak -= 1
        
    if person.frail > 0:
        person.frail -= 1
        
    if person.vulnerable:
        person.vulnerable -= 1
    
    if person.poison > 0:
        person.poison -= 1
    
    if person.burn > 0:
        person.burn -= 1
            
    if person.poison > 0:
        if not D20(mustRoll=6):
            person.weak += 1
    
    if person.burn > 0:
        if not D20(mustRoll=6):
            person.frail += 1


def NewTurn(player, enemy):
        
    #first reset mana
    player.mana = 3
    
    #now decide what the enemy is doing
    action1 = RNGesus(enemy.possibleActions)
    action2 = RNGesus(enemy.possibleActions)
    enemy.UpdateCurrentTurn(action1)
    enemy.UpdateCurrentTurn(action2)
    
    #most of what the enemy is doing is applied after the player's turn but
    # if the enemy is blocking that applies prior to the player's attacks
    if enemy.currentTurn[1] > 0:
        enemy.Block(enemy.currentTurn[1])
        
    #now draw our hand
    for ix in range(player.drawCount):
        drawnCard = player.deck.TopDeck()
        player.hand.append(drawnCard)
        
        
def EndTurn(player, enemy):
    
    #finish the enemy's turn
    dmg, block, buffs, debuffs = enemy.currentTurn
    
    if dmg > 0:
        player.TakeDamage(dmg)
        
    #block's already been handled
    
    if len(buffs) > 0:
        for buff in buffs:
            enemy.ProcessBuffDebuff(buff)
    
    if len(debuffs) > 0:
        for debuff in debuffs:
            player.ProcessBuffDebuff(debuff)
            
    #now take damage from poison & burn if appropriate
    if player.poison:
        player.health = max(player.health - player.poison, 0)
        
    if player.burn:
        player.health = max(player.health - player.burn, 0)
        
    if enemy.poison:
        enemy.health = max(enemy.health - enemy.poison, 0)
        
    if enemy.burn:
        enemy.health = max(enemy.health - enemy.burn, 0)
        
    #and decrement all the status effects that need it
    EndTurnDecrements(player)
    EndTurnDecrements(enemy)
    
    #armor needs to be reset
    player.armor = 0
    enemy.armor = 0
    
    #enemy currentTurn needs to be reset
    enemy.currentTurn = [0, 0, [], []]
    
    #and any cards remaining in your hand must be discarded
    for ix in range(len(player.hand)-1, -1, -1):
        card = player.hand.pop(ix)
        player.deck.Discard(card)
        
    gameOver = CheckGameOver(player, enemy)
    return gameOver
    
    
def CheckGameOver(player, enemy):
    
    if player.health <= 0:
        player.dead = True
        
    if enemy.health <= 0:
        enemy.dead = True
        
    return (player.dead or enemy.dead)