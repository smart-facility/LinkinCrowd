# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 19:39:12 2016

@author: nhuynh
"""

import csv;
import math;

def readInCSVFile(filename):
    rawContent = [];
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',');
        for row in reader:
            rawContent.append(row);
    return rawContent;


def appendToCSV(filename,newRows):
    with open(filename,'a',newline='') as fp:
        a = csv.writer(fp,delimiter=',');
        a.writerows(newRows);


def convertTimeFormatToSecs(timeString):
    """Converts the time in format h:mm:ss to seconds from midnight.
    The input is a string and must have the format h:mm:ss or hh:mm:ss.
    Example:    
    #print(convertTimeFormatToSecs('14:03:04'));
    """
    # gets the value of hour, minute, and second
    hhStr = timeString[:timeString.find(':')];
    mmStr = timeString[(timeString.find(':')+1):timeString.rfind(':')];
    ssStr = timeString[timeString.rfind(':')+1:];
    
    # converts the string values into int values
    hhInt = int(hhStr);
    mmInt = int(mmStr);
    ssStr = int(ssStr);
    
    # calculates the number of seconds from midnight
    return (hhInt*3600 + mmInt*60 + ssStr);

    
def convertSecsToTimeFormat(secsFromMidNight):
    hhInt = int(math.floor(secsFromMidNight/3600));
    mmInt = int(math.floor(int(secsFromMidNight%3600)/60));
    ssInt = int(secsFromMidNight%60);
    
    hhStr = str(hhInt);
    if hhInt<10:
        hhStr = '0' + str(hhInt);
    
    mmStr = str(mmInt);
    if mmInt<10:
        mmStr = '0' + str(mmInt);

    ssStr = str(ssInt);
    if ssInt<10:
        ssStr = '0' + str(ssInt);

    return hhStr + ':' + mmStr + ':' + ssStr;


def toNearestInt(floatValue):
    return int(floatValue+0.5);
