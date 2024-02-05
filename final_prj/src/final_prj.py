#!/usr/bin/python3
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped   
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
import time

class PointNavigator:
    def __init__(this, points): #Constructor
        rospy.init_node('point_navigator', anonymous=True)
        this.points = points
        this.move_base = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        this.move_base.wait_for_server(rospy.Duration(5))

    def navigate_points(this):
        global robo_position_x
        global robo_position_y
        while this.points:
            distances = [((point[0] - robo_position_x)**2 + (point[1] - robo_position_y)**2)**0.5 for point in this.points]
            print(distances)
            nearest_index = distances.index(min(distances))
            this.navigate_to_point(this.points[nearest_index])
            robo_position_x = this.points[nearest_index][0]
            robo_position_y = this.points[nearest_index][1]
            this.points.pop(nearest_index) 
            time.sleep(3)

    def navigate_to_point(this, point):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.pose.position.x = point[0]
        goal.target_pose.pose.position.y = point[1]
        goal.target_pose.pose.orientation.w = 1.0

        this.move_base.send_goal(goal)
        this.move_base.wait_for_result()

def callback(msg):
    global robo_position_x
    global robo_position_y
    robo_position_x = msg.pose.pose.position.x
    robo_position_y = msg.pose.pose.position.y
    print("Roboterposition anfang:", robo_position_x, robo_position_y)
    sub.unregister()


robo_position_x = None
robo_position_y = None
sub = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, callback)
points = [(0.6005246632133149, -0.6776412129809746),  (0.5607425787850996, 0.4217468734034219), 
          (1.6125032021020735, 0.5237475106979254),   (1.509958339246486, 0.19558333954969645),   
          (1.5086980167606192, -0.5475501299138569),  (1.8019151461294831, -0.15583176115046346), 
          (2.322932771181492, -0.8548445362402348),   (2.476438384597017, -0.9626416879676888),
          (2.720641179153032, 0.4364358664632906),    (3.054392139257511, -0.36481126057671576)]
navigator = PointNavigator(points)
navigator.navigate_points()

        

     
