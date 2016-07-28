# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 22:45:20 2016

@author: nam
"""

import mmRef;
import utilities;

def prepareActionEventFile(actionEventFileName,stnName,plfName,refEventName):
    newActionEventRows = []
    
    # prepares row for action waiting on platform
    newRow = [];
    for i in range(len(mmRef.ActionEventCols)):
        newRow.append('');
    newRow[mmRef.ActionEventCols.refEventName.value] = refEventName;
    newRow[mmRef.ActionEventCols.timeOffset.value] = mmRef.ConstTimeValues.dwellTime.value;
    newRow[mmRef.ActionEventCols.duration.value] = mmRef.ConstTimeValues.failedBoardingWaitTime.value;
    newRow[mmRef.ActionEventCols.keyToken.value] = mmRef.TimetableDict.trainTicket.value + plfName;
    newRow[mmRef.ActionEventCols.action.value] = mmRef.ActionDict.getWaitAction(stnName,plfName);
    newActionEventRows.append(newRow);
    
    # prepare row for action go back to seats
    newRow = [];
    for i in range(len(mmRef.ActionEventCols)):
        newRow.append('');
    newRow[mmRef.ActionEventCols.refEventName.value] = refEventName;
    newRow[mmRef.ActionEventCols.timeOffset.value] = mmRef.ConstTimeValues.backToSeatTimeOffset.value;
    newRow[mmRef.ActionEventCols.action.value] = mmRef.ActionDict.back2SeatsTrain.value + plfName;
    newActionEventRows.append(newRow);
    
    utilities.appendToCSV(actionEventFileName,newActionEventRows);

