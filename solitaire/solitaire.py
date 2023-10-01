from typing import Any
import numpy as np
from termcolor import colored
from time import sleep
import sys

class Card:
    seed = ''
    value = 0
    status = 'neutral'

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
    
    def Check(self, table):
        row, column = self.GetPosition()
        if table[row, column] == self:
            return True

    def Update(self, string):
        self.status = string

    def PrintCard(self, color = None):
        stat = self.status
        val = self.value
        if val == 10:
            val = 'K'
        if not color:
            if stat == 'correct':
                print(colored(self.seed + str(val), 'blue'), end = ' ')
            elif stat == 'incorrect':
                print(colored(self.seed + str(val), 'red'), end = ' ')
            elif stat == 'to_be_substituted':
                print(colored(self.seed + str(val), 'yellow'), end = ' ')
            elif stat == 'neutral':
                print(colored(self.seed + str(val), 'white'), end = ' ')
        elif color:
            print(colored(self.seed + str(val), color), end = ' ')
        else:
            print(self.seed + str(val), end = ' ')


def TableState(table, true_indexes, kings):
    success = True
    for ii in range(table.shape[0]):
        for jj in range(table.shape[1]):
            if [ii, jj] not in true_indexes:
                if table[ii, jj] not in kings:
                    if table[ii, jj].Check(table) == True:
                        true_indexes.append([ii, jj])
                        table[ii, jj].Update('correct')
                    else:
                        table[ii, jj].Update('incorrect')
                        success = False
    return [true_indexes, success]   


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


def PrintState(table, card_number, next_card, hand, moves):
    print('\n------ Card: ' + str(card_number) + ' || Move: ' + str(moves))
    for ii in range(table.shape[0]):
        for jj in range(table.shape[1]):
            next_row, next_column = next_card.GetPosition()
            if next_row == ii and next_column == jj:
                state = 'to_be_substituted'
                table[ii, jj].Update(state)
            table[ii, jj].PrintCard()
        print()
    print('------ Hand:', end = ' ')
    for hand_card in hand:        
        hand_card.PrintCard(color = 'grey')
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
    table = np.array(deck.reshape(4, 9), dtype = Card)

    # define king cards
    ck = Card('C', 10)
    qk = Card('Q', 10)
    pk = Card('P', 10)
    fk = Card('F', 10)
    kings = [ck, qk, pk, fk]

    # let's count the number of necessary actions and the number of cards drawn from the hand
    card_counter = 0
    actions = 0
    true_positions = []
    success = False
    
    for card in hand:
        card_counter += 1
        this_card = card
        card_index = np.where(hand == this_card)
        hand = np.delete(hand, card_index)

        # eventually print the configuration at the very beginning of the game
        if display == True and actions == 0:
            true_positions, success = TableState(table, true_positions, kings)
            PrintState(table, card_counter, this_card, hand, actions)

        while this_card not in kings:
                        
            # read future position for the card
            row, column = this_card.GetPosition()

            # memorize current table card located in that position
            temp_card = table[row, column]

            # substitute the card in that position
            table[row, column] = this_card

            # the new card must be put in the right position!
            this_card = temp_card

            # keep track of the number of moves
            actions += 1

            # check table state during each loop
            true_positions, success = TableState(table, true_positions, kings)
            
            # eventually print the table status at the beginning of each loop
            if display == True:
                PrintState(table, card_counter, this_card, hand, actions)

            # if we want to follow the process we can simply slow things down!
            if slow_down:
                sleep(slow_down)

    return success 
 
def main():
    slowing_time = None
    disp = False
    success = []
    number_of_games = int(1e5)
    if len(sys.argv) > 1:
        disp = sys.argv[1]
        if disp == 'False':
            disp = False
        elif disp == 'True':
            disp = True
        slowing_time = float(sys.argv[2])
    
    success = Solitaire(display = disp, slow_down = slowing_time)
    print('\nSuccess: ' + str(success) +'\n')
    
    '''
    for ii in range(number_of_games):
        if Solitaire(display = False, slow_down = slowing_time) == True:
            success.append(1)
        else:
            success.append(0)
    good = np.sum(success)
    print('\nSuccess proboability is: ' + str((good/len(success))*100) + '%')
    '''    

if __name__ == "__main__":
    main()