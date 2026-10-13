import os

from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, Command
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource

import xacro

def generate_launch_description():
    # Configuring launch params
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Processing the urdf file
    pkg_name = 'demo_bot'
    pkg_path = get_package_share_directory(pkg_name)
    ros_gz_sim = get_package_share_directory('ros_gz_sim')

    # Calling the rsp node
    node_rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(pkg_path, 'launch', 'rsp.launch.py')]),
        launch_arguments = {'use_sim_time': 'true'}.items()
    )

    # Creating the rviz2 launch node
    node_rviz2 = Node(
            package = 'rviz2',
            executable = 'rviz2',
            output = 'screen'
        )

    # Creating the gazebo launch node
    node_gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments = {'gz_args': '-r empty.sdf'}.items()
    )

    node_spawn = Node(
        package = 'ros_gz_sim',
        executable = 'create',
        arguments = ['-topic', 'robot_description', '-name', 'demo_bot', '-z', '0.1'],
        output = 'screen'
    )

    node_gz_bridge = Node(
        package = 'ros_gz_bridge',
        executable = 'parameter_bridge',
        arguments = [
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/tf@tf2_msgs/msg/TFMessage[gz.msg.Pose_V',
            '/joint_state@sensor_msgs/msg/JointState[gz.msgs.Model'
        ],
        output = 'screen'
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value = 'true',
            description = 'Use sim time if True'
        ),
        node_rsp,
        node_rviz2,
        node_gz_sim,
        node_spawn,
        node_gz_bridge
    ])