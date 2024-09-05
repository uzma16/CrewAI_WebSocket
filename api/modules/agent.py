from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager


class InterviewAgent:
    def __init__(self) -> None:
        self.config_list = [
            {
                'model': 'gpt-3.5-turbo-16k',
                'api_key': 'sk-proj-lG2Fk8i7e6nt5N9fNTovT3BlbkFJ74J0EJw5Vooi5pKyMgFT'
            }
        ]

        self.llm_config = {
            "seed": 42,
            "config_list": self.config_list,
            "temperature": 0,
        }
    
    def handler(self, recipient, messages, sender, config):
        if "callback" in config and  config["callback"] is not None:
            callback = config["callback"]
            callback(sender, recipient, messages[-1])
    
        with open('result.txt', 'a') as file:
            file.write(f"{messages[len(messages)-1]} \n")
        return False, None  # required to ensure the agent communication flow continues

    # UserProxyAgent to simulate the user input from terminal
    def user_proxy(self):
        proxy = UserProxyAgent(
            name="User_proxy",
            system_message="You are now interacting with the interview system.",
            code_execution_config={"use_docker":False},
            human_input_mode="NEVER",
            is_termination_msg=lambda message: True # Always True
        )
        return proxy
    
    # InterviewerAgent to ask questions and process responses
    def interviewer(self):
        interviewer_agent = AssistantAgent(
            name="Interviewer",
            system_message= '''My first question would be 'Tell me the problem that you want to solve' then going forward I will ask 
            another question related to user's problem only, because my work is to collect all the info about user problem by asking 
            question. So that when my planner team works to solve the problem or plan the solution it will have all the information given
            by user.I will also ask about the timeline of completion of problem''',
            llm_config=self.llm_config,
        )
        return interviewer_agent

class ResumableGroupChatManager(GroupChatManager):
    groupchat: GroupChat

    def __init__(self, groupchat, history, **kwargs):
        self._groupchat = groupchat
        self.groupchat.speaker_selection_method = "round_robin"
        if history:
            self._groupchat.messages = history

        super().__init__(self._groupchat, **kwargs)

        if history:
            self.restore_from_history(history)

    def restore_from_history(self, history) -> None:
        for message in history:
            # broadcast the message to all agents except the speaker.  This idea is the same way GroupChat is implemented in AutoGen for new messages, this method simply allows us to replay old messages first.
            for agent in self._groupchat.agents:
                if agent != self:
                    self.send(message, agent, request_reply=False, silent=True)
    
    #The default message uses the full system message, which is a long string.  We are overriding this to use a shorter message.
    

# agents.py
# from autogen import Agent, AssistantAgent, UserProxyAgent

# # Configuration for the Large Language Model (LLM)
# llm_config = {
#     "seed": 42,
#     "config_list": [
#         {
#             'model': 'gpt-3.5-turbo-16k',
#             'api_key': 'sk-proj-lG2Fk8i7e6nt5N9fNTovT3BlbkFJ74J0EJw5Vooi5pKyMgFT'
#         }
#     ],
#     "temperature": 0,
# }

# class InterviewAgent:
#     def __init__(self):
#         self.user_proxy = UserProxyAgent(
#             name="User_proxy",
#             system_message="You are now interacting with the interview system.",
#             code_execution_config={"use_docker": False}
#         )
#         self.interviewer = AssistantAgent(
#             name="Interviewer",
#             system_message="My first question would be 'Tell me the problem that you want to solve'...",
#             llm_config=llm_config
#         )
