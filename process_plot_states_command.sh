#!/bin/bash
#シェルスクリプトのディレクトリを取得
shell_dir=$(cd $(dirname $0); pwd)
#csvファイルのディレクトリを取得
csv_dir=$(dirname $(dirname $shell_dir)) 

echo $csv_dir

#python3 plot_states_command.py -j 20241121_motor2_effort_3000_joint_states.csv -c 20241121_motor2_effort_3000_commands.csv -n 2 -o 20241121_motor2_effort_3000
python3 $shell_dir/plot_states_command.py -j $csv_dir/20241121_motor2_effort_3000_joint_states.csv -c $csv_dir/20241121_motor2_effort_3000_command.csv -n 2 -o 20241121_motor2_effort_3000
#20241121_motor2_position_180_10s
#python3 plot_states_command.py -j 20241121_motor2_position_180_10s_joint_states.csv -c 20241121_motor2_position_180_10s_command.csv -n 2 -o 20241121_motor2_position_180_10s
python3 $shell_dir/plot_states_command.py -j $csv_dir/20241121_motor2_position_180_10s_joint_states.csv -c $csv_dir/20241121_motor2_position_180_10s_command.csv -n 2 -o 20241121_motor2_position_180_10s
##20241121_motor2_velocity_30000
#python3 plot_states_command.py -j 20241121_motor2_velocity_30000_joint_states.csv -c 20241121_motor2_velocity_30000_command.csv -n 2 -o 20241121_motor2_velocity_30000
python3 $shell_dir/plot_states_command.py -j $csv_dir/20241121_motor2_velocity_30000_joint_states.csv -c $csv_dir/20241121_motor2_velocity_30000_command.csv -n 2 -o 20241121_motor2_velocity_30000
##20241121_motor4_effort_3000
#python3 plot_states_command.py -j 20241121_motor4_effort_3000_joint_states.csv -c 20241121_motor4_effort_3000_command.csv -n 4 -o 20241121_motor4_effort_3000
python3 $shell_dir/plot_states_command.py -j $csv_dir/20241121_motor4_effort_3000_joint_states.csv -c $csv_dir/20241121_motor4_effort_3000_command.csv -n 4 -o 20241121_motor4_effort_3000
##20241121_motor4_position_180_10s
#python3 plot_states_command.py -j 20241121_motor4_position_180_10s_joint_states.csv -c 20241121_motor4_position_180_10s_command.csv -n 4 -o 20241121_motor4_position_180_10s
python3 $shell_dir/plot_states_command.py -j $csv_dir/20241121_motor4_position_180_10s_joint_states.csv -c $csv_dir/20241121_motor4_position_180_10s_command.csv -n 4 -o 20241121_motor4_position_180_10s
##20241121_motor4_velocity_30000
#python3 plot_states_command.py -j 20241121_motor4_velocity_30000_joint_states.csv -c 20241121_motor4_velocity_30000_command.csv -n 4 -o 20241121_motor4_velocity_30000
python3 $shell_dir/plot_states_command.py -j $csv_dir/20241121_motor4_velocity_30000_joint_states.csv -c $csv_dir/20241121_motor4_velocity_30000_command.csv -n 4 -o 20241121_motor4_velocity_30000
