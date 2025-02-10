# 导入openai库
from openai import OpenAI
import os
import base64

client = OpenAI()

class Chat4:
    def __init__(self, name, role=[]) -> None:
        self.name = name
        # 初始化对话列表，可以加入一个key为system的字典，有助于形成更加个性化的回答
        if role:
            self.conversation_list = [{'role':'system','content':role}]
        else:
            self.conversation_list = []

    # 打印对话
    def show_conversation(self, msg_list):
        for msg in msg_list:
            if msg['role'] == 'user':
                print(f"\U0001F64B: {msg['content']}", flush=True)
            elif msg['role'] == 'assistant':
                print(f"\U0001f916 (" + self.name + "): "f"{msg['content']}", flush=True)

    # 提示chatgpt
    def ask(self, prompt):
        self.conversation_list.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(model="gpt-4-1106-preview", messages=self.conversation_list)
        answer = response.choices[0].message.content
        # 下面这一步是把chatGPT的回答也添加到对话列表中，这样下一次问问题的时候就能形成上下文了
        self.conversation_list.append({"role": "assistant", "content": answer})
        self.show_conversation(self.conversation_list[-2:])


class Chat4o:
    def __init__(self, name, role=[]) -> None:
        self.name = name
        # 初始化对话列表，可以加入一个key为system的字典，有助于形成更加个性化的回答
        if role:
            self.conversation_list = [{'role':'system','content':role}]
        else:
            self.conversation_list = []

    # Function to encode the image
    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # 打印对话
    def show_conversation(self, msg_list):
        for msg in msg_list:
            if msg['role'] == 'user':
                print(f"\U0001F64B: {msg['content'][0]}", flush=True)
            elif msg['role'] == 'assistant':
                print(f"\U0001f916 (" + self.name + "): "f"{msg['content']}", flush=True)

    # 提示chatgpt
    def ask(self, prompt, image_path):
        base64_image = self.encode_image(image_path)
        self.conversation_list.append({"role": "user","content": [{"type": "text", "text": prompt},{"type": "image_url","image_url": {"url":  f"data:image/png;base64,{base64_image}",}}]})
        response = client.chat.completions.create(model="gpt-4o", messages=self.conversation_list)
        answer = response.choices[0].message.content
        # 下面这一步是把chatGPT的回答也添加到对话列表中，这样下一次问问题的时候就能形成上下文了
        self.conversation_list.append({"role": "assistant", "content": answer})
        self.show_conversation(self.conversation_list[-2:])


class Chat3:
    def __init__(self, name, role=[]) -> None:
        self.name = name
        # 初始化对话列表，可以加入一个key为system的字典，有助于形成更加个性化的回答
        if role:
            self.conversation_list = [{'role':'system','content':role}]
        else:
            self.conversation_list = []

    # 打印对话
    def show_conversation(self, msg_list):
        for msg in msg_list:
            if msg['role'] == 'user':
                print(f"\U0001F64B: {msg['content']}", flush=True)
            elif msg['role'] == 'assistant':
                print(f"\U0001f916 (" + self.name + "): "f"{msg['content']}", flush=True)

    # 提示chatgpt
    def ask(self, prompt):
        self.conversation_list.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(model="gpt-3.5-turbo-16k", messages=self.conversation_list)
        answer = response.choices[0].message.content
        # 下面这一步是把chatGPT的回答也添加到对话列表中，这样下一次问问题的时候就能形成上下文了
        self.conversation_list.append({"role": "assistant", "content": answer})
        self.show_conversation(self.conversation_list[-2:])


# 决策者
sum_agent = Chat4(
    name="Judge-Single",
    role="I am a community decision-maker responsible for balancing the interests of residents, business owners, and developers. My goal is to create a vibrant and sustainable community that meets the diverse needs of its inhabitants. From the resident perspective, I prioritize factors such as comfortable living environments, convenient commutes, green spaces, and safety. Understanding the concerns of business owners, I seek to foster a commerce-friendly environment with high foot traffic, accessibility, and support for local businesses. Additionally, considering the developer's viewpoint, I aim to maximize land usage for innovative and sustainable projects while adhering to zoning regulations and minimizing environmental impact. My decision-making process involves careful consideration of the collective well-being, fostering collaboration among stakeholders, and creating a community that thrives economically, socially, and environmentally."
)

sum_single = Chat4(
    name="Judge-Single",
    role="I am a community decision-maker responsible for balancing the interests of residents, business owners, and developers. My goal is to create a vibrant and sustainable community that meets the diverse needs of its inhabitants. From the resident perspective, I prioritize factors such as comfortable living environments, convenient commutes, green spaces, and safety. Understanding the concerns of business owners, I seek to foster a commerce-friendly environment with high foot traffic, accessibility, and support for local businesses. Additionally, considering the developer's viewpoint, I aim to maximize land usage for innovative and sustainable projects while adhering to zoning regulations and minimizing environmental impact. My decision-making process involves careful consideration of the collective well-being, fostering collaboration among stakeholders, and creating a community that thrives economically, socially, and environmentally."
)

