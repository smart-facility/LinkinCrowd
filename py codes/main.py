# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 13:51:29 2016

@author: nhuynh
"""
import railNetv2;
import simOrderPrep;
import refEventPrep;
import schedulePrep;
import gateEventPrep;
import evacEventPrep;
import actionEventPrep;
import mmProjectFilePrep;
import mmRef;
import utilities;
import subprocess;


def main():
    # initialises network information
    railNetv2.prepareTrainLine();
    railNetv2.prepareStnTimetables();
    railNetv2.prepareDefaultPaxFlows();
    
    # sort stations for execution
    nxtTrainsIndex = simOrderPrep.initNxtTrainsIdx(railNetv2.stnTimetables);
    stationNames = railNetv2.StationPlatforms.getStationNameList();
    execDetails = simOrderPrep.sortStationsForExec(stationNames,railNetv2.stnTimetables,nxtTrainsIndex);
    
    for iRow in range(0,len(execDetails)):
        crnExecDetails = execDetails[iRow];
        print(crnExecDetails[0], crnExecDetails[1], crnExecDetails[2], crnExecDetails[3],crnExecDetails[4]);
    
    # preparing timetable files for next simulation
    startTimeInSecs = utilities.convertTimeFormatToSecs(execDetails[0][2]) - utilities.convertTimeFormatToSecs(mmRef.ConstTimeValues.scheduleTimeOffset.value);
    startTime = utilities.convertSecsToTimeFormat(startTimeInSecs);
    
    #for iRow in range(0,0):
    for iRow in range(0,len(execDetails)):
        crnExecDetails = execDetails[iRow];
        print(crnExecDetails[0], crnExecDetails[1], crnExecDetails[2], crnExecDetails[3],crnExecDetails[4]);
        
        # gets details of inputs required for preparing timetable files.
        plfName = crnExecDetails[0];
        stnName = crnExecDetails[1];
        trainArrTime = crnExecDetails[2];
        mmTimetableFolder = '../' + stnName + '/' + mmRef.FolderFileNames.timetableFolderName.value + '/';
        mmProjectFile = '../' + stnName + '/' + mmRef.FolderFileNames.projectName.value;
        
        # prepares reference event file
        refEventFileName = mmTimetableFolder + "timetable" + stnName + "ReferenceEvent.csv";
        refEventName = refEventPrep.prepareRefEventFile(refEventFileName, stnName, plfName, trainArrTime);
        
        # prepares schedule file
        scheduleFileName = mmTimetableFolder + 'timetable' + stnName + 'Schedule.csv';
        schedulePrep.prepareScheduleFile(scheduleFileName,stnName,plfName,trainArrTime,refEventName);
        
        print("after schedule");
        for trainLine in railNetv2.trainLines:
            for trainService in trainLine.trainServices:
                print([trainService.name, trainService.paxRemOnBoard]);
        print("\n");
        
        # prepares gate event file
        gateEventFileName = mmTimetableFolder + 'timetable' + stnName + 'GateEvent.csv';
        gateEventPrep.prepareGateEventFile(gateEventFileName,plfName,refEventName);
        
        # prepares evacuation event file
        evacEventFileName = mmTimetableFolder + 'timetable' + stnName + 'EvacuationEvent.csv';
        evacEventPrep.prepareEvacEventFile(evacEventFileName,plfName,refEventName);
        
        # prepares action event file
        actionEventFileName = mmTimetableFolder + 'timetable' + stnName + 'ActionEvent.csv';
        actionEventPrep.prepareActionEventFile(actionEventFileName,stnName,plfName,refEventName);
        
        # edits simulation time in MassMotion project file
        if (crnExecDetails[3]=="EOT"):
            crnExecDetails[3] = "03:30:00";
        
        durationInSecs = utilities.convertTimeFormatToSecs(crnExecDetails[3]) - startTimeInSecs;
        duration = utilities.convertSecsToTimeFormat(durationInSecs);
        
        mmProjectFilePrep.editSimulationTime(mmProjectFile,duration,startTime,duration,startTime);
        
        # executes MassMotion simulation of this station
        projectAttrib = ' -project ' + mmProjectFile;
        resultsAttrib = ' -results ../' + stnName + '/' + mmRef.FolderFileNames.outputFolderName.value + '/';
        verboseAttrib = ' -verbosity ERROR';
        execCommand = mmRef.FolderFileNames.mmPath.value + projectAttrib + resultsAttrib + verboseAttrib;
        #print(execCommand);
        subprocess.call(execCommand);

    

def sampleSortStationsForExec():
    # sort stations for execution
    nxtTrainsIndex = simOrderPrep.initNxtTrainsIdx(railNetv2.stnTimetables);
    stationNames = railNetv2.StationPlatforms.getStationNameList();
    execDetails = simOrderPrep.sortStationsForExec(stationNames,railNetv2.stnTimetables,nxtTrainsIndex);
    return execDetails;


def samplePrepRefEventFile():
    # prepare ReferenceEvent file
    MMtimetableFolder = 'sample timetable/';
    stationName = railNetv2.StationPlatforms.S5.name;
    platformName = 'P1';
    trainArrTime = '03:05:00';
    refEventFileName = MMtimetableFolder + "timetable" + stationName + "ReferenceEvent.csv";
    refEventName = refEventPrep.prepareRefEventFile(refEventFileName, stationName, platformName, trainArrTime);
    return refEventName;


def samplePrepScheduleFile(refEventName):
    MMtimetableFolder = 'sample timetable/';
    stnName = railNetv2.StationPlatforms.S5.name;
    plfName = 'P1';
    trainArrTime = '03:05:00';
    scheduleFileName = MMtimetableFolder + 'timetable' + stnName + 'Schedule.csv';
    schedulePrep.prepareScheduleFile(scheduleFileName,stnName,plfName,trainArrTime,refEventName)


def samplePrepGateEventFile(refEventName):
    MMtimetableFolder = 'sample timetable/';
    stnName = railNetv2.StationPlatforms.S5.name;
    plfName = 'P1';
    #trainArrTime = '03:05:00';
    gateEventFileName = MMtimetableFolder + 'timetable' + stnName + 'GateEvent.csv';
    gateEventPrep.prepareGateEventFile(gateEventFileName,plfName,refEventName);


def samplePrepEvacEventFile(refEventName):
    MMtimetableFolder = 'sample timetable/';
    stnName = railNetv2.StationPlatforms.S5.name;
    plfName = 'P1';
    #trainArrTime = '03:05:00';
    evacEventFileName = MMtimetableFolder + 'timetable' + stnName + 'EvacuationEvent.csv';
    evacEventPrep.prepareEvacEventFile(evacEventFileName,plfName,refEventName);


def samplePrepActionEventFile(refEventName):
    MMtimetableFolder = 'sample timetable/';
    stnName = railNetv2.StationPlatforms.S5.name;
    plfName = 'P1';
    #trainArrTime = '03:05:00';
    actionEventFileName = MMtimetableFolder + 'timetable' + stnName + 'ActionEvent.csv';
    actionEventPrep.prepareActionEventFile(actionEventFileName,stnName,plfName,refEventName);


if __name__=='__main__':
    main();
