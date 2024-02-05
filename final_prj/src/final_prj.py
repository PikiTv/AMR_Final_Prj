#!/usr/bin/python3
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped   
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
import time

def navigate_points():
    global robo_position_x
    global robo_position_y

    while len(points_1_to_6) > 0:
        distances = [((point[0] - robo_position_x)**2 + (point[1] - robo_position_y)**2)**0.5 for point in points_1_to_6]
        nearest_index = distances.index(min(distances))
        navigate_to_point(points_1_to_6[nearest_index])
        robo_position_x = points_1_to_6[nearest_index][0]
        robo_position_y = points_1_to_6[nearest_index][1]
        points_1_to_6.pop(nearest_index)
        time.sleep(3)

        if robo_position_x == 1.8019151461294831 and robo_position_y == -0.15583176115046346:
            while len(points_7_to_10) > 0:
                distances = [((point[0] - robo_position_x)**2 + (point[1] - robo_position_y)**2)**0.5 for point in points_7_to_10]
                nearest_index = distances.index(min(distances))
                navigate_to_point(points_7_to_10[nearest_index])
                robo_position_x = points_7_to_10[nearest_index][0]
                robo_position_y = points_7_to_10[nearest_index][1]
                points_7_to_10.pop(nearest_index)
                time.sleep(3)

def navigate_to_point(point):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.pose.position.x = point[0]
    goal.target_pose.pose.position.y = point[1]
    goal.target_pose.pose.orientation.w = 1.0

    move_base.send_goal(goal)
    move_base.wait_for_result()

def callback(msg):
    global robo_position_x
    global robo_position_y
    robo_position_x = msg.pose.pose.position.x
    robo_position_y = msg.pose.pose.position.y
    print("Roboterposition anfang:", robo_position_x, robo_position_y)
    sub.unregister()

rospy.init_node('competition')
robo_position_x = None
robo_position_y = None
sub = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, callback)
move_base = actionlib.SimpleActionClient('move_base', MoveBaseAction)
move_base.wait_for_server(rospy.Duration(5))

points_1_to_6 =  [(0.6005246632133149, -0.6776412129809746),  (0.5607425787850996, 0.4217468734034219), 
                  (1.6125032021020735, 0.5237475106979254),   (1.509958339246486, 0.19558333954969645),   
                  (1.5086980167606192, -0.5475501299138569),  (1.8019151461294831, -0.15583176115046346)]

points_7_to_10 = [(2.322932771181492, -0.8548445362402348),   (2.476438384597017, -0.9626416879676888),
                  (2.720641179153032, 0.4364358664632906),    (3.054392139257511, -0.36481126057671576)]

navigate_points()
