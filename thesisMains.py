# the main functions to call all nessecary functions that create
#  graphs for the paper

import reduceAndAvg
import drawGraph
import classRunObj

import random
import os

# create a single comparison chart
# if no runindex spesified choose at random
#Hepatitis graphs from prospectus results
    # t 1038
    # af 7992
    # q 9699 rotation='vertical'
    # f 9128

# good lung cancer graph 9531
def chooseComparison(runObjList, dims, runindex=-1):
    if runindex == -1:
        runindex = random.randint(0,len(runObjList)-1)
        print(runindex)
    
    first = runObjList[runindex]
    compObjs = []
    for runObj in runObjList:
        if runObj.sameExcept(first,dims):
            compObjs.append(runObj)
            
    reduceAndAvg.sortRunObjList(compObjs, dims)
    return compObjs

def getStanderdAvg(runObjList,dim):
    transRunObjList, transDict = reduceAndAvg.avgByDim(runObjList,dim, True)
    nonTransRunObjList, nonTransDict = reduceAndAvg.avgByDim(runObjList,dim, False)

    reduceAndAvg.showGroupingAnalysis(transDict)
    reduceAndAvg.showGroupingAnalysis(nonTransDict)
    
    transRunObjList.extend(nonTransRunObjList)
    #capBarsAt(newRunObjList, 60000000000)
    reduceAndAvg.sortRunObjList(transRunObjList, dim)
    return transRunObjList

def avgAll(runObjList, title, showAARPP=True):
    baseObj = reduceAndAvg.avgRunObj(runObjList)
    drawGraph.barChartFor1(baseObj, title, showAARPP=showAARPP)

def avgTransistion(runObjList, showAARPP=True):
    avgRunObjList = getStanderdAvg('')
    drawGraph.barChartRunsGrouped(avgRunObjList, lableLineNums = 4, showAARPP=showAARPP, logscale=False, putTransInLabel=True)

def avgTransaction(runObjList, showAARPP=True):
    avgRunObjList = getStanderdAvg('t')
    drawGraph.barChartRunsGrouped(avgRunObjList, lableLineNums = 4, showAARPP=showAARPP, logscale=True, putTransInLabel=True)
    
def avgAtt(runObjList, showAARPP=True):
    avgRunObjList = getStanderdAvg('a')
    drawGraph.barChartRunsGrouped(avgRunObjList, lableLineNums = 4, showAARPP=showAARPP, logscale=True, putTransInLabel=True)

def avgFlexible(runObjList, showAARPP=True):
    avgRunObjList = getStanderdAvg('f')
    drawGraph.barChartRunsGrouped(avgRunObjList, lableLineNums = 4, showAARPP=showAARPP, logscale=True, putTransInLabel=True)

def avgQuery(runObjList, showAARPP=True):
    avgRunObjList = getStanderdAvg('q')
    drawGraph.barChartRunsGrouped(avgRunObjList, lableLineNums = 4, showAARPP=showAARPP, logscale=True, rotation='vertical')

def makeTransFairAvg(runObjList):
    groupingDict = reduceAndAvg.groupByDim(runObjList, '', True)
    groupingDictNon = reduceAndAvg.groupByDim(runObjList, '', False)
    groupingDict['trans'] = groupingDict.pop('')
    groupingDictNon['nonTrans'] = groupingDictNon.pop('')
    groupingDict.update(groupingDictNon)
    for key, group in groupingDict.items():
        print(len(group))
    fairGroupings = reduceAndAvg.makeGroupingFair(groupingDict, 'q')
    finalAvgRunObjlist = []
    for group in fairGroupings:
        print(len(group))
        finalAvgRunObjlist.append(reduceAndAvg.avgRunObj(group))
    for avgRun in finalAvgRunObjlist:
        print(avgRun.prettyStr())
    #reduceAndAvg.sortRunObjList(finalAvgRunObjlist, 'q')
    #drawGraph.barChartRunsGrouped(finalAvgRunObjlist)
    return fairGroupings, finalAvgRunObjlist

