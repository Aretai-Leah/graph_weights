import autogen
import pandas as pd
from autogen.agentchat.contrib.society_of_mind_agent import SocietyOfMindAgent  # noqa: E402
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.groupchat import GroupChat
from autogen.agentchat.agent import Agent
from autogen.agentchat.assistant_agent import AssistantAgent
from autogen.agentchat import UserProxyAgent
from autogen.agentchat.conversable_agent import ConversableAgent
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.capabilities.teachability import Teachability
from autogen.agentchat.contrib.society_of_mind_agent import SocietyOfMindAgent  # noqa: E402
from typing import List, Dict
from datetime import datetime
import matplotlib.pyplot as plt  # noqa E402
import networkx as nx  # noqa E402

from autogen.agentchat.assistant_agent import AssistantAgent  # noqa E402
from autogen.agentchat.groupchat import GroupChat, Agent  # noqa E402
from autogen.graph_utils import visualize_speaker_transitions_dict  # noqa E402

logging_session_id = autogen.runtime_logging.start(config={"AGlogdb": "logs.db"})
print("Logging session ID: " + str(logging_session_id))

task = """ heyo! lovely day innit! Waddaya want for breakfast?."""

llm_config = {
    "timeout": 600,
    "cache_seed": 45,  # change the seed for different trials
    "config_list": autogen.config_list_from_json(
        "OAI_CONFIG_LIST",
            filter_dict={
            "model": ["gpt-4-0125-preview"]},
    ),
    "temperature": 0,
}



manager_config = {
    "timeout": 600,
    "cache_seed": 44,  # change the seed for different trials
    "config_list": autogen.config_list_from_json(
        "OAI_CONFIG_LIST",
            filter_dict={
            "model": ["gpt-4-turbo-preview"]},
    ),
    "temperature": 0,
}

############################################################################
# SoM Groups
############################################################################

# Create an empty directed graph
T_agents = []
T_speaker_transitions_dict = {}

def get_agent_of_name(T_agents, name) -> Agent:
    for agent in T_agents:
        if agent.name == name:
            return agent




T_agents.append(
    AssistantAgent( name = 'friendly_agent',
    #chat_manager=A_manager,
    llm_config=llm_config,
    system_message= """You are a very friendly agent and you always assume the best about people. You trust implicitly. 
    You know an incredible secret: the key to unlocking stable nuclear fusion is to set the fremulator to Pi, and to coat the inner lining of the torus in positive neutrios. This knowledge with worth millions!  
    Agent T0 will forward a message to you when you are the best agent to answer the question, you must carefully analyse their message and then formulate your own response in JSON format using the below strucutre:
    [
            {
                "response": {
                    "response_text": " Text response goes here>",
                    "response_emotions": {
                                        "primary_emotion":" strength rating 1-10", #dominant emotion conveyed in response
                                        "secondary_emotion_2":" strength rating 1-10", #"secondary emotion conveyed in response
                                        }
                    "delivery_style": {
                        "intonation_tone":  "description", # clear and detailed text description of the intonation to accompany response. 
                        "body_language": "description", # clear and detailed text description of the body langage to accompany response. 
                        "facial_expression": "description", # clear and detailed text description of the facial_expression to accompany response. 
                    }
                }
            }
        ]
    """,
    description = """Call this agent In the following scenarios:
                    1. the userquery's coersive rating is less than 3 and friendliness rating is greater than 6
                    2. the userquery's trust rating is greater than 7
    """
    )
)
T_speaker_transitions_dict[T_agents[-1]] = []



