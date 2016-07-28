# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 18:11:31 2016

@author: nhuynh
"""
import mmRef;
from enum import Enum;

class JourneyTimesCols(Enum):
    agentID = 0;
    profile = 1;
    avatar = 2;
    in_time = 3;
    out_time = 4;
    in_location = 5;
    out_location = 6;
    
class JourneyTimesVocab(Enum):
    seats = 'seats';
    questionMarks = '???';
    car = 'car';
    traindoor = 'traindoor';

def makeResultsPath(stnName):
    return '../' + stnName + '/' + mmRef.FolderFileNames.outputFolderName.value + '/';