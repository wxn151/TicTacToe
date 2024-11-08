import numpy
import random
from collections import deque
import os

board = [
    ['-', '-', '-', '0'],
    ['-', '-', '-', '1'],
    ['-', '-', '-', '2'],
    ['A', 'B', 'C']
]

#to reinit the game
class Regret:
    _rndr = deque(['a0', 'b0', 'c0', 'a1', 'b1', 'c1', 'a2', 'b2', 'c2'])
    _plyrFigure = ('Ø', 'X')

rndr = Regret._rndr
rndrIndex = {'a0': '00', 'b0': '01', 'c0': '02', 'a1': '10', 'b1': '11', 'c1': '12', 'a2': '20', 'b2': '21', 'c2': '22'}
plyrBox = {'cpu': 'non', 'human': 'non'}
plyrAvaliable = Regret._plyrFigure
cpuTurn = False

def gameover(figure):
    #ways to win
    score = False
    bias = 0
    if (len(rndr) < 6):
        while True:

            # horizontal
            line = board[0][0:3]
            for n in line:
                if (n == figure):
                    bias+=1
            if (bias > 2):
                break;
            else:
                bias = 0
            line = board[1][0:3]
            for n in line:
                if (n == figure):
                    bias += 1
            if (bias > 2):
                break;
            else:
                bias = 0
            line = board[2][0:3]
            for n in line:
                if (n == figure):
                    bias += 1
            if (bias > 2):
                break;
            else:
                bias = 0

            # vertical
            for n in board:
                if (n[0] == figure):
                    bias += 1
            if (bias > 2):
                score = figure
                break;
            else:
                bias = 0
            for n in board:
                if (n[2] == figure):
                    bias += 1
            if (bias > 2):
                break;
            else:
                bias = 0
            for n in board:
                if (n[1] == figure):
                    bias += 1
            if (bias > 2):
                break;
            else:
                bias = 0

            #diagonal
            pos = 0
            for n in board:
                if (n[pos] == figure):
                    bias += 1
                if (pos<2):
                    pos += 1
            if (bias > 2):
                break;
            else:
                bias = 0
            for n in board:
                if (n[pos] == figure):
                    bias += 1
                if (pos > 0):
                    pos -= 1
            if (bias > 2):
                break;
            else:
                bias = 0
            break;

    if (bias > 2):
        score = True
    return score

def load():
    print("The board løcks like")
    for row in board:
        for element in row:
            print(element, end=' ')
        print()



####### RULES ######
# one turn per player

choice = input('Choose your figure Ø or X (for Ø introduce o, for X introduce x, any other character it return an random figure)\n')
choice = choice.lower()
if (choice == 'x'):
    plyrBox['human'] = 'X'
    plyrBox['cpu'] = 'Ø'
elif (choice == 'o'):
    plyrBox['cpu'] = 'X'
    plyrBox['human'] = 'Ø'
else:
    plyrBox['cpu'] = random.choice(plyrAvaliable)
    plyrAvaliable.remove(plyrBox['cpu'])
    plyrBox['human'] = plyrAvaliable[0]

if (plyrBox['cpu'] == 'X'):
    cpuTurn = True

while True:
    avaliable = ', '.join(rndr)
    if (len(rndr) == 0):
        print("No body wins ..▲..")
        break
    ############################## TIC TAC TOE ###############################
    if (cpuTurn):
        move = random.choice(rndr)
        rndr.remove(move)
        i = rndrIndex[move]
        k = list(i)
        board[int(k[0])][int(k[1])] = plyrBox['cpu']
        cpuTurn = False
        # end game
        if (gameover(plyrBox['cpu'])):
            load()
            print('Winner the CPU (you sucks!!!)')
            break

    else:
        load()
        move = input("Your turn. Avalaiable boxes:\n" + avaliable + "\n")

        if (move in rndr):
            rndr.remove(move)
            i = rndrIndex[move]
            k = list(i)
            board[int(k[0])][int(k[1])] = plyrBox['human']
            cpuTurn = True
            #end game
            if (gameover(plyrBox['human'])):
                load()
                f = input('Congrats, you are the winner\n Enter your name _')[0]
                # os.system('cls') # to wndws
                os.system('clear') # to lnx
                s = input(f'Congrats, you are the winner\n Enter your name {f} _')[0]
                os.system('clear')
                t = input(f'Congrats, you are the winner\n Enter your Name {f} {s} _')[0]
                os.system('clear')
                arcade = f + s + t
                print(f'bye {arcade}. thx to play')
                break
        else:
            print("Introduce an avaliable option\n")