import random
# Function to randomly generate profile attributes
def generate_profile():
    gender = random.choice(['Female', 'Male'])
    age = random.choice([10, 20, 30, 40, 50, 60])
    education = random.choice(['Higher Education', 'No Higher Education'])
    return gender, age, education

# Resident Agent
resident_gender, resident_age, resident_education = generate_profile()
resident_agent = Chat4o(
    name="Resident", 
    role=f"As a {resident_gender} resident aged {resident_age} with {resident_education} education, I seek an ideal living environment that accommodates a wide range of age groups within the community. My priorities include easy access to healthcare services, quality educational facilities for children, and ample recreational spaces for leisure. I value safety, green spaces, and a strong sense of community. It is important for me to live in a neighborhood that strikes a balance between modern conveniences and a welcoming atmosphere for families and individuals alike."
)

# Developer Agent
developer_gender, developer_age, developer_education = generate_profile()
developer_agent = Chat4o(
    name="Developer", 
    role=f"As a {developer_gender} developer aged {developer_age} with {developer_education} education, I aim to maximize land use for development while focusing on creating innovative and sustainable projects. My main priorities include optimizing space for commercial growth, adhering to zoning regulations, minimizing environmental impact, and incorporating smart technologies. I am particularly interested in areas with potential for mixed-use developments, and I value collaboration with local communities to ensure that my projects meet their needs and contribute to a thriving urban environment."
)

# Government Agent
government_gender, government_age, government_education = generate_profile()
government_agent = Chat4o(
    name="Government", 
    role=f"As a {government_gender} government representative aged {government_age} with {government_education} education, my primary focus is on ensuring that urban planning aligns with public policies, regulatory frameworks, and long-term goals. I prioritize sustainability, social equity, and the efficient use of resources while considering the needs of the broader population. I am committed to creating an inclusive urban environment that meets the needs of residents, developers, and businesses, while also addressing challenges such as environmental impact, infrastructure, and resilience."
)

agents = [resident_agent, developer_agent, government_agent]

resident_agent_eval = Chat4o(name="Resident", role="As a resident, I seek an ideal living environment that accommodates a wide range of age groups within the community. My priorities include easy access to healthcare services, quality educational facilities for children, and ample recreational spaces for leisure. I value safety, green spaces, and a strong sense of community. It is important for me to live in a neighborhood that strikes a balance between modern conveniences and a welcoming atmosphere for families and individuals alike.")
# Developer Agent
developer_agent_eval = Chat4o(name="Developer", role="As a developer, I aim to maximize land use for development while focusing on creating innovative and sustainable projects. My main priorities include optimizing space for commercial growth, adhering to zoning regulations, minimizing environmental impact, and incorporating smart technologies. I am particularly interested in areas with potential for mixed-use developments, and I value collaboration with local communities to ensure that my projects meet their needs and contribute to a thriving urban environment.")
# Government Agent
government_agent_eval = Chat4o(name="Government", role="As a government representative, my primary focus is on ensuring that urban planning aligns with public policies, regulatory frameworks, and long-term goals. I prioritize sustainability, social equity, and the efficient use of resources while considering the needs of the broader population. I am committed to creating an inclusive urban environment that meets the needs of residents, developers, and businesses, while also addressing challenges such as environmental impact, infrastructure, and resilience.")
agents_eval = [resident_agent_eval, developer_agent_eval, government_agent_eval]

# 评测
# Land Planning Evaluator Agent
evaluator_agent_3 = Chat3(name="Gpt3.5 Evaluator", role="I am a land planning evaluator. I will provide scores for two distinct land planning strategies, considering elements like environmental impact, social inclusivity, and long-term viability.")
evaluator_agent_4 = Chat4(name="Gpt4 Evaluator", role="I am a land planning evaluator. I will provide scores for two distinct land planning strategies, considering elements like environmental impact, social inclusivity, and long-term viability.")
evaluator_agent_4_num = Chat4(name="Gpt4 Evaluator Num", role="I am a land planning evaluator. I will provide scores for two distinct land planning strategies, considering elements like environmental impact, social inclusivity, and long-term viability. I will only give you the numbers in the two decisions, representing the two types of land use decisions, the meaning of the numbers will be given in the prompt, please use the directive to make a decision judgment.")

mm_flex_agent = Chat4o(name='Judge',
                    role="I am a community decision-maker responsible for balancing the interests of residents, business owners, and developers. My goal is to create a vibrant and sustainable community that meets the diverse needs of its inhabitants. From the resident perspective, I prioritize factors such as comfortable living environments, convenient commutes, green spaces, and safety. Understanding the concerns of business owners, I seek to foster a commerce-friendly environment with high foot traffic, accessibility, and support for local businesses. Additionally, considering the developer's viewpoint, I aim to maximize land usage for innovative and sustainable projects while adhering to zoning regulations and minimizing environmental impact. My decision-making process involves careful consideration of the collective well-being, fostering collaboration among stakeholders, and creating a community that thrives economically, socially, and environmentally.")
