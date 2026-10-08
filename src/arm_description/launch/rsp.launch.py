import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    # Specifying package name and xacro file path
    pkg_name = 'arm_description'
    file_subpath = 'description/example_robot.urdf.xacro'

    # Processing file with xacro
    xacro_file = os.path.join(get_package_share_directory(pkg_name), file_subpath)
    robot_description_raw = xacro.process_file(xacro_file).toxml()

    # Configuring the node
    node_robot_state_publisher = Node(
        package = 'robot_state_publisher',
        executable = 'robot_state_publisher',
        output = 'screen',
        parameters = [{'robot_description': robot_description_raw}]
    )

    # Running the node
    return LaunchDescription([
        node_robot_state_publisher
    ])