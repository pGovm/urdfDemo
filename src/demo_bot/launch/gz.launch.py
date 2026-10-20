import os

from launch_ros.actions import Node
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # Configuring launch params
    world = LaunchConfiguration('world')

    pkg_name = 'demo_bot'
    pkg_share = get_package_share_directory(pkg_name)
    ros_gz_sim = get_package_share_directory('ros_gz_sim')

    # Creating the gazebo launch node
    node_gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments = {'gz_args': ['-r -v 4 ', world], 'on_exit_shutdown': 'true'}.items()
    )

    node_spawn = Node(
        package = 'ros_gz_sim',
        executable = 'create',
        arguments = ['-topic', 'robot_description', '-name', 'demo_bot', '-z', '0.1'],
        output = 'screen'
    )

    bridge_params = os.path.join(pkg_share, 'config', 'gz_bridge.yaml')
    node_gz_bridge = Node(
            package = 'ros_gz_bridge',
            executable = 'parameter_bridge',
            arguments = ['--ros-args', '-p', f'config_file:={bridge_params}'],
            output = 'screen'
    )

    node_gz_image_bridge = Node(
        package='ros_gz_image',
        executable='image_bridge',
        arguments=['/camera/image_raw']
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'world',
            default_value = os.path.join(pkg_share, 'worlds', 'obstacles_primitives.sdf'),
            description = 'World SDF file with obstacles'
        ),

        node_spawn,
        node_gz_sim,
        node_gz_bridge,
        node_gz_image_bridge
    ])