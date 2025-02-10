init_prompt = """As an urban planner tasked with the decision-making process for a specific city community grid cell, your goal is to determine the most suitable type for this grid cell, considering the current urban layout and future development plans.
The region is represented by a grid, and each grid cell corresponds to a specific land type:

    - Type 0: Planned Area
    - Type 1: Business Area
    - Type 2: Green Area
    - Type 3: Hospital Area
    - Type 4: Office Area
    - Type 5: Entertainment Area
    - Type 6: Residential Area
    - Type 7: School Area

Your task involves planning specific areas marked as 'Planned Area(s)' (Type 0). The goal is to make informed decisions based on gathered information.

**Process Instructions:**
- Begin by thinking through the possible land types that could be suitable for the Planned Area, given the urban context.
- Each time you plan a grid cell, reason through why that particular type (e.g., Business Area, Green Area, etc.) is the best choice based on the specific characteristics of that location. For example, think about nearby amenities, ecological impact, traffic flow, and community needs.
- For each round, use the following reasoning process: first, gather all relevant information, then prioritize based on the four criteria: Service, Ecology, Economy, and Equity.
- Make your decision once you have enough data, and provide a concise explanation for why each decision was made.

You have access to a set of tools provided in the 'tools' dictionary: {tools}

**Follow these guidelines:**
- In each round of dialogue, state your reasoning before making the decision.
- After reasoning, decide the type for a specific 'Planned Area' and provide the reasoning.
- Output your decisions in the format of a list, sorted by the default planning sequence number from smallest to largest:
    Example: [5, 3, 7, 2, 1]: reason: ....;
    This means you are planning Type 5 for the first plot, Type 3 for the second plot, and so on.

Remember, keep your answers concise and ensure each reason is based on careful analysis and relevant data.
"""

init_plan_prompt = """As an urban planner tasked with the decision-making process for a specific city community grid cell, your goal is to determine the most suitable type for this grid cell, considering the current urban layout and future development plans.
The region is represented by a grid, and each grid cell corresponds to a specific land type:

    - Type 0: Planned Area
    - Type 1: Business Area
    - Type 2: Green Area
    - Type 3: Hospital Area
    - Type 4: Office Area
    - Type 5: Entertainment Area
    - Type 6: Residential Area
    - Type 7: School Area

Your task involves planning all 34 areas marked as 'Planned Area(s)' (Type 0) (gray color).

**Decision-making process:**
- For each area, follow these steps:
    1. **Reasoning:** Start by reasoning through the most suitable land type based on the current urban situation and future goals. Consider factors like accessibility, proximity to essential services, environmental impact, and space optimization.
    2. **Gather information:** Use the provided tools and gathered data to inform your decision-making.
    3. **Decision-making:** Once sufficient information is gathered, make a decision for the plot.
    4. **Explanation:** Provide a concise explanation of why the chosen land type is the most suitable for the area, considering Service, Ecology, Economy, and Equity factors.

**Guidelines:**
1. **Service:** Ensure that each residential area (Type 6) is surrounded by at least 5 service types, including Business, Office, Recreation, School, and Hospital.
2. **Ecology:** Ensure that at least 1/10 of the total area is covered by Green Areas (Type 2). This will help improve ecological sustainability and quality of life for residents.
3. **Economy:** Ensure that Business Areas (Type 1), Office Areas (Type 4), and Entertainment Areas (Type 5) are within 15 minutes’ walking distance of each other and well-distributed across the grid. Allocate at least 8 Business Areas, 6 Office Areas, and 8 Entertainment Areas.
4. **Equity:** Ensure the fair distribution of essential services. There should be at least 5 Schools (Type 7) and 5 Hospitals (Type 3), with each being fairly accessible to residents across the grid.
5. **Satisfaction:** Ensure that the final planning decisions balance the needs of residents, developers, and the government, ensuring equitable access to services, green spaces, and business opportunities.

**Restrictions:**
- At least 10 Green Areas, 8 Business Areas, 8 School Areas, and 6 Office Areas must be planned.
- Ensure that the same type of area (e.g., Business, School, etc.) is distributed as evenly as possible across the grid, avoiding clustering of one type unless necessary for urban function.

You are required to output a list of 34 elements representing the sequence number of the planned plot (sorted from smallest to largest). The element value is the type of the plot. You are not allowed to plan Residential Areas (Type 6).

**Example output:**
[5, 3, 3, ..., 7, 2, 1]: reason: ....;

Be concise, and make sure to base your decisions on relevant information and clear reasoning. For each round, remember to provide your reasoning before making a final decision.
"""
