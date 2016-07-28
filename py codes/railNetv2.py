# -*- coding: utf-8 -*-
"""
Created on Wed May 11 13:21:21 2016

@author: nhuynh
"""
from enum import Enum;
import utilities;
import mmRef;
import TrainLine;

defPaxFlowsPath = '../user inputs/defaultPaxFlowAtStns/';

trainLines = [];
stnTimetables = {};
stnDefPaxFlows = {};


def getPrevStop(crnStopName,crnArrTime):
    prevStop = (None,-1);
    for trainLine in trainLines:
        if crnStopName in trainLine.stopNames:
            stopIndexOnThisLine = trainLine.stopNames.index(crnStopName);
            if crnArrTime in trainLine.timetable[stopIndexOnThisLine]:
                if stopIndexOnThisLine==0: # if this is the first stop of the line
                    prevStop = ('',-1);
                    break;
                else:
                    trainIndex = trainLine.timetable[stopIndexOnThisLine].index(crnArrTime);
                    prevStop = (trainLine.stopNames[stopIndexOnThisLine-1],\
                                trainLine.timetable[stopIndexOnThisLine-1][trainIndex]);
                    break;
    return prevStop;


def readDefPaxFlows(filename):
    rawContent = utilities.readInCSVFile(filename);
    initValuesByOD = {};
    for iRow in range(1,len(rawContent)):
        crnRow = rawContent[iRow];

        fromTimeInSecs = utilities.convertTimeFormatToSecs(crnRow[0]);
        toTimeInSecs = utilities.convertTimeFormatToSecs(crnRow[1]);
        timeWindow = (fromTimeInSecs, toTimeInSecs);
        paxFlowInfoThisWindow = {};
        if (timeWindow in initValuesByOD):
            paxFlowInfoThisWindow = initValuesByOD.get(timeWindow);
        
        odPair = (crnRow[2], crnRow[3]);
        newValue = [float(crnRow[4]), crnRow[5]];
        paxValues = [];
        if odPair in paxFlowInfoThisWindow:
            paxValues = paxFlowInfoThisWindow.get(odPair);
        paxValues.append(newValue);
        paxFlowInfoThisWindow[odPair] = paxValues;
        
        initValuesByOD[timeWindow] = paxFlowInfoThisWindow;
        
    return initValuesByOD;


def prepareDefaultPaxFlows():
    global stnDefPaxFlows;
    for stn,value in StationPlatforms.__members__.items():
        stnDefPaxFlows[stn] = readDefPaxFlows(defPaxFlowsPath + stn + '.csv');
    

def prepareStnTimetables():
    global stnTimetables;
    for stn,value in StationPlatforms.__members__.items():
        stnTimetables[stn] = [];
        stopsThisStn = value.value;
        # searches through the timetable of all lines for trains that arrive at
        # this stop and if this stop is used/passed by multiple lines, 
        # aggregates the arrival time from each line into a 1 dimentional 
        # array. This array of arrival time will have to be sorted by 
        # chronological order.
        for stop in stopsThisStn:
            arrTimeAtThisStop = [];
            for trainLine in trainLines:
                if stop in trainLine.stopNames:
                    stopIndexOnThisLine = trainLine.stopNames.index(stop);
                    newArrTimeAtThisStop = trainLine.timetable[stopIndexOnThisLine];
                    arrTimeAtThisStop = arrTimeAtThisStop + newArrTimeAtThisStop;
            arrTimeAtThisStop.sort();
            stnTimetables[stn].append(arrTimeAtThisStop);
            

def prepareTrainLine():
    global trainLines;
    trainLines.append(TrainLine.TrainLine('line1'));
    trainLines.append(TrainLine.TrainLine('line2'));
    trainLines.append(TrainLine.TrainLine('line3'));
    trainLines.append(TrainLine.TrainLine('line4'));


def getTrainService(fullStopName,startTimeInSecs):
    for trainLine in trainLines:
        for trainService in trainLine.trainServices:
            if (fullStopName in trainService.line.stopNames):
                iStop = trainService.line.stopNames.index(fullStopName);
                if (trainService.timetable[iStop]==startTimeInSecs):
                    return trainService;
    return None;

'''
def getTrainService(fullStopName,startTimeInSecs):
    for iTrainLine in range(0,len(trainLines)):
        for iTrainService in range(0,len(trainLines[iTrainLine].trainServices)):
            if (fullStopName in trainLines[iTrainLine].trainServices[iTrainService].line.stopNames):
                iStop = trainLines[iTrainLine].trainServices[iTrainService].line.stopNames.index(fullStopName);
                if (trainLines[iTrainLine].trainServices[iTrainService].timetable[iStop]==startTimeInSecs):
                    return [iTrainLine,iTrainService];
    return [-1,-1];
'''

