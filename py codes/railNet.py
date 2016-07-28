# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 21:02:11 2016

@author: nhuynh
"""

from enum import Enum;
import utilities;
import csv;

stnDefPaxFlows = {};
stnDefPaxOnBoard = {};
stnTimetables = {};
lineTimetables = {};

timetblFileS1 = '../user inputs/station timetables/trainArrS1.csv';
timetblFileS2 = '../user inputs/station timetables/trainArrS2.csv';
timetblFileS3 = '../user inputs/station timetables/trainArrS3.csv';
timetblFileS4 = '../user inputs/station timetables/trainArrS4.csv';
timetblFileS5 = '../user inputs/station timetables/trainArrS5.csv';

defPaxFlowsFileS1 = '../user inputs/defaultPaxFlowAtStns/S1.csv';
defPaxFlowsFileS2 = '../user inputs/defaultPaxFlowAtStns/S2.csv';
defPaxFlowsFileS3 = '../user inputs/defaultPaxFlowAtStns/S3.csv';
defPaxFlowsFileS4 = '../user inputs/defaultPaxFlowAtStns/S4.csv';
defPaxFlowsFileS5 = '../user inputs/defaultPaxFlowAtStns/S5.csv';

class StationPlatforms(Enum):
    S1 = ['P1S1', 'P2S1'];
    S2 = ['P1S2', 'P2S2', 'P3S2', 'P4S2'];
    S3 = ['P1S3', 'P2S3'];
    S4 = ['P1S4', 'P2S4'];
    S5 = ['P1S5', 'P2S5'];
    
    def getPlatformIndex(stnName,stopName):
        for stn,value in StationPlatforms.__members__.items():
            if stn==stnName:
                return value.value.index(stopName);
    
    def getPlatformsByStn(stnName):
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


class Line(Enum):
    line1 = [[StationPlatforms.S1.value[1], StationPlatforms.S1.name],
             [StationPlatforms.S2.value[1], StationPlatforms.S2.name],
             [StationPlatforms.S3.value[1], StationPlatforms.S3.name]];
    line2 = [[StationPlatforms.S3.value[0], StationPlatforms.S3.name],
             [StationPlatforms.S2.value[0], StationPlatforms.S2.name],
             [StationPlatforms.S1.value[0], StationPlatforms.S1.name]];
    line3 = [[StationPlatforms.S4.value[1], StationPlatforms.S4.name],
             [StationPlatforms.S2.value[3], StationPlatforms.S2.name],
             [StationPlatforms.S5.value[1], StationPlatforms.S5.name]];
    line4 = [[StationPlatforms.S5.value[0], StationPlatforms.S5.name],
             [StationPlatforms.S2.value[2], StationPlatforms.S2.name],
             [StationPlatforms.S4.value[0], StationPlatforms.S4.name]];

    def getStopList(self):
        stopList = [];
        for stopDetails in self.value:
            stopName = stopDetails[0];
            stopList.append(stopName);
        return stopList;



def readStationTimetbl(filename):
    """
    Reads in filename for the timetable of train arrival at a station.
    Values in each line in filename represents arrival times at a platform.
    The order of lines in the numbering order of platforms at the station.
    Values of time should be string in format hh:mm:ss or h:mm:ss.
    The function also converts these time strings into number of seconds from midnight.
    The return object is a nested array dimensions of which are identical to the dimensions of strings in filename.
    Values in this nested array is the arrival time of trains at this station in terms of number of seconds from midnight.
    Example:    
    #print(readStationTimetbl('trainArrS1.csv'));
    """
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',');
        stationTimetbl = [];
        for row in reader:
            platformTime = [];
            for time in row:
                platformTime.append(utilities.convertTimeFormatToSecs(time));
            stationTimetbl.append(platformTime);
            
    return stationTimetbl;


def readDefPaxFlows(filename):
    rawContent = utilities.readInCSVFile(filename);
    initValuesByOD = {};
    for iRow in range(len(rawContent)):
        if iRow==0:
            continue;
        else:
            odPair = (rawContent[iRow][0], rawContent[iRow][1]);
            newValue = [float(rawContent[iRow][2]), rawContent[iRow][3]];
            paxValues = [];
            if odPair in initValuesByOD:
                paxValues = initValuesByOD.get(odPair);
            paxValues.append(newValue);
            initValuesByOD[odPair] = paxValues;
    return initValuesByOD;


def prepareDefaultPaxFlows():
    global stnDefPaxFlows;
    stnDefPaxFlows = {
                StationPlatforms.S1.name: readDefPaxFlows(defPaxFlowsFileS1),
                StationPlatforms.S2.name: readDefPaxFlows(defPaxFlowsFileS2),
                StationPlatforms.S3.name: readDefPaxFlows(defPaxFlowsFileS3),
                StationPlatforms.S4.name: readDefPaxFlows(defPaxFlowsFileS4),
                StationPlatforms.S5.name: readDefPaxFlows(defPaxFlowsFileS5)};


def prepareStationTimetables():
    global stnTimetables;
    stnTimetables = {
                StationPlatforms.S1.name: readStationTimetbl(timetblFileS1),
                StationPlatforms.S2.name: readStationTimetbl(timetblFileS2),
                StationPlatforms.S3.name: readStationTimetbl(timetblFileS3),
                StationPlatforms.S4.name: readStationTimetbl(timetblFileS4),
                StationPlatforms.S5.name: readStationTimetbl(timetblFileS5)};


def prepareLineTimetables():
    global lineTimetables;
    for line,value in Line.__members__.items():
        lineTimetables[line] = [];
        for stopDetails in value.value:
            stnName = stopDetails[1];
            stopName = stopDetails[0];
            platformIdx = StationPlatforms.getPlatformIndex(stnName,stopName);
            lineTimetables[line].append(stnTimetables[stnName][platformIdx]);
        print(line);
        print(lineTimetables[line]);



def getPrevStop(crnStopName,crnArrTime):
    prevStop = (None,-1);
    for line,value in Line.__members__.items():
        route = value.getStopList();
        #print(value);
        #print(route);
        timetable = lineTimetables[line];
        if crnStopName in route:
            iCrnStop = route.index(crnStopName);
            if crnArrTime in timetable[iCrnStop]:
                iCrnTrain = timetable[iCrnStop].index(crnArrTime);
                # if this is the first stop of the line, 
                if iCrnStop==0: 
                    prevStop = ('',-1);
                    break;
                else:
                    prevStop = (route[iCrnStop-1],timetable[iCrnStop-1][iCrnTrain]);
                    break;
    return prevStop;


