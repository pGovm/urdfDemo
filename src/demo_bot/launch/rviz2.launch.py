import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg_path = os.path.join(get_package_share_directory('demo_bot'))
    
    node_rviz2 = Node(
        package = 'rviz2',
        executable = 'rviz2',
        output = 'screen'
    )

    return LaunchDescription([
        node_rviz2
    ])