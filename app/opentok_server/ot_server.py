'''
Created on Sep 17, 2014

@author: frank
'''
import os
import time
import threading
from opentok import Roles, opentok
from base import data_location, json_fname, readData, writeData, Log, ip_addresses, timeFromEpoch

class OpenTokServer(object):
    '''
    Gather commands and call OpenTok SDK
    '''


    def __init__(self):
        '''
        Constructor
        '''
        try:
            self.configFname = data_location + json_fname
            self.dataDict = readData(self.configFname)
            self.opentok_sdk = None
            self.opentok_sdk = opentok.OpenTok(self.dataDict["KEY"], self.dataDict["SECRET"], api_url='https://api.opentok.com')
        except Exception, msg:
            Log("error", "openTok_sdk "+str(Exception) + str(msg))
    
        
    def create_session(self):
        '''
            if no session id is stored in persistant data, create one
                using the local ip as sessionAddress.  And the opentok_sdk object derived from persistent data.
            return session_id or "" if error occurs
        '''
        try:
            sessionAddress = ip_addresses()[0]
            if not self.dataDict.has_key("SESSION_ID"):
                session = self.opentok_sdk.create_session(sessionAddress, opentok.MediaModes.routed)
                self.dataDict["SESSION_ID"] = session.session_id
                writeData(self.configFname, self.dataDict)
                return session.session_id
        except Exception, msg:
            Log("error", "openTok_sdk create_session "+str(Exception) + str(msg))
        return ""
    
    @staticmethod
    def start_archive(session_id=""):
        try:
            archive_id = ""
            ots = OpenTokServer()
            if not ots.opentok_sdk:
                return None, None
            if len(session_id) > 0:
                ots.dataDict["SESSION_ID"] = session_id
            else:
                ots.create_session()
            archive = ots.opentok_sdk.start_archive(ots.dataDict["SESSION_ID"], name=u'Important Presentation')

            # Store this archive_id in the database
            archive_id = archive.id
            return ots.dataDict["SESSION_ID"], archive_id
        except Exception, msg:
            Log("error", "openTok_sdk  start_archive "+str(Exception) + str(msg))
        return False

    @staticmethod
    def stop_archive(archive_id=""):
        try:
            ots = OpenTokServer()
            if not ots.opentok_sdk:
                return False
            # Stop an Archive from an archive_id (fetched from database)
            archive = opentok.stop_archive(archive_id)
            # Stop an Archive from an instance (returned from opentok.start_archive)
            archive.stop()
            return True
        except Exception, msg:
            Log("error", "openTok_sdk  stop_archive "+str(Exception) + str(msg))
        return False
        
    @staticmethod
    def get_archive(archive_id=""):
        try:
            ots = OpenTokServer()
            if not ots.opentok_sdk:
                return None
            # Get an Archive from an archive_id (fetched from database)
            archive = opentok.get_archive(archive_id)
            # Stop an Archive from an instance (returned from opentok.start_archive)
            return str(archive)
        except Exception, msg:
            Log("error", "openTok_sdk  stop_archive "+str(Exception) + str(msg))
        return None
        
    @staticmethod
    def delete_archive(archive_id=""):
        try:
            ots = OpenTokServer()
            if not ots.opentok_sdk:
                return False
            # Delete an Archive from an archive_id (fetched from database)
            opentok.delete_archive(archive_id)
            return True
        except Exception, msg:
            Log("error", "openTok_sdk  stop_archive "+str(Exception) + str(msg))
        return False
        
    @staticmethod
    def list_archives():
        try:
            ots = OpenTokServer()
            if not ots.opentok_sdk:
                return "No LIst"
            # Delete an Archive from an archive_id (fetched from database)
            archive_list = opentok.list_archive()

            # Get a specific Archive from the list
            #archive = archive_list.items[i]

            # Iterate over items
            return str(archive_list)
            #for archive in iter(archive_list):
              
        except Exception, msg:
            Log("error", "openTok_sdk  stop_archive "+str(Exception) + str(msg))
        return "No List"

    @staticmethod
    def generate_token(session_id="", expiration_in_seconds=0, metadata="project=edison, foo=bar"):
        try:
            ots = OpenTokServer()
            if not ots.opentok_sdk:
                return None
            if len(session_id) > 0:
                ots.dataDict["SESSION_ID"] = session_id
            else:
                ots.create_session()
            connectionMetadata = metadata
            if expiration_in_seconds == 0:
                expiration_in_seconds = 7.0 * 24.0 * 3600.0
            expiration = timeFromEpoch( expiration_in_seconds )
            token = ots.opentok_sdk.generate_token(ots.dataDict["SESSION_ID"], Roles.moderator, expiration, connectionMetadata)
            return ots.dataDict["KEY"], ots.dataDict["SESSION_ID"], token, expiration
        except Exception, msg:
            Log("error", "openTok_sdk  generate_token "+str(Exception) + str(msg))
        return None
        
      
if __name__ == "__main__":
    try:
        print OpenTokServer().generate_token()
        
    except SystemExit:
        os._exit(0)
    except KeyboardInterrupt:
        os._exit(0)        
        
