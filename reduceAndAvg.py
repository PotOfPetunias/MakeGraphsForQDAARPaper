# make graphs automatically for my convenience and fun

import copy
from enum import Enum
import datetime

class Dim(Enum):
    TRANSACTION = 't'
    ATTRIBUTE = 'a'
    FLEXABLE = 'f'
    QUERY = 'q'
    MINSUP = 'm'
    DATASET = 'd'
    QUERYSUP = 's'

def sortRunObjList(runObjList, dim, reverse=True):
    for letter in reversed(dim):
        if Dim.TRANSACTION.value in letter:
            runObjList.sort(key=lambda x: x.transactions, reverse=reverse)
        elif Dim.ATTRIBUTE.value in letter:
            runObjList.sort(key=lambda x: x.attributes, reverse=reverse)
        elif Dim.FLEXABLE.value in letter:
            runObjList.sort(key=lambda x: x.flexPrecentage, reverse=reverse)
        elif Dim.QUERY.value in letter:
            runObjList.sort(key=lambda x: x.query, reverse= not reverse)
        elif Dim.MINSUP.value in letter:
            runObjList.sort(key=lambda x: x.minsup, reverse= not reverse)
        elif Dim.QUERYSUP.value in letter:
            runObjList.sort(key=lambda x: x.qSup, reverse=reverse)

def aAndFEqual(runObjList):
    newList = []
    for runObj in runObjList:
        if runObj.attributes == runObj.flexable:
            newList.append(runObj)
    return newList

def capBarsAt(runObjList, maxnum):
    for runObj in runObjList:
        if runObj.avgTtime > maxnum:
            runObj.avgTtime = maxnum
        if runObj.avgNtime > maxnum:
            runObj.avgNtime = maxnum
        if runObj.avgStime > maxnum:
            runObj.avgStime = maxnum

# overwrites base obj attributes so that only the
# attributes that match with the run obj remain
def makeIntersectObj(baseObj, runObj):
    if baseObj.query != runObj.query:
        baseObj.query = ''
    if baseObj.isTrans != runObj.isTrans:
        baseObj.isTrans = False
    if baseObj.minsup != runObj.minsup:
        baseObj.minsup = -1
    if baseObj.transactions != runObj.transactions:
        baseObj.transactions = -1
    if baseObj.attributes != runObj.attributes:
        baseObj.attributes = -1
    if baseObj.flexable != runObj.flexable:
        baseObj.flexable = -1
    if baseObj.flexPrecentage != runObj.flexPrecentage:
        baseObj.flexPrecentage = -1
    if baseObj.qSup != runObj.qSup:
        baseObj.qSup = -1
    baseObj.date = datetime.datetime.now()
    baseObj.setsGen = -1
    for i in range(len(baseObj.t_times)):
        baseObj.t_times[i] = ''
    for i in range(len(baseObj.n_times)):
        baseObj.n_times[i] = ''
    for i in range(len(baseObj.s_times)):
        baseObj.s_times[i] = ''
    for i in range(len(baseObj.t_Mem)):
        baseObj.t_Mem[i] = ''
    for i in range(len(baseObj.n_Mem)):
        baseObj.n_Mem[i] = ''
    for i in range(len(baseObj.s_Mem)):
        baseObj.s_Mem[i] = ''

def avgRunObj(runObjList):
    if len(runObjList) <= 0:
        return
    if len(runObjList) == 1:
        return runObjList[0]
    
    avgTimeT = []
    avgTimeN = []
    avgTimeS = []
    baseObj = copy.deepcopy(runObjList[0])
    for runObj in runObjList:
        makeIntersectObj(baseObj,runObj)
        if runObj.avgTtime > 0:
            avgTimeT.append(runObj.avgTtime)
        if runObj.avgNtime > 0:
            avgTimeN.append(runObj.avgNtime)
        if runObj.avgStime > 0:
            avgTimeS.append(runObj.avgStime)

    try:
        baseObj.avgTtime = (sum(avgTimeT)/len(avgTimeT))
    except ZeroDivisionError:
        baseObj.avgTtime = 0
    try:
        baseObj.avgNtime = (sum(avgTimeN)/len(avgTimeN))
    except ZeroDivisionError:
        baseObj.avgNtime = 0
    try:
        baseObj.avgStime = (sum(avgTimeS)/len(avgTimeS))
    except ZeroDivisionError:
        baseObj.avgStime = 0

    return baseObj

