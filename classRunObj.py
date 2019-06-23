# parse the data from the input files
# create the run objects

import datetime

class ExperamentalRun:
    cutOffTime = 10800000000000
    date = 0
    transactions = 0
    attributes = 0
    flexable = 0
    query = ''
    qSup = 0
    isTrans = False
    minsup = 0
    setsGen = 0
    flexPrecentage = 0.0
    avgTtime = 0
    avgNtime = 0
    avgStime = 0
    t_times = 0
    n_times = 0
    s_times = 0
    t_Mem = 0
    n_Mem = 0
    s_Mem = 0
    tavgM =0
    navgM =0
    savgM = 0
    
    def __init__(self, logString):
        self.parseLog(logString)
        self.fixCutOffTimes()
        
    def parseLog(self, logString):
        #Date,Time,Transactions,Attributes,Flexable,query,isTrans,qSup,minsup,
        #setsGen,avgTtime,avgNtime,avgStime,
        #T_times,,,,,N_times,,,,,S_times,,,,,FP_times,,,,,
        #T_Mem,(megabytes),,,,N_Mem,,,,,S_Mem,,,,,FP_Mem
        dataPoints = logString.split(",")
        if '-' in dataPoints[1]:
            timep = dataPoints[1]
            timep = timep[:timep.index('-')]
            self.date = datetime.datetime.strptime(dataPoints[0]+","+timep, "%m/%d/%Y, %H:%M:%S")
        else:
            self.date = datetime.datetime.strptime(dataPoints[0]+","+dataPoints[1], "%m/%d/%Y, %H:%M:%S.%f")
        self.transactions = int(dataPoints[2])
        self.attributes = int(dataPoints[3])
        self.flexable = int(dataPoints[4])
        self.query = dataPoints[5]
        self.isTrans = dataPoints[6] == 'TRUE'
        self.qSup = int(dataPoints[7])
        self.minsup = int(dataPoints[8])
        self.setsGen = int(dataPoints[9])
        if self.flexable != -1:
            self.flexPrecentage = round((self.flexable/self.attributes)*4)/4
        else:
            self.flexPrecentage = -1
        
        try:
            self.avgTtime = int(dataPoints[10])
        except ValueError:
            try:
                self.avgTtime = perseEpoNotation(dataPoints[10])
            except ValueError:
                self.avgTtime = float(dataPoints[10])
        try:
            self.avgNtime = int(dataPoints[11])
        except ValueError:
            try:
                self.avgNtime = perseEpoNotation(dataPoints[11])
            except ValueError:
                self.avgNtime = float(dataPoints[11])
        try:
            self.avgStime = int(dataPoints[12])
        except ValueError:
            try:
                self.avgStime = perseEpoNotation(dataPoints[12])
            except ValueError:
                self.avgStime = float(dataPoints[12])
            
        self.t_times = dataPoints[13:18]
        self.n_times = dataPoints[18:23]
        self.s_times = dataPoints[23:28]
        self.t_Mem = dataPoints[28:33]
        self.n_Mem = dataPoints[33:38]
        self.s_Mem = dataPoints[38:43]
        
    def getListOfAvgTimes(self):
        return [self.avgTtime,self.avgNtime,self.avgStime]

    def parseAvgMemUsage(self):
        tsum = 0
        for line in self.t_Mem:
            if line.strip() != '':
                tsum += float(line)
        nsum = 0
        for line in self.n_Mem:
            if line.strip() != '':
                nsum += float(line)
        ssum = 0
        for line in self.s_Mem:
            if line.strip() != '':
                ssum += float(line)

        self.tavgM = tsum/len(self.t_Mem)
        self.navgM = nsum/len(self.n_Mem)
        self.savgM = ssum/len(self.s_Mem)

    def getMaxMemory(self):
        maxNum = 0
        for line in self.t_Mem:
            if line.strip() != '':
                tempNum = float(line)
                if tempNum > maxNum:
                    maxNum = tempNum
                    
        for line in self.n_Mem:
            if line.strip() != '':
                tempNum = float(line)
                if tempNum > maxNum:
                    maxNum = tempNum
        
        for line in self.s_Mem:
            if line.strip() != '':
                tempNum = float(line)
                if tempNum > maxNum:
                    maxNum = tempNum
        return maxNum
        
    def fixCutOffTimes(self):
        if self.avgTtime > self.cutOffTime:
            self.avgTtime = self.cutOffTime
        if self.avgNtime > self.cutOffTime:
            self.avgNtime = self.cutOffTime
        if self.avgStime > self.cutOffTime:
            self.avgStime = self.cutOffTime
            
    def sameExcept(self, compObj, dims=''):
        if self.transactions != compObj.transactions and 't' not in dims:
            return False
        if self.attributes != compObj.attributes and 'a' not in dims:
            return False
        if self.flexable != compObj.flexable and 'f' not in dims:
            return False
        if self.query != compObj.query and 'q' not in dims:
            return False
        if self.minsup != compObj.minsup and 'm' not in dims:
            return False
