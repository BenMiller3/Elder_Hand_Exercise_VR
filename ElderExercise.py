"""
THE MAIN CODE GOES HERE


"""

import sys, thread, time
import Leap
from Leap import *    # I am just importing the whole LEAP class so don't worry about specific

# THIS class will connect the controller -- the backend process.

class LeapMotionListener(Leap.listener):
  
  fingerNames = ["Pinky","Index","Middle","Ring","Thumb"]
  boneNames = ["Metacarpal", "Proximal", "Intermediate","Distal"]
  stateNames = ["STATE_INVALID", "STATE_START", "STATE_UPDATE", "STATE_END"]
  
  def on_init(self, controller):
    print("Initialized")
    
  def on_connect(self, controller):
    print("Motion Sensor Connected")
    
    controller.enable_gestrue(Leap.Gesture.TYPE_CIRCLE);
    controller.enable_gestrue(Leap.Gesture.TYPE_KEY_TAP);
    controller.enable_gestrue(Leap.Gesture.TYPE_SCREEN+TAP);
    controller.enable_gestrue(Leap.Gesture.TYPE_SWIPE);
    
  def on_disconnect(self, controller):
    print("Motion Sensor Disconnected")
    
  def on_exit(self, controller):
    print("Exited")
    
  def on_frame(self, controller):
    pass
  
def main():
  listener = LeapMotionListener()
  controller = Leap.Controller()
  
  contoller.add_listener(listener)
  
  print("Press ENTER to quit")
  
  try:
    sys.stdin.readline()
  except KeyboardInterrupts:
    pass
  finally:
    controller.remove_listener(listener)
    
if __name__ == "__main__":
  main()
