# convert_rosbag2_commands_to_csv.py
from pathlib import Path
import csv
from datetime import datetime
import argparse
from rosbags.highlevel import AnyReader
from rosbags.typesys import Stores, get_typestore

def get_command_topics(reader):
    """Get all command topics from the bag"""
    command_topics = [x.topic for x in reader.connections if x.topic.endswith('/command')]
    return sorted(command_topics)

def convert_commands_to_csv(bagpath, output_file='commands.csv'):
    typestore = get_typestore(Stores.ROS2_HUMBLE)
    
    print(f"Reading ROS2 bag from '{bagpath}'...")
    
    with AnyReader([Path(bagpath)], default_typestore=typestore) as reader:
        # コマンドトピックの取得
        command_topics = get_command_topics(reader)
        if not command_topics:
            print("Error: No command topics found in the bag")
            return
            
        print(f"Found command topics: {', '.join(command_topics)}")
        
        # ヘッダーの準備
        headers = ['timestamp', 'topic']
        # データの最初のメッセージを読んで配列の長さを確認
        for connection, _, rawdata in reader.messages(connections=[x for x in reader.connections if x.topic in command_topics]):
            msg = reader.deserialize(rawdata, connection.msgtype)
            if hasattr(msg, 'data'):
                headers.extend([f'command_{i+1}' for i in range(len(msg.data))])  # インデックスを1から開始
            break
        
        print(f"Command values will be saved to: {output_file}")
        
        with open(output_file, 'w', newline='') as commands_file:
            commands_writer = csv.writer(commands_file)
            commands_writer.writerow(headers)
            
            command_connections = [x for x in reader.connections if x.topic in command_topics]
            commands_count = 0
            
            for connection, timestamp, rawdata in reader.messages(connections=command_connections):
                msg = reader.deserialize(rawdata, connection.msgtype)
                if hasattr(msg, 'data'):
                    # タイムスタンプの変換
                    timestamp_sec = timestamp * 1e-9
                    timestamp_str = datetime.fromtimestamp(timestamp_sec).strftime('%Y-%m-%d %H:%M:%S.%f')
                    
                    # データの作成
                    row_data = [timestamp_str, connection.topic]
                    row_data.extend(msg.data)
                    
                    commands_writer.writerow(row_data)
                    commands_count += 1

    print(f"Conversion complete!")
    print(f"Processed {commands_count} command messages")

def main():
    parser = argparse.ArgumentParser(
        description='Convert ROS2 command messages from a rosbag to CSV'
    )
    parser.add_argument(
        'bagpath',
        type=str,
        help='Path to the ROS2 bag directory'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='commands.csv',
        help='Output CSV filename (default: commands.csv)'
    )

    args = parser.parse_args()
    convert_commands_to_csv(args.bagpath, args.output)

if __name__ == '__main__':
    main()