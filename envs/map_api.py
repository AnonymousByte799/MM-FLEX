import pandas as pd
import shutil
from envs import map_loader
import re
import string
import random
from framework.evaluator import get_reward

def rewrite(city, city_data):
    # Source and destination file paths
    source_path = city_data + city + '_GEO_INFO.csv'
    destination_path = city_data + city + '_GEO_INFO_COPY.csv'

    # Copy the file with overwrite
    shutil.copyfile(source_path, destination_path, follow_symlinks=True)  # 强制覆盖

    print(f"File '{source_path}' copied to '{destination_path}' with overwrite.", flush=True)


def query_range(city, city_data):
    # Read the 'loc.csv' file
    csv_path = city_data + city + '_GEO_INFO_COPY.csv'
    df = pd.read_csv(csv_path)  # Specify the index column and encoding

    # 查询经度和纬度的范围
    lon_range = (df['lon'].min(), df['lon'].max())
    lat_range = (df['lat'].min(), df['lat'].max())

    print(f'经度范围: {lon_range}', flush=True)
    print(f'纬度范围: {lat_range}', flush=True)


def query_info(query_str, city, city_data):
    # Read the 'loc.csv' file
    csv_path = city_data + city + '_GEO_INFO_COPY.csv'
    df = pd.read_csv(csv_path)  # Specify the index column and encoding

    # Extract query information
    query_info = query_str[11:]
    # Check the type of query information
    if query_info.isdigit():
        # If it is a serial number
        query_result = df.loc[int(query_info)-1, ['num', 'lon', 'lat', 'type_id', 'area']]
    else:
        return 'Invalid query information'

    # Convert the results to a string
    result_str = f"Query Information: {query_info}\n"
    result_str += f"Block Information:\n"

    # Access 'values' attribute only if 'query_result['num']' is a Pandas Series
    serial_number = int(query_result['num'])
    result_str += f"Serial Number: {serial_number}\n"
    # lon = query_result['lon'].values[0] if isinstance(query_result['lon'], pd.Series) else query_result['lon']
    # result_str += f"Center Longitude: {lon}\n"
    # lat = query_result['lat'].values[0] if isinstance(query_result['lat'], pd.Series) else query_result['lat']
    # result_str += f"Center Latitude: {lat}\n"

    # Convert type_id to the corresponding English string
    type_id_mapping = {
        0: 'Planned Area',
        1: 'Business Area',
        2: 'Green Area',
        3: 'Hospital Area',
        4: 'Office Area',
        5: 'Entertainment Area',
        6: 'Residential Area',
        7: 'School Area',
    }
    land_use_type = type_id_mapping[int(query_result['type_id'])]
    result_str += f"Land Use Type: {land_use_type}\n"

    # Access 'values' attribute only if 'query_result['area']' is a Pandas Series
    area = query_result['area'].values[0] if isinstance(query_result['area'], pd.Series) else query_result['area']
    result_str += f"Area of Region: {area}\n"

    adj_path = city_data + city + '_GEO_ADJ.csv'
    adj_matrix = pd.read_csv(adj_path, dtype=int, header=None)
    query_info = serial_number
    neighbors = adj_matrix.loc[query_info, adj_matrix.loc[query_info] == 1].index.tolist()
    # Extract information for each neighbor
    neighbor_info = []
    for neighbor in neighbors:
        neighbor_data = df.loc[neighbor, ['num', 'lon', 'lat', 'type_id', 'area']]
        neighbor_info.append({
            'Serial Number': int(neighbor_data['num']),
            'Land Use Type': {
                0: 'Planned Area',
                1: 'Business Area',
                2: 'Green Area',
                3: 'Hospital Area',
                4: 'Office Area',
                5: 'Entertainment Area',
                6: 'Residential Area',
                7: 'School Area'
            }[int(neighbor_data['type_id'])],
            'Area': neighbor_data['area']
        })
    result_str += f"Neighbors Information:\n"
    for neighbor_data in neighbor_info:
        result_str += f"\nSerial Number: {neighbor_data['Serial Number']}\n"
        result_str += f"Land Use Type: {neighbor_data['Land Use Type']}\n"
        result_str += f"Area: {(int)(neighbor_data['Area'])}\n"

    return result_str
    