##        if self.qSup != compObj.qSup and 's' not in dims:
##            return False
        return True

    def getPrettyDatasetDimentions(self):
        return 'T' + str(self.transactions) + 'A' + str(self.attributes) + 'F' + str(self.flexable)
    
    def prettyStr(self, lines = 1, trans=False):
        tstr = ''
        astr = ''
        fstr = ''
        fpstr = ''
        qstr = self.query
        qsstr = ''
        mstr = ''
        transStr = ''
        if self.transactions != -1:
            tstr = 'T' + str(self.transactions)
        if self.attributes != -1:
            astr = 'A' + str(self.attributes)
        if self.flexable != -1:
            fstr = 'F' + str(self.flexable)
        if self.flexPrecentage != -1:
            fpstr = 'F%' + str(self.flexPrecentage)
        if self.qSup != -1:
            qsstr = 'Query support ' + str(self.qSup)
        if self.minsup != -1:
            mstr = 'minsup ' + str(self.minsup)
        if trans:
            if self.isTrans:
                transStr = ' Trans'
            else:
                transStr = ' Non-Trans'
        output = ''
        if lines == 1:
            output = qstr + qsstr + mstr + tstr + astr + fstr + fpstr + transStr
        elif lines == 2:
            output = qstr + mstr + '\n' + tstr + astr + fstr + fpstr + transStr
        elif lines == 3:
            output = qstr + '\n' + mstr + '\n' +tstr + astr + fstr + fpstr + transStr
        elif lines == 4:
            output = qstr + '\n' + mstr + '\n' +tstr + astr + fstr + fpstr + '\n' + qsstr + transStr
        return output.strip()

    def specificStringFormat(self, key, lines, trans=False):
        if key == 0:
            return self.prettyStr(lines, trans)
        if key == 1:
            return 'A' + str(self.attributes)
        if key == 2:
            return str(self.flexPrecentage*100) + '%'
        return ""
    
    def getFileStr(self):
        output = ''
        output += self.date.strftime("%m/%d/%Y, %H:%M:%S.%f") + ','
        output += str(self.transactions) + ','
        output += str(self.attributes) + ','
        output += str(self.flexable) + ','
        output += str(self.query) + ','
        output += str(self.isTrans).upper() + ','
        output += str(self.qSup) + ','
        output += str(self.minsup) + ','
        output += str(self.setsGen) + ','
        output += str(self.avgTtime) + ','
        output += str(self.avgNtime) + ','
        output += str(self.avgStime) + ','
        for x in self.t_times:
            output += x + ','
        for x in self.n_times:
            output += x + ','
        for x in self.s_times:
            output += x + ','
        for x in self.t_Mem:
            output += x + ','
        for x in self.n_Mem:
            output += x + ','
        for x in self.s_Mem:
            output += x.strip(' \t\n\r')
        output += '\n'
        return output
        
def perseEpoNotation(string):
    num = float(string[:string.index('E')])
    magnitude = 10**int(string[string.index('E')+1:])
    return num * magnitude

def parseFile(path, header=True):
    file = open(path,'r')
    lines = file.readlines()
    file.close()
    
    if header:
        lines.pop(0)

    runObjList = []
    for i in range(len(lines)):
        runObjList.append(ExperamentalRun(lines[i]))

    return runObjList



