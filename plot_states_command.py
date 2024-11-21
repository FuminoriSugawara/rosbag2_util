import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import argparse

def load_and_convert_time(df):
    """タイムスタンプを datetime オブジェクトに変換"""
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def ensure_output_dir(output_dir):
    """出力ディレクトリが存在しない場合は作成"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def plot_joint_states_and_command(joint_states_file, commands_file, joint_number=1, output_dir='plots'):
    """
    ジョイントの状態とコマンドをプロットする関数
    
    Parameters:
    -----------
    joint_states_file : str
        ジョイント状態のCSVファイルパス
    commands_file : str
        コマンドのCSVファイルパス
    joint_number : int
        分析対象のジョイント番号
    output_dir : str
        出力ディレクトリのパス
    """
    # 出力ディレクトリの作成
    ensure_output_dir(output_dir)
    
    # データの読み込み
    try:
        joint_states_df = pd.read_csv(joint_states_file)
        commands_df = pd.read_csv(commands_file)
    except FileNotFoundError as e:
        print(f"Error: Could not find input file - {e}")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: One of the input files is empty")
        return
    except Exception as e:
        print(f"Error reading input files: {e}")
        return
    
    # タイムスタンプの変換
    joint_states_df = load_and_convert_time(joint_states_df)
    commands_df = load_and_convert_time(commands_df)
    
    # 必要なカラムの存在確認
    required_columns = [
        f'joint_{joint_number}_effort',
        f'joint_{joint_number}_pos',
        f'joint_{joint_number}_vel'
    ]
    
    if not all(col in joint_states_df.columns for col in required_columns):
        print(f"Error: Missing required columns for joint {joint_number} in joint states file")
        return
    
    # サブプロット作成（4つの縦に並んだグラフ）
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 16), sharex=True)
    
    # 時間範囲の取得
    time_min = min(joint_states_df['timestamp'].min(), commands_df['timestamp'].min())
    time_max = max(joint_states_df['timestamp'].max(), commands_df['timestamp'].max())
    
    # Command のプロット
    if f'command_{joint_number}' in commands_df.columns:
        ax1.scatter(commands_df['timestamp'], 
                   commands_df[f'command_{joint_number}'],
                   label='Command',
                   alpha=0.6,
                   marker='x',
                   s=30)
        ax1.set_ylabel('Command')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
    else:
        print(f"Warning: command_{joint_number} not found in commands file")
    
    # Position のプロット
    ax2.scatter(joint_states_df['timestamp'], 
               joint_states_df[f'joint_{joint_number}_pos'],
               label='Position',
               alpha=0.6,
               marker='o',
               s=30)
    ax2.set_ylabel('Position')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Velocity のプロット
    ax3.scatter(joint_states_df['timestamp'], 
               joint_states_df[f'joint_{joint_number}_vel'],
               label='Velocity',
               alpha=0.6,
               marker='o',
               s=30)
    ax3.set_ylabel('Velocity')
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    
    # Current(Effort) のプロット
    ax4.scatter(joint_states_df['timestamp'], 
               joint_states_df[f'joint_{joint_number}_effort'],
               label='Current',
               alpha=0.6,
               marker='o',
               s=30)
    ax4.set_ylabel('Current')
    ax4.grid(True, alpha=0.3)
    ax4.legend()
    
    # x軸の範囲を設定
    for ax in [ax1, ax2, ax3, ax4]:
        ax.set_xlim(time_min, time_max)
    
    # グラフ全体の設定
    plt.suptitle(f'Joint {joint_number} States and Command Analysis')
    ax4.set_xlabel('Time')
    
    # x軸の時刻表示を見やすく調整
    plt.gcf().autofmt_xdate()
    
    # グラフのレイアウト調整
    plt.tight_layout()
    
    # プロットを画像として保存
    filename = os.path.join(output_dir, f'joint_{joint_number}_all_states.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Saved plot to: {filename}")
    
    # プロットを表示（オプション）
    plt.show()
    
    # メモリ解放
    plt.close()

def main():
    # コマンドライン引数のパーサーを作成
    parser = argparse.ArgumentParser(
        description='Plot joint states and commands from CSV files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:
  python script.py -j joint_states.csv -c commands.csv -n 1 -o output_dir
  python script.py --joint-states data/joint_states.csv --commands data/commands.csv --joint-number 2
        """
    )
    
    # 引数の追加
    parser.add_argument('-j', '--joint-states', 
                        required=True,
                        help='Path to the joint states CSV file')
    parser.add_argument('-c', '--commands',
                        required=True,
                        help='Path to the commands CSV file')
    parser.add_argument('-n', '--joint-number',
                        type=int,
                        default=1,
                        help='Joint number to analyze (default: 1)')
    parser.add_argument('-o', '--output-dir',
                        default='joint_states_plots',
                        help='Output directory for plots (default: joint_states_plots)')
    
    # 引数をパース
    args = parser.parse_args()
    
    # プロット関数を呼び出し
    plot_joint_states_and_command(
        joint_states_file=args.joint_states,
        commands_file=args.commands,
        joint_number=args.joint_number,
        output_dir=args.output_dir
    )

if __name__ == "__main__":
    main()