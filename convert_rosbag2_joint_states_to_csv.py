from pathlib import Path
import csv
from datetime import datetime
import argparse
from rosbags.highlevel import AnyReader
from rosbags.typesys import Stores, get_typestore

def convert_rosbag_to_csv(bagpath, output_file='joint_states.csv'):
    # Create a type store to use if the bag has no message definitions
    typestore = get_typestore(Stores.ROS2_HUMBLE)
    
    # Prepare CSV headers
    #headers = ['timestamp', 
    #          'joint_1_pos', 'joint_2_pos', 'joint_3_pos', 'joint_4_pos', 'joint_5_pos', 'joint_6_pos', 'joint_7_pos',
    #          'joint_1_vel', 'joint_2_vel', 'joint_3_vel', 'joint_4_vel', 'joint_5_vel', 'joint_6_vel', 'joint_7_vel',
    #          'joint_1_effort', 'joint_2_effort', 'joint_3_effort', 'joint_4_effort', 'joint_5_effort', 'joint_6_effort', 'joint_7_effort']
    #headers = ['timestamp', 'joint_3_pos', 'joint_3_vel', 'joint_3_effort']
    headers = ['timestamp', 'joint_1_pos', 'joint_1_vel', 'joint_1_effort']

    print(f"Converting ROS2 bag from '{bagpath}' to CSV file '{output_file}'...")

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        
        # Create reader instance and open for reading
        with AnyReader([Path(bagpath)], default_typestore=typestore) as reader:
            connections = [x for x in reader.connections if x.topic == '/joint_states']
            
            message_count = 0
            for connection, timestamp, rawdata in reader.messages(connections=connections):
                msg = reader.deserialize(rawdata, connection.msgtype)
                
                # Convert ROS timestamp to human-readable format
                timestamp_sec = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
                timestamp_str = datetime.fromtimestamp(timestamp_sec).strftime('%Y-%m-%d %H:%M:%S.%f')
                
                # Reorder joints to match the header order (1-7)
                joint_order = {name: i for i, name in enumerate(msg.name)}
                ordered_indices = [joint_order[f'joint_{i}'] for i in range(1, 2)]
                
                # Extract data in correct order
                positions = [msg.position[i] for i in ordered_indices]
                velocities = [msg.velocity[i] for i in ordered_indices]
                efforts = [msg.effort[i] for i in ordered_indices]
                
                # Combine all data into a single row
                row = [timestamp_str] + positions + velocities + efforts
                writer.writerow(row)
                message_count += 1

    print(f"Conversion complete! Processed {message_count} messages.")

def main():
    parser = argparse.ArgumentParser(
        description='Convert ROS2 joint_states messages from a rosbag to CSV format'
    )
    parser.add_argument(
        'bagpath',
        type=str,
        help='Path to the ROS2 bag directory'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='joint_states.csv',
        help='Output CSV filename (default: joint_states.csv)'
    )

    args = parser.parse_args()
    convert_rosbag_to_csv(args.bagpath, args.output)

if __name__ == '__main__':
    main()