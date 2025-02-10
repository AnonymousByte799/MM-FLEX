def land_planning_prompt():
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

    Follow these guidelines:
    - Make a decision on pecific type for the 'Planned Area(s)' based on the gathered information.
    - Use the following list format to make decisions for all planning regions at the same time, with the types in the list sorted by default planning sequence number from smallest to largest:
        [Type, Type, Type, Type, Type]: reason: ...;

    Example:
        [5, 3, 7, 2, 1]: reason: ...;
    which means the three planning plots are successively 5, 3, 7, 2 and 1 planning.

    Please control the reason within one sentence.
    """
    return prompt


def generate_debate_prompt():
    debate = """
    In the discussion on land use planning, various roles hold diverse opinions. The aim is to reach a consensus through dialogue. Here is a summary of the opinions of other roles and yours.
    
    Please share your current stance conversation. You can stick to or change your comments and still output in the original format.

    - Type 0: Planned Area
    - Type 1: Business Area
    - Type 2: Green Area
    - Type 3: Hospital Area
    - Type 4: Office Area
    - Type 5: Entertainment Area
    - Type 6: Residential Area
    - Type 7: School Area

    Example:
        5: reason: ...;

    Please control the reason within one sentence.
    """
    return debate


def generate_sum(agent1, agent2, agent3):
    return f"Resident: {agent1.conversation_list[-1]['content']}\nBusiness: {agent2.conversation_list[-1]['content']}\nDeveloper: {agent3.conversation_list[-1]['content']}"