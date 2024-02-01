#!/usr/bin/python3
import rospy
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
import time

class PointNavigator:
    def __init__(self, points):
        rospy.init_node('point_navigator', anonymous=True)
        self.points = points
        self.move_base = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.move_base.wait_for_server(rospy.Duration(5))

    def navigate_to_point(self, point):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.pose.position.x = point[0]
        goal.target_pose.pose.position.y = point[1]
        goal.target_pose.pose.orientation.w = 1.0

        self.move_base.send_goal(goal)
        self.move_base.wait_for_result()

    def navigate_points(self):
        for point in self.points:
            self.navigate_to_point(point)
            time.sleep(3)  # Warte 3 Sekunden

if __name__ == '__main__':
    try:
        points = [(0.6005246632133149, -0.6776412129809746), (0.5607425787850996, 0.4217468734034219), (1.6125032021020735, 0.5237475106979254), 
        (1.509958339246486, 0.19558333954969645), (1.5086980167606192, -0.5475501299138569), 
        (1.8019151461294831, -0.15583176115046346), (2.322932771181492, -0.8548445362402348), (2.476438384597017, -0.9626416879676888),
        (2.720641179153032, 0.4364358664632906), (3.054392139257511, -0.36481126057671576)]
        navigator = PointNavigator(points)
        navigator.navigate_points()
    except rospy.ROSInterruptException:
        pass 
