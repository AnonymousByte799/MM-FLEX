from framework.role_generator import evaluator_agent_3, evaluator_agent_4, evaluator_agent_4_num, agents_eval
from framework.prompt_generator import generate_sum
from envs import map_api
from geopy.distance import geodesic
import pandas as pd
import os
import math

def referee_prompt():
    prompt = """
    Community Land Planning - Referee Assessment:

    As the referee, your role is to evaluate and provide insights on the decisions made by other agents in the community land planning task. The decisions are represented in the format:

    Type: reason: ...;

    Example:
        6: reason: ...;

    where:
    - Type 0: Planned Area
    - Type 1: Business Area
    - Type 2: Green Area
    - Type 3: Hospital Area
    - Type 4: Office Area
    - Type 5: Entertainment Area
    - Type 6: Residential Area
    - Type 7: School Area

    Instructions for interacting with the system:

    1. `query_info query`: Use this command to retrieve information about a specific location. For example, `query_info 25` returns details about the area at Serial Number 25.

    2. `query_neigh query`: Use this command to obtain information about neighboring locations. For example, `query_neigh 25` returns information like: [26]: Type 1; [24]: Type 2; [25]: Type 6, which are the details about the area around Serial Number 25.

    3. `query_area area_type`: Use this command to calculate the percentage of a specific land type in the entire region. For example, `query_area Residential Area` returns the percentage of Residential Areas in the region.

    When providing your assessment, strictly follow the format:
    - Decision_multi is preferred over Decision_single because [reasons].
    OR
    - Decision_single is preferred over Decision_multi because [reasons].

    Begin by issuing commands to gather information about the region. You can only enter one command at a time. When you have gathered what you think is enough information about the region, judge it according to the format.
    """
    return prompt

def evaluate_agents(decision_and_reasons, city, city_data, save_path, img_path):
    print("Evaluating agents' decisions and reasons...", flush=True)
    
    # 将决策和理由打印出来进行检查
    for decision_reason in decision_and_reasons:
        print("Decision:", decision_reason["decision"], flush=True)
        print("Reason:", decision_reason["reason"], flush=True)
    
    agents = agents_eval  # 假设这是之前定义的代理人列表
    for agent in agents:
        for decision_reason in decision_and_reasons:
            # 构建代理人的任务，包含决策和理由
            decision = decision_reason["decision"]
            reason = decision_reason["reason"]
            
            # 给代理人发送决策和理由信息，要求它们进行评分
            agent.ask(f"""
                I'm going to give you a decision for a block, along with the reason for the decision. Please rate this decision on a scale of 0 to 10, with decimal points.
                
                The decision type for block is: {', '.join(str(i) for i in decision)}.
                
                The corresponding types are:
                - Type 1: Business Area
                - Type 2: Green Area
                - Type 3: Hospital Area
                - Type 4: Office Area
                - Type 5: Entertainment Area
                - Type 6: Residential Area
                - Type 7: School Area
                
                The reason for this decision is: {reason}.
                
                Please rate the appropriateness of this decision based on the provided reasoning and your own opinion. Output your score as a decimal number between 0 and 10.
            """, image_path=img_path)

    # 保存代理人的评分和总结到日志文件
    with open(os.path.join(save_path, 'log.txt'), 'a') as f:
        f.write('Agent Evaluation:\n')
        for agent in agents:
            # 记录代理人评分的总结（假设这里有一个 generate_sum 函数）
            f.write(generate_sum(agent) + '\n')
        f.write('-----------------------------------------------------------\n')

def evaluate_3(decide1, decide2, city, city_data, save_path):
    eval = evaluator_agent_3
    eval.ask("""decision_multi: """ + decide1 +
             """decision_single: """ + decide2 +
             referee_prompt())
    while True:
        answer = eval.conversation_list[-1]['content']
        if 'prefer' in answer or 'decision' in answer.lower():
            break
        info = map_api.process_query(answer, city=city, city_data=city_data)
        eval.ask(info)
    with open(os.path.join(save_path, 'log.txt'), 'a') as f:
        f.write('Evaluate Gpt3.5:\n')
        f.write(eval.conversation_list[-1]['content'] + '\n')
        f.write('-----------------------------------------------------------\n')

