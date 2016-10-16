import sys
import Leap
import time
from numpy import inf


class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        frame = controller.frame()

        # Get hands
        for hand in frame.hands:
            handType = "Left hand" if hand.is_left else "Right hand"

            # Fist Gesture
            if fistGesture(hand):
                print "You made a fist with your %s" % (handType)
                time.sleep(2)

            # Touch Gesture
            if touchGesture(hand):
                print self.finger_names[touchGesture(hand)]
                time.sleep(2)

            # Twist Gesture
            if twistGesture(hand):
                print "You twisted your %s" % (handType)
                time.sleep(2)


def fistGesture(hand):
    strength = hand.grab_strength
    if strength == 1.0:
        return True
    else:
        return False


def touchGesture(hand):
    closest = float(inf)
    leap_thumb_tip = hand.fingers[0].tip_position
    pincher = 5
    for finger in hand.fingers:
        if finger.type != 0:
            for b in range(1, 4):
                bone = finger.bone(b).next_joint
                thumb_tip_distance = bone.distance_to(leap_thumb_tip)
                if thumb_tip_distance < closest:
                    closest = thumb_tip_distance
                    pincher = finger.type

    if hand.pinch_strength == 1.0 and hand.grab_strength != 1.0:
        return pincher
    else:
        return False


def twistGesture(hand):
    normal = hand.palm_normal
    roll = normal.roll * Leap.RAD_TO_DEG
    if (hand.is_right and roll < -170) or (hand.is_left and roll > 170):
        return True
    else:
        return False


def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