def avgMemRunObj(runObjList, doAARPP=True):
    if len(runObjList) <= 0:
        return
    if len(runObjList) == 1:
        return runObjList[0]
    
    avgMemT = []
    avgMemN = []
    avgMemS = []
    baseObj = copy.deepcopy(runObjList[0])
    for runObj in runObjList:
        runObj.parseAvgMemUsage()
        makeIntersectObj(baseObj,runObj)
        if doAARPP:
            if runObj.tavgM > 0 and runObj.navgM > 0 and runObj.savgM > 0:
                avgMemT.append(runObj.tavgM)
                avgMemN.append(runObj.navgM)
                avgMemS.append(runObj.savgM)
        else:
            if runObj.tavgM > 0 and runObj.navgM > 0:
                avgMemT.append(runObj.tavgM)
                avgMemN.append(runObj.navgM)
                avgMemS.append(runObj.savgM)
    try:
        baseObj.tavgM = (sum(avgMemT)/len(avgMemT))
    except ZeroDivisionError:
        baseObj.tavgM = 0
    try:
        baseObj.navgM = (sum(avgMemN)/len(avgMemN))
    except ZeroDivisionError:
        baseObj.navgM = 0
    try:
        baseObj.savgM = (sum(avgMemS)/len(avgMemS))
    except ZeroDivisionError:
        baseObj.savgM = 0

    return baseObj

def groupByDim(runObjList, dim, trans):
    avgGroupingDict = {}
    for runObj in runObjList:
        # determine the attributes to be used as the key for grouping
        keyAtt = ''
        if Dim.TRANSACTION.value in dim:
            keyAtt = runObj.transactions
        elif Dim.ATTRIBUTE.value in dim:
            keyAtt = runObj.attributes
        elif Dim.FLEXABLE.value in dim:
            keyAtt = runObj.flexPrecentage
        elif Dim.QUERY.value in dim:
            keyAtt = runObj.query
        elif Dim.DATASET.value in dim:
            keyAtt = runObj.getPrettyDatasetDimentions()
        elif Dim.QUERYSUP.value in dim:
            keyAtt = runObj.qSup
            
        # preform the group by that attribute
        if runObj.isTrans == trans: # go in when we get the answer that was given in the parameters 
            if keyAtt in avgGroupingDict:
                avgGroupingDict[keyAtt].append(runObj)
            else:
                avgGroupingDict[keyAtt] = []
                avgGroupingDict[keyAtt].append(runObj)
    return avgGroupingDict

# remove all the extranious experaments hopefully
# dim must be equal to the dim used to make grouping
# may completely empty the grouping object
def makeGroupingFair(groupingDict, dim):
    groupingList = []
    for key, runObjListByKey in groupingDict.items():
        groupingList.append(runObjListByKey)

    for index in range(len(groupingList)):
        shortestIndex = 0
        shortestLen = len(groupingList[0])
        # find the shortest of the groups
        for i in range(len(groupingList)):
            if len(groupingList[i]) < shortestLen:
                shortestLen = len(groupingList[i])
                shortestIndex = i
        print('Progress',index,'/',len(groupingList))
        # keep only matching runs
        fairGroupList = []
        for runObjGroup in groupingList:
            fairGroup = []
            for minRunObj in groupingList[shortestIndex]:
                for runObj in runObjGroup:
                    if minRunObj.sameExcept(runObj,dim):
                        fairGroup.append(runObj)
                        break
            fairGroupList.append(fairGroup)
        groupingList = fairGroupList
        print('Progress',index+1,'/',len(groupingList))

    return groupingList
    

# give no dim: simply keep only trans/nontrans
def avgByDim(runObjList, dim, trans):
    avgGroupingDict = groupByDim(runObjList, dim, trans)
    newRunObjList = []

    for key, runObjListByKey in avgGroupingDict.items():
        newRunObjList.append(avgRunObj(runObjListByKey))

    return newRunObjList, avgGroupingDict

def showGroupingAnalysis(groupDict):
    for key, runObjListByKey in groupDict.items():
        print(key, len(runObjListByKey))
