import numpy
import random
from collections import deque
import os

#to reinit the game
class TicTacToe:
    def __init__(self):
        self.board = [
            ['-', '-', '-', '0'],
            ['-', '-', '-', '1'],
            ['-', '-', '-', '2'],
            ('A', 'B', 'C')
        ]
        self.rndr = deque(['a0', 'b0', 'c0', 'a1', 'b1', 'c1', 'a2', 'b2', 'c2'])
        self.rndrIndex = {'a0': '00', 'b0': '01', 'c0': '02', 'a1': '10', 'b1': '11', 'c1': '12', 'a2': '20', 'b2': '21', 'c2': '22'}
        self.plyrBox = {'cpu': 'non', 'human': 'non'}
        self.plyrAvaliable = ['Ø', 'X']
        self.cpuTurn = False

    def gameover(self, figure):
        #ways to win
        score = False
        bias = 0
        prompter = 0
        if (len(self.rndr) < 6):
            while True:

                # horizontal
                while (prompter <= 2):
                    line = self.board[prompter][0:3]
                    for n in line:
                        if (n == figure):
                            bias+=1
                    if (bias > 2):
                        break;
                    else:
                        bias = 0
                        prompter += 1


                # vertical
                prompter = 2
                while (prompter >= 0):
                    for n in self.board:
                        if (n[prompter] == figure):
                            bias += 1
                    if (bias > 2):
                        score = figure
                        break;
                    else:
                        bias = 0
                        prompter -=1


                #diagonal
                prompter = 0
                for n in self.board:
                    if (n[prompter] == figure):
                        bias += 1
                    if (prompter<2):
                        prompter += 1
                if (bias > 2):
                    break;
                else:
                    bias = 0
                for n in self.board:
                    if (n[prompter] == figure):
                        bias += 1
                    if (prompter > 0):
                        prompter -= 1
                if (bias > 2):
                    break;
                else:
                    bias = 0
                break;

        if (bias > 2):
            score = True
        return score

    def load(self):
        print("The board løcks like")
        for row in self.board:
            for element in row:
                print(element, end=' ')
            print()

    ####### RULES ######
    # one turn per player
    # x fgr always start
    def press_start(self):

        choice = input('Choose your figure Ø or X (for Ø introduce o, for X introduce x, any other character it return an random figure)\n')
        choice = choice.lower()
        if (choice == 'x'):
            self.plyrBox['human'] = 'X'
            self.plyrBox['cpu'] = 'Ø'
        elif (choice == 'o'):
            self.plyrBox['cpu'] = 'X'
            self.plyrBox['human'] = 'Ø'
        else:
            self.plyrBox['cpu'] = random.choice(self.plyrAvaliable)
            self.plyrAvaliable.remove(self.plyrBox['cpu'])
            self.plyrBox['human'] = self.plyrAvaliable[0]

        if (self.plyrBox['cpu'] == 'X'):
            self.cpuTurn = True

        while True:
            avaliable = ', '.join(self.rndr)
            if (len(self.rndr) == 0):
                print("No body wins ▲....▲")
                break
            ############################## TIC TAC TOE ###############################
            if (self.cpuTurn):
                move = random.choice(self.rndr)
                self.rndr.remove(move)
                i = self.rndrIndex[move]
                k = list(i)
                self.board[int(k[0])][int(k[1])] = self.plyrBox['cpu']
                self.cpuTurn = False
                # end game
                if (self.gameover(self.plyrBox['cpu'])):
                    self.load()
                    print('Winner the CPU (you sucks!!!)')

            else:
                self.load()
                move = input("Your turn. Avalaiable boxes:\n" + avaliable + "\n")

                if (move in self.rndr):
                    self.rndr.remove(move)
                    i = self.rndrIndex[move]
                    k = list(i)
                    self.board[int(k[0])][int(k[1])] = self.plyrBox['human']
                    self.cpuTurn = True
                    #end game
                    if (self.gameover(self.plyrBox['human'])):
                        self.load()
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

while True:
    onArcade = TicTacToe()
    onArcade.press_start()
    plyAgain = input('Press enter to play again.')
    if (plyAgain != ''):
        break
    else:
        del onArcade

