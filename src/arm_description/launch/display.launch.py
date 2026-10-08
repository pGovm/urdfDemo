import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory("arm_description")

    # Includes the existing rsp.launch.py which runs xacro on the urdf file
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, 'launch', 'rsp.launch.py')
        )
    )

    # GUI sliders to move each joint independently
    joint_state_publisher_gui = Node(
        package = 'joint_state_publisher_gui',
        executable = 'joint_state_publisher_gui',
        output = 'screen'
    )

    rviz2 = Node(
        package = 'rviz2',
        executable = 'rviz2',
        output = 'screen'
    )

    return LaunchDescription([
        rsp,
        joint_state_publisher_gui,
        rviz2
    ])
