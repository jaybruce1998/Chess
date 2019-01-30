import sys
class Square(object):
      
   def becomes(self, c, t):
      self.color=c
      self.type=t
      self.moved=0
      self.specialMoved=False
   
   def turnsInto(self, s):
      self.color=s.color
      self.type=s.type
      self.moved=s.moved
      self.specialMoved=s.specialMoved
      
   def reset(self):
      self.color=' '
      self.type="  "
      self.moved=1
      self.specialMoved=False
      
   def __str__( self ):
      return self.color+self.type
      
   
def resetBoard():
   col='W'
   kings[0]=row=7
   kings[1]=kings[3]=4
   kings[2]=kings[4]=0
   tmp[0].reset()
   for r in range(2, 6):
      for c in range(0, 8):
         board[r][c].reset()
   while col!=' ':
      board[row][0].becomes(col, "Rk")
      board[row][7].becomes(col, "Rk")
      board[row][1].becomes(col, "Kt")
      board[row][6].becomes(col, "Kt")
      board[row][2].becomes(col, "Bp")
      board[row][5].becomes(col, "Bp")
      board[row][3].becomes(col, "Qn")
      board[row][4].becomes(col, "Kg")
      if row<7:
         row=2
      for c in range(0, 8):
         board[row-1][c].becomes(col, "Pn")
      if col=='W':
         col='B'
         row=0
      else:
         col=' '
         
def showBoard(col):
   print()
   if col=='W':
      for r in range(0, 8):
         sys.stdout.write(str(8-r)+"|")
         for c in range(0, 8):
            sys.stdout.write(str(board[r][c])+"|")
         print()
      print("   A   B   C   D   E   F   G   H")
   else:
      for r in range(0, 8):
         sys.stdout.write(str(r+1)+"|")
         for c in range(0, 8):
            sys.stdout.write(str(board[7-r][7-c])+"|")
         print()
      print("   H   G   F   E   D   C   B   A")
      
def couldMove(col, r1, c1, r2, c2):
   type=board[r1][c1].type
   if type=="Rk" or type=="Qn":
      if c1==c2:
         if r2<r1:
            for r in range(r2+1, r1):
               if board[r][c1].color!=' ':
                  return False
            return True
         else:
            for r in range(r1+1, r2):
               if board[r][c1].color!=' ':
                  return False
            return True
      if r1==r2:
         if c2<c1:
            for c in range(c2+1, c1):
               if board[r1][c].color!=' ':
                  return False
            return True
         else:
            for c in range(c1+1, c2):
               if board[r1][c].color!=' ':
                  return False
            return True
   if type=="Kt":
      if abs(r1-r2)==1 and abs(c1-c2)==2:
         return True
      return abs(r1-r2)==2 and abs(c1-c2)==1
   if type=="Bp" or type=="Qn":
      dif=abs(r1-r2)
      if dif==abs(c1-c2):
         if(r2<r1):
            if(c2<c1):
               for i in range(1, dif):
                  if board[r1-i][c1-i].color!=' ':
                     return False
               return True
            else:
               for i in range(1, dif):
                  if board[r1-i][c1+i].color!=' ':
                     return False
               return True
         else:
            if(c2<c1):
               for i in range(1, dif):
                  if board[r1+i][c1-i].color!=' ':
                     return False
               return True
            else:
               for i in range(1, dif):
                  if board[r1+i][c1+i].color!=' ':
                     return False
               return True
   if type=="Kg":
      if board[r1][c1].moved<1:
         if col=='W' and r2==7 and not anyCanMoveTo(False, 'B', 7, 4):
            if c2==2:
               for c in range(2, 4):
                  if board[7][c].color!=' ' or anyCanMoveTo(False, 'B', 7, c):
                     return False
               return board[7][1].color==' '
            if c2==6:
               for c in range(5, 7):
                  if board[7][c].color!=' ' or anyCanMoveTo(False, 'B', 7, c):
                     return False
               return True
         if col=='B' and r2==0 and not anyCanMoveTo(False, 'W', 0, 4):
            if c2==2:
               for c in range(2, 4):
                  if board[0][c].color!=' ' or anyCanMoveTo(False, 'W', 0, c):
                     return False
               return board[0][1].color==' '
            if c2==6:
               for c in range(5, 7):
                  if board[0][c].color!=' ' or anyCanMoveTo(False, 'W', 0, c):
                     return False
               return True
      return abs(r1-r2)<2 and abs(c1-c2)<2
   if type=="Pn":
      if c1==c2 and board[r2][c1].color==' ':
         if abs(r1-r2)==2 and board[r1][c1].moved<1:
            if col=='W' and board[5][c1].color==' ':
               return True
            return col=='B' and board[2][c1].color==' '
         if col=='W' and r1-r2==1:
            return True
         return col=='B' and r2-r1==1
      if abs(c1-c2)==1:
         if col=='W' and r1-r2==1:
            return board[r2][c2].color=='B' or board[r1][c2].specialMoved
         if col=='B' and r2-r1==1:
            return board[r2][c2].color=='W' or board[r1][c2].specialMoved
   return False

