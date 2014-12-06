#!/usr/bin/env python
__author__ = "Frank Vaughn(frankv@nytec.com)"
__version__ = "$Revision: 1.0 $"

import os
import csv
import json
import time
import datetime
import platform
import subprocess
import logging.handlers
import socket

hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)

data_location = "./app/static/ajax/"
json_fname = "edison.json"
LOG_LEVEL = 10
""" Set up baseline logging functionality """
LOG = logging.getLogger( __name__ )
LOG.addHandler( logging.handlers.SysLogHandler( \
   address = ( 'localhost', 514 ), \
   facility = logging.handlers.SysLogHandler.LOG_LOCAL2 ) )
LOG.setLevel( LOG_LEVEL )

def Log(log_type, msg):
    """ different types of log entries """
    print log_type, msg
    if log_type == "critical":
        LOG.critical(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + msg)
    if log_type == "warning":
        LOG.warning(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + msg)
    if log_type == "error":
        LOG.error(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + msg)
    if log_type == "debug":
        LOG.debug(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + msg)
    if log_type == "info":
        LOG.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + msg)

"""
Get the IP address for specific platform type
"""
ip_commands = {
    'Darwin': {'ipv4': "ifconfig  | grep -E 'inet.[0-9]' | grep -v '127.0.0.1' | awk '{ print $2}'", 'ipv6': "ifconfig  | grep -E 'inet6.[0-9]' | grep -v 'fe80:' | awk '{ print $2}'"},
    'Darwin2': {'ipv4': "ifconfig  | grep -E 'inet.[0-9]' | grep -v '127.0.0.1' | awk '{ print $2}'", 'ipv6': "ifconfig  | grep -E 'inet6.[0-9]' | grep -v 'fe80:' | awk '{ print $2}'"},
    'Linux': {'ipv4': "/sbin/ifconfig  | grep 'inet addr:' | grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}'", 'ipv6': "/sbin/ifconfig  | grep 'inet6 addr:' | grep -v 'fe80' | awk '{ print $3}'"},
    'Linux2': {'ipv4': "/sbin/ifconfig  | grep 'inet ' | grep -v '127.0.0.1' | awk '{ print $2}'", 'ipv6': "/sbin/ifconfig  | grep 'inet6 addr:' | grep -v 'fe80' | awk '{ print $3}'"},
}

"""
Get the MAC address for specific platform type
"""
mac_commands = {
    'Darwin': "/sbin/ifconfig  | grep 'HWaddr' | awk '{ print $5}'",
    'Darwin2': "/sbin/ifconfig  | grep 'HWaddr' | awk '{ print $5}'",
    'Linux': "/sbin/ifconfig  | grep 'HWaddr' | awk '{ print $5}'",
    'Linux2': "/sbin/ifconfig  | grep 'HWaddr' | awk '{ print $5}'"
}

def ip_addresses():
    """ 
    local ip address 
    """
    if platform.system() == "Windows":
        return [IP]
    if platform.system() != "Darwin":
        proc = subprocess.Popen(ip_commands[platform.system()]['ipv4'], shell=True, stdout=subprocess.PIPE)
        addrs = proc.communicate()
        if len(addrs) > 0:
            addr_split = addrs[0].split('\n')        
            if addr_split[0] != '':
                if addr_split[-1] == '':
                    return addr_split[0:-1]
                else:
                    return addr_split
    proc = subprocess.Popen(ip_commands[platform.system() + '2']['ipv4'], shell=True, stdout=subprocess.PIPE)
    addrs = proc.communicate()
    if len(addrs) > 0:
        addr_split = addrs[0].split('\n')
        if addr_split[0] != '':
            if addr_split[-1] == '':
                return addr_split[0:-1]
            else:
                return addr_split
    return []

def timeFromEpoch(seconds):
    return seconds + time.time()

def readData(fName):      
    '''
    Read OpenTok data from json
    '''
    try:
        data = {}
        with open(fName, 'rb') as fp:
            data = json.load(fp)
        return data
    except Exception, msg:
        Log("error","cwd "+os.getcwd())
        Log("error", "readData " + str(Exception)+str(msg))
        return None

def writeData(fName, data):
    '''
    Write OpenTok data to json
    '''
    try:
        with open(fName, 'wb') as fp:
            json.dump(data, fp) 
    except Exception, msg:
        Log("error", "writeData " + fName + str(Exception)+str(msg))
        return None

