import numpy as np
from termcolor import colored

def Number(number):
    if number == 1:
        string = 'first'
    elif number == 2:
        string = 'second'
    elif number == 3:
        string = 'third'
    elif number == 4:
        string = 'fourth'
    
    return string

def CheckSuccess(table):
    success_matrix = ([['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9'],
                        ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9'], ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9']])
    if (table == success_matrix).all():
        return 1
    else:
        return 0
    
def Row(seed):
    if seed == 'C':
        row = 0
    elif seed == 'Q':
        row = 1
    elif seed == 'P':
        row = 2
    elif seed == 'F':
        row = 3
    return row

def Card2Position(string):
    seed = string[0]
    row = Row(seed)
    column = int(string[1:]) - 1

    return row, column

def Sequence2Deck(array):
    '''Convert a number sequence in gaming cards'''
    deck = []
    for ii in range(len(array)):
        if 1 <= array[ii] <= 10:
            this_value = 'C' + str(array[ii])
        elif 11 <= array[ii] <= 20:
            this_value = 'Q' + str(array[ii] - 10)
        elif 21 <= array[ii] <= 30:
            this_value = 'P' + str(array[ii] - 20)
        elif 31 <= array[ii] <= 40:
            this_value = 'F' + str(array[ii] - 30)

        deck.append(this_value)
    return np.array(deck)

def PrintTable(table, actions, current_hand):
    print('-------------------   ' + str(actions))
    for i in range(4):
        table_row = table[i, :]
        for dummy_table in table_row:
            print(colored(dummy_table, 'blue'), end = '  ')
        print()
    print('---------------- ' + colored('Hand:', 'red'), end = ' ')
    if len(current_hand) > 0:
        for dummy_hand in current_hand:
            if len(current_hand) > 0:
                print(colored(dummy_hand, 'red'), end = ' ')
        print('\n')
    else:
        print(colored('empty!', 'red'))   
    print('--------------------------------------------------')
    
def Solitaire(display = True):

    # build the deck, define seed and numbers and shuffle the deck!
    sequence = np.arange(1, 41, 1)
    np.random.shuffle(sequence)
    deck = Sequence2Deck(sequence)

    # define player's hand and table
    table = (deck[4:]).reshape(4, 9)
    hand = deck[0:4]

    # define king cards
    kings = ['C10', 'Q10', 'P10', 'F10']

    # let's count the number of necessary actions and the number of cards drawn from the hand
    card_counter = 0
    actions = 0
    current_hand = hand

    for card in hand:
        card_counter += 1
        this_card = card      

        # eventually print the hand status when a new card is drawn
        if display == True:
            print('--------------------------------------------------')
            print('Card: ' + colored(this_card, 'red') + ', ' + Number(card_counter) + ' card drawn.')
            card_index = np.where(current_hand == this_card)
            current_hand = np.delete(current_hand, card_index)

        while this_card not in kings:

            # eventually print the table status at the beginning of each loop
            if display == True:
                PrintTable(table, actions, current_hand)

            # read card future position
            row, column = Card2Position(this_card)

            # memorize current card in that position
            temp_card = table[row, column]

            # substitute the card in that position
            table[row, column] = this_card

            # the new card must be put in the right position!
            this_card = temp_card

            # let's count the action!
            actions += 1
    
    return CheckSuccess(table), actions