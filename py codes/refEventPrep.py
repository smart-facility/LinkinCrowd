# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 11:11:27 2016

@author: nhuynh
"""

import mmRef;
import utilities;
import railNetv2;

def getMaxTrainNumberFromRefEventNameList(refEventNames,platformName):
    """
    Values in refEventNames must have the format trainXArrivingPY.
    X is the train number arriving at platform Y. 
    An example of such a value is 'train1ArrivingP2'.
    'PY' denotes platform name, e.g. 'P2'
    """
    #if the list of exising ref event names is empty, max train number is 0;    
    if len(refEventNames)==0:
        return 0;
    
    maxTrainNumber = 0;
    for refEvent in refEventNames:
        if refEvent[refEvent.find('P'):]==platformName:
            trainNumber = int(refEvent[len(mmRef.TimetableDict.train.name):\
                        refEvent.find(mmRef.TimetableDict.Arriving.name)]);
            if trainNumber>maxTrainNumber:
                maxTrainNumber = trainNumber;
            
    return maxTrainNumber;


def makeRefEventName(trainNumber, platformName):
    return mmRef.TimetableDict.train.name + str(trainNumber) + \
                mmRef.TimetableDict.Arriving.name + platformName;


def getListOfExistingEventName(contentRefEvent):
    refEventNames = [];
    
    # if the content of reference event file has only header    
    if len(contentRefEvent)==1:
        return refEventNames;
    
    for iRow in range(len(contentRefEvent)):
        if iRow==0:
            continue;
        refEventNames.append(contentRefEvent[iRow]\
                            [mmRef.RefEventCols.refEventName.value]);
    
    return refEventNames;
    


#def prepareRefEventFile(refEventFileName,stationName,platformName,startTime):
    """
    #stationName = 'S5';
    #platformName = 'P1';
    #startTime = '3:00:00';
    #Example:
    #prepareRefEventFile('sample timetable/timetableS5Schedule.csv', 'S5', 'P2', '03:40:00');
    """
    """
    contentRefEvent = utilities.readInCSVFile(refEventFileName);
    
    refEventNames = getListOfExistingEventName(contentRefEvent);
    newTrainNumber = 1 + \
            getMaxTrainNumberFromRefEventNameList(refEventNames,platformName);
    
    newRefEventRow = [];
    newRefEventRow.append([]);
    for i in range(len(mmRef.RefEventCols)):
        newRefEventRow[0].append('');
    
    global refEventName;
    refEventName = makeRefEventName(newTrainNumber, platformName);
    newRefEventRow[0][mmRef.RefEventCols.refEventName.value] = refEventName;
                                
    newRefEventRow[0][mmRef.RefEventCols.startTime.value] = startTime;
    newRefEventRow[0][mmRef.RefEventCols.duration.value] = \
                            mmRef.ConstTimeValues.dwellTime.value;
    newRefEventRow[0][mmRef.RefEventCols.location.value] = \
                mmRef.TimetableDict.trainSeats.name + platformName;

    #print(newRefEventRow);
    utilities.appendToCSV(refEventFileName,newRefEventRow);
    
    return refEventName;
    """

def prepareRefEventFile(refEventFileName,stationName,platformName,startTime):
    fullStopName = platformName + stationName;    
    trainService = railNetv2.getTrainService(fullStopName,utilities.convertTimeFormatToSecs(startTime));
    
    refEventName = trainService.name + mmRef.TimetableDict.Arriving.name + fullStopName;
    
    trainService = None;
    
    newRefEventRow = [];
    newRefEventRow.append([]);
    for i in range(len(mmRef.RefEventCols)):
        newRefEventRow[0].append('');
    
    newRefEventRow[0][mmRef.RefEventCols.refEventName.value] = refEventName;
    newRefEventRow[0][mmRef.RefEventCols.startTime.value] = startTime;
    newRefEventRow[0][mmRef.RefEventCols.duration.value] = mmRef.ConstTimeValues.dwellTime.value;
    newRefEventRow[0][mmRef.RefEventCols.location.value] = mmRef.TimetableDict.trainSeats.name + platformName;
    
    print(newRefEventRow);
    utilities.appendToCSV(refEventFileName,newRefEventRow);
    
    return refEventName;
    