def makeQueryFairAvg(runObjList):
    # tMake a fair average grouping
    groupingDict = reduceAndAvg.groupByDim(runObjList, 'q', True)
    groupingDictNon = reduceAndAvg.groupByDim(runObjList, 'q', False)
    groupingDict.update(groupingDictNon)
    underKeys = []
    for key, group in groupingDict.items():
        print(len(group))
        if len(group) < 100:
            underKeys.append(key)
    for key in underKeys:
        del groupingDict[key]

    fairGroupings = reduceAndAvg.makeGroupingFair(groupingDict, 'qm')
    finalAvgRunObjlist = []
    for group in fairGroupings:
        print(len(group))
        finalAvgRunObjlist.append(reduceAndAvg.avgRunObj(group))
    for avgRun in finalAvgRunObjlist:
        print(avgRun.prettyStr())
    reduceAndAvg.sortRunObjList(finalAvgRunObjlist, 'q')
    #drawGraph.barChartRunsGrouped(finalAvgRunObjlist)
    return fairGroupings, finalAvgRunObjlist

def makeStanderdFairAvg(runObjList, groupingVar, fairVar, isTrans):
    # tMake a fair average grouping
    groupingDict = reduceAndAvg.groupByDim(runObjList, groupingVar, isTrans)
    for key, group in groupingDict.items():
        print(len(group))

    fairGroupings = reduceAndAvg.makeGroupingFair(groupingDict, fairVar)
    finalAvgRunObjlist = []
    for group in fairGroupings:
        print(len(group))
        finalAvgRunObjlist.append(reduceAndAvg.avgRunObj(group))
    for avgRun in finalAvgRunObjlist:
        print(avgRun.prettyStr())
    reduceAndAvg.sortRunObjList(finalAvgRunObjlist, groupingVar)
    #drawGraph.barChartRunsGrouped(finalAvgRunObjlist)
    return fairGroupings, finalAvgRunObjlist

def saveFigure(fairGroupings, groupAvgs, figNum, overwrite):
    figDir = "figure" + str(figNum)
    try:
        os.mkdir(figDir)
    except FileExistsError:
        print('dir already made')
        if not overwrite:
            return 

    header = "Date,Time,Transactions,Attributes,Flexable,query,is Trans,qSup,minsup,setsGen,"
    header += "avgTtime,avgNtime,avgStime,T_times,,,,,N_times,,,,,S_times,,,,,T_Mem,(megabytes),,,,N_Mem,,,,,S_Mem,,,,\n"

    for i in range(len(fairGroupings)):
        file = open(figDir + "/group" + str(i) + ".csv", "w+")
        file.write(header)
        for run in fairGroupings[i]:
            file.write(run.getFileStr())
        file.close()

    file = open(figDir + "/averages.csv", "w+")
    file.write(header)
    for i in range(len(groupAvgs)):
        file.write(groupAvgs[i].getFileStr())
    file.close()

def getRunObjsForFigure(figNum):
    figDir = "figure" + str(figNum)
    if not os.path.isdir(figDir):
        return
    return classRunObj.parseFile(figDir + "/averages.csv")

def showF1(save=False):
    figfilename = ''
    if save:
        figfilename = 'autoSavedFigs/figure1'
    title = 'Hepatitis Algorithm Execution Time Comparison'
    runObjList = classRunObj.parseFile("simpleData/hepatitisNoSup2.csv")
    baseObj = reduceAndAvg.avgRunObj(runObjList)
    drawGraph.timeUnit = "seconds"
    drawGraph.barChartFor1(baseObj, title, filename=figfilename, yTopLim=51)
    return baseObj

def showF1a(save=False):
    figfilename = ''
    if save:
        figfilename = 'autoSavedFigs/figure1a'
    title = 'Hepatitis Algorithm Memory Usage Comparison'
    runObjList = classRunObj.parseFile("simpleData/hepatitisNoSup2.csv")
    baseObj = reduceAndAvg.avgMemRunObj(runObjList)
    drawGraph.memBarChartFor1(baseObj, title, filename=figfilename, logscale=False,showAARPP=True)
    return baseObj

