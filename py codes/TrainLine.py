# -*- coding: utf-8 -*-
"""
Created on Tue May 17 22:14:49 2016

@author: nam
"""

import utilities;
import csv;
import mmRef;
import TrainService;

lineTimetablesPath = '../user inputs/lineTimetables/';
lineInitPaxPath = '../user inputs/initPaxOnLines/';
percentPaxStayOnBoardPath = '../user inputs/percentPaxStayOnBoard/';

class TrainLine():
    def __init__(self,lineName):
        # initialises line timetable and list of stops along this line
        # e.g. a stop name is 'P1S4'
        # timetable is a 2d integer array, number of rows of which equals 
        # number of stops.
        # number of columns is the number of trains servicing the line.
        # integer values are arrival time of trains at the stops in terms of 
        # the number of seconds from midnight
        fileLineTimetable = lineTimetablesPath + lineName + '.csv';
        stopNames = [];
        lineTimetable = [];
        with open(fileLineTimetable) as csvTimetable:
            timetblReader = csv.reader(csvTimetable, delimiter=',');
            # each row represents arrival time of trains at a stop along this 
            # line
            for row in timetblReader: 
                stopNames.append(row[0]);
                timesThisStop = [];
                for i in range(1,len(row)):
                    timesThisStop.append(\
                                    utilities.convertTimeFormatToSecs(row[i]));
                lineTimetable.append(timesThisStop);
        self.lineName = lineName;
        self.stopNames = stopNames;
        self.timetable = lineTimetable;
        self.initPaxOnLine = TrainLine.readInitPaxOnline(lineName);
        self.percentRemainOnBoard = TrainLine.readPercentRemainOnBoard(lineName);
        self.trainServices = self.initialiseTrainServices();
        #self.paxRemOnBoard = TrainLine.initialisePaxOnBoard(stopNames);
    
    def readInitPaxOnline(lineName):
        # initialises the initial number of passengers already onboard trains
        # on this line before entering the simulation
        fileLineInitPax = lineInitPaxPath + lineName + '.csv';
        rawInitPax = utilities.readInCSVFile(fileLineInitPax);
        initPax = {};
        # each row represents the number of passengers in a profile that 
        # are already on this line before its trains entering the simulation
        # within a time window, which is given in the 1st 2 values of the 
        # row (i.e. fromTime and toTime)
        for iRow in range(1,len(rawInitPax)): 
            row = rawInitPax[iRow];
            fromTimeInSecs = utilities.convertTimeFormatToSecs(row[0]);
            toTimeInSecs = utilities.convertTimeFormatToSecs(row[1]);
            key = (fromTimeInSecs, toTimeInSecs);
            initPaxDataThisKey = [];
            if key in initPax:
                initPaxDataThisKey = initPax[key];
            initPaxDataThisKey.append([int(row[2]), row[3]]);
            initPax[key] = initPaxDataThisKey;
        return initPax;
        
    def readPercentRemainOnBoard(lineName):
        # initialises proportion of passengers remaining onboard at each stop 
        # along a line
        filePercentPaxStayOnBoard = percentPaxStayOnBoardPath + lineName + \
                                                                        '.csv';
        rawPercentOnBoard = utilities.readInCSVFile(filePercentPaxStayOnBoard);
        percentOnBoard = {};
        for iRow in range(1,len(rawPercentOnBoard)):
            row = rawPercentOnBoard[iRow];
            stopName = row[0];
            fromTimeInSecs = utilities.convertTimeFormatToSecs(row[1]);
            toTimeInSecs = utilities.convertTimeFormatToSecs(row[2]);
            datThisStop = {};
            if stopName in percentOnBoard:
                datThisStop = percentOnBoard[stopName];
            timeWindow = (fromTimeInSecs,toTimeInSecs);
            percentByProfile = [];
            if timeWindow in datThisStop:
                percentByProfile = datThisStop[timeWindow];
            percentByProfile.append([float(row[3]),row[4]]);
            datThisStop[timeWindow] = percentByProfile;
            percentOnBoard[stopName] = datThisStop;
        return percentOnBoard;

    def initialisePaxOnBoard(stopNames):
        paxRemOnBoard = {};
        for stopName in stopNames:
            paxRemOnBoard[stopName] = {
                mmRef.Profiles.slimFastActiv.name: [],
                mmRef.Profiles.DefaultProfile.name: [],
                mmRef.Profiles.fatSlowLazy.name: []
            };
        return paxRemOnBoard;
    
    def initialiseTrainServices(self):
        nServices = len(self.timetable[0]);
        nStops = len(self.stopNames);
        trainServices = [];
        for iService in range(nServices):
            # prepares service name
            servcName = 'train' + str(iService) + self.lineName;
            
            # prepare service timetable
            servcTtb = [];
            for iStop in range(nStops):
                servcTtb.append(self.timetable[iStop][iService]);
            
            # prepare initial passengers on the service
            # (based on the arrival time at the 1st stop)
            timeAt1stStop = servcTtb[0];
            initPax = [];
            for timeWindow,paxInfo in self.initPaxOnLine.items():
                if (timeAt1stStop>=timeWindow[0] & timeAt1stStop<=timeWindow[1]):
                    initPax = paxInfo;
                        
            # prepare initial values for remaining passengers on board
            # these initial values are identical to the initital passengers on the service
            paxRemOnBoard = initPax;
            
            # prepare percentage of passengers remaining on board this service
            pcPaxRemThisService = {};
            for stopName,pcPaxRemThisStop in self.percentRemainOnBoard.items():
                timeAtThisStop = servcTtb[self.stopNames.index(stopName)];
                for timeWindow,pcPaxRem in pcPaxRemThisStop.items():
                    if (timeAtThisStop>=timeWindow[0] & timeAtThisStop<=timeWindow[1]):
                        pcPaxRemThisService[stopName] = pcPaxRem;
            
            trainServices.append(TrainService.TrainService(self,servcName,servcTtb,initPax,pcPaxRemThisService,paxRemOnBoard));
            
        return trainServices;
