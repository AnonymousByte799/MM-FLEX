import framework.function
import framework.function.debate
import framework.prompt.decider_prompt as decider_prompt
import framework.prompt.npc_prompt
from framework.function_tree import tools, mm_tools
import envs.map_api
import framework.evaluator as evaluator
import framework.role_generator as role_generator
import os
import pandas as pd
import framework.prompt_generator as prompt_generator
import random


def simulator_syn(num, city, city_data, model, save_path):
    
    decision_and_reasons = []
    # 构建文件路径
    csv_path = city_data + city + '_GEO_INFO_COPY.csv'
    # 读取CSV文件
    df = pd.read_csv(csv_path)
    # 检查是否存在type_id等于0的行
    planned_areas = df[df['type_id'] == 0].index


    origin_csv_path = city_data + city + '_GEO_INFO_ORIGIN.csv'
    df_origin = pd.read_csv(origin_csv_path)
    decision_list = []
    for index in planned_areas:
        # 获取原始文件中对应行的type_id
        type_id_origin = df_origin.iloc[index]['type_id']
        # 将type_id添加到decision_list中
        decision_list.append(int(type_id_origin))

    decision_and_reasons.append({
        "decision": decision_list,
        "reason": "human expert decision "
    })
    
    
    print("Welcome to the Community Planning Simulation!\n", flush=True)

    # agent_single = role_generator.sum_single
    # question = 'Can you tell me your criteria for judging the quality of similar urban planning tasks, what are the quantitative or qualitative indicators?'

    with open(os.path.join(save_path, 'log.txt'), 'a') as f:
        f.write('Origin Rewards:\n')
    evaluator.print_reward_origin(city=city, city_data=city_data, save_path=save_path)

    envs.map_api.plot(city=city, city_data=city_data, save_path=os.path.join(save_path, 'to_plan.png'))
    image_path = os.path.join(save_path, 'to_plan.png')
    
    #random baseline
    print('====== Random Turn ======', flush=True)
    envs.map_api.rewrite(city=city, city_data=city_data)
    with open(os.path.join(save_path, 'log.txt'), 'a') as f:
        f.write('Random Rewards:\n')
    
    decision_list = (envs.map_api.update_planned_area_type_rand(num, city=city, city_data=city_data))
    evaluator.print_reward(city=city, city_data=city_data, save_path=save_path)
    envs.map_api.plot(city=city, city_data=city_data, save_path=os.path.join(save_path, 'random.png'))

    decision_and_reasons.append({
        "decision": decision_list,
        "reason": "random decision "
    })

    # # single agent framework
    # print('====== Agent Info Turn ======', flush=True)
    # envs.map_api.rewrite(city=city, city_data=city_data)
    # agent_single = role_generator.sum_agent
    # # agent_single.ask(question)
    # agent_single.ask(decider_prompt.init_prompt.format(tools=tools) + 'Your task of planning is: ' + envs.map_api.planned_area_all(city=city, city_data=city_data))
    # time = 0

    # while True:
    #     answer = agent_single.conversation_list[-1]['content']
    #     if 'reason' in answer:
    #         if time >= 3:
    #             break
    #         else:
    #             agent_single.ask('Please get enough information before making a decision! Do not make up information yourself. Also, be careful to enter only one instruction at a time and nothing else.')
    #     info = envs.map_api.process_query(answer, city=city, city_data=city_data)
    #     if "debate" in answer:
    #         if info is None:
    #             info = function_tree_framework.function.debate.debate(city=city, city_data=city_data)
    #         else:
    #             info = info + function_tree_framework.function.debate.debate(city=city, city_data=city_data)
    #     agent_single.ask(info)
    #     time = time + 1

    # decision_single = agent_single.conversation_list[-1]['content']
    # decision_numbers_single = envs.map_api.process_and_update_decisions(decision_single, city=city, city_data=city_data)

    # decision_list.append(decision_numbers_single)


    # with open(os.path.join(save_path, 'log.txt'), 'a') as f:
    #     f.write('Single Rewards:\n')
    
    # evaluator.print_reward(city=city, city_data=city_data, save_path=save_path)

    # MM agent framework
    agent = role_generator.mm_flex_agent
    print('====== MM Info Turn ======', flush=True)
    envs.map_api.rewrite(city=city, city_data=city_data)

    # 使用 init_plan_prompt 完成初步规划并保存
    initial_plan = agent.ask(decider_prompt.init_plan_prompt.format(tools=mm_tools) + 'Your task of planning is: ' + envs.map_api.planned_area_all(city=city, city_data=city_data), image_path=image_path)

    # 将初步规划结果保存到文件
    with open(os.path.join(save_path, 'initial_plan.txt'), 'a') as f:
        f.write('Initial Plan:\n')
        f.write(initial_plan + '\n')

    # 更新图片，保存初步规划结果
    initial_image_path = os.path.join(save_path, f'{city}_initial_plan.png')
    envs.map_api.plot(city=city, city_data=city_data, save_path=initial_image_path)

    # 保存图片路径作为变量
    image_path = initial_image_path

    time = 0 

    # 优化过程：每次选择地块进行优化
    while True:
        answer = agent.conversation_list[-1]['content']
        
        # 检查是否需要更多信息
        if 'reason' in answer or ':' in answer:
            if time >= 3:  # 优化最多进行3次
                break
            else:
                agent.ask('Please get enough information before making a decision! Do not make up information yourself. Also, be careful to enter only one instruction at a time and nothing else.', initial_image_path)
        
        # 处理当前回答，获取规划信息
        info = envs.map_api.process_query(answer, city=city, city_data=city_data)
        
        # 如果回答中有涉及到"debate"，则执行辩论机制
        if "debate" in answer:
            if info is None:
                info = framework.function.debate.debate(city=city, city_data=city_data)
            else:
                info = info + framework.function.debate.debate(city=city, city_data=city_data)
        
        # 提供更多信息给代理人
        agent.ask(info, image_path)
        time += 1

    # 获取最终决策
    decision_single = agent.conversation_list[-1]['content']
    decision_numbers_single = envs.map_api.process_and_update_decisions(decision_single, city=city, city_data=city_data)

    # 保存决策结果
    with open(os.path.join(save_path, 'log.txt'), 'a') as f:
        f.write('MM Rewards:\n')

    # 评估和图表输出
    evaluator.print_reward(city=city, city_data=city_data, save_path=save_path)
    envs.map_api.plot(city=city, city_data=city_data, save_path=os.path.join(save_path, 'mm.png'))


    # 获取代理人对最终决策的理由
    decision_reason = agent.ask("Please provide a simple reason for the final decision you made regarding the land planning.", image_path)

    # 将决策和理由添加到决策列表
    decision_and_reasons.append({
        "decision": decision_numbers_single,
        "reason": decision_reason
    })


    # Multi-agent framework
    print('====== Multi Info Turn ======', flush=True)
    envs.map_api.rewrite(city=city, city_data=city_data)

    # 通过 init_plan_prompt 完成初步规划并保存
    initial_plan = agent.ask(decider_prompt.init_plan_prompt.format(tools=mm_tools) + 'Your task of planning is: ' + envs.map_api.planned_area_all(city=city, city_data=city_data), image_path=image_path)

    # 将初步规划结果保存到文件
    with open(os.path.join(save_path, 'initial_plan.txt'), 'a') as f:
        f.write('Initial Plan:\n')
        f.write(initial_plan + '\n')

    # 更新并保存初步规划图片
    initial_image_path = os.path.join(save_path, f'{city}_initial_plan.png')
    envs.map_api.plot(city=city, city_data=city_data, save_path=initial_image_path)
    image_path = initial_image_path  # 保存更新的图片路径

    # 启动多代理优化流程
    agents = role_generator.agents
    for agent in agents:
        agent.ask(prompt_generator.land_planning_prompt_syn() + 'Your task of planning is: ' + envs.map_api.planned_area_all(city=city, city_data=city_data) + 'Please output the decision of ' + str(num) + ' plots at the same time after obtaining the information.')
        
        time = 0
        while True:
            answer = agent.conversation_list[-1]['content']
            
            # 检查是否有足够的信息来做决策
            if 'reason' in answer or ':' in answer:
                if time >= 2:
                    break
                else:
                    agent.ask('Please get enough information before making a decision! Do not make up information yourself. Also, be careful to enter only one instruction at a time and nothing else.', image_path)
            
            # 获取规划信息并进行处理
            info = envs.map_api.process_query(answer, city=city, city_data=city_data)
            agent.ask(info, image_path)
            time += 1

    print('====== Debate Turn ======')
    sum = role_generator.sum_multi
    agree = 0

    # 辩论过程
    for turn in range(3):
        debate = prompt_generator.generate_debate_prompt()
        sum.ask(prompt_generator.generate_sum(agents[0], agents[1], agents[2]))
        
        if 'stop' in sum.conversation_list[-1]['content'].lower():
            agree = 1
            break
        
        for agent in agents:
            agent.ask(debate + sum.conversation_list[-1]['content'])

    # 如果没有达成共识，询问总结最合理方案
    if agree == 0:
        sum.ask('It is obvious that they could not reach an agreement. Please give us your own opinion on the most reasonable plan.')

    # 最终决策总结
    sum.ask("""Please summarize the final decisions and provide them in the following format:
                land_type: reason;
                - Type 1: Business Area
                - Type 2: Green Area
                - Type 3: Hospital Area
                - Type 4: Office Area
                - Type 5: Entertainment Area
                - Type 6: Residential Area
                - Type 7: School Area
                Example:
                25: 6, reason: ...;
                33: 5, reason: ...;
                35: 2, reason: ...;
                """)

    # 获取并更新决策
    decision_multi = sum.conversation_list[-1]['content']
    decision_numbers_multi = envs.map_api.process_and_update_decisions(decision_multi, city=city, city_data=city_data)

    # 更新图片并保存
    multi_image_path = os.path.join(save_path, f'{city}_multi_plan.png')
    envs.map_api.plot(city=city, city_data=city_data, save_path=multi_image_path)

    # 获取代理人对最终决策的理由
    decision_reason = agent.ask("Please provide a simple reason for the final decision you made regarding the land planning.", image_path)

    # 将决策和理由添加到决策列表
    decision_and_reasons.append({
        "decision": decision_numbers_single,
        "reason": decision_reason
    })

    # 记录多智能体奖励结果
    with open(os.path.join(save_path, 'log.txt'), 'a') as f:
        f.write('Multi Rewards:\n')

    # 评估奖励并保存结果
    evaluator.print_reward(city=city, city_data=city_data, save_path=save_path)



    # eval
    print('====== Eval Turn ======', flush=True)

    evaluator.evaluate_agents(decision_and_reasons, city=city, city_data=city_data, save_path=save_path, img_path=image_path)