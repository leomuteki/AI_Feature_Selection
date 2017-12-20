import sys
import math
import copy
INSTANCES=2
ROWS=0
COLS=0
alreadyVisited=set()

def forwardSelection(data):
    print "Beginning search.\n"
    global alreadyVisited
    alreadyVisited=set()
    levelBestAcc=-1
    levelBestCombo=[]
    totalBestAcc=-1
    totalBestCombo=[]
    while len(levelBestCombo)<COLS-1:
        expandedParent=copy.deepcopy(levelBestCombo)
        levelBestAcc=-1
        #populate level with combinations
        for newFeature in range(1,COLS):
            if newFeature not in expandedParent:
                combo=copy.deepcopy(expandedParent)
                combo.append(newFeature)
                if listToID(combo) not in alreadyVisited:
                    alreadyVisited.add(listToID(combo))
                    if levelBestAcc<0:
                        badLimit=float('inf')
                    else:
                        badLimit=ROWS-levelBestAcc*ROWS
                    acc=getAcc(combo,badLimit)
                    print "    Using feature(s) ",combo," accuracy is ",acc*100.0,"%"
                    if acc>levelBestAcc:
                        levelBestAcc=acc
                        levelBestCombo=combo
                    if acc>totalBestAcc:
                        totalBestAcc=acc
                        totalBestCombo=combo
        if levelBestAcc < totalBestAcc:
            print "(Warning, Accuracy has decreased! Continuing search in case of local maxima)"
        print "\nFeature set ",levelBestCombo," was best, accuracy is ",levelBestAcc*100.0,"%\n"
    print "Finised Search! The best feature subset is ",totalBestCombo,","
    print "which has an accuracy of ",totalBestAcc*100.0,"%"

def BackwardElimination(data):
    print "Beginning search.\n"
    global alreadyVisited
    alreadyVisited=set()
    #populate level with initial combination
    levelBestCombo=[]
    for colNum in range(1,COLS):
        levelBestCombo.append(colNum)
    alreadyVisited.add(listToID(levelBestCombo))
    badLimit=float('inf')
    acc=getAcc(levelBestCombo,badLimit)
    print "    Using feature(s) ",levelBestCombo," accuracy is ",acc*100.0,"%"
    levelBestAcc=acc
    totalBestAcc=acc
    totalBestCombo=levelBestCombo
    while len(levelBestCombo)>1:
        expandedParent=copy.deepcopy(levelBestCombo)
        levelBestAcc=-1
        #populate level with combinations
        for deleteFeature in expandedParent:
            combo=copy.deepcopy(expandedParent)
            combo.remove(deleteFeature)
            if listToID(combo) not in alreadyVisited:
                alreadyVisited.add(listToID(combo))
                if levelBestAcc<0:
                    badLimit=float('inf')
                else:
                    badLimit=ROWS-levelBestAcc*ROWS
                acc=getAcc(combo,badLimit)
                print "    Using feature(s) ",combo," accuracy is ",acc*100.0,"%"
                if acc>levelBestAcc:
                    levelBestAcc=acc
                    levelBestCombo=combo
                if acc>totalBestAcc:
                    totalBestAcc=acc
                    totalBestCombo=combo
        if levelBestAcc < totalBestAcc:
            print "(Warning, Accuracy has decreased! Continuing search in case of local maxima)"
        print "\nFeature set ",levelBestCombo," was best, accuracy is ",levelBestAcc*100.0,"%\n"
    print "Finised Search! The best feature subset is ",totalBestCombo,","
    print "which has an accuracy of ",totalBestAcc*100.0,"%"
    
def FurthestCOM(data):
    print "Beginning search.\n"
    global alreadyVisited
    alreadyVisited=set()
    levelBestScore=-1
    levelBestAcc=-1
    levelBestCombo=[]
    totalBestAcc=-1
    totalBestCombo=[]
    averages=[]
    fillAverages(data,averages)
    while len(levelBestCombo)<COLS-1:
        expandedParent=copy.deepcopy(levelBestCombo)
        levelBestScore=-1
        #populate level with combinations
        for newFeature in range(1,COLS):
            if newFeature not in expandedParent:
                combo=copy.deepcopy(expandedParent)
                combo.append(newFeature)
                if listToID(combo) not in alreadyVisited:
                    alreadyVisited.add(listToID(combo))
                    badLimit=float('inf')
                    acc=getAcc(combo,badLimit)
                    # Get distance between Center Of Masses
                    distCOM=euclideanDist(averages,0,1,combo)
                    # We want the highest accuracy and the furthest center of mass
                    score=acc*distCOM
                    print "    Feature(s): ",combo," accuracy: ",acc*100.0,"%, distCOM: ",distCOM,", score: ",score
                    if score>levelBestScore:
                        levelBestScore=score
                        levelBestAcc=acc
                        levelBestCombo=combo
                    if acc>totalBestAcc:
                        totalBestAcc=acc
                        totalBestCombo=combo
        if levelBestAcc < totalBestAcc:
            print "(Warning, Accuracy has decreased! Continuing search in case of local maxima)"
        print "\nFeature set ",levelBestCombo," was best, score is ",levelBestScore, ", acc: ",levelBestAcc,", distCOM: ",score/levelBestAcc
    print "Finised Search! The best feature subset is ",totalBestCombo,","
    print "which has an accuracy of ",totalBestAcc*100.0,"%"
    