def getTrainLineFromArrivalDetails(stopName,arrivalTime):
    '''
    searchs in trainLines for a line that has a train arriving at stopName at 
    arrivalTime
    '''
    for line in trainLines:
        if stopName in line.stopNames:
            thisStopIndex = line.stopNames.index(stopName);
            timetblThisStop = line.timetable[thisStopIndex];
            if arrivalTime in timetblThisStop:
                return line;
    return None;


def getTrainLineFromFirstStop(stopName,arrivalTime):
    '''
    returns the train line that has stopName as first stop and 
    trains arriving at this stop at arrivalTime
    '''
    for line in trainLines:
        if stopName==line.stopNames[0]:
            timetblThisStop = line.timetable[0];
            if arrivalTime in timetblThisStop:
                return line;
    return None;


def getInitPaxOnTrainLine(trainLine,arrivalTime):
    '''
    returns the initial passengers of each profile on trainLine 
    corresponding to arrivalTime.
    '''
    initSlimOnBoard = 0;
    initDefaultOnBoard = 0;
    initFatOnBoard = 0;
    
    if trainLine==None:
        return [initSlimOnBoard, initDefaultOnBoard, initFatOnBoard];
    
    initPaxThisLine = trainLine.initPaxOnLine;
    for timeWindow,initPaxInfo in initPaxThisLine.items():
        if arrivalTime<=timeWindow[1] and arrivalTime>=timeWindow[0]:
            for paxInfo in initPaxInfo:
                if paxInfo[1]==mmRef.Profiles.DefaultProfile.name:
                    initDefaultOnBoard = paxInfo[0];
                elif paxInfo[1]==mmRef.Profiles.fatSlowLazy.name:
                    initFatOnBoard = paxInfo[0];
                elif paxInfo[1]==mmRef.Profiles.slimFastActiv.name:
                    initSlimOnBoard = paxInfo[0];
            return [initSlimOnBoard, initDefaultOnBoard, initFatOnBoard];
    
    return [initSlimOnBoard, initDefaultOnBoard, initFatOnBoard];


def getPercentPaxRemainOnBoard(trainLine,stopName,arrivalTime):
    percentSlimRemOnBoard = 0;
    percentDefaultRemOnBoard = 0;
    percentFatRemOnBoard = 0;
    
    if trainLine==None:
        return [percentSlimRemOnBoard, percentDefaultRemOnBoard, percentFatRemOnBoard];
    
    percentOnBoardData = trainLine.percentRemainOnBoard[stopName];
    for timeWindow,percentPax in percentOnBoardData.items():
        if arrivalTime<=timeWindow[1] and arrivalTime>=timeWindow[0]:
            for row in percentPax:
                if row[1]==mmRef.Profiles.DefaultProfile.name:
                    percentDefaultRemOnBoard = row[0];
                elif row[1]==mmRef.Profiles.fatSlowLazy.name:
                    percentFatRemOnBoard = row[0];
                elif row[1]==mmRef.Profiles.slimFastActiv.name:
                    percentSlimRemOnBoard = row[0];
            return [percentSlimRemOnBoard, percentDefaultRemOnBoard, percentFatRemOnBoard];
    
    return [percentSlimRemOnBoard, percentDefaultRemOnBoard, percentFatRemOnBoard];
    

class StationPlatforms(Enum):
    S1 = ['P1S1', 'P2S1'];
    S2 = ['P1S2', 'P2S2', 'P3S2', 'P4S2'];
    S3 = ['P1S3', 'P2S3'];
    S4 = ['P1S4', 'P2S4'];
    S5 = ['P1S5', 'P2S5'];
    
    def getStopIndex(stnName,stopName):
        for stn,value in StationPlatforms.__members__.items():
            if stn==stnName:
                return value.value.index(stopName);
    
    def getStopsByStn(stnName):
        for stn,value in StationPlatforms.__members__.items():
            if stn==stnName:
                return value.value;

    def getStationNameByStopName(stopName):
        for stn,value in StationPlatforms.__members__.items():
            if stopName in value.value:
                return stn;

    def getStationNameList():
        stnNames = [];
        for stn,value in StationPlatforms.__members__.items():
            stnNames.append(stn);
        return stnNames;


