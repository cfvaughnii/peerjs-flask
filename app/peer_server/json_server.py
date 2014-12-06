'''
Created on Sep 17, 2014

@author: frank
'''
import os
import time
import threading
from base import data_location, json_fname, readData, writeData, Log, ip_addresses, timeFromEpoch

class PeerServer(object):
    '''
    Gather commands and call peerjs SDK
    '''


    def __init__(self, peerjs_key=None, peerjs_id=None):
        '''
        Constructor
        '''
        try:
            self.configFname = data_location + json_fname
            self.dataDict = readData(self.configFname)
            if peerjs_key:
                self.dataDict["KEY"] = peerjs_key
                writeData(self.configFname, self.dataDict)
            if peerjs_id:
                self.dataDict["ID"] = peerjs_id
                writeData(self.configFname, self.dataDict)
        except Exception, msg:
            Log("error", "peerjs_sdk "+str(Exception) + str(msg))
    
        

    @staticmethod
    def get_peerjs_info():
        try:
            ots = PeerServer()
            return ots.dataDict["KEY"], ots.dataDict["ID"]
        except Exception, msg:
            Log("error", "peerjs_sdk  generate_token "+str(Exception) + str(msg))
        return None

    @staticmethod
    def save_peerjs(peerjs_key=None, peerjs_id=None):
        try:
            ots = PeerServer(peerjs_key, peerjs_id)
            return True
        except Exception, msg:
            Log("error", "peerjs_sdk  generate_token "+str(Exception) + str(msg))
        return False
        
      
if __name__ == "__main__":
    try:
        print PeerServer().get_peerjs_info()
        
    except SystemExit:
        os._exit(0)
    except KeyboardInterrupt:
        os._exit(0)        
        