def canMove(chk, col, r1, c1, r2, c2):
   if r1>=0 and r1<8 and c1>=0 and c1<8 and r2>=0 and r2<8 and c2>=0 and c2<8 and board[r1][c1].color==col and board[r2][c2].color!=col and couldMove(col, r1, c1, r2, c2):
      if(chk):
         doMove(col, r1, c1, r2, c2)
         if (col=='W' and anyCanMoveTo(False, 'B', kings[0], kings[1])) or (col=='B' and anyCanMoveTo(False, 'W', kings[2], kings[3])):
            undoMove(r1, c1, r2, c2)
            return False
         undoMove(r1, c1, r2, c2)
      return True
   return False

def doMove(col, r1, c1, r2, c2):
   tmp[0].turnsInto(board[r2][c2])
   kings[4]=0
   type=board[r1][c1].type
   if type=="Kg":
      if col=='W':
         kings[0]=r2
         kings[1]=c2
      else:
         kings[2]=r2
         kings[3]=c2
      if c1==4:
         if c2==2:
            board[r][3].turnsInto(board[r][0])
            board[r][0].reset()
         if c2==6:
            board[r][5].turnsInto(board[r][7])
            board[r][7].reset()
   if type=="Pn":
      if abs(r1-r2)==2:
         board[r1][c1].specialMoved=True
      if abs(c1-c2)==1 and board[r1][c2].specialMoved:
         tmp[0].turnsInto(board[r1][c2])
         board[r1][c2].reset()
         kings[4]=9
   board[r2][c2].turnsInto(board[r1][c1])
   board[r2][c2].moved+=1
   board[r1][c1].reset()
   
def undoMove(r1, c1, r2, c2):
   type=board[r2][c2].type
   if type=="Kg":
      if board[r2][c2].color=='W':
         kings[0]=r1
         kings[1]=c1
      else:
         kings[2]=r1
         kings[3]=c1
      if c1==4:
         if c2==2:
            board[r][0].turnsInto(board[r][3])
            board[r][3].reset()
         if c2==6:
            board[r][7].turnsInto(board[r][5])
            board[r][5].reset()
   board[r1][c1].turnsInto(board[r2][c2])
   board[r1][c1].moved-=1
   board[r1][c1].specialMoved=False
   if type=="Pn" and kings[4]==9 and abs(c1-c2)==1 and tmp[0].specialMoved:
      board[r1][c2].turnsInto(tmp[0])
   else:
      board[r2][c2].turnsInto(tmp[0])
   
def anyCanMoveTo(chk, col, r2, c2):
   for r in range(0, 8):
      for c in range(0, 8):
         if canMove(chk, col, r, c, r2, c2):
            return True
   return False

def anyCanMove(col):
   for r in range(0, 8):
      for c in range(0, 8):
         if anyCanMoveTo(True, col, r, c):
            return True
   return False

def over(col):
   wmp=bmp=0
   if col=='W':
      for c in range(0, 8):
         board[4][c].specialMoved=False
   else:
      for c in range(0, 8):
         board[3][c].specialMoved=False
   for r in range(0, 8):
      for c in range(0, 8):
         if board[r][c].type=="Kt" or board[r][c].type=="Bp":
            if board[r][c].color=='W':
               wmp+=1
            else:
               bmp+=1
         else:
            return not anyCanMove(col)
   return wmp<2 and bmp<2

def doTurn(col):
   r1=c1=r2=c2=8
   showBoard(col)
   if col=='W':
      if anyCanMoveTo(False, 'B', kings[0], kings[1]):
         print("Check!")
   if col=='B':
      if anyCanMoveTo(False, 'W', kings[2], kings[3]):
         print("Check!")
   while not canMove(True, col, r1, c1, r2, c2):
      typed=input()
      if len(typed)>4:
         r1=8-ord(typed[1])+48
         c1=ord(typed[0])-97
         r2=8-ord(typed[4])+48
         c2=ord(typed[3])-97
   doMove(col, r1, c1, r2, c2)
   if board[r2][c2].type=="Pn":
      if (col=='W' and r2<1) or (col=='B' and r2>6):
         print("Your pawn has advanced to the back row! Would you like a Rk, Kt, Bp or Qn?")
         while typed!="Rk" and typed!="Kt" and typed!="Bp" and typed!="Qn":
            typed=input()
         board[r2][c2].type=typed
def meth(x):
   x=6   
x=3
meth(x)
print(x)
board=[[Square() for c in range(0, 8)]for r in range(0, 8)]
tmp=[Square() for i in range(0, 1)]
kings=[0 for i in range(0, 5)]
going=True
resetBoard()
while going:
   if over('W'):
      going=False
      showBoard('W')
      if anyCanMoveTo(False, 'B', kings[0], kings[1]):
         print("White was checkmated!")
      else:
         print("Draw!")
   else:
      doTurn('W')
   if going:
      if over('B'):
         going=False
         showBoard('B')
         if anyCanMoveTo(False, 'W', kings[2], kings[3]):
            print("Black was checkmated!")
         else:
            print("Draw!")
      else:
         doTurn('B')