def query_influ(query_str, city, city_data):
    # Read the 'loc.csv' file
    csv_path = city_data + city + '_GEO_INFO_COPY.csv'
    csv_origin_path = city_data + city + '_GEO_INFO_ORIGIN.csv'
    df = pd.read_csv(csv_path)
    df_origin = pd.read_csv(csv_origin_path)

    print(query_str, flush=True)
    # Extract query information
    parts = query_str.split()
    print(parts, flush=True)
    number_part = parts[1]
    area_part = " ".join(parts[2:])
    # Check the type of query information
    if not number_part.isdigit():
        return 'Invalid query information'

    query_result_origin = df_origin.loc[int(number_part)-1]
    query_result = df.loc[int(number_part)-1]
    print("origin:", query_result_origin, flush=True)
    print("now", query_result, flush=True)
    
    # Access 'values' attribute only if 'query_result' is a Pandas Series
    original_type_id = query_result_origin['type_id']
    old_type_id = query_result['type_id']
    print("query_influ", flush=True)

    print("old:", old_type_id, flush=True)

    # Convert the results to a string
    result_str = f"Query Type: {area_part}\n"

    # Convert type_id to the corresponding English string
    type_id_mapping = {
        0: 'planned area',
        1: 'business area',
        2: 'green area',
        3: 'hospital area',
        4: 'office area',
        5: 'entertainment area',
        6: 'residential area',
        7: 'school area',
    }

    # 检查查询信息是否在映射中
    area_part = area_part.lower()
    if area_part not in type_id_mapping.values():
        return 'Invalid area type'
    # 获取查询区域对应的type_id
    new_type_id = [k for k, v in type_id_mapping.items() if v.lower() == area_part][0]

    print("new:", new_type_id, flush=True)
    # Temporarily update the type_id for this block
    df.at[int(number_part)-1, 'type_id'] = new_type_id

    print(get_reward(df), flush=True)
    print(get_reward(df_origin), flush=True)

    # Calculate the reward
    service_reward, ecology_reward, economic_reward, equity_reward, total_reward = tuple(a - b for a, b in zip(get_reward(df), get_reward(df_origin)))


    # Restore the original type_id for further calculations
    df.at[int(number_part), 'type_id'] = old_type_id

    result_str += "The impact value for the entire area, and the larger the value, the better\n"
    result_str += f"service_reward,: {service_reward}\n"
    result_str += f"ecology_reward: {ecology_reward}\n"
    result_str += f"economic_reward {economic_reward}\n"
    result_str += f"equity_reward: {equity_reward}\n"
    result_str += f"total_reward: {total_reward}\n"

    return result_str


