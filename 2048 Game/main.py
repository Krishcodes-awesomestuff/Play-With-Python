from tkinter import *
from tkinter import messagebox
import random
import os

class Board:
    bg_color={
        #'2': '#eee4da',
        '2': '#CAFF70',
        '4': '#BCEE68',
        '8': '#00C957',
        '16': '#00CD00',
        '32': '#ADFF2F',
        '64': '#32CD32',
        '128': '#9ACD32',
        '256': '#00EE76',
        '512': '#00CD66',
        '1024': '#54FF9F',
        '2048': '#FFFF00',
    }
    color={
         '2': '#776e65',
        '4': '#f9f6f2',
        '8': '#f9f6f2',
        '16': '#f9f6f2',
        '32': '#f9f6f2',
        '64': '#f9f6f2',
        '128': '#f9f6f2',
        '256': '#f9f6f2',
        '512': '#776e65',
        '1024': '#f9f6f2',
        '2048': '#f9f6f2',
    }
    def __init__(self):
        self.number=4
        self.main_window=Tk()
        self.main_window.title('2048 Game')
        
        # Load high score
        self.high_score = self.load_high_score()
        
        # Modified score frame to include restart button
        self.score_frame = Frame(self.main_window)
        self.score_frame.grid(row=0, column=0, columnspan=4, pady=5)
        self.score_label = Label(self.score_frame, text="Score: 0", font=('arial', 20, 'bold'))
        self.score_label.grid(row=0, column=0, padx=10)
        self.high_score_label = Label(self.score_frame, text=f"High Score: {self.high_score}", font=('arial', 20, 'bold'))
        self.high_score_label.grid(row=0, column=1, padx=10)
        self.restart_button = Button(self.score_frame, text="Restart", font=('arial', 15, 'bold'), command=self.restart_game)
        self.restart_button.grid(row=0, column=2, padx=10)
        
        self.gameArea=Frame(self.main_window,bg= 'dark green')
        self.board=[]
        self.grid=[[0]*4 for i in range(4)]
        self.compress=False
        self.merge=False
        self.moved=False
        self.score=0
        for i in range(4):
            rows=[]
            for j in range(4):
                lab=Label(self.gameArea,text='',bg='green',
                font=('arial',22,'bold'),width=4,height=2)
                lab.grid(row=i,column=j,padx=7,pady=7)
                rows.append(lab);
            self.board.append(rows)
        self.gameArea.grid()
    def reverse(self):
        for index in range(4):
            i=0
            j=3
            while(i<j):
                self.grid[index][i],self.grid[index][j]=self.grid[index][j],self.grid[index][i]
                i+=1
                j-=1
    def transpose(self):
        self.grid=[list(t)for t in zip(*self.grid)]
    def compressGrid(self):
        self.compress=False
        temp=[[0] *4 for i in range(4)]
        for i in range(4):
            count=0
            for j in range(4):
                if self.grid[i][j]!=0:
                    temp[i][count]=self.grid[i][j]
                    if count!=j:
                        self.compress=True
                    count+=1
        self.grid=temp
    def load_high_score(self):
        try:
            with open('high_score.txt', 'r') as file:
                return int(file.read())
        except:
            return 0
            
    def save_high_score(self):
        with open('high_score.txt', 'w') as file:
            file.write(str(self.high_score))

    def mergeGrid(self):
        self.merge=False
        for i in range(4):
            for j in range(4 - 1):
                if self.grid[i][j] == self.grid[i][j + 1] and self.grid[i][j] != 0:
                    self.grid[i][j] *= 2
                    self.grid[i][j + 1] = 0
                    self.score += self.grid[i][j]
                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.save_high_score()
                        self.high_score_label.config(text=f"High Score: {self.high_score}")
                    self.score_label.config(text=f"Score: {self.score}")
                    self.merge = True
    def random_cell(self):
        cells=[]
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    cells.append((i, j))
        curr=random.choice(cells)
        i=curr[0]
        j=curr[1]
        self.grid[i][j]=2
    
    def can_merge(self):
        for i in range(4):
            for j in range(3):
                if self.grid[i][j] == self.grid[i][j+1]:
                    return True
        
        for i in range(3):
            for j in range(4):
                if self.grid[i+1][j] == self.grid[i][j]:
                    return True
        return False
    def paintGrid(self):
        for i in range(4):
            for j in range(4):
                if self.grid[i][j]==0:
                    self.board[i][j].config(text='',bg='chartreuse2')
                else:
                    self.board[i][j].config(text=str(self.grid[i][j]),
                    bg=self.bg_color.get(str(self.grid[i][j])),
                    fg=self.color.get(str(self.grid[i][j])))
    def restart_game(self):
        # Reset grid
        self.grid = [[0]*4 for i in range(4)]
        self.score = 0
        self.compress = False
        self.merge = False
        self.moved = False
        
        # Update score display
        self.score_label.config(text="Score: 0")
        
        # Initialize new game
        self.random_cell()
        self.random_cell()
        self.paintGrid()
