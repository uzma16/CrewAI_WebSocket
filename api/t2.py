# Set the correct Groq API key and base URL

import os
import requests
from autogen import Agent, AssistantAgent, UserProxyAgent,GroupChat,GroupChatManager


os.environ["GROQ_API_KEY"] = "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"
os.environ["GROQ_API_BASE"] = "https://api.groq.com/openai/v1"  # Ensure this is correct

# Verify environment variables
print("GROQ_API_KEY:", os.environ.get("GROQ_API_KEY"))
print("GROQ_API_BASE:", os.environ.get("GROQ_API_BASE"))



# # Encapsulating API call into a function for better reuse and testing
# def test_api_connection(api_base, api_key):
#     url = f"{api_base}/test-endpoint"
#     headers = {"Authorization": f"Bearer {api_key}"}
#     try:
#         response = requests.post(url, headers=headers, json={"message": "test"})
#         response.raise_for_status()  # Ensures HTTPError is raised for bad responses
#         print("Manual API call response:", response.json())
#     except requests.exceptions.RequestException as e:
#         print("Error during manual API call:", e)

# test_api_connection(os.environ['GROQ_API_BASE'], os.environ['GROQ_API_KEY'])

# Configuration for the Groq model now uses a function to encapsulate logic
def get_llm_config(api_key, api_base):
    return {
        "cache_seed": 48,
        "config_list": [{
            "model": "gemma-7b-it",
            "api_key": api_key,
            "base_url": api_base
        }],
    }


class AssistantAgentProxy:
    def __init__(self, real_assistant):
        self.real_assistant = real_assistant
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, message):
        for observer in self.observers:
            observer.handle_message(message, self)

    def send_message(self, message, recipient):
        print(f"{self.real_assistant.name} to {recipient.name}: {message}")
        recipient.receive_message(message, self.real_assistant)
        self.notify_observers(message)

    def receive_message(self, message, sender):
        print(f"Message received from {sender.name}: {message}")
        self.notify_observers(message)

class TriggerAgent:
    def __init__(self, name, stop_trigger):
        self.name = name
        self.interaction_count = 0
        self.stop_trigger = stop_trigger

    def handle_message(self, message, sender):
        self.interaction_count += 1
        print(f"{self.name} noticed message: {message} (Count: {self.interaction_count})")
        if self.interaction_count >= 10:  # Stop after 10 questions
            self.stop_trigger()
            sender.send_message("Thank you for your responses. We have all the information we need.", sender)

def stop_interview():
    print("Stopping the interview as sufficient interactions have been made.")
    group_chat.active = False

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

user_proxy = UserProxyAgent(
    name="User_proxy",
    system_message="You are now interacting with the interview system.",
    code_execution_config={"use_docker": False},
)

# Initialize the assistant agent
real_interviewer = AssistantAgent(
    name="Interviewer",
    system_message='''I will give one (single) question at a time. My first question would be 'How can I assist you today?' Then, going forward, I will ask 
            another question related to the user's problem only, because my work is to collect all the information about the user's problem by asking 
            questions. So that when my planner team works to solve the problem or plan the solution, it will have all the information given
            by the user. I will also ask about the timeline for the completion of the problem. 
            Here the question should be a single string.
            The output of my LLM should be in the format <Question 1> & every question should be enclosed in {}
            For example:
            {
            Question 1 : "How can I assist you today?" (Single question at a time)
            }
            Remember my end goal is to collect information by asking single question at a time from user which will help planner team to plan the schedule for a given user problem''',
    llm_config=get_llm_config(os.environ['GROQ_API_KEY'], os.environ['GROQ_API_BASE'])
)

# Wrap the real interviewer with a proxy
interviewer = AssistantAgentProxy(real_interviewer)

# Create and add the trigger agent
trigger_agent = TriggerAgent("TriggerAgent", stop_interview)
interviewer.add_observer(trigger_agent)
group_chat = GroupChat(
            agents=[
                real_interviewer, user_proxy
            ],
            messages=[]
        )

manager = ResumableGroupChatManager(
    name="Manager",
    groupchat=group_chat,
    llm_config=get_llm_config(os.environ['GROQ_API_KEY'], os.environ['GROQ_API_BASE']),
    history=group_chat.messages
)

user_proxy.initiate_chat(
            manager,
            message="How can I assist you today?",
        )