def evaluate_4(decide1, decide2, city, city_data, save_path):
    eval = evaluator_agent_4
    eval.ask("""decision_multi: """ + decide1 +
             """decision_single: """ + decide2 +
             referee_prompt())
    while True:
        answer = eval.conversation_list[-1]['content']
        if 'prefer' in answer.lower():
            break
        info = map_api.process_query(answer, city=city, city_data=city_data)
        eval.ask(info)
    with open(os.path.join(save_path, 'log.txt'), 'a') as f:
        f.write('Evaluate Gpt4:\n')
        f.write(eval.conversation_list[-1]['content'] + '\n')
        f.write('-----------------------------------------------------------\n')


def evaluate_4_num(decide1, decide2, city, city_data, save_path):
    eval = evaluator_agent_4_num
    eval.ask("""decision_multi: """ + decide1 +
             """decision_single: """ + decide2 +
             referee_prompt())
    while True:
        answer = eval.conversation_list[-1]['content']
        if 'prefer' in answer.lower():
            break
        info = map_api.process_query(answer, city=city, city_data=city_data)
        eval.ask(info)
    with open(os.path.join(save_path, 'log.txt'), 'a') as f:
        f.write('Evaluate Gpt4 Only Num:\n')
        f.write(eval.conversation_list[-1]['content'] + '\n')
        f.write('-----------------------------------------------------------\n')

LIFE_CIRCLE_SIZE = 1000
GREEN_COVERAGE_DEMANDS = 0.2
BUSINESS_COVERAGE_DEMANDS = 0.1
OFFICE_COVERAGE_DEMANDS = 0.1
RECREATION_COVERAGE_DEMANDS = 0.1
HOSPITAL_NUM = 8
SCHOOL_NUM = 8

def get_distance(region1, region2, geo_info):
    """
    Get distance between two regions.
    :param region1: int
    :param region2: int
    :param geo_info: DataFrame
    :return: distance: float
    """
    loc1_lon = geo_info.loc[region1, 'lon']
    loc1_lat = geo_info.loc[region1, 'lat']
    loc2_lon = geo_info.loc[region2, 'lon']
    loc2_lat = geo_info.loc[region2, 'lat']

    distance = geodesic((loc1_lat, loc1_lon), (loc2_lat, loc2_lon)).km * 1000  # Convert to meters
    return distance


def get_living_circle_idx(region_idx, geo_info):
    """
    Get the regions in the living circle.
    :param region_idx: int
    :param geo_info: DataFrame
    :return: living_circle_idx: list
    """
    living_circle_radius = LIFE_CIRCLE_SIZE
    living_circle_idx = []

    for i in range(len(geo_info)):
        if i == region_idx:
            living_circle_idx.append(i)
        else:
            distance = get_distance(region_idx, i, geo_info)
            if distance <= living_circle_radius:
                living_circle_idx.append(i)

    return living_circle_idx

def get_nearest_type_distance_list(region_type, geo_info):
    """
    get the nearest distance of a certain region type to residential area
    :param region_type: str
    :return: nearest_distance: list [float, float, ...]
    """
    nearest_distance = []
    for region_idx in range(len(geo_info)):
        if geo_info.loc[region_idx, 'type_id'] == 6:
            distance = get_nearest_distance(region_idx, region_type, geo_info)
            if distance == 100000:
                pass
            else:
                nearest_distance.append(distance)
    return nearest_distance

