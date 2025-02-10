def land_planning_prompt():
    # Prompt for land planning task
    prompt = """
    Region Land Planning Task:

    You are responsible for planning land use in a specific region. The region is represented by a grid, and each grid cell corresponds to a specific land type:

    - Type 0: Planned Area
    - Type 1: Business Area
    - Type 2: Green Area
    - Type 3: Hospital Area
    - Type 4: Office Area
    - Type 5: Entertainment Area
    - Type 6: Residential Area
    - Type 7: School Area

    Your task involves planning a specific area marked as 'Planned Area' (Type 0). The goal is to make informed decisions based on gathered information.

    Instructions for interacting with the system:

    1. `query_info query`: Use this command to retrieve information about a specific location. For example, `query_info 25` returns details about the area at Serial Number 25.

    2. `query_neigh query`: Use this command to obtain information about neighboring locations. For example, `query_neigh 25` returns information like: [26]: Type 1; [24]: Type 2; [25]: Type 6, which are the details about the area around Serial Number 25.

    3. `query_area area_type`: Use this command to calculate the percentage of a specific land type in the entire region. For example, `query_area Residential Area` returns the percentage of Residential Areas in the region.

    Follow these guidelines:

    - Gather information using 'query_info', query_area' and 'query_neigh' commands.
    - Make a decision on one specific type for the 'Planned Area' based on the gathered information.
    - Provide decisions in the following format:
        Type: reason: ...;

    Example:
        5: reason: ...;

    When the final decision is made, strictly follow the format of the example to output. Each line should include the keyword 'reason'. Do not output additional supplementary sentences.

    Begin by issuing commands to gather information about the region. You can only enter one command at a time. You can only enter one command at a time. You can only enter one command at a time.

    Do not plan for residential areas, i.e., do not make decisions numbered 6!
    """
    return prompt


def generate_debate_prompt():
    debate = "In the discussion on land use planning, various roles hold diverse opinions. The aim is to reach a consensus through dialogue. Here is a summary of the opinions of other roles and yours. Share your current stance in the ongoing conversation. At the conclusion of each exchange, specify any updated decisions. If you agree, a simple expression of agreement is sufficient."
    return debate


def generate_sum(agent1, agent2, agent3):
    return f"resident: {agent1.conversation_list[-1]['content']}\nbusiness: {agent2.conversation_list[-1]['content']}\ndeveloper: {agent3.conversation_list[-1]['content']}"


def next_turn_prompt():
    return "Next Turn:\n\n"\
           "Building upon your previous decisions, I now present another area within the community for planning. "\
           "Similar to before, you can use commands to gather information about this new area and proceed with its planning. "\
           "Feel free to continue using the available instructions to make informed decisions for the community."


def land_planning_prompt_syn():
    # Prompt for land planning task
    prompt = """
    Region Land Planning Task:

    You are responsible for planning land use in a specific region. The region is represented by a grid, and each grid cell corresponds to a specific land type:

    - Type 0: Planned Area
    - Type 1: Business Area
    - Type 2: Green Area
    - Type 3: Hospital Area
    - Type 4: Office Area
    - Type 5: Entertainment Area
    - Type 6: Residential Area
    - Type 7: School Area

    Your task involves planning a specific area marked as 'Planned Area' (Type 0). The goal is to make informed decisions based on gathered information.

    Instructions for interacting with the system:

    1. `query_info query`: Use this command to retrieve information about a specific location. For example, `query_info 25` returns details about the area at Serial Number 25.

    2. `query_neigh query`: Use this command to obtain information about neighboring locations. For example, `query_neigh 25` returns information like: [26]: Type 1; [24]: Type 2; [25]: Type 6, which are the details about the area around Serial Number 25.

    3. `query_area area_type`: Use this command to calculate the percentage of a specific land type in the entire region. For example, `query_area Residential Area` returns the percentage of Residential Areas in the region.

    Follow these guidelines:

    - Gather information using 'query_info', query_area' and 'query_neigh' commands.
    - Make a decision on one specific type for the 'Planned Area' based on the gathered information.
    - Provide decisions in the following format:
        Serial Number: land_type, reason_number;

    Example:
        25: 6, reason: ...;
        33: 5, reason: ...;
        35: 2, reason: ...;
        ...;

    When the final decision is made, strictly follow the format of the example to output. Each line should include the keyword 'reason'. Do not output additional supplementary sentences.

    Begin by issuing commands to gather information about the region. You can only enter one command at a time. You can only enter one command at a time. You can only enter one command at a time.
    """
    return prompt


def land_planning_prompt_syn_mm():
    # Prompt for land planning task
    prompt = """
    Region Land Planning Task:

    You are responsible for planning land use in a specific region. The region is represented by a grid, and each grid cell corresponds to a specific land type:

    - Type 0: Planned Area
    - Type 1: Business Area
    - Type 2: Green Area
    - Type 3: Hospital Area
    - Type 4: Office Area
    - Type 5: Entertainment Area
    - Type 6: Residential Area
    - Type 7: School Area

    Your task involves planning a specific area marked as 'Planned Area' (Type 0). The goal is to make informed decisions based on gathered information.

    Instructions for interacting with the system:

    1. `query_info query`: Use this command to retrieve information about a specific location. For example, `query_info 25` returns details about the area at Serial Number 25.

    2. `query_area area_type`: Use this command to calculate the percentage of a specific land type in the entire region. For example, `query_area Residential Area` returns the percentage of Residential Areas in the region.

    Follow these guidelines:

    - Gather information using 'query_info', query_area' and 'query_neigh' commands.
    - Make a decision on one specific type for the 'Planned Area' based on the gathered information.
    - Provide decisions in the following format:
        Serial Number: land_type, reason_number;

    Example:
        25: 6, reason: ...;
        33: 5, reason: ...;
        35: 2, reason: ...;
        ...;

    When the final decision is made, strictly follow the format of the example to output. Each line should include the keyword 'reason'. Do not output additional supplementary sentences.

    Begin by issuing commands to gather information about the region. You can only enter one command at a time. You can only enter one command at a time. You can only enter one command at a time.
    """
    return prompt