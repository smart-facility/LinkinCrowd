# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 20:04:06 2016

@author: nhuynh
"""

import railNetv2;
import utilities;
import mmRef;
import TrainService;

'''
function description
'''
def prepareScheduleFile(scheduleFileName,stnName,plfName,startTime,refEventName):
    #scheduleFileName = path + 'timetable' + stationName + 'Schedule.csv';
    crnStopName = plfName + stnName;
    startTimeInSecs = utilities.convertTimeFormatToSecs(startTime);
    trainService = railNetv2.getTrainService(crnStopName,startTimeInSecs);
    
    slimRemOnBoard = trainService.getPaxRemOnBoard(mmRef.Profiles.slimFastActiv.name);
    defRemOnBoard = trainService.getPaxRemOnBoard(mmRef.Profiles.DefaultProfile.name);
    fatRemOnBoard = trainService.getPaxRemOnBoard(mmRef.Profiles.fatSlowLazy.name);
    
    slimOnBoard = 0;
    defOnBoard = 0;
    fatOnBoard = 0;
    
    # if this stop is the 1st one
    if trainService.line.stopNames[0]==crnStopName:
        # slimRemOnBoard, defRemOnBoard, and fatRemOnBoard are all passengers that are onboard
        slimOnBoard = slimRemOnBoard;
        defOnBoard = defRemOnBoard;
        fatOnBoard = fatRemOnBoard;
        #print(["1st stop", trainService.name, crnStopName, startTime, "slimRem", slimRemOnBoard, "defRem", defRemOnBoard, "fatRem", fatRemOnBoard]);
    else:
        # ok, this is not the 1st stop.
        # reads in JourneyTimes.csv from the results of previous stop
        # and extracts the number of passengers for each profile 
        # boarding this train at the previous stop.
        # then adds these values to slimRemOnBoard, defRemOnBoard, and fatRemOnBoard for the total number of passengers on this train
        # get the previous stop name
        iCrnStop = trainService.line.stopNames.index(crnStopName);
        prevStopName = trainService.line.stopNames[iCrnStop-1];
        prevStopTime = trainService.timetable[iCrnStop-1];
        #[slimPrevBoard, fatPrevBoard, defaultPrevBoard] = analysis.getBoardingPaxAtPrevStop(prevStopName,prevStopTime);
        slimPrevBoard = 46;
        fatPrevBoard = 32;
        defaultPrevBoard = 45
        
        #print(["mid stop", trainService.name, crnStopName, startTime, "slimRem", slimRemOnBoard, "defRem", defRemOnBoard, "fatRem", fatRemOnBoard]);
        #print([prevStopName, prevStopTime, "slimPrevBrd", slimPrevBoard, "defPrevBrd", defaultPrevBoard, "fatPrevBrd", fatPrevBoard]);
        
        slimOnBoard = slimRemOnBoard + slimPrevBoard;
        fatOnBoard = fatRemOnBoard + fatPrevBoard;
        defOnBoard = defRemOnBoard + defaultPrevBoard;
        
    pcSlimRemOnBoard = trainService.getPcPaxRemOnBoard(crnStopName,mmRef.Profiles.slimFastActiv.name);
    pcDefRemOnBoard = trainService.getPcPaxRemOnBoard(crnStopName,mmRef.Profiles.DefaultProfile.name);
    pcFatRemOnBoard = trainService.getPcPaxRemOnBoard(crnStopName,mmRef.Profiles.fatSlowLazy.name);
    
    slimRemOnBoard = utilities.toNearestInt(pcSlimRemOnBoard*slimOnBoard);
    defRemOnBoard = utilities.toNearestInt(pcDefRemOnBoard*defOnBoard);
    fatRemOnBoard = utilities.toNearestInt(pcFatRemOnBoard*fatOnBoard);
    
    trainService.updatePaxRemOnBoard(slimRemOnBoard,defRemOnBoard,fatRemOnBoard)
    
    slimAlight = utilities.toNearestInt((1-pcSlimRemOnBoard)*slimOnBoard);
    defAlight = utilities.toNearestInt((1-pcDefRemOnBoard)*defOnBoard);
    fatAlight = utilities.toNearestInt((1-pcFatRemOnBoard)*fatOnBoard);
    
    #print(["crn stop", trainService.name, crnStopName, startTime, "slimAlight", slimAlight, "defAlight", defAlight, "fatAlight", fatAlight]);
    #print("\n");
    
    # gets the distribution of passenger flows to station gate and to other 
    # platforms from this platform
    paxFlowDataPackAllDay = railNetv2.stnDefPaxFlows[stnName];
    paxFlowDataPack = {};
    for timeWindow,paxFlowData in paxFlowDataPackAllDay.items():
        if (startTimeInSecs>=timeWindow[0] & startTimeInSecs<=timeWindow[1]):
           paxFlowDataPack = paxFlowData;
           break;
    
    paxFlowFromStop = {
        mmRef.Profiles.slimFastActiv.name: getPaxFlowDistrib(mmRef.Profiles.slimFastActiv.name,stnName,crnStopName,slimAlight,paxFlowDataPack),
        mmRef.Profiles.DefaultProfile.name: getPaxFlowDistrib(mmRef.Profiles.DefaultProfile.name,stnName,crnStopName,defAlight,paxFlowDataPack),
        mmRef.Profiles.fatSlowLazy.name: getPaxFlowDistrib(mmRef.Profiles.fatSlowLazy.name,stnName,crnStopName,fatAlight,paxFlowDataPack)};
    #print("paxFlowFromStop");
    #print(paxFlowFromStop);
    
    paxFlowFromGate = paxFlowDataPack[(mmRef.TimetableDict.gate.value+stnName,crnStopName)];
    #print("paxFlowFromGate");
    #print(paxFlowFromGate);
    
    newSchedRows = prepareNewScheduleRows(paxFlowFromStop, paxFlowFromGate, stnName, plfName, refEventName);
    utilities.appendToCSV(scheduleFileName,newSchedRows);


'''
function description
'''
def prepareNewScheduleRows(paxFlowFromStop, paxFlowFromGate, stnName, plfName, refEventName):
    gateName = mmRef.TimetableDict.gate.value + stnName;
    
    newSchedRows = [];
    
    # makes schedule records of passengers coming from station gate to this 
    # platform
    for record in paxFlowFromGate:
        paxProfile = record[1];
        paxNumber = utilities.toNearestInt(record[0]);
        newRow = [];
        for i in range(len(mmRef.ScheduleCols)):
            newRow.append('');
        newRow[mmRef.ScheduleCols.fromCol.value] = gateName;
        newRow[mmRef.ScheduleCols.toCol.value] = refEventName;
        newRow[mmRef.ScheduleCols.population.value] = paxNumber;
        newRow[mmRef.ScheduleCols.timeOffset.value] = mmRef.ConstTimeValues.scheduleTimeOffset.value;
        newRow[mmRef.ScheduleCols.curve.value] = mmRef.TimetableDict.paxArrRateAtStn.value;
        newRow[mmRef.ScheduleCols.avatar.value] = mmRef.Profiles.getAvatarByProfileStr(paxProfile);
        newRow[mmRef.ScheduleCols.profile.value] = paxProfile;
        newRow[mmRef.ScheduleCols.initAction.value] = mmRef.ActionDict.getWaitAction(stnName,plfName);
        newRow[mmRef.ScheduleCols.giveTokens.value] = mmRef.TimetableDict.trainTicket.value + plfName;
        
        newSchedRows.append(newRow);
    
    for paxProfile,flowData in paxFlowFromStop.items():
        for record in flowData:
            dest = record[0][1];
            paxNumber = utilities.toNearestInt(record[1]);
            newRow = [];
            for i in range(len(mmRef.ScheduleCols)):
                newRow.append('');
            newRow[mmRef.ScheduleCols.fromCol.value] = refEventName;
            newRow[mmRef.ScheduleCols.population.value] = paxNumber;
            newRow[mmRef.ScheduleCols.avatar.value] = mmRef.Profiles.getAvatarByProfileStr(paxProfile);
            newRow[mmRef.ScheduleCols.profile.value] = paxProfile;
            # if the destination of this row is the station gate
            if mmRef.TimetableDict.gate.value in dest:
                newRow[mmRef.ScheduleCols.toCol.value] = dest;
            else: 
                # get the name destination platform from dest
                # dest has value like 'P2S2' and stnName has value like 'S2'.
                # dest[:dest.index(stnName)] therefore returns 'P2'.
                destPlfName = dest[:dest.index(stnName)];
                correctDest = mmRef.TimetableDict.trainSeats.value + destPlfName;
                newRow[mmRef.ScheduleCols.toCol.value] = correctDest;
                newRow[mmRef.ScheduleCols.initAction.value] = \
                            mmRef.ActionDict.getWaitAction(stnName,destPlfName);
                newRow[mmRef.ScheduleCols.giveTokens.value] = \
                        mmRef.TimetableDict.trainTicket.value + destPlfName;
            newSchedRows.append(newRow);
    
    return newSchedRows;
    
    

'''
paxProfile = 'slimFastActiv';
stnName = 'S1';
fromStopName = 'P1S1';
nPaxFromStopName = 173;
'''
def getPaxFlowDistrib(queryPaxProfile,stnName,fromStopName,nPaxFromStopName,paxFlowThisStopThisTime):

    stopsThisStn = railNetv2.StationPlatforms.getStopsByStn(stnName);
    paxFlowByOD = [];
    
    for stop in stopsThisStn:
        if stop==fromStopName:
            continue;
        odPair = (fromStopName,stop);
        paxFlowThisPair = paxFlowThisStopThisTime[odPair];
        for row in paxFlowThisPair:
            paxProfile = row[1];
            flowValue = row[0];
            if paxProfile==queryPaxProfile:
                paxFlowByOD.append([odPair,flowValue]);
            
    odPair = (fromStopName,mmRef.TimetableDict.gate.value+stnName);
    paxFlowThisPair = paxFlowThisStopThisTime[odPair];
    for row in paxFlowThisPair:
        paxProfile = row[1];
        flowValue = row[0];
        if paxProfile==queryPaxProfile:
            paxFlowByOD.append([odPair,flowValue]);

    tempSum = 0;
    for row in paxFlowByOD:
        row[1] = max(row[1],0); # if this flowValue is negative, set it to 0
        tempSum = tempSum + row[1];
    
    for row in paxFlowByOD:
        row[1] = row[1]/tempSum*nPaxFromStopName;
        row[1] = utilities.toNearestInt(row[1]); # round new flowValue to nearest integer
    
    return paxFlowByOD;
    

'''
returns the initial/dafault values of number of passengers in each profile
leaving platform plfName (for gate and for other platforms) at station stnName.
'''
'''
def getDefaultAlightingPax(stnName, plfName):
    slimCounts = 0;
    fatCounts = 0;
    defaultCounts = 0;
    
    origStr = plfName + stnName;
    destStr = mmRef.TimetableDict.gate.value + stnName;
    defPaxVal = railNetv2.stnDefPaxFlows.get(stnName).get((origStr,destStr));
    for row in defPaxVal:
        if row[1]==mmRef.Profiles.slimFastActiv.name:
            slimCounts = slimCounts + utilities.toNearestInt(row[0]);
        elif row[1]==mmRef.Profiles.fatSlowLazy.name:
            fatCounts = fatCounts + utilities.toNearestInt(row[0]);
        elif row[1]==mmRef.Profiles.DefaultProfile.name:
            defaultCounts = defaultCounts + utilities.toNearestInt(row[0]);
    
    plfsThisStn = railNetv2.StationPlatforms.getPlatformsByStn(stnName);
    for plf in plfsThisStn:
        if plf==origStr:
            continue;
        else:
            destStr = plf;
            defPaxVal = \
                railNetv2.stnDefPaxFlows.get(stnName).get((origStr,destStr));
            for row in defPaxVal:
                if row[1]==mmRef.Profiles.slimFastActiv.name:
                    slimCounts = slimCounts + utilities.toNearestInt(row[0]);
                elif row[1]==mmRef.Profiles.fatSlowLazy.name:
                    fatCounts = fatCounts + utilities.toNearestInt(row[0]);
                elif row[1]==mmRef.Profiles.DefaultProfile.name:
                    defaultCounts = defaultCounts + utilities.toNearestInt(row[0]);
                    
    return [slimCounts, fatCounts, defaultCounts];



def createGatePlatformSched(stnName,plfName,refEventName):
    # read from railnet.stnDefPaxFlows the default number of passenges in each 
    # profile from gate of this station to the platform being considered
    origStr = mmRef.TimetableDict.gate.value + stnName;
    destStr = plfName + stnName;
    defPaxVal = railNetv2.stnDefPaxFlows.get(stnName).get((origStr,destStr));
    schedRecords = [];
    for row in defPaxVal:
        nPax = str(row[0]);
        paxProfile = row[1];
        newRecord = [origStr, \
                    refEventName, \
                    nPax, \
                    mmRef.ConstTimeValues.scheduleTimeOffset.value,\
                    mmRef.TimetableDict.paxArrRateAtStn.value,\
                    mmRef.Profiles.getAvatarByProfileStr(paxProfile),\
                    paxProfile,\
                    mmRef.ActionDict.getWaitAction(stnName,plfName),\
                    mmRef.TimetableDict.trainTicket.value + plfName
                    ];
        schedRecords.append(newRecord);
    return schedRecords;



def createPlatformGateSched(stnName,refEventName, nSlim, nDefault, nFat):
    destStr = mmRef.TimetableDict.gate.value + stnName;
    schedRecords = [];
    schedRecords.append([refEventName, destStr, str(nSlim), '', '',\
                mmRef.Profiles.slimFastActiv.value,\
                mmRef.Profiles.slimFastActiv.name,\
                '', '']);
    schedRecords.append([refEventName, destStr, str(nDefault), '', '',\
                mmRef.Profiles.DefaultProfile.value,\
                mmRef.Profiles.DefaultProfile.name,\
                '', '']);
    schedRecords.append([refEventName, destStr, str(nFat), '', '',\
                mmRef.Profiles.fatSlowLazy.value,\
                mmRef.Profiles.fatSlowLazy.name,\
                '', '']);
    return schedRecords;


def createInterPlatformsSched(\
                        stnName,refEventName,desPlfName,nSlim,nDefault,nFat):
    destStr = mmRef.TimetableDict.trainSeats.value + desPlfName;
    schedRecords = [];
    schedRecords.append([refEventName, destStr, str(nSlim), '', '',\
                mmRef.Profiles.slimFastActiv.value,\
                mmRef.Profiles.slimFastActiv.name,\
                mmRef.ActionDict.getWaitAction(stnName,desPlfName),\
                mmRef.TimetableDict.trainTicket.value + desPlfName]);
    schedRecords.append([refEventName, destStr, str(nDefault), '', '',\
                mmRef.Profiles.DefaultProfile.value,\
                mmRef.Profiles.DefaultProfile.name,\
                mmRef.ActionDict.getWaitAction(stnName,desPlfName),\
                mmRef.TimetableDict.trainTicket.value + desPlfName]);
    schedRecords.append([refEventName, destStr, str(nFat), '', '',\
                mmRef.Profiles.fatSlowLazy.value,\
                mmRef.Profiles.fatSlowLazy.name,\
                mmRef.ActionDict.getWaitAction(stnName,desPlfName),\
                mmRef.TimetableDict.trainTicket.value + desPlfName]);
    return schedRecords;
'''