def showF2(make=False, save=False):
    figfilename = ''
    if save:
        figfilename = 'autoSavedFigs/figure2'
    if make:
        makeF2()
    title = 'Hepatitis Trans vs. Non-trans Query Comparison'
    runObjList = getRunObjsForFigure(2)
    drawGraph.timeUnit = "milliseconds"
    drawGraph.barChartRunsGrouped(runObjList, title, filename=figfilename, lableLineNums = 4, showAARPP=True, logscale=True, putTransInLabel=True, yBottomLim=10)
    return runObjList

def makeF2():
    runObjList = classRunObj.parseFile("simpleData/hepatitisNoSup2.csv")
    fairGroupings, finalAvgRunObjlist = makeTransFairAvg(runObjList)
    saveFigure(fairGroupings, finalAvgRunObjlist, 2, True)

def showF3(make=False, save=False):
    figfilename = ''
    if save:
        figfilename = 'autoSavedFigs/figure3'
    if make:
        makeF3()
    title = 'Hepatitis Number of Attributes Comparison'
    runObjList = getRunObjsForFigure(3)
    drawGraph.timeUnit = "nanoseconds"
    drawGraph.barChartRunsGrouped(runObjList, title, logscale=True, yBottomLim=100000, filename=figfilename)
    return runObjList

def makeF3():
    runObjList = classRunObj.parseFile("simpleData/hepatitisNoSup2.csv")
    fairGroupings, finalAvgRunObjlist = makeStanderdFairAvg(runObjList,'a','af',True)
    saveFigure(fairGroupings, finalAvgRunObjlist, 3, True)

def showF4(save=False):
    figfilename = ''
    if save:
        figfilename = 'autoSavedFigs/figure4'
    title = 'Hepatitis Number of Flexable Attributes Comparison'
    runObjList = classRunObj.parseFile("simpleData/hepatitisNoSup2.csv")
    fairGroupings, finalAvgRunObjlist = makeStanderdFairAvg(runObjList,'f','f',True)
    saveFigure(fairGroupings, finalAvgRunObjlist, 4, True)
    #runObjList = getRunObjsForFigure(4)
    drawGraph.timeUnit = "milliseconds"
    drawGraph.barChartRunsGrouped(finalAvgRunObjlist, title, filename=figfilename, logscale=True, yBottomLim=100, labelKey=2)
    return finalAvgRunObjlist

def showF5(make=False, save=False):
    figfilename = ''
    if save:
        figfilename = 'autoSavedFigs/figure5'
    if make:
        makeF5()
    title = 'Hepatitis Query Comparison'
    runObjList = getRunObjsForFigure(5)
    drawGraph.timeUnit = "microseconds"
    drawGraph.barChartRunsGrouped(runObjList, title, filename=figfilename, logscale=True, yBottomLim=10, rotation='vertical')
    return runObjList

def makeF5():
    runObjList = classRunObj.parseFile("simpleData/hepatitisNoSup2.csv")
    fairGroupings, finalAvgRunObjlist = makeQueryFairAvg(runObjList)
    saveFigure(fairGroupings, finalAvgRunObjlist, 5, True)

def showF5a(make=False, save=False):
    figfilename = ''
    if save:
        figfilename = 'autoSavedFigs/figure5a'
    if make:
        makeF5a()
    title = 'Hepatitis Number of Transactions Comparison'
    runObjList = getRunObjsForFigure('5a')
    drawGraph.timeUnit = "microseconds"
    drawGraph.barChartRunsGrouped(runObjList, title, filename=figfilename, lableLineNums=4 ,logscale=True, yBottomLim=10)
    return runObjList

def makeF5a():
    runObjList = classRunObj.parseFile("simpleData/hepatitisNoSup2.csv")
    fairGroupings, finalAvgRunObjlist = makeStanderdFairAvg(runObjList,'t','t',True)
    saveFigure(fairGroupings, finalAvgRunObjlist, '5a', True)

