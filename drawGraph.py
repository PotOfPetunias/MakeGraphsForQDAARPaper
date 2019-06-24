# use matplotlib to create the actual bar graphs

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

barColors8 = ['#003f5c', '#2f4b7c', '#665191', '#a05195', '#d45087', '#f95d6a', '#ff7c43', '#ffa600']
barColors5 = ['#003f5c', '#58508d', '#bc5090','#ff6361','#ffa600']
barColors3 = ['#003f5c', '#bc5090', '#ffa600']
barColors2 = ['#003f5c', '#ffa600']

conversionDict = {"seconds":1000000000, "milliseconds":1000000, "microseconds":1000, "nanoseconds":1}

timeUnit = "nanoseconds"

def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2., height,
                 str(round(height,2)),
                 ha='center', va='bottom')

def barChartFor1(runObj, title, filename='', logscale=False, showAARPP=True,  yTopLim=0):
    global barColors3
    global timeUnit
    global conversionDict
    objects = ['QDAAR', 'IAMPoM']#, 'AARPP')
    if showAARPP:
        objects.append('IAMPoMwFPT')
    fig, ax = plt.subplots()
    y_pos = np.arange(len(objects))
    performance = [runObj.avgTtime/conversionDict[timeUnit],
                   runObj.avgNtime/conversionDict[timeUnit]]
    if showAARPP:
        performance.append(runObj.avgStime/conversionDict[timeUnit])
     
    rects = plt.bar(y_pos, performance, align='center', color=barColors3, log=logscale)
    plt.xticks(y_pos, objects)
    plt.ylabel('Execution Time ('+ timeUnit +')')
    plt.title(title)

    if yTopLim != 0:
        ax.set_ylim(top=yTopLim)
    #plt.subplots_adjust(left=0,wspace=0.2)
    
    autolabel(rects)

    if filename == '':
        plt.show()
    else:
        plt.savefig(filename+".pdf", bbox_inches='tight')
        plt.savefig(filename+".jpg", bbox_inches='tight')

def memBarChartFor1(runObj, title, filename='', logscale=False, showAARPP=True):
    global barColors3
    global conversionDict
    objects = ['QDAAR', 'IAMPoM']#, 'AARPP')
    if showAARPP:
        objects.append('IAMPoMwFPT')
    y_pos = np.arange(len(objects))
    performance = [runObj.tavgM,
                   runObj.navgM]
    if showAARPP:
        performance.append(runObj.savgM)
    rects = plt.bar(y_pos, performance, align='center', color=barColors3, log=logscale)
    plt.xticks(y_pos, objects)
    plt.ylabel('Memory usage (megabytes)')
    plt.title(title)

    autolabel(rects)
    
    if filename == '':
        plt.show()
    else:
        plt.savefig(filename+".pdf", bbox_inches='tight')
        plt.savefig(filename+".jpg", bbox_inches='tight')

def barChartRunsGrouped(runObjList, title, filename='', lableLineNums = 3, showAARPP=True, logscale=False,
                        rotation='horizontal', putTransInLabel=False, yBottomLim=0, yTopLim=0, labelKey=0):
    global timeUnit
    global conversionDict
    if len(runObjList) < 1:
        print('given empty list')
        return 
    global barColors3
    # data to plot
    n_groups = len(runObjList)# one for each run

    groupList = []
    if showAARPP:
        groupList = [[] for i in range(3)]
    else:
        groupList = [[] for i in range(2)]
    for runObj in runObjList:
        groupList[0].append(runObj.avgTtime)
        groupList[1].append(runObj.avgNtime)
        if showAARPP:
            groupList[2].append(runObj.avgStime)
     
    # create plot
    fig, ax = plt.subplots()
    spaceBetweenGroups = 2
    index = np.arange(0,n_groups*spaceBetweenGroups,spaceBetweenGroups)
    bar_width = 0.35
    opacity = 1

    barPltList = []
    lableList = ['QDAAR', 'IAMPoM']
    if showAARPP:
        lableList.append('IAMPoMwFPT')
    
    for i in range(len(groupList)):
        barPltList.append(plt.bar(index + (bar_width*i),
                          [t/conversionDict[timeUnit] for t in groupList[i]],
                          bar_width,
                          alpha=opacity,
                          color=barColors3[i],
                          label=lableList[i],
                          log=logscale))
     
    plt.xlabel('Run')
    plt.ylabel('Execution Time ('+ timeUnit +')')
    plt.title(title)
    plt.xticks(index + bar_width, [runObj.specificStringFormat(key=labelKey, lines=lableLineNums, trans=putTransInLabel) for runObj in runObjList], rotation=rotation)
    plt.legend()

    if yBottomLim != 0 and yTopLim != 0:
        ax.set_ylim(bottom=yBottomLim, top=yTopLim)
    elif yBottomLim != 0:
        ax.set_ylim(bottom=yBottomLim)
    
    plt.tight_layout()
    if filename == '':
        plt.show()
    else:
        fig.savefig(filename+".pdf", bbox_inches='tight')
        fig.savefig(filename+".jpg", bbox_inches='tight')