def query_neigh(query_str, city, city_data):
    # Read the 'loc.csv' file
    csv_path = city_data + city + '_GEO_INFO_COPY.csv'
    df = pd.read_csv(csv_path)  # Specify the index column and encoding

    adj_path = city_data + city + '_GEO_ADJ.csv'
    adj_matrix = pd.read_csv(adj_path, dtype=int, header=None)

    # Extract query information
    query_info = query_str[12:]

    # Check if query_info is a valid serial number
    if not query_info.isdigit():
        return 'Invalid query information'

    # Convert query_info to integer
    query_info = int(query_info)

    # Check if the serial number is within the valid range
    if query_info not in df.index:
        return 'Invalid serial number'
    if query_info not in adj_matrix.index:
        return 'No neighbors found for the given block'
    # Find neighbors using the adjacency matrix
    neighbors = adj_matrix.loc[query_info, adj_matrix.loc[query_info] == 1].index.tolist()
    # Extract information for each neighbor
    neighbor_info = []
    for neighbor in neighbors:
        neighbor_data = df.loc[neighbor, ['num', 'lon', 'lat', 'type_id', 'area']]
        neighbor_info.append({
            'Serial Number': int(neighbor_data['num']),
            'Center Longitude': neighbor_data['lon'],
            'Center Latitude': neighbor_data['lat'],
            'Land Use Type': {
                0: 'Planned Area',
                1: 'Business Area',
                2: 'Green Area',
                3: 'Hospital Area',
                4: 'Office Area',
                5: 'Entertainment Area',
                6: 'Residential Area',
                7: 'School Area'
            }[int(neighbor_data['type_id'])],
            'Area': neighbor_data['area']
        })

    # Convert the results to a string
    result_str = f"Query Information: {query_info}\n"
    result_str += f"Neighbors Information:\n"

    for neighbor_data in neighbor_info:
        result_str += f"\nSerial Number: {neighbor_data['Serial Number']}\n"
        result_str += f"Center Longitude: {neighbor_data['Center Longitude']}\n"
        result_str += f"Center Latitude: {neighbor_data['Center Latitude']}\n"
        result_str += f"Land Use Type: {neighbor_data['Land Use Type']}\n"
        result_str += f"Area: {neighbor_data['Area']}\n"

    return result_str


def query_area(query_str, city, city_data):
    # Read the 'loc.csv' file
    csv_path = city_data + city + '_GEO_INFO_COPY.csv'
    df = pd.read_csv(csv_path)  # Specify the index column and encoding

    # 提取查询信息
    query_area = query_str[11:].lower()
    # Convert type_id to the corresponding English string
    type_id_mapping = {
        0: 'planned area',
        1: 'business area',
        2: 'green area',
        3: 'hospital area',
        4: 'office area',
        5: 'entertainment area',
        6: 'residential area',
        7: 'school area',
    }

    # 检查查询信息是否在映射中
    if query_area not in type_id_mapping.values():
        return 'Invalid area type'

    # 获取查询区域对应的type_id
    type_id = [k for k, v in type_id_mapping.items() if v.lower() == query_area][0]

    # 筛选出指定类型的区块
    selected_blocks = df[df['type_id'] == type_id]

    # 计算该类型的面积
    area_of_selected_type = selected_blocks['area'].sum()

    # 计算总面积
    total_area = df['area'].sum()

    # 计算比例
    proportion = area_of_selected_type / total_area

    # 构造输出字符串
    result_str = f"Area Type: {query_area.capitalize()}\n"
    result_str += f"Total Area of {query_area}: {area_of_selected_type}\n"
    result_str += f"Proportion of {query_area} in Total Area: {proportion:.2%}"

    return result_str


# def process_query(query_str):
#     # 根据输入字符串判断调用哪个函数
#     if query_str.startswith("query_info"):
#         return query_info(query_str)
#     elif query_str.startswith("query_neigh"):
#         return query_neigh(query_str)
#     elif query_str.startswith("query_area"):
#         return query_area(query_str)
#     else:
#         return 'Invalid query. Please enter only the instructions and do not enter any other text.'
def remove_non_digits(input_str):
    return re.sub(r'\D', '', input_str)


def remove_punctuation(input_str):
    # 使用 str.maketrans 创建映射表，将标点符号替换为 None
    translator = str.maketrans('', '', string.punctuation)

    # 使用 translate 方法删除所有标点符号
    result = input_str.translate(translator)

    return result


