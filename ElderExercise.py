import sys
import Leap
import time
from numpy import inf
killer = False


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

    level = 0
    count = 10
    f_count = 1
    hand_assert = "right"

    def on_frame(self, controller):
        frame = controller.frame()

        # Get hands
        for hand in frame.hands:
            handType = "Left hand" if hand.is_left else "Right hand"

            # Fist Gesture
            if self.level == 0:
                print "Exercise 1"
                print "Make a fist with your right hand"
                print "Remaining: %d" % (self.count)
                self.level += 1
            if self.level == 1 and self.count > 1:
                if fistGesture(hand) and hand.is_right:
                    print "You made a fist with your %s" % (handType)
                    print "Remaining: %d" % (self.count - 1)
                    time.sleep(2)
                    self.count -= 1
            elif self.level == 1 and self.count == 1:
                self.count = 10
                self.level += 1
                print "Make a fist with your left hand"
                print "Remaining: %d" % (self.count)
            elif self.level == 2 and self.count > 1:
                if fistGesture(hand) and hand.is_left:
                    print "You made a fist with your %s" % (handType)
                    print "Remaining: %d" % (self.count - 1)
                    time.sleep(2)
                    self.count -= 1
            elif self.level == 2 and self.count == 1:
                print "Exercise 2"
                print "Touch your %s finger to your thumb (%s Hand)" % (self.finger_names[self.f_count], self.hand_assert)
                self.count = 10
                self.level += 1
            elif self.level == 3 and self.count > -1:
                if self.hand_assert == "right":
                    # Touch Gesture
                    if touchGesture(hand):
                        if touchGesture(hand) == self.f_count:
                            print self.finger_names[touchGesture(hand)]
                            if self.f_count < 4:
                                self.f_count += 1
                            else:
                                self.f_count = 1
                                self.hand_assert = "left"
                            print "Touch your %s finger to your thumb (%s Hand)" % (self.finger_names[self.f_count], self.hand_assert)
                            time.sleep(2)
                        self.count -= 1
                elif self.hand_assert == "left":
                    # Touch Gesture
                    if touchGesture(hand):
                        if touchGesture(hand) == self.f_count:
                            print self.finger_names[touchGesture(hand)]
                            if self.f_count < 4:
                                self.f_count += 1
                            else:
                                self.f_count = 1
                                self.hand_assert = "right"
                            print "Touch your %s finger to your thumb (%s Hand)" % (self.finger_names[self.f_count], self.hand_assert)
                            time.sleep(2)
                        self.count -= 1

            elif self.level == 3 and self.count == -1:
                self.count = 10
                self.level += 1
                print "Exercise 3"
                print "Place your right hand horizontally, palm downward"
                print "Point your fingers towards the screen"
                print "Rotate your hand until your palm faces upward"
                print "Remaining: %d" % (self.count)
            elif self.level == 4 and self.count > 1:
                # Twist Gesture
                if twistGesture(hand) and hand.is_right:
                    print "You twisted your %s" % (handType)
                    print self.count - 1
                    time.sleep(2)
                    self.count -= 1
            elif self.level == 4 and self.count == 1:
                self.count = 10
                self.level += 1
                print "Do the same with your left hand"
            elif self.level == 5 and self.count > 1:
                # Twist Gesture
                if twistGesture(hand) and hand.is_left:
                    print "You twisted your %s" % (handType)
                    print self.count - 1
                    time.sleep(2)
                    self.count -= 1
            elif self.level == 5 and self.count == 1:
                print "Congrats! You did it!"
                killer = True


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
