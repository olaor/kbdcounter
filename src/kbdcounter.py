#!/usr/bin/env python

import os
import subprocess
import time
from datetime import datetime, timedelta
from optparse import OptionParser
import csv
from xlib import XEvents



class KbdCounter(object):
    def __init__(self, options):
        self.storepath=os.path.expanduser(options.storepath)

        self.muted = False
        # Pulse capture disbled by default
        self.mutecommands = ['amixer -D pulse sset Capture']
        cards = subprocess.check_output("pacmd list-cards | grep 'alsa.card =' | awk '{print $NF}' | tr -d '\"'", shell=True).split('\n')
        for card in cards:
            try:
                controls = subprocess.check_output("amixer -c %s scontrols 2> /dev/null" % card , shell=True)
            except:
                controls = False
            if controls:
                for control in controls.split("\n"):
                    if not control:
                        continue
                    controlname = control.split("'")[1]
                    if controlname not in ["Headset", "Capture"]:
                        continue
                    print "Added control for %s on card %s" % (controlname, card)
                    self.mutecommands.append("amixer -c %s sset %s" % (card, controlname))
                    
            
        self.set_thishour()
        self.set_nextsave()
        self.read_existing()

    def togglemute(self):
        if self.muted == True:
            action = "cap"
        else:
            action = "nocap"
            
        for command in self.mutecommands:
            os.system("%s %s 2>&1 > /dev/null" % (command, action))

        return
    
    def set_thishour(self):
        self.thishour = datetime.now().replace(minute=0, second=0, microsecond=0)
        self.nexthour = self.thishour + timedelta(hours=1)
        self.thishour_count = 0

    def set_nextsave(self):
        now = time.time()
        self.nextsave = now + min((self.nexthour - datetime.now()).seconds+1, 300)

    def read_existing(self):

        if os.path.exists(self.storepath):
            thishour_repr = self.thishour.strftime("%Y-%m-%dT%H")
            for (hour, value) in csv.reader(open(self.storepath)):
                if hour == thishour_repr:
                    self.thishour_count = int(value)
                    break
        

    def save(self):
        self.set_nextsave()        
        if self.thishour_count == 0:
            return 
        
        tmpout = csv.writer(open("%s.tmp" % self.storepath, 'w'))
        thishour_repr = self.thishour.strftime("%Y-%m-%dT%H")        

        if os.path.exists(self.storepath):
            for (hour, value) in csv.reader(open(self.storepath)):
                if hour != thishour_repr:
                    tmpout.writerow([hour, value])

        tmpout.writerow([thishour_repr, self.thishour_count])
        os.rename("%s.tmp" % self.storepath, self.storepath)


    def run(self):
        events = XEvents()
        events.start()

        lastkeyat = time.time()
        
        while not events.listening():
            # Wait for init
            time.sleep(1)

        try:
            while events.listening():
                evt = events.next_event()

                if time.time() - lastkeyat > 0.75 and self.muted:
                    self.togglemute()
                    self.muted = False

                if not evt:
                    time.sleep(0.5)
                    continue
                
                if evt.type != "EV_KEY" or evt.value != 1: # Only count key down, not up.
                    continue

                if not self.muted and not "BTN_" in evt.code:
                    self.togglemute()
                    self.muted = True
                    
                lastkeyat = time.time()
                    
                self.thishour_count+=1
            
                if time.time() > self.nextsave:
                    self.save()
            
                    if datetime.now().hour != self.thishour.hour:
                        self.set_thishour()
            
        except KeyboardInterrupt:
            events.stop_listening()
            self.save()

            

if __name__ == '__main__':
    oparser = OptionParser()
    oparser.add_option("--storepath", dest="storepath",
                       help="Filename into which number of keypresses per hour is written",
                       default="~/.kbdcounter.db")

    (options, args) = oparser.parse_args()

    kc = KbdCounter(options)
    kc.run()

    
    
