from collections import Counter
from random import randrange,uniform
from time import sleep

class App():
 
    def __init__(self):
        self.stones = [[0]*8 for _ in range(8)]
        self.stones[3][3],self.stones[4][4] = 1,1
        self.stones[3][4],self.stones[4][3] = 2,2
        self.coord = [[[j,i] for i in range(8)] for j in range(8)]

        self.menu()


    def menu(self):
        while 1:
            print("----------------")
            print("Hello Othello!\n\n Solo: 1\nMulti: 2\n Quit: 3")
            print("----------------")
            inp = input("please select>>")
            if inp in ["1","2"]:
                self.result(self.play(int(inp)-1))
            elif inp == "3":
                print("\nThank you!\n")
                break
            else:
                print("\nInvalid value...\n")


    def play(self,player):
        turn = 0
        print()
        self.pri()
        passtime = 0
        while len(Counter([point for row in self.stones for point in row])) == 3:
            self.turn = turn%2 + 1
            bw = "Black" if self.turn == 1 else "White"
            if self.passing():
                flag = not player and self.turn-1 # CPUのターンのみTrue
                self.put = self.cpu() if flag else input(f"{bw} turn.\nRowCol?>> ")
                while 1:
                    if self.check(self.put):
                        inp = list(map(lambda x: x-1,map(int,[self.put[0],self.put[1]])))
                        if flag:
                            print("CPU is thinking...\n")
                            sleep(uniform(1,3))
                            print(f"{bw} turn.\nRowCol?>> {self.put[0]}{self.put[1]}")
                        self.over_run(inp)
                        self.pri()
                        passtime = 0
                        break
                    else:
                        print("\nInvalid value...\n")
                        self.pri()
                        self.put = input(f"{bw} turn.\nRowCol?>> ")
            else:
                print(f"{bw} passed...\n")
                passtime += 1
            turn += 1
            if passtime > 1: break
        con = []
        for i in range(3):
            con.append(Counter([point for row in self.stones for point in row])[i])
        return con


    def result(self,con):
        if con[1] == con[2]:
            print("Draw...\n")
        else:
            win = "Black" if con[1] > con[2] else "White"
            print(f"{win} Win! (B: {con[1]}, W: {con[2]})\n")


    def passing(self):
        for i,row in enumerate(self.stones):
            for j,p in enumerate(row):
                if not p:
                    if self.check([i,j]):
                        return True


    def check(self,inp):
        con = True
        try:
            inp = list(map(lambda x: x-1,map(int,[inp[0],inp[1]])))
            if len(inp) != 2 or not (0 <= min(inp) and max(inp) <= 7) or self.stones[inp[0]][inp[1]] != 0:
                con = False
            else:
                if not any(self.spider(inp)):
                    con = False
        except IndexError:
            con = False
        return con


    def spider(self,inp):
        vh = [self.coord[inp[0]][inp[1]:],[row[inp[1]] for row in self.coord[inp[0]:]],
                list(reversed(self.coord[inp[0]][:inp[1]+1])),list(reversed([row[inp[1]] for row in self.coord[:inp[0]+1]]))]
        dea = [[inp[0]+inp[1]-7, inp[0]+inp[1]>7, 0, "list(reversed(self.coord[end:inp[0]+1]))", 1],
                [7-(inp[1]-inp[0])+1, inp[0]<inp[1], 9 ,"self.coord[inp[0]:end]", 1],
                [inp[0]+inp[1]+1, inp[0]+inp[1]<7 ,9 ,"self.coord[inp[0]:end]", -1],
                [inp[0]-inp[1], inp[0]>inp[1],0 ,"list(reversed(self.coord[end:inp[0]+1]))", -1]]
        self.bind = []
        self.over = [False]*8
        for d in vh: # 右下左上
            self.bind.append(d)
        for d in dea: # 斜め
            table,j = [],inp[1]
            end = d[0] if d[1] else d[2]
            for i in eval(d[3]):
                table.append(i[j])
                j += d[4]
            self.bind.append(table)

        for n,che in enumerate(self.bind):
            flag = 0
            for i in che[1:]:
                t = self.stones[i[0]][i[1]]
                if t == self.turn and flag is True:
                    self.over[n] = True
                elif t == 3-self.turn:
                    flag = True
                else:
                    break
        return self.over


    def over_run(self,inp):
        self.stones[inp[0]][inp[1]] = self.turn
        for n,tf in enumerate(self.over):
            if tf:
                for i in self.bind[n][1:]:
                    if self.stones[i[0]][i[1]] == 3-self.turn:
                        self.stones[i[0]][i[1]] = self.turn
                    else:
                        break


    def pri(self):
        change = ord("１")-ord("1")
        print("　",end="")
        for m,table in enumerate([range(8),self.stones]):
            for n,row in enumerate(table):
                print(chr(ord(str(n+1))+change),end="")
                if m:
                    for j in row:
                        print("{}".format("○" if j == 1 else "●" if j == 2 else "・"),end="")
                    print()
            print()
 

    def cpu(self):
        poss = []
        coord = [[[j,i] for i in range(1,9)] for j in range(1,9)]
        self.turn = 2
        for row in coord:
            for point in row:
                if self.check(point):
                    poss.append(point)
        return poss[randrange(len(poss))]

 
play = App()