def plotAllMemUsage(runObjList):
    maxMems = []
    runObjSubset = runObjList#[:1000]
    print(len(runObjSubset), len(runObjList ))
    for runObj in runObjSubset:
        for string in runObj.t_Mem:
            try:
                maxMems.append(float(string))
            except ValueError:
                maxMems.append(0)
    ticks = np.arange(0,len(maxMems),1)

    fig, ax = plt.subplots()
    ax.plot(ticks, maxMems)

    ax.set(xLabel = 'experament', ylabel = 'max memory usage (megabytes)', title = 'Max Memory usage')
    ax.grid()
    plt.show()

def plotAbsoluteMax(runObjListHep,runObjListLung, title, filename=''):
    global barColors2
    global conversionDict
    objects = ['Hepatitis', 'Lung Cancer']
    
    y_pos = np.arange(len(objects))
    maxHep = runObjListHep[0].getMaxMemory()
    maxLung = runObjListLung[0].getMaxMemory()
    for runObj in runObjListLung:
        tempNum = runObj.getMaxMemory()
        if tempNum > maxLung:
            maxLung = tempNum
    for runObj in runObjListHep:
        tempNum = runObj.getMaxMemory()
        if tempNum > maxHep:
            maxHep = tempNum
    
    performance = [maxHep/1000,
                   maxLung/1000]
    print('Hep:',maxHep,'Lung:',maxLung)

    
    rects = plt.bar(y_pos, performance, align='center', color=barColors2)
    autolabel(rects)
    plt.xticks(y_pos, objects)
    plt.ylabel('Maximum memory usage (gigabyte)')
    plt.title(title)
    
    if filename == '':
        plt.show()
    else:
        plt.savefig(filename+".pdf", bbox_inches='tight')
        plt.savefig(filename+".jpg", bbox_inches='tight')

##def barChartAlgsGrouped(runObjList, title, filename='', logscale=False):
##    global timeUnit
##    global conversionDict
##    if len(runObjList) < 1:
##        print('given empty list')
##        return
##    global barColors5
##    # data to plot
##    n_groups = 3 # one for each algorithm
##
##    groupList = [runObj.getListOfAvgTimes() for runObj in runObjList]
##     
##    # create plot
##    fig, ax = plt.subplots()
##    spaceBetweenGroups = len(runObjList)/2
##    index = np.arange(0,n_groups*spaceBetweenGroups,spaceBetweenGroups)
##    bar_width = 0.35
##    opacity = 1
##
##    barPltList = []
##    
##    for i in range(len(groupList)):
##        barPltList.append(plt.bar(index + (bar_width*i),
##                          [t/conversionDict[timeUnit] for t in groupList[i]],
##                          bar_width, alpha=opacity,
##                          color=barColors5[i],
##                          label=runObjList[i].prettyStr(),
##                          log=logscale))
##     
##    plt.xlabel('Algorithm')
##    plt.ylabel('Execution Time ('+ timeUnit +')')
##    plt.title(title)
##    plt.xticks(index + bar_width, ('QDAAR', 'IAMPoM', 'AARPP'))
##    plt.legend()
##     
##    plt.tight_layout()
##    if filename == '':
##        plt.show()
##    else:
##        fig.savefig(filename+".pdf", bbox_inches='tight')
##        fig.savefig(filename+".jpg", bbox_inches='tight')