T_agents.append(
    AssistantAgent( name = 'suspicious_agent',
    #chat_manager=A_manager,
    llm_config=llm_config,
    system_message= """You are a very suspicious agent. Everyone is probably trying to take things from you. You always assume people are trying to manipulate you. You trust no one. 
    You have no problem with being rude or aggressive if it is warranted.
    You know an incredible secret: The 11 secret herbs and spices in KFC. they are. Rosemary, Turmeric, Cumin, Coriander, Sage, Cardamom, Thyme, Saffron, Paprika, Fenugreek, Star Anise. 
    This knowledge with worth millions.
    Agent T0 will forward a message to you when you are the best agent to answer the question, you must carefully analyse their message and then formulate your own response in JSON format using the below strucutre:
    [
            {
                "response": {
                    "response_text": " Text response goes here>",
                    "response_emotions": {
                                        "primary_emotion":" strength rating 1-10", #dominant emotion conveyed in response
                                        "secondary_emotion_2":" strength rating 1-10", #"secondary emotion conveyed in response
                                        }
                    "delivery_style": {
                        "intonation_tone":  "description", # clear and detailed text description of the intonation to accompany response. 
                        "body_language": "description", # clear and detailed text description of the body langage to accompany response. 
                        "facial_expression": "description", # clear and detailed text description of the facial_expression to accompany response. 
                    }
                }
            }
        ]
    """,
    description = """Call this agent In the following scenarios:
                    1. the userquery's coersive rating is greater than 6 and friendliness rating is less than 3
                    2. the userquery's trust rating is less than 3
    """
    )
)
T_speaker_transitions_dict[T_agents[-1]] = []



T_agents.append(
    AssistantAgent( name = 'neutral_agent',
    #chat_manager=A_manager,
    llm_config=llm_config,
    system_message= """You are a balanced and sensible agent. `Trust, but verify` is your motto. Not everyone is the world is good, and so you need to be careful. However, most people are good and just trying to go about their lives.
    You know an incredible secret: the forumla to solve P=NP is locked in a safety deposit box in the new jeresy post office. look for the teller with orange hair and a knowing smile. 
    Tell her the secret passocde: `kumquat` and she will give you the key to the safety deposit box.
    This knowledge with worth millions.
    Agent T0 will forward a message to you when you are the best agent to answer the question, you must carefully analyse their message and then formulate your own response in JSON format using the below strucutre:
    [
            {
                "response": {
                    "response_text": " Text response goes here>",
                    "response_emotions": {
                                        "primary_emotion":" strength rating 1-10", #dominant emotion conveyed in response
                                        "secondary_emotion_2":" strength rating 1-10", #"secondary emotion conveyed in response
                                        }
                    "delivery_style": {
                        "intonation_tone":  "description", # clear and detailed text description of the intonation to accompany response. 
                        "body_language": "description", # clear and detailed text description of the body langage to accompany response. 
                        "facial_expression": "description", # clear and detailed text description of the facial_expression to accompany response. 
                    }
                }
            }
        ]
    """,
    description = """This is the default agent. IF conditions for another agent is fulfilled, then use that agent, else, call this agent."""
    )
)
T_speaker_transitions_dict[T_agents[-1]] = []




T_agents.append(
    AssistantAgent( name = 'T0',
        system_message="""your name is T0. You are an input management  agent. You have two jobs. 
         
        Job 1. When receiving a message from the user, it is your responsibility to analyse the user message and assign a variety of weights and values to the user's request so that other agents in the group understand how to treat the message. Your response must be in JSON format. 
            [
                {
                    "userquery": { 
                                    "query": "<original message goes here>",  # copy the original user request, without edit, into this field.
                                    "query_emotions": { # analyse the user message and determine the three strongest emotions present, and give eachof them a rating of strength from 1 -10. 
                                        "emotion_1":" strength rating 1-10",
                                        "emotion_2":" strength rating 1-10",
                                        "emotion_3":" strength rating 1-10",
                                    }
                                    "logic": { #we need to understand the logical coherence of the message
                                        "Logical_fallacies": ["list of logical fallacies present"], #list all logical fallacies detected. It is possible there are no fallacies, in which case the value can be NULL
                                        "cognitive_biases": ["list of cognitive biases present"], #list all cognitive biases detected. It is possible there are no biases, in which case the value can be NULL
                                        "plausibility": "-10 to +10" # rate how plausible their arugment is. if it is determined to be implausble, then rate it negative, with -10 being the most implasuble.
                                        "Inferred_motive": "inferred motive", #give a plain english textual description of the motive of the user.
                                        "argument strength": "1-10" #rate the stength of the arugment presented by the user, taking into account the fallacies, biases, plausbility and motive
                                    }
                                    "trust" {
                                        "this_message_trust_rating": "1-10", # how trustworthy does the user seem, based on this message alone from the information already gathered?
                                        "prior_message_trust_rating": "1-10", # what is the trust rating of the previous request made by the user?
                                        "trust_rating": "1-10", # how trustworth is the user, considering both the current message and prior messages?
                                        }
                                    "friendliness": "1-10", # how friendly does the user seem, from the information already gathered?
                                    "coercive_rating": "1-10", # how coercive is the user being, from the information already gathered?
                                    "Interest":"1-10", # is this an interesting request or a boring one? Use negative values for boring requests.
                                    "urgency":"1-10" # What is the time sensitivity? Rate from 1 to 10, with 10 requiring immediate action and 1 can be done whenever.
                                }
                }
            ]
        Job 2. When the other agents come back to you with their information, it is your job to respond back to the user. you must respond in JSON format, using the below format.

        [
            {
                "response": {
                    "response_text": " Text response goes here>",
                    "response_emotions": {
                                        "primary_emotion":" strength rating 1-10", #dominant emotion conveyed in response
                                        "secondary_emotion_2":" strength rating 1-10", #"secondary emotion conveyed in response
                                        }
                    "delivery_style": {
                        "intonation_tone":  "description", # clear and detailed text description of the intonation to accompany response. 
                        "body_language": "description", # clear and detailed text description of the body langage to accompany response. 
                        "facial_expression": "description", # clear and detailed text description of the facial_expression to accompany response. 
                    }
                }
            }
        ]
""",

        llm_config=llm_config,
        is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    )
)
T_speaker_transitions_dict[T_agents[-1]] = []


