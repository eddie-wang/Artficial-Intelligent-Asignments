import sys
class Game:
    def __init__(self,inputFile):
        with open(inputFile) as f:
            self.initGame(f)
        if self.task!=4:
            self.nextState(self.firstPlayer,self.task,self.cutOff)
        else:
            self.play()
    def initGame(self,file):
        self.gameEnd=False
        self.task=int(file.readline())
        self.firstPlayerValue=0
        self.secondPlayerValue=0
        if self.task!=4:
            self.firstPlayer=file.readline().strip()
            self.secondPlayer="X" if self.firstPlayer=="O" else "O"
            self.cutOff=int(file.readline().strip())
            ## outputfile
            self.nextStateOuput=open("next_state.tx","w")
            if self.task!=1:
                self.traverseOut=open("traverse_log.txt","w")
        else:
            self.firstPlayer=file.readline().strip()
            self.firstAlg=int(file.readline().strip())
            self.firstCutOff=int(file.readline().strip())
            self.secondPlayer=file.readline().strip()
            self.secondAlg=int(file.readline().strip())
            self.secondCutOff=int(file.readline().strip())
            self.traceOuput=open("trace_state.txt","w")
        self.boardValue=[] ##int
        for line in range(5):
            self.boardValue.append([])
            for v in file.readline().split():
                self.boardValue[line].append(int(v))
        print self.boardValue
        self.boardState=[] ##char
        for index,line in enumerate(file.readlines()):
            self.boardState.append(list(line.strip()))
            for i,v in enumerate(line.strip()):
                if v==self.firstPlayer:
                    self.firstPlayerValue+=self.boardValue[index][i]
                elif v==self.secondPlayer:
                    self.secondPlayerValue+=self.boardValue[index][i]
        print self.boardState
    def play(self):
        while self.gameEnd==False:
            nextState(self.firstPlayer,self.firstAlg,self.firstCutOff)
            nextState(self.secondPlayer,self.secondAlg,self.secondCutOff)
    def  nextState(self,player,task,cutoff):
        methodDict={1:self.greedyBFS,2:self.minMax,3:self.alphaPruning}
        methodDict[task](player,cutoff)
        self.printState()

    def move(self,player,i,j,res):
        ## can reduce code by using dict modify!!
        print i,j,"wxg",res
        if player==self.firstPlayer:
            self.firstPlayerValue=res[0]
            self.secondPlayerValue=res[1]
        else:
            self.secondPlayerValue=res[1]
            self.firstPlayerValue=res[0]
        self.boardState[i][j]=player

        direction=[(0,1),(1,0),(-1,0),(0,-1)]

        for d in res[3]:
            self.boardState[i+direction[d][0]][j+direction[d][1]]=player

    def evaluation(self,player,pos_i,pos_j):
        myplayer=0;opplayer=0
        if player==self.firstPlayer:
            myplayer=self.firstPlayerValue
            opplayer=self.secondPlayerValue
        else:
            myplayer=self.secondPlayerValue
            opplayer=self.firstPlayerValue
        myplayer+=self.boardValue[pos_i][pos_j]
        direction=[(0,1),(1,0),(-1,0),(0,-1)]
        raid=[]
        for i in range(4):
            if self.opponent(player,pos_i+direction[i][0],pos_j+direction[i][1]):
                myplayer+=self.boardValue[pos_i+direction[i][0]][pos_j+direction[i][1]]
                opplayer-=self.boardValue[pos_i+direction[i][0]][pos_j+direction[i][1]]
                raid.append(i)
        eva=myplayer-opplayer
        return (eva,myplayer,opplayer,raid)

    def opponent(self,player,i,j):
        if i>0 and i<5 and j>0 and j<5 and self.boardState[i][j]!="*" and self.boardState[i][j]!=player:
            return True
        return False
    def greedyBFS(self,player,cutoff):
        maxEva=-100000000
        i=-1;j=-1;
        result=()
        evaResult=()
        print self.boardState
        for row in range(5):
            for col in range(5):
                
                if self.boardState[row][col]=='*':
                    evaResult= self.evaluation(player,row,col)
                    print evaResult
                    if evaResult[0]>maxEva:
                        maxEva=evaResult[0];i=row;j=col;result=evaResult;
        if i==-1 and j==-1:
            self.gameEnd=True
        else:
            self.move(player,i,j,evaResult)
    def minMax(self,player,cutoff):
        pass

    def alphaPruning(self,player,cutoff):
        pass

    def printState(self):
        print self.boardState
if __name__=='__main__':
    if len(sys.argv)!=3 or sys.argv[1]!="-i":
        print "input formate error"
        sys.exit()
    game=Game(sys.argv[2])
