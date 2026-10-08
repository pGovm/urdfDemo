import os

import ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    # Specifying package name and xacro file path
    pkg_path = os.path.join(get_package_share_directory('demo_bot'))
    xacro_file = os.path.join(pkg_path, 'description', 'robot.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file)

    # Create the rsp node
    params = {'robot_description': robot_description_config}
    node_robot_state_publisher = Node(
        package = 'robot_state_publisher',
        executable = 'robot_state_publisher',
        output = 'screen',
        parameters = [params]
    )

    # Launch the node
    return LaunchDescription([
        node_robot_state_publisher
    ])