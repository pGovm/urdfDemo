import os

from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # Processing the urdf file
    pkg_name = 'demo_bot'
    pkg_share = get_package_share_directory(pkg_name)

    # Calling the rsp node
    node_rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(pkg_share, 'launch', 'rsp.launch.py')]),
        launch_arguments = {'use_sim_time': 'true'}.items()
    )

    # Calling the rviz2 launch node
    node_rviz2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(pkg_share, 'launch', 'rviz2.launch.py')])
    )

    # Calling the gazebo nodes
    node_gz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(pkg_share, 'launch', 'gz.launch.py')])
    )

    # ROS2 controller nodes
    node_diff_spawner = Node(
        package = 'controller_manager',
        executable = 'spawner',
        arguments = ['diff_drive_controller', '--controller-manager-timeout', '60']
    )

    node_joint_broad_spawner = Node(
        package = 'controller_manager',
        executable = 'spawner',
        arguments = ['joint_broad', '--controller-manager-timeout', '60']
    )

    return LaunchDescription([
        node_gz,
        node_rsp,
        node_rviz2,
        node_diff_spawner,
        node_joint_broad_spawner
    ])