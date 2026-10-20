import os

from launch_ros.actions import Node
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')

    pkg_share = get_package_share_directory('demo_bot')
    mux_config = os.path.join(pkg_share, 'config', 'twist_mux.yaml')

    node_mux = Node(
        package='twist_mux',
        executable='twist_mux',
        parameters=[mux_config, {'use_sim_time': use_sim_time}],
        remappings=[("cmd_vel_out", '/diff_drive_controller/cmd_vel')],
        output='screen'
    )

    node_keyboard = Node(
        package='teleop_twist_keyboard',
        executable='teleop_twist_keyboard',
        parameters=[{'stamped': True, 'use_sim_time': use_sim_time}],
        remappings=[('/cmd_vel', '/cmd_vel_keyboard')],
        prefix='xterm -e',
        output='screen'
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use sim time if true'
        ),

        node_mux,
        node_keyboard
    ])