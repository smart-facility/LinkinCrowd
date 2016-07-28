# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 21:55:50 2016

@author: nam
"""

import xml.etree.ElementTree as ET

def editSimulationTime(projectFilename,runTimeDurationVal,runTimeStartVal,iceCacheWinDurationVal,iceCacheWinStartVal):
    tree = ET.parse(projectFilename);
    root = tree.getroot();
    
    maxDuration = root.find('Settings').find('Runtime').find('MaxDuration');
    startTime = root.find('Settings').find('Runtime').find('StartTime');
    #print(maxDuration.attrib.get('v'));
    #print(startTime.attrib.get('v'));
    
    iceCacheWindowDuration = root.find('Settings').find('Reporting').find('ICECacheWindowDuration');
    iceCacheWindowStart = root.find('Settings').find('Reporting').find('ICECacheWindowStart');
    #print(iceCacheWindowDuration.attrib.get('v'));
    #print(iceCacheWindowStart.attrib.get('v'));
    
    maxDuration.attrib['v'] = runTimeDurationVal; #"0:25:00";
    startTime.attrib['v'] = runTimeStartVal;
    iceCacheWindowDuration.attrib['v'] = iceCacheWinDurationVal;
    iceCacheWindowStart.attrib['v'] = iceCacheWinStartVal; #"02:59:00";
    
    tree.write(projectFilename);
