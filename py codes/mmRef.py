# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 19:46:13 2016

@author: nhuynh
"""

from enum import Enum;


class RefEventCols(Enum):
    refEventName = 0;
    startTime = 1;
    duration = 2;
    location = 3;
    initAction = 4;
    giveTokens = 5;

class ScheduleCols(Enum):
    fromCol = 0;
    toCol = 1;
    population = 2;
    timeOffset = 3;
    curve = 4;
    avatar = 5;
    profile = 6;
    initAction = 7;
    giveTokens = 8;

class GateEventCols(Enum):
    refEventName = 0;
    timeOffset = 1;
    duration = 2;
    apply2RefEvent = 3;
    keyToken = 4;
    gate = 5;

class EvacEventCols(Enum):
    refEventName = 0;
    timeOffset = 1;
    duration = 2;
    apply2RefEvent = 3;
    keyToken = 4;
    targetZone = 5;
    preMovementDuration = 6;
    location = 7;
    giveTokens = 8;

class ActionEventCols(Enum):
    refEventName = 0;
    timeOffset = 1;
    duration = 2;
    apply2RefEvent = 3;
    keyToken = 4;
    targetZone = 5;
    action = 6;
    giveTokens = 7;

class TimetableDict(Enum):
    gate = 'gate';
    trainSeats = 'trainSeats';
    paxArrRateAtStn = 'paxArrRateAtStn';
    traindoors = 'traindoors';
    trainTicket = 'trainTicket';
    train = 'train';
    Arriving = 'Arriving';

class ConstTimeValues(Enum):
    dwellTime = '0:00:45';
    scheduleTimeOffset = '-0:06:00';
    evacTimeOffset = '0:00:15';
    failedBoardingWaitTime = '23:59:00';
    backToSeatTimeOffset = '0:00:46';


class FolderFileNames(Enum):
    outputFolderName = 'output';
    timetableFolderName = 'timetables';
    projectName = 'Project.mmxsi';
    mmPath = 'C:/Program Files/Oasys/MassMotion 7.0/MassMotionConsole.exe';


class ActionDict(Enum):
    back2SeatsTrain = 'back2SeatsTrain';
    
    def getWaitAction(stnName,platformName):
        if stnName=='S1' or stnName=='S3':
            if platformName=='P1' or platformName=='P2':            
                return 'waitOnP1_2';
            else:
                return 'invalidP@S1S3';
        elif stnName=='S4' or stnName=='S5':
            if platformName=='P1' or platformName=='P2':
                return 'waitOn'+platformName;
            else:
                return 'invalidP@S4S5';
        elif stnName=='S2':
            if platformName=='P1' or platformName=='P2':
                return 'waitOnP1_2';
            elif platformName=='P3' or platformName=='P4':
                return 'waitOnP3_4';
            else:
                return 'invalidP@S2';
        else:
            return 'invalidS';


class Profiles(Enum):
    slimFastActiv = 'Blue_LowPoly';
    DefaultProfile = 'Green_LowPoly';
    fatSlowLazy = 'Orange_LowPoly';
    
    def getAvatarByProfileStr(queryStr):
        for profile,value in Profiles.__members__.items():
            if profile==queryStr:
                return value.value;
    
