# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 22:29:29 2016

@author: nam
"""

import mmRef;
import utilities;

def prepareEvacEventFile(evacEventFileName,plfName,refEventName):
    newRow = [];
    for i in range(len(mmRef.EvacEventCols)):
        newRow.append('');
    
    newRow[mmRef.EvacEventCols.refEventName.value] = refEventName;
    newRow[mmRef.EvacEventCols.timeOffset.value] = mmRef.ConstTimeValues.evacTimeOffset.value;
    newRow[mmRef.EvacEventCols.keyToken.value] = mmRef.TimetableDict.trainTicket.value + plfName;
    newRow[mmRef.EvacEventCols.location.value] = mmRef.TimetableDict.trainSeats.value + plfName;
    
    newEvacEventRow = [];
    newEvacEventRow.append(newRow);
    
    utilities.appendToCSV(evacEventFileName,newEvacEventRow);

