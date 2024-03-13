# Author: nono_t27 

import sys
import os
import ac
import acsys
import platform
import configparser

# Magic import stuff to make sure ctypes and sim_info work properly. Gotta learn how to do this better.
if platform.architecture()[0] == "64bit":
    libdir = 'third_party_dir_lapcounter/lib64'
else:
    libdir = 'third_party_dir_lapcounter/lib'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), libdir))
os.environ['PATH'] = os.environ['PATH'] + ";."

import ctypes
from third_party_dir_lapcounter.sim_info import info
from ctypes.wintypes import MAX_PATH

bestLap = 0 
bestLapLabel = 0 
currentLap = 0
currentLapLabel = 0
lastLap = 0 
lastLapLabel = 0 
lapCounterLabel = 0 

# The main app window where everything is shown. 
def acMain(ac_version):
   global lapCounterLabel, bestLapLabel, currentLapLabel, lastLapLabel
   
   # Basic app setup.
   appWindow = ac.newApp("Lap Counter")
   ac.setSize(appWindow, 200, 200)

   # Lables the displays of the things on the app.
   lapCounterLabel = ac.addLabel(appWindow, "Lap: 1")
   bestLapLabel = ac.addLabel(appWindow, "Best Lap: ")
   lastLapLabel = ac.addLabel(appWindow, "Last Lap: ")
   currentLapLabel = ac.addLabel(appWindow, "Current Lap: ")


   ac.setPosition(lapCounterLabel, 3, 30)
   ac.setPosition(currentLapLabel, 3, 60)
   ac.setPosition(bestLapLabel, 3, 90)
   ac.setPosition(lastLapLabel, 3, 120)
   return "appName"

# Updates the window pretty much the fucntionally goes here.
def acUpdate(deltaT):
   global bestLap, currentLap, lastLap

   laps = ac.getCarState(0, acsys.CS.LapCount) + 1

   currentLap = ac.getCarState(0, acsys.CS.LapTime)
   currentLapSeconds = (currentLap / 1000) % 60
   currentLapMinutes = (currentLap // 1000) // 60
   
   bestLap = ac.getCarState(0, acsys.CS.BestLap)
   bestLapSeconds = (bestLap / 1000) % 60
   bestLapMinutes = (bestLap // 1000) // 60

   lastLap = ac.getCarState(0, acsys.CS.LastLap)
   lastLapSecond = (lastLap / 1000) % 60
   lastLapMinutes = (lastLap // 1000) // 60

   # Lap counter thing.
   ac.setText(lapCounterLabel, "Laps: {}".format(laps))
   ac.setText(currentLapLabel, "Current Lap: {}:{:06.3f}".format(currentLapMinutes, currentLapSeconds))
   ac.setText(bestLapLabel, "Best Lap: {}:{:06.3f}".format(bestLapMinutes, bestLapSeconds))
   ac.setText(lastLapLabel, "Last Lap: {}:{:06.3f}".format(lastLapMinutes, lastLapSecond))

# Initializes the user's AC folder. 
def init_ac_folder(): 
   global ac_user_folder

   dll = ctypes.windll.shell32
   buf = ctypes.create_unicode_buffer(MAX_PATH + 1)

   if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
      document_folder = buf.value
      ac_folder = os.path.join(document_folder, 'Assetto Corsa')

      if os.path.isdir(ac_folder):
         ac_user_folder = ac_folder
   
# Used for when the application exits. This is here for safety.
def acShutdown():
   return


# Pretty basic and gets the job done.