def fillAverages(data,averages):
    # 'averages' has a row per instance
    # column 0 will be the count, other columns will be the sum per feature
    emptyCols=[]
    for colNum in range(COLS):
        emptyCols.append(0)
    for instanceNum in range(INSTANCES):
        emptyColsCpy=copy.deepcopy(emptyCols)
        averages.append(emptyColsCpy)
    for rowNum in range(ROWS):
        # Parse instance number to averages index and increse instance count
        instance=int(data[rowNum][0])-1
        averages[instance][0]+=1
        for colNum in range(1,COLS):
            averages[instance][colNum]+=data[rowNum][colNum]
    # Divide sums by count in column 0 to get averages
    for instance in range(INSTANCES):
        for colNum in range(1,COLS):
            averages[instance][colNum]/=float(averages[instance][0])

def euclideanDist(data,rowA,rowB,cols):
    sum=0
    for colNum in cols:
        curDist=data[rowA][colNum]-data[rowB][colNum]
        sum+=curDist*curDist
    return math.sqrt(sum)

def normalizeData(data):
    global ROWS
    ROWS=len(data)
    global COLS
    COLS=len(data[0])
    print "\nThis dataset has ",COLS-1," features (not including the class attributes)"
    print "with ",ROWS," instances.\n"
    sys.stdout.write("Please wait while I normalize the data... ")
    sys.stdout.flush()
    for colNum in range(1,len(data[0])):
        # Get min/max
        minRow=0
        maxRow=0
        for rowNum in range(ROWS):
            if data[rowNum][colNum]<data[minRow][colNum]: minRow=rowNum
            if data[rowNum][colNum]>data[maxRow][colNum]: maxRow=rowNum
        gap=data[maxRow][colNum]-data[minRow][colNum]
        # Normalize
        for rowNum in range(ROWS):
            if data[rowNum][colNum] not in [data[minRow][colNum],data[maxRow][colNum]]:
                data[rowNum][colNum]=(data[rowNum][colNum]-data[minRow][colNum])/gap
        data[minRow][colNum]=0.0
        data[maxRow][colNum]=1.0
    print "Done!\n"
        
def listToID(combo):
    combo.sort()
    string=""
    for feature in combo:
        string+=str(feature)+' '
    return string
    
def getAcc(combo,badLimit):
        badSoFar=0
        for a in range(ROWS):
            # Find the closest instance b to a
            minDist=-1
            minDistRow=0
            for b in range(ROWS):
                if b != a:
                    dist=euclideanDist(data,a,b,combo)
                    if minDist==-1 or dist<minDist:
                        minDist=dist
                        minDistRow=b
            if data[a][0] != data[minDistRow][0]:
                badSoFar+=1
            if badSoFar>badLimit:
                return 0
        return 1.0*(ROWS-badSoFar)/ROWS

if __name__ == '__main__':
    print "Welcome to Emmilio Segovia's Feature Selection Algorithm."
    input = raw_input("Type in the name of the file to test: ")
    data=[]
    file = open(input, "r" )
    for line in file:
        row = line.split()
        rowOfFloats = [float(n) for n in row]
        data.append(rowOfFloats)
    algorithm = int(raw_input("\nType the number of the algorithm you want to run.\n\n"
    +"1) Forward Selection\n"
    +"2) Backward Elimination\n"
    +"3) Emmilio's Special Algorithm\n\n"))
    normalizeData(data)
    print "Running nearest neighbor with all ",COLS-1," features, using \"leaving-one-out\" evaluation,"
    print "I get an accuracy of ___\n"
    if algorithm==1:
        forwardSelection(data)
    elif algorithm==2:
        BackwardElimination(data)
    elif algorithm==3:
        FurthestCOM(data)
    else:
        print "invalid algorithm choice."