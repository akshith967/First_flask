from ros import initialize_node, talker
from unittest.mock import patch, MagicMock

@patch('ros.rospy')
def test_initialize_node(mock_rospy):
    # Call the function you want to test
    initialize_node()
    # Assert that rospy.init_node was called with specific arguments
    mock_rospy.init_node.assert_called_once_with('my_node', anonymous=True)
    mock_rospy.loginfo.assert_called_once_with("Node initialized")
@patch('ros.rospy')
def test_talker(mock_rospy):
    # Mock the Publisher
    mock_publisher = MagicMock()
    mock_rospy.Publisher.return_value = mock_publisher

    # Mock the get_time and loginfo
    mock_rospy.get_time.return_value = '123456'
    mock_rospy.is_shutdown.side_effect = [False, True]  # Stop after one iteration

    # Run the talker function
    talker()

    # Check that init_node was called
    mock_rospy.init_node.assert_called_once_with('talker', anonymous=True)

    # Check that publish was called with the correct message
    mock_publisher.publish.assert_called_once_with("Hello ROS 123456")

    # Check that loginfo was called with the correct message
    mock_rospy.loginfo.assert_called_with("Hello ROS 123456")