def process_query(query_str, city, city_data):
    # 使用正则表达式匹配指令部分
    match = re.search(r'(query_info|query_neigh|query_area|query_influ|debate)\s+(\S+)', query_str)

    if match:
        # 提取匹配到的指令和参数
        instruction = match.group(1)

        # 根据指令调用相应的函数
        if instruction == "query_info":
            return query_info(instruction + ' ' + remove_non_digits(match.group(2)), city, city_data)
        elif instruction == "query_neigh":
            return query_neigh(instruction + ' ' + remove_non_digits(match.group(2)), city, city_data)
        elif instruction == "query_area":
            match = re.search(r'(query_info|query_neigh|query_area)\s+(\S+)\s+(\S+)', query_str)
            return query_area(instruction + ' ' + match.group(2) + ' ' + remove_punctuation(match.group(3)), city, city_data)
        elif instruction == "query_influ":
            match = re.search(r'(query_influ)\s+(\d+)\s+(\S+)\s+(\S+)', query_str)
            return query_influ(instruction + ' ' + match.group(2) + ' ' + match.group(3) + ' ' + remove_punctuation(match.group(4)), city, city_data)
        
    else:
        return 'Invalid query. Please enter only the instructions and do not enter any other text.'


def planned_area(city, city_data):
    # Read the 'loc.csv' file
    csv_path = city_data + city + '_GEO_INFO_COPY.csv'
    df = pd.read_csv(csv_path)  # Specify the index column and encoding

    # 选择待规划区域
    planned_df = df[df['type_id'] == 0]

    # 找到序号最小的待规划区域
    min_serial_number = planned_df['num'].idxmin()
    min_planned_area = planned_df.loc[min_serial_number]

    # 将查询结果转换为字符串
    result_str = f"Planned Area Information:\n"
    result_str += f"Serial Number: {int(min_planned_area['num'])}\n"
    result_str += f"Center Longitude: {min_planned_area['lon']}\n"
    result_str += f"Center Latitude: {min_planned_area['lat']}\n"
    result_str += f"Land Use Type: Planned Area\n"
    result_str += f"Area: {min_planned_area['area']}"

    return result_str


def planned_area_all(city, city_data):
    # Read the 'loc.csv' file
    csv_path = city_data + city + '_GEO_INFO_COPY.csv'
    df = pd.read_csv(csv_path)  # Specify the index column and encoding

    # 选择待规划区域
    planned_df = df[df['type_id'] == 0]

    # 检查是否有待规划区域
    if planned_df.empty:
        return "No planned areas found."

    # 遍历所有待规划区域并生成信息字符串
    result_str = "Planned Areas Serial Number:\n"
    for _, area_info in planned_df.iterrows():
        result_str += f"{int(area_info['num'])}; "

    return result_str

def planned_area_num(num, city, city_data):
    # Read the 'loc.csv' file
    csv_path = city_data + city + '_GEO_INFO_COPY.csv'
    df = pd.read_csv(csv_path)  # Specify the index column and encoding if necessary

    # 选择待规划区域
    planned_df = df[df['type_id'] == 0]

    # 检查是否有足够的待规划区域
    if planned_df.empty:
        return "No planned areas found."
    elif len(planned_df) < num:
        return "Not enough planned areas available."

    # 随机选择num个待规划区域
    sampled_planned_df = planned_df.sample(n=num)

    # 遍历所有选定的待规划区域并生成信息字符串
    result_str = "Planned Areas Serial Number:"
    for _, area_info in sampled_planned_df.iterrows():
        result_str += f"\n{int(area_info['num'])}"

    return result_str


def update_planned_area_type_rand(num, city, city_data):
    # 构建文件路径
    csv_path = city_data + city + '_GEO_INFO_COPY.csv'
    # 读取CSV文件
    df = pd.read_csv(csv_path)

    # 检查是否存在type_id等于0的行
    planned_areas = df[df['type_id'] == 0]
    if planned_areas.empty:
        return "No planned areas found."

    # 生成num个随机数，范围是1到7但不包括6
    random_types = [random.choice([1, 2, 3, 4, 5, 7]) for _ in range(num)]
    
    # 选取前num个待规划区域
    planned_area_indices = planned_areas.index[:num]

    # 更新这些区域的type_id
    for index, new_type in zip(planned_area_indices, random_types):
        if index < len(df):  # 确保索引有效
            df.at[index, 'type_id'] = new_type

    # 保存到CSV文件
    df.to_csv(csv_path, index=False)
    return random_types

