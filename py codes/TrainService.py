# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 21:47:08 2016

@author: nam
"""
import mmRef;

class TrainService():
    def __init__(self, trainLine, servcName, newTimetable, initPaxOnTrain, pcPaxRem, paxRem):
        self.name = servcName;
        self.line = trainLine;
        self.timetable = newTimetable;
        self.initPax = initPaxOnTrain;
        self.percentPaxRemOnBoard = pcPaxRem;
        # this is the number of passengers remaining on board after (successfull and unsuccessful) alighting.
        # it does not include passengers newly boarded or failing to board.
        self.paxRemOnBoard = paxRem; 
    
    def getInitPax(self,paxProfile):
        for row in self.initPax:
            if (row[1]==paxProfile):
                return row[0];
        return 0;
    
    def getPcPaxRemOnBoard(self,stopName,paxProfile):
        pcPaxRemOnBoard = [];
        if stopName in self.percentPaxRemOnBoard:
            pcPaxRemOnBoard = self.percentPaxRemOnBoard[stopName];
        else:
            return 0;
        
        for row in pcPaxRemOnBoard:
            if row[1]==paxProfile:
                return row[0];
        return 0;
    
    def getPaxRemOnBoard(self,paxProfile):
        for row in self.paxRemOnBoard:
            if (row[1]==paxProfile):
                return row[0];
        return 0;
    
    def getCopyPaxRemOnBoard(self):
        copyPaxRem = [];
        for row in self.paxRemOnBoard:
            newRow=[];
            for iItem in range(0,len(row)):
                newRow.append(row[iItem]);
            copyPaxRem.append(newRow);
        return copyPaxRem;
    
    def updatePaxRemOnBoard(self,slimRemOnBoard,defRemOnBoard,fatRemOnBoard):
        copyPaxRemOnBoard = self.getCopyPaxRemOnBoard();
        for iRow in range(0,len(copyPaxRemOnBoard)):
            if (copyPaxRemOnBoard[iRow][1]==mmRef.Profiles.slimFastActiv.name):
                copyPaxRemOnBoard[iRow][0] = slimRemOnBoard;
            elif (copyPaxRemOnBoard[iRow][1]==mmRef.Profiles.DefaultProfile.name):
                copyPaxRemOnBoard[iRow][0] = defRemOnBoard;
            elif (copyPaxRemOnBoard[iRow][1]==mmRef.Profiles.fatSlowLazy.name):
                copyPaxRemOnBoard[iRow][0] = fatRemOnBoard;
        self.paxRemOnBoard = copyPaxRemOnBoard;