def get_nearest_distance(region_idx, region_type, geo_info):
    nearest_distance = 100000
    for i in range(len(geo_info)):
        if  geo_info.loc[i, 'type_id'] == region_type:
            distance = get_distance(region_idx, i, geo_info)
            if distance < nearest_distance:
                nearest_distance = distance
    return nearest_distance

def equity_cal(distances):
    # if len(distances) == 0:
    #     return 0
    # else:
    #     mean_distance = np.mean(distances)
    #     n = len(distances)
    #     similarity = 1 - np.sum((distances - mean_distance) ** 2) / (n * mean_distance ** 2)
    #     return similarity
    if len(distances) == 0:
        return 0
    else:
        # 最大距离和最小距离的差值
        max_distance = max(distances)
        min_distance = min(distances)
        s = ((max_distance - min_distance) / 800) ** 3
        # 计算公平性
        equity = math.e ** (-s)
        return equity

def get_reward(geo_info):
    """
    Get reward.
    :param geo_info: DataFrame
    :return: service_reward, ecology_reward, economic_reward, total_reward
    """
    # Living Service reward
    service_reward = 0
    residential_num = 0

    for region_idx in range(len(geo_info)):
        if geo_info.loc[region_idx, 'type_id'] == 6:  # Assuming 6 corresponds to Residential
            residential_num += 1
            living_circle_neighborhood_idx = get_living_circle_idx(region_idx, geo_info)

            school_exist = False
            hospital_exist = False
            business_exist = False
            office_exist = False
            recreation_exist = False

            for neighbor in living_circle_neighborhood_idx:
                if geo_info.loc[neighbor, 'type_id'] == 7:  # Assuming 7 corresponds to School
                    school_exist = True
                if geo_info.loc[neighbor, 'type_id'] == 3:  # Assuming 3 corresponds to Hospital
                    hospital_exist = True
                if geo_info.loc[neighbor, 'type_id'] == 1:  # Assuming 1 corresponds to Business
                    business_exist = True
                if geo_info.loc[neighbor, 'type_id'] == 4:  # Assuming 4 corresponds to Office
                    office_exist = True
                if geo_info.loc[neighbor, 'type_id'] == 5:  # Assuming 5 corresponds to Recreation
                    recreation_exist = True
            service_reward += (school_exist + hospital_exist + business_exist + office_exist + recreation_exist) / 5
    if residential_num == 0:
        service_reward = 0
    else:
        service_reward = service_reward / residential_num

    # Ecological Environment reward
    green_area = geo_info.loc[(geo_info['type_id'] == 2) | (geo_info['type_id'] == 0), 'area'].sum()
    total_area = geo_info['area'].sum()

    if green_area < total_area * GREEN_COVERAGE_DEMANDS:
        ecology_reward = green_area / (total_area * GREEN_COVERAGE_DEMANDS)
    else:
        ecology_reward = 1

    # Economic reward
    valid_business_area = 0
    valid_office_area = 0
    valid_recreation_area = 0
    for region_idx in range(len(geo_info)):
        if geo_info.loc[region_idx, 'type_id'] in [1, 5, 4]:  # Assuming 1, 5, 4 correspond to Business, Recreation, and Office
            living_circle_neighborhood_idx = get_living_circle_idx(region_idx, geo_info)
            for neighbor in living_circle_neighborhood_idx:
                if geo_info.loc[neighbor, 'type_id'] == 6:  # Assuming 6 corresponds to Residential
                    if geo_info.loc[region_idx, 'type_id'] == 1:
                        valid_business_area += geo_info.loc[region_idx, 'area']
                    elif geo_info.loc[region_idx, 'type_id'] == 5:
                        valid_recreation_area += geo_info.loc[region_idx, 'area']
                    elif geo_info.loc[region_idx, 'type_id'] == 4:
                        valid_office_area += geo_info.loc[region_idx, 'area']
                    break
    if (valid_business_area < total_area * BUSINESS_COVERAGE_DEMANDS or
                valid_office_area < total_area * OFFICE_COVERAGE_DEMANDS or
                valid_recreation_area < total_area * RECREATION_COVERAGE_DEMANDS):
        economic_reward = (min(valid_business_area / (total_area * BUSINESS_COVERAGE_DEMANDS), 1) +
                               min(valid_office_area / (total_area * OFFICE_COVERAGE_DEMANDS), 1) +
                               min(valid_recreation_area / (total_area * RECREATION_COVERAGE_DEMANDS), 1)) / 3
    else:
        economic_reward = 1

    # Equity reward
    school_distance_list = get_nearest_type_distance_list(7, geo_info)
    hospital_distance_list = get_nearest_type_distance_list(3, geo_info)
    hospital_num = (geo_info['type_id'] == 3).sum()
    school_num = (geo_info['type_id'] == 7).sum()

    # 建设数量的奖励
    num_reward = (pow(math.e, - abs(hospital_num - HOSPITAL_NUM) / 2)
                    + pow(math.e, - abs(school_num - SCHOOL_NUM) / 2))

    # 基于基尼系数的公平性度量
    # school_equity_reward = 1 - gini_coef(school_distance_list)
    # hospital_equity_reward = 1 - gini_coef(hospital_distance_list)

    # 基于方差的公平性度量
    school_equity_reward = equity_cal(school_distance_list)
    hospital_equity_reward = equity_cal(hospital_distance_list)

    equity_reward = ((school_equity_reward + hospital_equity_reward) / 2 + num_reward) / 2
    # equity_reward = 0

    total_reward = service_reward + ecology_reward + economic_reward + equity_reward

    return service_reward, ecology_reward, economic_reward, equity_reward, total_reward


