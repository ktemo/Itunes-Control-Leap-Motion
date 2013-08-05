import Leap
import sys
import math
from Leap import SwipeGesture

# bridge with itunes
from Foundation import *
from ScriptingBridge import *
# ------


class SampleListener(Leap.Listener):
    iTunes = None
    swipe_start = False
    swipe_start_position = None
    swipe_start_direction = None

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        self.iTunes = SBApplication.applicationWithBundleIdentifier_("com.apple.iTunes")
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        if not frame.hands.empty:
            # Gestures
            for gesture in frame.gestures():
                if gesture.type == Leap.Gesture.TYPE_SWIPE:
                    self.swipe(gesture)

                if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                    self.screen_tap(gesture)

    def swipe(self, gesture):
        swipe = SwipeGesture(gesture)

        if gesture.state == Leap.Gesture.STATE_START:
            x, y, z = swipe.direction.to_float_array()
            #horizontal gesture
            if abs(x) > abs(y):
                self.swipe_start = True
                self.swipe_start_position = swipe.position
                self.swipe_start_direction = swipe.direction

        if gesture.state == Leap.Gesture.STATE_UPDATE:
            x, y, z = swipe.direction.to_float_array()
            #vertical gesture
            if abs(x) < abs(y):
                #upward
                if y > 0:
                    self.iTunes.setSoundVolume_(self.iTunes.soundVolume() + 1)
                else:
                    self.iTunes.setSoundVolume_(self.iTunes.soundVolume() - 1)

        if gesture.state == Leap.Gesture.STATE_STOP:
            if self.swipe_start:
                self.swipe_start = False
                distance = self.swipe_start_position.distance_to(swipe.position)
                if(distance > 20):
                    x, y, z = self.swipe_start_direction.to_float_array()
                    if x > 0:
                        #left to rigth
                        self.iTunes.nextTrack()
                    else:
                        #rigth to left
                        self.iTunes.nextTrack()

                    print "next song: ", self.iTunes.currentTrack().name()

    def screen_tap(self, gesture):
        self.iTunes.playpause()
        print "play / pausa"


def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()

    # Remove the sample listener when done
    controller.remove_listener(listener)


if __name__ == "__main__":
    main()
