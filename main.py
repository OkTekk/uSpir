# -*- coding: utf-8 -*-

'''
    IO data from/to multiple sensors

    Written by Laurent Fournier, October 2016
'''

import os, sys, subprocess
import time, datetime
import serial
import argparse
import threading
import Queue

from bs4         import BeautifulSoup as bs
from lxml        import etree
from collections import Counter

# External libraries
import file_manager as fm
from tools     import *
from licor_6xx import Licor6xx
from licor_7xx import Licor7xx
from licor_8xx import Licor8xx

#-------------------------------------------------------------
#------------------ Open configurations ----------------------
#-------------------------------------------------------------

  ############
  # Terminal #
  ############

parser = argparse.ArgumentParser(description = '')
parser.add_argument('-c', '--continuous', type=bool, help='No outputs limitation', default=True,  choices=[True, False])
parser.add_argument('-C', '--config',     type=bool, help='Configuration mode',    default=False, choices=[True, False])
parser.add_argument('-d', '--debug',      type=bool, help='Debugging mode',        default=True,  choices=[True, False])
parser.add_argument('-l', '--loops',      type=int,  help='Number of outputs',     default=5)
parser.add_argument('-L', '--logging',    type=bool, help='Storing in .CSV files', default=True,  choices=[True, False])
parser.add_argument('-m', '--model',      type=int,  help='Select device model',   default=6262,  choices=[820, 840, 6262, 7000])
args = parser.parse_args()

  ############
  # Settings #
  ############

CONFIG     = args.config
CONTINUOUS = args.continuous
DEBUG      = args.debug
DEVICE     = args.model
LOG        = args.logging
LOOPS      = args.loops                                                                 # Nr of data extractions

FREQ       = 5
PORT       = '/dev/ttyUSB0'
BAUD       = 9600
PARITY     = 'N'
STOPBIT    = 1
BYTE_SZ    = 8
TIMEOUT    = 5.0
LOG_DIR    = 'logs/'

exitFlag   = 0
threadList = ["Thread-1", "Thread-2", "Thread-3"]
nameList   = ["One", "Two", "Three", "Four", "Five"]
queueLock  = threading.Lock()
workQueue  = Queue.Queue(10)
threads    = []
threadID   = 1
args_list  = { 'port' : PORT,    'baud': BAUD,             'timeout': TIMEOUT,
               'config': CONFIG, 'continuous': CONTINUOUS, 'debug': DEBUG,
               'device': DEVICE, 'log': LOG,               'loops': LOOPS }

#-------------------------------------------------------------
#------------------ Create 'thread' object -------------------
#-------------------------------------------------------------
class myThread(threading.Thread):
    def __init__(self, threadID, name, counter, **kwargs):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print "Starting " + self.name
        Licor(**kwargs)
        print "Finishing " + self.name

#-------------------------------------------------------------
#----------------- Tests for Licor sensors -------------------
#-------------------------------------------------------------
def Licor(**kwargs):
    try:                                                                                    # Connect to device
        if   DEVICE == 820 or DEVICE == 840: probe = Licor8xx(**kwargs)
        elif DEVICE == 6262:                 probe = Licor6xx(**kwargs)
        elif DEVICE == 7000:                 probe = Licor7xx(**kwargs)

        probe.connect()

    except Exception as e:
        if DEBUG: print ("ERROR: {}".format(e))
        sys.exit("Could not connect to the device")

      ###################
      # Writing routine #
      ###################
    if CONFIG:                                                                              # Configure the device if required
        try:
            #probe.config_R()
            probe.config_W()

        except Exception as e:
            if DEBUG: print ("ERROR: {}".format(e))
            sys.exit("Could not connect to the device")

      ###################
      # Reading routine #
      ###################
    filename = 'licor{0}/licor{0}-data-{1}.csv'.format(DEVICE, datetime.datetime.now())

    if LOG_DIR:                                                                             # If LOG_DIR is set, add it to filename
        filename = os.path.join(LOG_DIR, filename)

    if LOG:                                                                                 # If logging is enabled
        try:                                                                                # Verify if directory already exists
            with open(filename, 'r'): pass

        except Exception:                                                                   # If not, create them
            os.system('mkdir {}licor{}/'.format(LOG_DIR, DEVICE))
            pass

        with open(filename, 'w') as fp:
            fp.write(';'.join(probe._header))                                               # Write headers
            fp.write('\n')

            while LOOPS:
                if (datetime.datetime.now().strftime("%S") == "59" and isDone == 0):
                    isDone = 1
                    try:
                        data = probe.read()                                                     # Read from device
                        fp.write(';'.join(data))                                                # Write data
                        fp.write('\n')

                    except Exception as e:
                        if DEBUG: print ("ERROR: {}".format(e))

                else:
                    isDone = 0
                    if not CONTINUOUS: LOOPS += 1

                if not CONTINUOUS: LOOPS -= 1

            fp.close()

    else:                                                                                   # If logging is Disabled
        while LOOPS:
<<<<<<< d86ac455dd6cbda691d610feaafbecf3bfd179cc
            if (datetime.datetime.now().strftime("%S") == "00" and isDone == 0):
                isDone = 1                
                try:                
                    data = probe.read()                                                     # Read from device
                    fp.write(';'.join(data))                                                # Write data
                    fp.write('\n')
                    
                except Exception as e:
                    if DEBUG: print ("ERROR: {}".format(e))
=======
            if (datetime.datetime.now().strftime("%S") == "59" and isDone == 0):
                isDone = 1
                data = probe.read()
>>>>>>> 4a77396567bd2b4e122ad7facb0d4bbf8b1c092e

            else:
                isDone = 0
                if not CONTINUOUS: LOOPS += 1

            if not CONTINUOUS: LOOPS -= 1
<<<<<<< d86ac455dd6cbda691d610feaafbecf3bfd179cc
                
        fp.close()
            
else:                                                                                   # If logging is Disabled
    while LOOPS:
        if (datetime.datetime.now().strftime("%S") == "00" and isDone == 0):
            isDone = 1
            data = probe.read()

        else:
            isDone = 0
            if not CONTINUOUS: LOOPS += 1

        if not CONTINUOUS: LOOPS -= 1
            
=======

#-------------------------------------------------------------
#----------------------- Main program ------------------------
#-------------------------------------------------------------
# Create new threads
for tName in threadList:
    thread = myThread(threadID, tName, workQueue, args_list)
    thread.start()
    threads.append(thread)
    threadID += 1

# Fill the queue
queueLock.acquire()

for word in nameList:
    workQueue.put(word)

queueLock.release()

# Wait for queue to empty
while not workQueue.empty():
    pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
    t.join()

print "Exiting Main Thread"
>>>>>>> 4a77396567bd2b4e122ad7facb0d4bbf8b1c092e
