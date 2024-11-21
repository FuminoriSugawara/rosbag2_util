import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

def load_and_convert_time(df):
    """タイムスタンプを datetime オブジェクトに変換"""
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def get_available_joints(joint_states_df):
    """利用可能なジョイント番号を取得"""
    joints = []
    for col in joint_states_df.columns:
        if col.endswith('_effort'):
            joint_num = col.split('_')[1]
            if joint_num.isdigit():
                joints.append(int(joint_num))
    return sorted(joints)

def ensure_output_dir(output_dir):
    """出力ディレクトリが存在しない場合は作成"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def plot_effort_command_comparison(joint_states_file, commands_file, output_dir='plots'):
    # 出力ディレクトリの作成
    ensure_output_dir(output_dir)
    
    # データの読み込み
    joint_states_df = pd.read_csv(joint_states_file)
    commands_df = pd.read_csv(commands_file)
    
    # タイムスタンプの変換
    joint_states_df = load_and_convert_time(joint_states_df)
    commands_df = load_and_convert_time(commands_df)
    
    # 利用可能なジョイントの取得
    available_joints = get_available_joints(joint_states_df)
    
    if not available_joints:
        print("No joint effort data found in the CSV file")
        return
        
    print(f"Found data for joints: {available_joints}")
    
    # 時間範囲の取得（x軸の範囲を統一するため）
    time_min = min(joint_states_df['timestamp'].min(), commands_df['timestamp'].min())
    time_max = max(joint_states_df['timestamp'].max(), commands_df['timestamp'].max())
    
    # データの値の範囲を取得（y軸の範囲を適切に設定するため）
    effort_min = float('inf')
    effort_max = float('-inf')
    command_min = float('inf')
    command_max = float('-inf')
    
    for joint_number in available_joints:
        effort_col = f'joint_{joint_number}_effort'
        command_col = f'command_{joint_number}'
        
        effort_min = min(effort_min, joint_states_df[effort_col].min())
        effort_max = max(effort_max, joint_states_df[effort_col].max())
        
        if command_col in commands_df.columns:
            command_min = min(command_min, commands_df[command_col].min())
            command_max = max(command_max, commands_df[command_col].max())
    
    # y軸の範囲を設定（余白を含む）
    y_min = min(effort_min, command_min)
    y_max = max(effort_max, command_max)
    y_margin = (y_max - y_min) * 0.1  # 10%のマージン
    
    # 各ジョイントについてプロット
    for joint_number in available_joints:
        plt.figure(figsize=(12, 6))
        
        # effortのプロット
        plt.scatter(joint_states_df['timestamp'], 
                   joint_states_df[f'joint_{joint_number}_effort'],
                   label='Measured Effort',
                   alpha=0.6,
                   marker='o',
                   s=30)
        
        # commandのプロット（存在する場合）
        command_col = f'command_{joint_number}'
        if command_col in commands_df.columns:
            plt.scatter(commands_df['timestamp'], 
                       commands_df[command_col],
                       label='Command',
                       alpha=0.1,
                       marker='x',
                       s=30)
        
        # グラフの設定
        plt.title(f'Joint {joint_number} Effort and Command Comparison')
        plt.xlabel('Time')
        plt.ylabel('Effort/Command Value')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 軸の範囲を設定
        plt.xlim(time_min, time_max)
        plt.ylim(y_min - y_margin, y_max + y_margin)
        
        # x軸の時刻表示を見やすく調整
        plt.gcf().autofmt_xdate()
        
        # グラフのレイアウト調整
        plt.tight_layout()
        
        # プロットを画像として保存
        filename = os.path.join(output_dir, f'joint_{joint_number}_comparison.png')
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Saved plot to: {filename}")
        
        # プロットを表示（オプション）
        plt.show()
        
        # メモリ解放
        plt.close()

def main():
    joint_states_file = 'joint_states.csv'
    commands_file = 'commands.csv'
    output_dir = 'effort_command_plots'  # 出力ディレクトリ名
    
    # 間引きなしの場合
    plot_effort_command_comparison(joint_states_file, commands_file, output_dir)

if __name__ == "__main__":
    main()