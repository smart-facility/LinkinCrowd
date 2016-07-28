# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 19:04:11 2016

@author: nhuynh

this is a test space for csv handling.
"""

import utilities;

def initNxtTrainsIdx(stationTimetbls):
    """
    initialises nxtTrainsIdx
    """    
    nxtTrainsIdx = {};
    for stnName,timeTbl in stationTimetbls.items():
        index = [];
        for i in range(len(timeTbl)):
            index.append(0);
        nxtTrainsIdx[stnName] = index;
        index = None;
    return nxtTrainsIdx;


def getSimulationStopTime(stnName,nxtArrTimeIndices,stnTimeTbls):
    timeTbl = stnTimeTbls[stnName];    
    nPlatforms = len(nxtArrTimeIndices[stnName]);
    
    # searches for the next earliest event at this station, i.e. train arrival on any platform.
    # first, searches for an initial value of nxtArrTime
    iNxtArrPlatform = -1;
    nxtArrTime = -1;
    for iPlatform in range(nPlatforms):
        arrTimeIdx = nxtArrTimeIndices[stnName][iPlatform];
        # if a valid arrival time of a next train is found
        if arrTimeIdx<=len(timeTbl[iPlatform])-1:
            iNxtArrPlatform = iPlatform;
            nxtArrTime = stnTimeTbls[stnName][iNxtArrPlatform][arrTimeIdx];
            break;
    
    # only starts searching for time of next earliest event if a valid initial value is found
    if nxtArrTime>-1:
        for iPlatform in range(nPlatforms):
            arrTimeIdx = nxtArrTimeIndices[stnName][iPlatform];
            if arrTimeIdx>len(timeTbl[iPlatform])-1:
                continue;
            arrTime = timeTbl[iPlatform][arrTimeIdx];
            if arrTime<nxtArrTime:
                iNxtArrPlatform = iPlatform;
                nxtArrTime = arrTime;
        
        #outText = utilities.convertSecsToTimeFormat(nxtArrTime) + ' P' + str(iNxtArrPlatform+1) + stnName;
        outText = [];
        outText.append(utilities.convertSecsToTimeFormat(nxtArrTime));
        outText.append(' P' + str(iNxtArrPlatform+1) + stnName);
        return outText;
        
    else:
        return ['EOT','N/A'];



def sortStationsForExec(stationNames,stnTimeTbls,nxtArrTimeIndices):
    moreTrainsComing = True;
    
    execDetails = [];
    
    while moreTrainsComing:
        # searches for an initial value of nxtArrTime
        iNxtExecStn = -1;
        iNxtArrPlatform = -1;
        nxtArrTime = -1;
        for iStn in range(len(stationNames)):
            stnName = stationNames[iStn];
            timeTbl = stnTimeTbls[stnName];
            nPlatforms = len(nxtArrTimeIndices[stnName]);
            for iPlatform in range(nPlatforms):
                arrTimeIdx = nxtArrTimeIndices[stnName][iPlatform];
                # if a valid arrival time of a next train is found
                if arrTimeIdx<=len(timeTbl[iPlatform])-1:
                    iNxtExecStn = iStn;
                    iNxtArrPlatform = iPlatform;
                    nxtArrTime = stnTimeTbls[stnName][iNxtArrPlatform][arrTimeIdx];
                    break;
            if nxtArrTime > -1:
                break;
        
        # only starts searching for next arrival time if a valid initial value is found
        if nxtArrTime > -1:
            # searches for the next earliest train arrival time at all stations        
            for iStn in range(len(stationNames)):
                stnName = stationNames[iStn];
                timeTbl = stnTimeTbls[stnName];
                nPlatforms = len(nxtArrTimeIndices[stnName]);
                for iPlatform in range(nPlatforms):
                    arrTimeIdx = nxtArrTimeIndices[stnName][iPlatform];
                    if arrTimeIdx>len(timeTbl[iPlatform])-1:
                        continue;
                    arrTime = timeTbl[iPlatform][arrTimeIdx];
                    if arrTime<nxtArrTime:
                        iNxtExecStn = iStn;
                        iNxtArrPlatform = iPlatform;
                        nxtArrTime = arrTime;
                timeTbl = None;
            
            nxtExecStnName = stationNames[iNxtExecStn];
            nxtArrTimeIndices[nxtExecStnName][iNxtArrPlatform] = nxtArrTimeIndices[nxtExecStnName][iNxtArrPlatform] + 1;
            
            #outText = 'P' + str(iNxtArrPlatform+1) + nxtExecStnName;
            newExecDetails = [];
            newExecDetails.append('P' + str(iNxtArrPlatform+1))
            newExecDetails.append(nxtExecStnName);
            newExecDetails.append(utilities.convertSecsToTimeFormat(nxtArrTime));
            pauseTimeDetails = getSimulationStopTime(nxtExecStnName,nxtArrTimeIndices,stnTimeTbls);            
            newExecDetails.append(pauseTimeDetails[0]);
            newExecDetails.append(pauseTimeDetails[1]);
            #print(execDetails[0], execDetails[1], execDetails[2], execDetails[3]);
            #outText = None;
            
            execDetails.append(newExecDetails);
            
        else:
            moreTrainsComing = False;

    return execDetails;