def print_reward(city, city_data, save_path):
    geo_info_path = city_data + city + '_GEO_INFO_COPY.csv'
    geo_info = pd.read_csv(geo_info_path)

    # Get reward for the region
    service_reward, ecology_reward, economic_reward, equity_reward, total_reward = get_reward(geo_info)
    # return total_reward
    # Print the rewards
    print(f"Service Reward: {service_reward}", flush=True)
    print(f"Ecology Reward: {ecology_reward}", flush=True)
    print(f"Economic Reward: {economic_reward}", flush=True)
    print(f"Equity Reward: {equity_reward}", flush=True)
    print(f"Total Reward: {total_reward}", flush=True)

    with open(os.path.join(save_path, 'log.txt'), 'a') as f:
        f.write('Service Reward: {}\n'.format(service_reward))
        f.write('Ecology Reward: {}\n'.format(ecology_reward))
        f.write('Economic Reward: {}\n'.format(economic_reward))
        f.write('Equity Reward: {}\n'.format(equity_reward))
        f.write('Total Reward: {}\n'.format(total_reward))
        f.write('-----------------------------------------------------------\n')



def print_reward_origin(city, city_data, save_path):
    geo_info_path = city_data + city + '_GEO_INFO_ORIGIN.csv'
    geo_info = pd.read_csv(geo_info_path)

    # Get reward for the region
    service_reward, ecology_reward, economic_reward, equity_reward, total_reward = get_reward(geo_info)
    # Print the rewards
    print(f"Service Reward: {service_reward}", flush=True)
    print(f"Ecology Reward: {ecology_reward}", flush=True)
    print(f"Economic Reward: {economic_reward}", flush=True)
    print(f"Equity Reward: {equity_reward}", flush=True)
    print(f"Total Reward: {total_reward}", flush=True)

    with open(os.path.join(save_path, 'log.txt'), 'a') as f:
        f.write('Service Reward: {}\n'.format(service_reward))
        f.write('Ecology Reward: {}\n'.format(ecology_reward))
        f.write('Economic Reward: {}\n'.format(economic_reward))
        f.write('Equity Reward: {}\n'.format(equity_reward))
        f.write('Total Reward: {}\n'.format(total_reward))
        f.write('-----------------------------------------------------------\n')