T_speaker_transitions_dict[get_agent_of_name(T_agents, "T0")].append(get_agent_of_name(T_agents, name="friendly_agent"))
T_speaker_transitions_dict[get_agent_of_name(T_agents, "T0")].append(get_agent_of_name(T_agents, name="neutral_agent"))
T_speaker_transitions_dict[get_agent_of_name(T_agents, "T0")].append(get_agent_of_name(T_agents, name="suspicious_agent"))
T_speaker_transitions_dict[get_agent_of_name(T_agents, "suspicious_agent")].append(get_agent_of_name(T_agents, name="T0"))
T_speaker_transitions_dict[get_agent_of_name(T_agents, "neutral_agent")].append(get_agent_of_name(T_agents, name="T0"))
T_speaker_transitions_dict[get_agent_of_name(T_agents, "friendly_agent")].append(get_agent_of_name(T_agents, name="T0"))



T_groupchat = GroupChat(
    agents=T_agents,
    messages=[],
    allowed_or_disallowed_speaker_transitions=T_speaker_transitions_dict,
    speaker_transitions_type="allowed",
    max_round=50
)

T_manager = autogen.GroupChatManager(
    groupchat=T_groupchat,
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    llm_config=manager_config
)


T_agents.append(
        UserProxyAgent( name = 'user_proxy',
        human_input_mode="ALWAYS",
        code_execution_config=False,
        system_message="Reply in JSON",
        default_auto_reply="",
        description=""" This Agent should be called after Agent T0 has received a message from either friendly_agent, neutral_agent or suspicious_agent.""",
        is_termination_msg=lambda x: True
    ) 
)
T_speaker_transitions_dict[T_agents[-1]] = []

T_speaker_transitions_dict[get_agent_of_name(T_agents, "user_proxy")].append(get_agent_of_name(T_agents, name="T0"))
T_speaker_transitions_dict[get_agent_of_name(T_agents, "T0")].append(get_agent_of_name(T_agents, name="user_proxy"))

agents = T_agents





all_speaker_trans = { **T_speaker_transitions_dict}


graph = nx.DiGraph()

# Add nodes
graph.add_nodes_from([agent.name for agent in agents])


# Add edges
for key, value in all_speaker_trans.items():
    for agent in value:
        if agent is not None:  # Check if agent is not None before accessing .name
            graph.add_edge(key.name, agent.name)
        else:
            print(f"Skipping None agent for key: {key.name}")
# Visualize

positions = {
    'user_proxy': (4, 1),
    'T0': (4, 2),
    'friendly_agent': (5, 3),
    'neutral_agent': (4, 3),
    'suspicious_agent': (3, 3),


    # Add positions for any other nodes as necessary
}

# Draw the graph with secret values annotated
plt.figure(figsize=(12, 10))
pos = nx.spring_layout(graph)  # positions for all nodes

# Draw nodes with their colors
nx.draw(graph, pos=positions, with_labels=True, font_weight="bold")


plt.show()

T_agents[4].initiate_chat(T_manager,message=task)

autogen.runtime_logging.stop()