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

        if robo_position_x == 1.8429984853420682  and robo_position_y == -0.1617990672953716:
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

points_1_to_6 =  [(0.5501051104825838, -0.6613339040071848),  (0.7042378844427495, 0.40062969535519694), 
                  (1.585038196175153, 0.525089589836042),   (1.4976576705609883, 0.22688055532593648),   
                  (1.3981962101741294, -0.5562330174384863),  (1.8429984853420682,-0.1617990672953716)]

points_7_to_10 = [(2.21536315872618953,  -0.762704286852852),   (2.632011350334101, -0.9169242855145681),
                  (2.5868600606513574, 0.49600983491037404),    (3.1377350106707613,-0.24128989724875355)]

navigate_points()