class Game:
    def __init__(self,playpanel):
        self.playpanel = playpanel
        self.end = False
        self.won = False
        
        # Add restart method to reset game state
        self.playpanel.restart_game = lambda: self.restart()
    
    def restart(self):
        self.end = False
        self.won = False
        self.playpanel.restart_game()
    def start(self):
        self.playpanel.random_cell()
        self.playpanel.random_cell()
        self.playpanel.paintGrid()
        self.playpanel.main_window.bind('<Key>', self.link_keys)
        self.playpanel.main_window.mainloop()
    
    def link_keys(self,event):
        if self.end or self.won:
            return
        self.playpanel.compress = False
        self.playpanel.merge = False
        self.playpanel.moved = False
        presed_key=event.keysym
        if presed_key=='Up':
            self.playpanel.transpose()
            self.playpanel.compressGrid()
            self.playpanel.mergeGrid()
            self.playpanel.moved = self.playpanel.compress or self.playpanel.merge
            self.playpanel.compressGrid()
            self.playpanel.transpose()
        elif presed_key=='Down':
            self.playpanel.transpose()
            self.playpanel.reverse()
            self.playpanel.compressGrid()
            self.playpanel.mergeGrid()
            self.playpanel.moved = self.playpanel.compress or self.playpanel.merge
            self.playpanel.compressGrid()
            self.playpanel.reverse()
            self.playpanel.transpose()
        elif presed_key=='Left':
            self.playpanel.compressGrid()
            self.playpanel.mergeGrid()
            self.playpanel.moved = self.playpanel.compress or self.playpanel.merge
            self.playpanel.compressGrid()
        elif presed_key=='Right':
            self.playpanel.reverse()
            self.playpanel.compressGrid()
            self.playpanel.mergeGrid()
            self.playpanel.moved = self.playpanel.compress or self.playpanel.merge
            self.playpanel.compressGrid()
            self.playpanel.reverse()
        else:
            pass
        self.playpanel.paintGrid()
        print(self.playpanel.score)
        flag=0
        for i in range(4):
            for j in range(4):
                if(self.playpanel.grid[i][j]==2048):
                    flag=1
                    break
        if(flag==1): #found 2048
            self.won=True
            messagebox.showinfo('2048', message='Congratulations! You have won!')
            print("WON")
            return
        for i in range(4):
            for j in range(4):
                if self.playpanel.grid[i][j]==0:
                    flag=1
                    break
        if not (flag or self.playpanel.can_merge()):
            self.end=True
            messagebox.showinfo('2048','Game Over!!!')
            print("Over")
        if self.playpanel.moved:
            self.playpanel.random_cell()
        
        self.playpanel.paintGrid()
    
playpanel =Board()
game2048 = Game( playpanel)
game2048.start()
