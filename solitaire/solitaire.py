from typing import Any
import numpy as np
from termcolor import colored
from time import sleep
import sys

class Card:
    seed = ''
    value = 0
    status = ''

    def __init__(self, s, n):
        self.seed = s
        self.value = n

    def __eq__(self, other):
        return (self.seed == other.seed and self.value == other.value)
    
    def GetColumn(self):
        return self.value - 1
    
    def GetRow(self):
        seeds = ['C', 'Q', 'P', 'F']
        index = seeds.index(self.seed)
        return index
    
    def GetPosition(self):
        row = self.GetRow()
        column = self.GetColumn()
        return row, column
    
    def SetStatus(self, string):
        self.status = string

    def PrintCard(self, color = None):
        stat = self.status
        val = self.value
        if val == 10:
            val = 'K'
        if stat == 'correct':
            print(colored(self.seed + str(val), 'blue'), end = ' ')
        elif color:
            print(colored(self.seed + str(val), color), end = ' ')
        else:
            print(self.seed + str(val), end = ' ')

    


def Sequence2Deck(array):
    '''Convert a number sequence in gaming cards'''
    deck = []
    for ii in range(len(array)):
        if 1 <= array[ii] <= 10:
            card = Card('C', array[ii])
        elif 11 <= array[ii] <= 20:
            card = Card('Q', array[ii] - 10)
        elif 21 <= array[ii] <= 30:
            card = Card('P', array[ii] - 20)
        elif 31 <= array[ii] <= 40:
            card = Card('F', array[ii] - 30)
        deck.append(card)   
    return np.array(deck)

def PrintStatus(table_matrix, card_number, next_card, hand, moves):
    print('\n------ Card: ' + str(card_number) + ' || Move: ' + str(moves))
    for ii in range(table_matrix.shape[0]):
        table_row = table_matrix[ii, :]
        for jj in range(len(table_row)):
            next_row, next_column = next_card.GetPosition()
            if next_row == ii and next_column == jj:
                color = 'yellow'
            else:
                color = 'white'
            table_row[jj].PrintCard(color)
        print()
    print('------ Hand:', end = ' ')
    for hand_card in hand:        
        hand_card.PrintCard(color = 'red')
    print('||', end = ' ')
    next_card.PrintCard(color = 'green')
    print()

def Solitaire(display = True, slow_down = None):

    # build the deck, define seed and numbers and shuffle the deck!
    sequence = np.arange(1, 41, 1)
    np.random.shuffle(sequence)
    deck = np.array(Sequence2Deck(sequence), dtype = Card)
    
    # define player's hand and table
    hand = deck[0:4]
    deck = deck[4:]
    table = deck.reshape(4, 9)

    # define king cards
    ck = Card('C', 10)
    qk = Card('Q', 10)
    pk = Card('P', 10)
    fk = Card('F', 10)
    kings = [ck, qk, pk, fk]

    # let's count the number of necessary actions and the number of cards drawn from the hand
    card_counter = 0
    actions = 0

    for card in hand:
        card_counter += 1
        this_card = card
        card_index = np.where(hand == this_card)
        hand = np.delete(hand, card_index)

        while this_card not in kings:
            
            # read future position for the card
            row, column = this_card.GetPosition()

            # eventually print the table status at the beginning of each loop
            if display == True:
                PrintStatus(table, card_counter, this_card, hand, actions)

            # memorize current card in that position
            temp_card = table[row, column]

            # substitute the card in that position
            table[row, column] = this_card
            this_card.SetStatus('correct')

            # the new card must be put in the right position!
            this_card = temp_card

            # let's count the action!
            actions += 1

            # if we want to follow the process we can simply slow things down!
            if slow_down:
                sleep(slow_down)

        if display == True:
            PrintStatus(table, card_counter, this_card, hand, actions)

def main():
    slowing_time = None
    if len(sys.argv) > 1:
        slowing_time = float(sys.argv[1])
    Solitaire(slow_down = slowing_time)

if __name__ == "__main__":
    main()