def showF6(save=False):
    figfilename = ''
    if save:
        figfilename = 'autoSavedFigs/figure6'
    title = 'Lung Cancer Algorithm Execution Time Comparison'
    runObjList = classRunObj.parseFile("simpleData/lungCancerNoSup2.csv")
    baseObj = reduceAndAvg.avgRunObj(runObjList)
    drawGraph.timeUnit = "seconds"
    drawGraph.barChartFor1(baseObj, title, filename=figfilename, logscale=False,showAARPP=False)
    return baseObj

def showF6a(save=False):
    figfilename = ''
    if save:
        figfilename = 'autoSavedFigs/figure6a'
    title = 'Lung Cancer Algorithm Memory Usage Comparison'
    runObjList = classRunObj.parseFile("simpleData/lungCancerNoSup2.csv")
    baseObj = reduceAndAvg.avgMemRunObj(runObjList)
    drawGraph.memBarChartFor1(baseObj, title, filename=figfilename, logscale=False,showAARPP=False)
    return baseObj

def showF7(make=False, save=False):
    figfilename = ''
    if save:
        figfilename = 'autoSavedFigs/figure7'
    if make:
        makeF7()
    title = 'Lung Cancer Trans vs. Non-trans Query Comparison'
    runObjList = getRunObjsForFigure(7)
    drawGraph.timeUnit = "milliseconds"
    drawGraph.barChartRunsGrouped(runObjList, title, filename=figfilename, lableLineNums = 4, showAARPP=False,
                                  logscale=True, putTransInLabel=True, yBottomLim=10, yTopLim=8000000)
    return runObjList

def makeF7():
    runObjList = classRunObj.parseFile("simpleData/lungCancerNoSup2NoCutOff.csv")
    fairGroupings, finalAvgRunObjlist = makeTransFairAvg(runObjList)
    saveFigure(fairGroupings, finalAvgRunObjlist, 7, True)

def showF8(make=False, save=False):
    figfilename = ''
    if save:
        figfilename = 'autoSavedFigs/figure8'
    if make:
        makeF8()
    title = 'Lung Cancer Number of Attributes Comparison'
    runObjList = getRunObjsForFigure(8)
    drawGraph.timeUnit = "nanoseconds"
    drawGraph.barChartRunsGrouped(runObjList, title, filename=figfilename, showAARPP=False, logscale=True, yBottomLim=100000, labelKey=1)
    return runObjList

def makeF8():
    runObjList = classRunObj.parseFile("simpleData/lungCancerNoSup2.csv")# hepatitisNoSup2  lungCancer
    fairGroupings, finalAvgRunObjlist = makeStanderdFairAvg(runObjList,'a','af',True)
    saveFigure(fairGroupings, finalAvgRunObjlist, 8, True)

def showF9(save=False):
    figfilename = ''
    if save:
        figfilename = 'autoSavedFigs/figure9'
    title = 'Lung Cancer Number of Flexable Attributes Comparison'
    runObjList = classRunObj.parseFile("simpleData/lungCancerNoSup2.csv")
    fairGroupings, finalAvgRunObjlist = makeStanderdFairAvg(runObjList,'f','f',True)
    saveFigure(fairGroupings, finalAvgRunObjlist, 9, True)
    #runObjList = getRunObjsForFigure(4)
    drawGraph.timeUnit = "milliseconds"
    drawGraph.barChartRunsGrouped(finalAvgRunObjlist, title, filename=figfilename, showAARPP=False, logscale=True, yBottomLim=100, yTopLim=8000000, labelKey=2)
    return finalAvgRunObjlist

def showF10(make=False, save=False):
    figfilename = ''
    if save:
        figfilename = 'autoSavedFigs/figure10'
    if make:
        makeF10()
    title = 'Lung Cancer Query Comparison'
    runObjList = getRunObjsForFigure(10)
    drawGraph.timeUnit = "milliseconds"
    drawGraph.barChartRunsGrouped(runObjList, title, filename=figfilename, showAARPP=False, logscale=True, yBottomLim=10, yTopLim=30000000, rotation='vertical')
    return runObjList

