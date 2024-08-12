import rospy

def initialize_node():
    rospy.init_node('my_node', anonymous=True)
    rospy.loginfo("Node initialized")

# publisher
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('/chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1)  # 1 Hz

    while not rospy.is_shutdown():
        hello_str = "Hello ROS %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()
