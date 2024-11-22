#!/bin/bash
shell_dir=$(cd $(dirname $0); pwd)
cd $shell_dir
./convert_rosbag2_to_csv.sh ../../rosbag2_2024_11_21-15_14_41_motor2_position_180_10s ../../20241121_motor2_position_180_10s 
./convert_rosbag2_to_csv.sh ../../rosbag2_2024_11_21-15_20_20_motor2_velocity_30000 ../../20241121_motor2_velocity_30000
./convert_rosbag2_to_csv.sh ../../rosbag2_2024_11_21-15_23_02_motor2_effort_3000 ../../20241121_motor2_effort_3000
./convert_rosbag2_to_csv.sh ../../rosbag2_2024_11_21-15_46_28_motor4_position_180_10s ../../20241121_motor4_position_180_10s
./convert_rosbag2_to_csv.sh ../../rosbag2_2024_11_21-16_30_12_motor4_effort_3000 ../../20241121_motor4_effort_3000
./convert_rosbag2_to_csv.sh ../../rosbag2_2024_11_21-18_28_17_motor4_velocity_30000 ../../20241121_motor4_velocity_30000
