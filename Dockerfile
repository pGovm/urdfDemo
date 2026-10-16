FROM ros:jazzy-ros-base

# Setting environment variables
ENV DISPLAY=:1


# Installing required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-pip \
    python3-yaml \
    python3-rosdep \
    cmake \
    python3-argcomplete \
    python3-colcon-common-extensions \
    libboost-system-dev \
    libudev-dev \
    git \
    nano \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root

RUN git clone -b gazebo_demo https://github.com/pGovm/urdfDemo.git

WORKDIR /root/urdfDemo

# Install ROS dependencies
RUN apt-get update && \
    rosdep update

RUN rosdep install --from-paths src --ignore-src -y \
    && rm -rf /var/lib/apt/lists*

# Source ROS2 and building packages
RUN bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && \
             cd /root/urdfDemo && \
             colcon build --symlink-install"

CMD ["bash"]