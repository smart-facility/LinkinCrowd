# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 19:54:03 2016

@author: nhuynh
"""
import csv;
import utilities;
import railNetv2;
import mmResultsRef;
import mmRef;

def readInFlowCounts(filename):
    """
    reads in the flow counts from simulation output files of a station.
    ignores the second row (don't know what it is and seems irrelevant).
    converts the first column, which is in hh:mm:ss format, to number of \
    seconds from midnight.
    Returns the a dictonary where key is the header of each column and value \
    is a 2-column array, which comprises number of seconds from midnight (1st \
    column) and flow counts (2nd column) corresponding to the header.
    Example:
    #flowCounts = readInFlowCounts('../newStation4/DefaultRun/FlowCounts.csv');
    """
    rawFlowCounts = [];    
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',');
        for row in reader:
            rawFlowCounts.append(row);
    
    timeStamps = [];
    for iRow in range(len(rawFlowCounts)):
        if iRow==0 or iRow==1:
            continue;
        timeStamps.append(utilities.convertTimeFormatToSecs(rawFlowCounts[iRow][0]));
    
    flowCounts = {};
    nColumns = len(rawFlowCounts[0]);
    for iCol in range(nColumns):
        if iCol == 0:
            continue;
        key = rawFlowCounts[0][iCol];
        counts = []; 
        for iRow in range(len(rawFlowCounts)):
            if iRow==0 or iRow==1:
                continue;
            counts.append([timeStamps[iRow-2],int(rawFlowCounts[iRow][iCol])]);
        flowCounts[key] = counts;
    
    return flowCounts;


def getBoardingPaxAtPrevStop(prevStopName,prevStopArrTime):
    """    
    reads in JourneyTimes and extracts the number of passengers in each \
    boarding a train at a given stop at the given arrival time of the train.
    Full stop name is prevStopDetails[0].
    The given arrival time is in prevStopDetails[1].
    """
    #prevStopName = prevStopDetails[0];
    #prevStopArrTime = prevStopDetails[1];
    prevStnName = railNetv2.StationPlatforms.getStationNameByStopName(prevStopName);
    journeyTimeFile = mmResultsRef.makeResultsPath(prevStnName) + 'JourneyTimes.csv';
    rawJourneyTimes = utilities.readInCSVFile(journeyTimeFile);
    
    countSlim = 0;
    countFat = 0;
    countDefault = 0;
    slimFastActiv = mmRef.Profiles.slimFastActiv.name;
    fatSlowLazy = mmRef.Profiles.fatSlowLazy.name;
    default = mmRef.Profiles.DefaultProfile.name;
    profileCol = mmResultsRef.JourneyTimesCols.profile.value;
    
    for row in rawJourneyTimes:
        if isBoarding(row,prevStopName,prevStopArrTime):
            #print(row[mmResultsRef.JourneyTimesCols.agentID.value]);
            if default in row[profileCol]:
                countDefault = countDefault + 1;
            elif slimFastActiv in row[profileCol]:
                countSlim = countSlim + 1;
            elif fatSlowLazy in row[profileCol]:
                countFat = countFat + 1;
            else:
                pass;
    
    return [countSlim, countFat, countDefault];
    #print(rawJourneyTimes[3]);
    

def isBoarding(row,prevStopName,prevStopArrTime):
    outLocationCol = mmResultsRef.JourneyTimesCols.out_location.value;
    outTimeCol = mmResultsRef.JourneyTimesCols.out_time.value;
    wordSeats = mmResultsRef.JourneyTimesVocab.seats.value;
    wordCar = mmResultsRef.JourneyTimesVocab.car.value;
    wordTraindoor = mmResultsRef.JourneyTimesVocab.traindoor.value;
    questionMarks = mmResultsRef.JourneyTimesVocab.questionMarks.value;
    
    totalCountTime = utilities.convertTimeFormatToSecs(mmRef.ConstTimeValues.backToSeatTimeOffset.value);
    
    # counts both passengers that sucessfully get to the seats and those who
    # were supposed to get off the train but failed (i.e. noted by question 
    # marks in their out location)
    if (wordSeats in row[outLocationCol] and prevStopName in row[outLocationCol]) or \
        (wordCar in row[outLocationCol] and prevStopName in row[outLocationCol]) or\
        (wordTraindoor in row[outLocationCol] and prevStopName in row[outLocationCol]) or \
        (questionMarks in row[outLocationCol]):
            outtime = utilities.convertTimeFormatToSecs(row[outTimeCol]);
            if outtime>=prevStopArrTime and outtime<=prevStopArrTime+totalCountTime:
                return True;
    
    return False;
