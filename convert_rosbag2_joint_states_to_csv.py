from pathlib import Path
import csv
from datetime import datetime
import argparse
from rosbags.highlevel import AnyReader
from rosbags.typesys import Stores, get_typestore

def convert_rosbag_to_csv(bagpath, output_file='joint_states.csv'):
    # Create a type store to use if the bag has no message definitions
    typestore = get_typestore(Stores.ROS2_HUMBLE)
    joint_names = ['joint_1', 'joint_2', 'joint_3', 'joint_4', 'joint_5', 'joint_6', 'joint_7']

    # Prepare CSV headers
    headers = ['timestamp']
    for joint in joint_names:
        headers.extend([f'{joint}_pos', f'{joint}_vel', f'{joint}_effort'])
    
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
                ordered_indices = [joint_order[joint] for joint in joint_names]
                
                # Combine all data into a single row
                row = [timestamp_str]
                for i in ordered_indices:
                    row.extend([msg.position[i], msg.velocity[i], msg.effort[i]])
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