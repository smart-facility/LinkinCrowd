# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 21:59:52 2016

@author: nam
"""

import mmRef;
import utilities;

def prepareGateEventFile(gateEventFileName,plfName,refEventName):
    newRow = [];
    for i in range(len(mmRef.GateEventCols)):
        newRow.append('');
    
    newRow[mmRef.GateEventCols.refEventName.value] = refEventName;
    newRow[mmRef.GateEventCols.gate.value] = mmRef.TimetableDict.traindoors.value + plfName;
    
    newGateEventRow = [];
    newGateEventRow.append(newRow);
    
    utilities.appendToCSV(gateEventFileName,newGateEventRow);
