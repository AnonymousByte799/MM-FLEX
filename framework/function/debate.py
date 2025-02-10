import framework.role_generator as role_generator
import framework.prompt.npc_prompt as npc_prompt
import envs.map_api
import re

def debate(city, city_data):
    agents = role_generator.agents
    for agent in agents:
        agent.ask(npc_prompt.land_planning_prompt() + 'Your task of planning is: ' + envs.map_api.planned_area_all(city=city, city_data=city_data) + envs.map_api.process_query('query_info ' + re.findall(r'\d+', envs.map_api.planned_area_all(city=city, city_data=city_data))[-1], city=city, city_data=city_data))
    
    # debate = npc_prompt.generate_debate_prompt()
    # for i in range(3):
    #     for agent in agents:
    #         agent.ask(debate + npc_prompt.generate_sum(agents[0], agents[1], agents[2]))
    return npc_prompt.generate_sum(agents[0], agents[1], agents[2])