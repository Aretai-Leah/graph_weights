# Pseudo Weights and Bias implementation in Graph Sequence for Multi Agent conversation
#                                        OR
# I heard you liked neural networks, so I put neural networks in your neural networks.


![8h1et9](https://github.com/Aretai-Leah/graph_weights/assets/147453745/153a8f37-ca5e-4b62-9cfb-5f65a4ff815b)
I know i know, they're not really neural networks. But this was funny.

One of the recurrent challenges of multi agent systems is the selection of the next agent. This becomes increasingly problematic the more complex a workflow your agent group has. 


To improve speaker transition accuracy, we have combined the Autogen framework using the FSM transition graph with Agent Description and OpenAI JSON mode to implement pseudo weights and bias into the graph network of speaker transitions. This enables very fine control over which agent is called. 

This is the current speaker transition for Aretai. 

![Agent speaking transition - speaker transition 27_02_24](https://github.com/Aretai-Leah/graph_weights/assets/147453745/c3e59a3c-3948-4634-a119-15550bba09a8)

This complexity enables some very interesting behavior, including some that has been discussed earlier. 

However, there are multiple points where an Agent needs to make a decision on the next agent, and therefore has the opportunity to get it wrong. Moreover, there exists the potential for loops which do not end and never respond.    

The Autogen team has recently released an FSM graph framework for speaker transition, which in addition to being very cool, is also very useful. It allows for the kind of explicit definition of next speaker options by defining agents as nodes with edges defining valid paths.  

JSON mode is part of the openai API specification but is easily implemented in autogen.  Just add a response format in your OAI_CONFIG_LIST, and add in the word JSON into the system message and you’re good to go. 

#################################################
{
        "model": "gpt-4-0125-preview",
        "api_key": "sk-yourkeygohere",
        "response_format": { "type": "json_object" }
        },
#################################################

Using JSON mode we can enable reliable output for calculable values. These are the “weights”


#################################################
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

#################################################
























