import os

from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # Configuring launch params
    world = LaunchConfiguration('world')

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
    node_rviz2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(pkg_path, 'launch', 'rviz2.launch.py')])
    )

    # Creating the gazebo launch node
    node_gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments = {'gz_args': ['-r -v 4 ', world]}.items()
    )

    node_spawn = Node(
        package = 'ros_gz_sim',
        executable = 'create',
        arguments = ['-topic', 'robot_description', '-name', 'demo_bot', '-z', '0.1'],
        output = 'screen'
    )

    node_diff_spawner = Node(
        package = 'controller_manager',
        executable = 'spawner',
        arguments = ['diff_driveCont', '--controller-manager-timeout', '60']
    )

    node_joint_broad_spawner = Node(
        package = 'controller_manager',
        executable = 'spawner',
        arguments = ['joint_broad', '--controller-manager-timeout', '60']
    )

    node_gz_bridge = Node(
        package = 'ros_gz_bridge',
        executable = 'parameter_bridge',
        arguments = [
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan'    
        ],
        output = 'screen'
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'world',
            default_value = os.path.join(pkg_path, 'worlds', 'obstacles.sdf'),
            description = 'World SDF file with obstacles'
        ),

        node_rsp,
        node_rviz2,
        node_gz_sim,
        node_spawn,
        node_diff_spawner,
        node_joint_broad_spawner,
        node_gz_bridge
    ])