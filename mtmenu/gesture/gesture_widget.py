import sys
sys.path.append("..")

from pymt import *
import subprocess
from datetime import datetime

from projectors_interface import is_projectors_on, set_projectors_on, in_schedule, set_last_activity, get_projectors_down_duration
from mtmenu.application_running import is_app_running, kill_app_running
from gesture.gesture_db import *
from config import GESTURE_ACCEPTANCE_MARGIN, PRODUCTION, UNAVAILABLE_PROJECTORS_TIME
from webmanager.appman.utils import projectors

class GestureWidget( MTGestureWidget ):
    def __init__(self):
        super(GestureWidget, self).__init__()
        self.gestures = Gestures()
        self.counter = 0
        print 'Gesture loaded'

    def on_gesture(self, gesture, touch):
        if not is_projectors_on() and in_schedule():
            try:
                print "duration since inactivity = %s" % get_projectors_down_duration()
                if get_projectors_down_duration() > UNAVAILABLE_PROJECTORS_TIME:
                    projectors.projectors_power(1)
                    set_projectors_on(True)
                    print "projectors power on"
                else:
                    print "projectors cannot be turned on because their down for few time"
                
            except Exception as e: #Pokemon
                print 'Error turning projectors on'
                print e
                if not PRODUCTION: 
                    set_projectors_on(True) 
        
        set_last_activity()
            
        print 'gesture: %d' % self.counter
        self.counter += 1
        #print self.gestures.gesture_to_str(gesture)
        
        # gesture recognition
        if self.gestures.find(gesture, GESTURE_ACCEPTANCE_MARGIN) and is_app_running():
            print "gesture recognized"
            kill_app_running()
            