def update_planned_area_type_best(num, city, city_data, type):
    # 构建文件路径
    csv_path = city_data + city + '_GEO_INFO_COPY.csv'
    # 读取CSV文件
    df = pd.read_csv(csv_path)

    # 检查是否存在type_id等于0的行
    planned_areas = df[df['type_id'] == 0]
    if planned_areas.empty:
        return "No planned areas found."

    # 生成num个随机数，范围是1到7但不包括6
    random_types = [type]
    
    # 选取前num个待规划区域
    planned_area_indices = planned_areas.index[:num]

    # 更新这些区域的type_id
    for index, new_type in zip(planned_area_indices, random_types):
        if index < len(df):  # 确保索引有效
            df.at[index, 'type_id'] = new_type

    # 保存到CSV文件
    df.to_csv(csv_path, index=False)
    return random_types[0]



def update_planned_area_type(decision_number, city, city_data):
    # Read the 'loc_copy.csv' file
    csv_path = city_data + city + '_GEO_INFO_COPY.csv'
    df = pd.read_csv(csv_path)  # Specify the index column and encoding

    # Check if there are any rows with type_id == 0
    planned_area_indices = df[df['type_id'] == 0].index.tolist()
    
    if not planned_area_indices:
        return  # If no rows with type_id == 0, do nothing

    # Ensure decision_number list has enough values to cover all planned areas
    if len(decision_number) < len(planned_area_indices):
        raise ValueError("decision_number list is too short for the number of planned areas.")
    
    # Update type_id of planned areas with values from decision_number
    for planned_area_index, decision in zip(planned_area_indices, decision_number):
        df.at[planned_area_index, 'type_id'] = int(decision)

    # Save the updated DataFrame back to 'loc_copy.csv'
    df.to_csv(city_data + city + '_GEO_INFO_COPY.csv', index=False)


def process_decision_string(decision_string):
    # Extract decision number using regular expression
    match = re.search(r'(?<=\b[1-7]:)\s*\d', decision_string)

    if match:
        decision_number = int(match.group())
        return decision_number
    else:
        # Handle the case where no valid decision number is found
        print("No valid decision number found in the string.", flush=True)
        return None


def process_and_update_decisions(decision_strings, city, city_data):
    # Find all occurrences of a digit between 1 and 7 preceded by ':'
    # First, locate the position of the word "reason" in the text
    # 正则表达式提取方括号内的数字
    pattern = r'\[(.*?)\]'

    # 查找所有匹配的列表，并将数字转换成整数存入列表
    matches = re.findall(pattern, decision_strings)

    # 转换为整数列表
    result = [list(map(int, match.split(','))) for match in matches]

    print('-------numbers----------', flush=True)
    print(result[0], flush=True)

    # Convert the matched strings to integers
    update_planned_area_type(result[0], city, city_data)

    return result[0]


def count_planned_areas(city, city_data):
    # Read the 'loc.csv' file
    csv_path = city_data + city + '_GEO_INFO_COPY.csv'
    df = pd.read_csv(csv_path)  # Specify the index column and encoding

    # Count the number of Planned Areas (Type 0)
    planned_areas_count = df[df['type_id'] == 0].shape[0]

    return planned_areas_count


def plot(city, city_data, save_path):
    map_loader.map_plot_num(city_data=city_data, city=city, save_path=save_path)


#
# # 示例调用
# result_planned_area = planned_area(df)
# print(result_planned_area)
#
#
# # 示例输入
# query_input = "query_neigh 25"
#
# # 输出查询结果
# result = query_neigh(query_input)
# print(result)