def makeF10():
    runObjList = classRunObj.parseFile("simpleData/lungCancerNoSup2.csv")
    fairGroupings, finalAvgRunObjlist = makeQueryFairAvg(runObjList)
    saveFigure(fairGroupings, finalAvgRunObjlist, 10, True)

def showF10a(make=False, save=False):
    figfilename = ''
    if save:
        figfilename = 'autoSavedFigs/figure10a'
    if make:
        makeF10a()
    title = 'Lung Cancer Number of Transactions Comparison'
    runObjList = getRunObjsForFigure('10a')
    drawGraph.timeUnit = "microseconds"
    drawGraph.barChartRunsGrouped(runObjList, title, filename=figfilename, lableLineNums=4 ,logscale=True, yBottomLim=10)
    return runObjList

def makeF10a():
    runObjList = classRunObj.parseFile("simpleData/lungCancerNoSup2.csv")
    fairGroupings, finalAvgRunObjlist = makeStanderdFairAvg(runObjList,'t','t',True)
    saveFigure(fairGroupings, finalAvgRunObjlist, '10a', True)

#Hepatitis graphs from prospectus results
    # t 1038
    # af 7992
    # q 9699 rotation='vertical'
    # f 9128

# good lung cancer graph 9531
def showF11(save=False):
    figfilename = ''
    if save:
        figfilename = 'autoSavedFigs/figure11'
    title = 'Hepatitis Number of Transactions Comparison'
    runObjList = classRunObj.parseFile("simpleData/hepatitis.csv")
    runObjList = chooseComparison(runObjList, 't', 1038)
    drawGraph.timeUnit = "microseconds"
    drawGraph.barChartRunsGrouped(runObjList, title, filename=figfilename, lableLineNums = 4, logscale=True, yBottomLim=10)
    return runObjList

def showF12(save=False):
    figfilename = ''
    if save:
        figfilename = 'autoSavedFigs/figure12'
    title = 'Lung Cancer Number of Transactions Comparison'
    runObjList = classRunObj.parseFile("simpleData/lungCancer.csv")
    runChoosen = []
    runChoosen = chooseComparison(runObjList, 't', 128) # 1974 # 25 # 29 # 128 # 3145
    drawGraph.timeUnit = "microseconds"
    drawGraph.barChartRunsGrouped(runChoosen, title, filename=figfilename, lableLineNums = 4, showAARPP=False, logscale=True, yBottomLim=10)
    return runChoosen

def showF13(save=False):
    figfilename = ''
    if save:
        figfilename = 'autoSavedFigs/figure13'
    title = 'Hepatitis Query Trans Attribute Comparison'
    runObjList = classRunObj.parseFile("simpleData/hepatitis.csv")
    runChoosen = []
    runChoosen = chooseComparison(runObjList, 'a', 6832)
    runChoosen.extend(chooseComparison(runObjList, 'a', 6828))
##    while len(runChoosen) != 4:
##        runChoosen = chooseComparison(runObjList, 'a')
##        print(len(runChoosen))
    drawGraph.timeUnit = "microseconds"
    drawGraph.barChartRunsGrouped(runChoosen, title, filename=figfilename, lableLineNums = 4, logscale=True, yBottomLim=10)
    return runChoosen

def showF14(save=False):
    figfilename = ''
    if save:
        figfilename = 'autoSavedFigs/figure13'
    title = 'Lung cancer Query Trans Attribute Comparison'
    runObjList = classRunObj.parseFile("simpleData/lungCancer.csv")
    runChoosen = []
    #runChoosen = chooseComparison(runObjList, 'a', 6832)
    #runChoosen.extend(chooseComparison(runObjList, 'a', 6828))
    while len(runChoosen) != 5:
        runChoosen = chooseComparison(runObjList, 'a', 805)
        print(len(runChoosen))
    drawGraph.timeUnit = "microseconds"
    drawGraph.barChartRunsGrouped(runChoosen, title, filename=figfilename, lableLineNums = 4, logscale=True)#, yBottomLim=10)
    return runChoosen

