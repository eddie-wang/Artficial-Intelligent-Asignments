class Game:
    def __init__(self,inputFile):
        with open(inputFile) as f:
            self.initGame(f)
        if self.task!=4:
            self.nextState(self.player,self.task,self.cutff)
        else:
            self.play()
    def initGame(self,file):
        self.gameEnd=False
        self.task=int(file.readline())
        self.firstPlayerValue=0
        self.secondPlayerValue=0
        if task!=4:
            self.player=file.readline()
            self.cutoff=int(file.readline())
            ## outputfile
            self.nextStateOuput=open("next_state.tx","w")
            if task!=1:
                self.traverseOut=open("traverse_log.txt","w")
        else:
            self.firstPlayer=file.readline()
            self.firstAlg=int(file.readline())
            self.firstCutOff=int(file.readline())
            self.secondPlayer=file.readline()
            self.secondAlg=int(file.readline())
            self.secondCutOff=int(file.readline())
            self.traceOuput=open("trace_state.txt","w")
        self.boardValue=[[]*5] ##int
        for line in range(5):
            for v in file.readline().split():
                self.boardValue[line].append(v)
        self.boardState[[]*5] ##char
        for line in range(5):
            for index,v in enumerate(file.readline().split()):
                self.boardState[line].append(v)
                if v==self.firstPlayer:
                    self.firstPlayerValue+=self.boardValue[line][index]
                elif v==self.secondPlayer:
                    self.secondPlayerValue+=self.boardValue[line][index]

    def play(self):
        while self.gameEnd==False:
            nextState(self.firstPlayer,self.firstAlg,self.firstCutOff)
            nextState(self.secondPlayer,self.secondAlg,self.secondCutOff)
    def  nextState(self,player,task,cutoff):
        methodDict={1:greedyBFS,2:minMax,3:alphaPruning}
        methodDict[task](player,cutoff)
        printState()

    def move(self,player,result):
        ## can reduce code by using dict modify!!

        if player==self.firstPlayer:
            self.firstPlayerValue=res[0]
            self.secondPlayerValue=res[1]
        else:
            self.secondPlayerValue=res[1]
            self.firstPlayerValue=res[0]
        self.boardState[i][j]=player

        direction=[(1:1),(1:-1),(-1,1),(-1,-1)]

        for d in result[2]:
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
        direction=[(1:1),(1:-1),(-1,1),(-1,-1)]
        raid=[]
        for i in range(4):
            if opponent(player,pos_i+direction[i][0],pos_j+direction[i][1]):
                myplayer+=self.boardValue[pos_i+direction[i][0]][pos_j+direction[i][1]]
                opplayer-=self.boardValue[pos_i+direction[i][0]][pos_j+direction[i][1]]
                raid.append(i)
        eva=myplayer-opplayer
        return (eva,myplayer,opplayer,raid)

    def opponent(self,player,i,j):
        if i>0 and i<5 and j>0 and j<5 and self.boardState[i][j]!="*" and self.boardState[i][j]!=player
    def greedyBFS(self,player,cutoff):
        maxEva=-100000000
        i=-1;j=-1;
        result=()
        for row in range(5):
            for col in range(5):
                if self.boardState[i][j]=='*'
                    evaResult= self.evaluation(player,row,col)
                    if evaResult[0]>maxEva:
                        maxEva=cur;i=row;j=col;result=evaResult;
        if i==-1 and j==-1:
            self.gameEnd=True
        move(player,evaResult)
    def minMax(self,player,cutoff):
        pass

    def alphaPruning(self,player,cutoff):
        pass

    def printState(self):
        pass
if __name__=='__main__':
    if len(sys.argv!=3) or sys.argv[1]!="-i":
        print "input formate error"
        sys.exit()
    game=Game(sys.argv[2])
