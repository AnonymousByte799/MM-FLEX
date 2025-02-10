import argparse
import framework.planning_simulator_syn
import framework.planning_simulator_single_multi
import shutil
import time
import pandas as pd
import random
import os
import sys

# Parameters settings
parser = argparse.ArgumentParser()

parser.add_argument('--city', type=str, default='BEIJING', help='City with uppercase.')
parser.add_argument('--city_data', type=str, default='data/beijing/', help='Path to load data files.')
parser.add_argument('--plan_num', type=int, default=20, help='Number of planned grids.')
parser.add_argument('--model', type=int, default=4, help='Use gpt3.5(choose 3) or gpt4(choose 4).')
parser.add_argument('--syn', type=int, default=1, help='Plan syn or not.')

args = parser.parse_args()


df_origin = pd.read_csv(args.city_data + args.city + '_GEO_INFO_ORIGIN.csv')
num_rows_to_change = args.plan_num
# 获取type_id不等于6的所有行的索引
rows_with_type_id_not_6 = df_origin.index[df_origin['type_id'] != 6].tolist()
# 如果需要修改的行数超过了筛选出来的行数，需要处理这种情况
num_rows_to_change = min(num_rows_to_change, len(rows_with_type_id_not_6))
args.plan_num = num_rows_to_change
# 从这些行中随机选择行索引
rows_to_change = random.sample(rows_with_type_id_not_6, num_rows_to_change)

# # 指定行索引
# rows_to_change = [6, 34, 58]


# 复制原始数据，以确保不改变原始数据
df_info = df_origin.copy()
# 将选定行的type_id修改为0
df_info.loc[rows_to_change, 'type_id'] = 0
# 将修改后的数据保存到info.csv
df_info.to_csv(args.city_data + args.city + '_GEO_INFO.csv', index=False)

# Source and destination file paths
source_path = args.city_data + args.city + '_GEO_INFO.csv'
destination_path = args.city_data + args.city + '_GEO_INFO_COPY.csv'

# Copy the file with overwrite
shutil.copyfile(source_path, destination_path, follow_symlinks=True)  # 强制覆盖

print(f"File '{source_path}' copied to '{destination_path}' with overwrite.", flush=True)


# save models and logs
log_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
# 创建文件夹
save_path = os.path.join('logs', args.city, log_time+'-NUM'+str(args.plan_num))
os.makedirs(save_path)

output_file = save_path + '/output.txt'
sys.stdout = open(output_file, 'w')

print(args.syn, flush=True)

if args.syn == 1:
    framework.planning_simulator_syn.simulator_syn(num=args.plan_num, model=args.model, city=args.city, city_data=args.city_data, save_path=save_path)
else:
    framework.planning_simulator_single_multi.simulator_syn(num=args.plan_num, model=args.model, city=args.city, city_data=args.city_data, save_path=save_path)