def showF15(save=False):
    figfilename = ''
    if save:
        figfilename = 'autoSavedFigs/figure15'
    title = 'Hepatitis Algorithm Memory Usage Comparison'
    runObjList = classRunObj.parseFile("simpleData/hepatitisNoSup2.csv")
    
    drawGraph.plotAllMemUsage(runObjList)

def showF16(save=False):
    figfilename = ''
    if save:
        figfilename = 'autoSavedFigs/figure16'
    title = 'Lung Cancer Algorithm Memory Usage Comparison'
    runObjList = classRunObj.parseFile("simpleData/lungCancerNoSup2.csv")
    
    drawGraph.plotAllMemUsage(runObjList)

def showF17(save=False):
    figfilename = ''
    if save:
        figfilename = 'autoSavedFigs/figure17'

    title = 'Maximum memory usage for hepatits vs lung cancer'
    runObjListHep = classRunObj.parseFile("simpleData/hepatitis.csv")
    runObjListLung = classRunObj.parseFile("simpleData/lungCancer.csv") #NoSup2
    drawGraph.plotAbsoluteMax(runObjListHep,runObjListLung, title, filename=figfilename)

def reMakeLungCacer():
    showF6(save=True)
    showF6a(save=True)
    showF7(save=True, make=True)
    showF8(save=True, make=True)
    showF9(save=True)
    showF10(save=True, make=True)
    showF10a(save=True, make=True)
    showF12(save=True)

def autoSaveAll():
    showF1(save=True)
    showF1a(save=True)
    showF2(save=True)
    showF3(save=True)
    showF4(save=True)
    showF5(save=True)
    showF5a(save=True)
    showF6(save=True)
    showF6a(save=True)
    showF7(save=True)
    showF8(save=True)
    showF9(save=True)
    showF10(save=True)
    showF11(save=True)
    showF12(save=True)
    

# make a graph
# make sure that the 3 hour cap is being used correctly in averages

#  hepatitis  lungCancer   hepatitisNoSup2
#runObjList = classRunObj.parseFile("simpleData/hepatitisNoSup2.csv")
runObjList = classRunObj.parseFile("../../oldflareResultsOld.csv")
drawGraph.timeUnit = "seconds"
avgAll(runObjList, "test avg")

#autoSaveAll()
#reMakeLungCacer()
#showF17()#make=True) #

#makeF10()
#showF6a(save=True)

##runs = showF2(save=True)
##if isinstance(runs, (list,)):
##    for run in runs:
##        print(run.avgTtime, run.avgNtime, run.avgStime, sep='\t')
##        print(run.tavgM, run.navgM, run.savgM, sep='\t')
##else:
##    print(runs.avgTtime, runs.avgNtime, runs.avgStime, sep='\t')
##    print(runs.tavgM, runs.navgM, runs.savgM, sep='\t')




# tMake a fair average grouping
#fairGroupings, finalAvgRunObjlist = makeStanderdFairAvg('t','t',True)
#saveFigure(fairGroupings, finalAvgRunObjlist, 1, True)


# group all the results by the support of the query
# and show the length of each new group
##grouping = reduceAndAvg.groupByDim(runObjList, reduceAndAvg.Dim.QUERYSUP.value, True)
##
##things = [[key,val] for key, val in grouping.items()]
##things = sorted(things, key=lambda x: x[0], reverse=False)
##for t in things:
##    print('Query support',t[0], 'len=', len(t[1]))

# Make a graph 
#  seconds,  milliseconds,  microseconds, nanoseconds
##drawGraph.timeUnit = "seconds"
##avgTransistion(runObjList, showAARPP=False)


'''
compObjs = chooseRandComparison(runObjList,'q',9699)
capBarsAt(compObjs, (1.08*(10**13)))
#compObjs = aAndFEqual(compObjs)
barChartRunsGrouped(compObjs, logscale=True,rotation='vertical')
'''
