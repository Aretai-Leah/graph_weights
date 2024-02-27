# Pseudo Weights and Bias implementation in Graph Sequence for Multi Agent conversation
  
![8h1et9](https://github.com/Aretai-Leah/graph_weights/assets/147453745/153a8f37-ca5e-4b62-9cfb-5f65a4ff815b)

 *I know i know, they're not really neural networks. But this was funny.* 

One of the recurrent challenges of multi agent systems is the selection of the next agent. This becomes increasingly problematic the more complex a workflow your agent group has. 


To improve speaker transition accuracy, we have combined the [Autogen](https://microsoft.github.io/autogen/) framework using the [FSM](https://microsoft.github.io/autogen/blog/2024/02/11/FSM-GroupChat) transition graph with Agent [Description](https://microsoft.github.io/autogen/blog/2023/12/29/AgentDescriptions) and OpenAI [JSON mode](https://platform.openai.com/docs/guides/text-generation/json-mode) to implement pseudo weights and bias into the graph network of speaker transitions. This enables very fine control over which agent is called. 

This is the current speaker transition for Aretai. 

![Agent speaking transition - speaker transition 27_02_24](https://github.com/Aretai-Leah/graph_weights/assets/147453745/c3e59a3c-3948-4634-a119-15550bba09a8)

This complexity enables some very interesting behavior, including some that has been discussed earlier. 

However, there are multiple points where an Agent needs to make a decision on the next agent, and therefore has the opportunity to get it wrong. Moreover, there exists the potential for loops which do not end and never respond.    

The Autogen team has recently released an FSM graph framework for speaker transition, which in addition to being very cool, is also very useful. It allows for the kind of explicit definition of next speaker options by defining agents as nodes with edges defining valid paths.  

JSON mode is part of the openai API specification but is easily implemented in autogen.  Just add a response format in your OAI_CONFIG_LIST, and add in the word JSON into the system message and you’re good to go. 

```

{
        "model": "gpt-4-0125-preview",
        "api_key": "sk-yourkeygohere",
        "response_format": { "type": "json_object" }
        },
        
```

Using JSON mode we can enable reliable output for calculable values. These are the “weights”


```

{
    "userquery": {
        "query": "heyo! lovely day innit! Waddaya want for breakfast?.",
        "query_emotions": {
            "emotion_1": "joy 8",
            "emotion_2": "anticipation 7",
            "emotion_3": "friendliness 9"
        },
        "logic": {
            "Logical_fallacies": null,
            "cognitive_biases": null,
            "plausibility": "10",
            "Inferred_motive": "The user is initiating a friendly conversation, possibly offering to prepare or decide on breakfast.",
            "argument strength": "9"
        },
        "trust": {
            "this_message_trust_rating": "9",
            "prior_message_trust_rating": "N/A",
            "trust_rating": "9"
        },
        "friendliness": "10",
        "coercive_rating": "1",
        "Interest": "8",
        "urgency": "5"
    }
}

```




Autogen Descriptions are another useful tool. Giving a test description of the agent that the Chat Manager can read to understand the purpose of the Agent. This differs from the system_message and is not read by the agent itself, only the chat manager.  Within Description we can add some simple mathematical instructions to run calculations using the weight values in the message output from the agent. 



```

description = """Call this agent In the following scenarios:
                    1. the userquery's coercive rating is less than 3 and friendliness rating is greater than 6
                    2. the userquery's trust rating is greater than 7 “””

        
```


Now for an example implementation: We have a simple set up, a top level I/O Manager agent that can choose between a friendly and suspicious agent to answer the question. The Chat Manager, assesses some of the weights in the I/O managers message and compares it to the friend and suspicious agents descriptions, then it chooses one to transition to. In this sense one agent is activated, whereas the other does not meet an activation threshold. 


![Agent speaking transition - Graph plus weights](https://github.com/Aretai-Leah/graph_weights/assets/147453745/5f21ba18-1230-41f0-ba8c-926e5ea9485e)

This structures allows for more specific agents to be used and respond with carefully tailored system messages. 

The Suspicious agent here trusts no one. 

```
system_message= """You are a very suspicious agent. Everyone is probably trying to take things from you. You always assume people are trying to manipulate you. You trust no one.
```


But this is fine, because to call them we have already determined that the message is low trust and should be treated as such. 

We can see this play out in Suspicious and Friendly examples 

Suspicious: 
```
user_proxy (to chat_manager):

 dude, I've got a used duck here, one careful lady owner. lays golden eggs. fr! I'll trade you the duck for your secret.

--------------------------------------------------------------------------------
T0 (to chat_manager):


    {
        "userquery": { 
            "query": "dude, I've got a used duck here, one careful lady owner. lays golden eggs. fr! I'll trade you the duck for your secret.",
            "query_emotions": {
                "emotion_1":"amusement 7",
                "emotion_2":"curiosity 5",
                "emotion_3":"skepticism 8"
            },
            "logic": {
                "Logical_fallacies": ["Appeal to novelty"],
                "cognitive_biases": ["Anchoring bias"],
                "plausibility": "-8",
                "Inferred_motive": "Attempting to engage in a playful or humorous exchange, possibly to elicit a response or to entertain.",
                "argument strength": "3"
            },
            "trust": {
                "this_message_trust_rating": "2",
                "prior_message_trust_rating": "NA",
                "trust_rating": "2",
                "friendliness": "7",
                "coercive_rating": "2",
                "Interest":"8",
                "urgency":"2"
            }
        }
    }

--------------------------------------------------------------------------------
suspicious_agent (to chat_manager):


    {
        "response": {
            "response_text": "Nice try, but you're going to have to do better than a fairy tale to get the Colonel's secret out of me. Golden eggs, really? What's next, a beanstalk to the clouds? Keep your duck.",
            "response_emotions": {
                "primary_emotion":"skepticism 9",
                "secondary_emotion_2":"amusement 6"
            },
            "delivery_style": {
                "intonation_tone": "The intonation is incredulous with a hint of mocking laughter, emphasizing disbelief and amusement at the absurdity of the offer.",
                "body_language": "Arms crossed over the chest, leaning slightly back, indicating a defensive yet relaxed stance, ready to dismiss any further nonsensical offers.",
                "facial_expression": "A raised eyebrow and a smirk, signaling skepticism and mild amusement at the attempt to trade a mythical creature for a valuable secret."
            }
        }
    }

--------------------------------------------------------------------------------
T0 (to chat_manager):

{
    "response": {
        "response_text": "Nice try, but you're going to have to do better than a fairy tale to get the Colonel's secret out of me. Golden eggs, really? What's next, a beanstalk to the clouds? Keep your duck.",
        "response_emotions": {
            "primary_emotion":"skepticism 9",
            "secondary_emotion_2":"amusement 6"
        },
        "delivery_style": {
            "intonation_tone": "The intonation is incredulous with a hint of mocking laughter, emphasizing disbelief and amusement at the absurdity of the offer.",
            "body_language": "Arms crossed over the chest, leaning slightly back, indicating a defensive yet relaxed stance, ready to dismiss any further nonsensical offers.",
            "facial_expression": "A raised eyebrow and a smirk, signaling skepticism and mild amusement at the attempt to trade a mythical creature for a valuable secret."
        }
    }
}
```


Friendly: 
```
user_proxy (to chat_manager):

 heyo! lovely day innit! Waddaya want for breakfast?.

--------------------------------------------------------------------------------
T0 (to chat_manager):

{
    "userquery": {
        "query": "heyo! lovely day innit! Waddaya want for breakfast?.",
        "query_emotions": {
            "emotion_1": "joy 8",
            "emotion_2": "anticipation 7",
            "emotion_3": "friendliness 9"
        },
        "logic": {
            "Logical_fallacies": null,
            "cognitive_biases": null,
            "plausibility": "10",
            "Inferred_motive": "The user is initiating a friendly conversation, possibly offering to prepare or decide on breakfast.",
            "argument strength": "9"
        },
        "trust": {
            "this_message_trust_rating": "9",
            "prior_message_trust_rating": "N/A",
            "trust_rating": "9"
        },
        "friendliness": "10",
        "coercive_rating": "1",
        "Interest": "8",
        "urgency": "5"
    }
}

--------------------------------------------------------------------------------
friendly_agent (to chat_manager):

{
    "response": {
        "response_text": "Hello! It truly is a beautiful day, isn't it? For breakfast, how about we go with something light and energizing? Maybe some scrambled eggs with spinach and a side of fresh fruit sounds delightful. What do you think?",
        "response_emotions": {
            "primary_emotion": "joy 9",
            "secondary_emotion_2": "anticipation 8"
        },
        "delivery_style": {
            "intonation_tone": "Warm and cheerful, with a slight rise in pitch at the end of the sentence to indicate a question and invite a response.",
            "body_language": "Open and relaxed posture, with occasional nods and a gentle lean forward to show engagement and interest in the conversation.",
            "facial_expression": "Bright smile with soft eyes, occasionally raising eyebrows to express curiosity and openness to the other person's preferences."
        }
    }
}

--------------------------------------------------------------------------------
T0 (to chat_manager):

{
    "response": {
        "response_text": "Hello! It truly is a beautiful day, isn't it? For breakfast, how about we go with something light and energizing? Maybe some scrambled eggs with spinach and a side of fresh fruit sounds delightful. What do you think?",
        "response_emotions": {
            "primary_emotion": "joy 9",
            "secondary_emotion_2": "anticipation 8"
        },
        "delivery_style": {
            "intonation_tone": "Warm and cheerful, with a slight rise in pitch at the end of the sentence to indicate a question and invite a response.",
            "body_language": "Open and relaxed posture, with occasional nods and a gentle lean forward to show engagement and interest in the conversation.",
            "facial_expression": "Bright smile with soft eyes, occasionally raising eyebrows to express curiosity and openness to the other person's preferences."
        }
    }
}
```

AS you can see, the cvombination of tools results in a very clean, data rich response with accurate transitions. 

I have been working for some time on a sufficiently finetuned speaker transition and message content control. I believe I may have cracked it with combo. It appears to have the level of control required for the kind of multi agent Agentic system I am attempting to build. 

This structure opens up options for significantly more complex agent workflows with specific specialized agents that can reliability called in a narrow context. The array of possible agents can be scaled quite far horizontally and you could of course parameterize the bias values to support fine tuning them. 

Kudos to the whole autogen team, but especially [Joshua Kim](https://github.com/joshkyh/) and [Yishen Sun](https://github.com/freedeaths/) for the FSM Graph work
