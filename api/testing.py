from autogen import Agent, AssistantAgent, UserProxyAgent
import os
import requests

# Set the correct Groq API key and base URL
os.environ["GROQ_API_KEY"] = "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"
os.environ["GROQ_API_BASE"] = "https://api.groq.com/openai/v1"  # Ensure this is correct

# Verify environment variables
print("GROQ_API_KEY:", os.environ.get("GROQ_API_KEY"))
print("GROQ_API_BASE:", os.environ.get("GROQ_API_BASE"))

# # Test manual API connection
# try:
#     response = requests.post(
#         f"{os.environ['GROQ_API_BASE']}/test-endpoint",
#         headers={"Authorization": f"Bearer {os.environ['GROQ_API_KEY']}"},
#         json={"message": "test"}
#     )
#     response.raise_for_status()  # Raise an error for bad status codes
#     print("Manual API call response:", response.json())
# except requests.exceptions.RequestException as e:
#     print("Error during manual API call:", e)

# Configuration for the Groq model
llm_config = {
    "cache_seed": 48,
    "config_list": [{
        "model": "gemma-7b-it",  # Explicitly set model name for Groq
        "api_key": os.environ["GROQ_API_KEY"], 
        "base_url": os.environ["GROQ_API_BASE"]
    }],
}

# # UserProxyAgent to simulate user input
# user_proxy = UserProxyAgent(
#     name="User_proxy",
#     system_message="You are now interacting with the interview system.",
#     code_execution_config={"use_docker": False},
# )

# # InterviewerAgent to ask questions and process responses
# class InterviewerAgent(AssistantAgent):
#     def __init__(self, name, system_message, llm_config):
#         super().__init__(name, system_message, llm_config)
#         self.questions = [
#             "How can I assist you today?",
#             "Tell me more about your product.",
#             "What are the key features of your product?",
#             "Who is your target audience?",
#             "What is your advertising budget?",
#             "What are your advertising goals?"
#         ]
#         self.current_question = 0
#         self.stop_interview = False

#     def handle_message(self, message, sender):
#         if self.stop_interview:
#             self.send_message("Thank you for providing all the information. Our team will review and get back to you.", recipient=sender)
#         else:
#             response = self.generate_response(message)
#             self.send_message(response, recipient=sender)

#     def generate_response(self, message):
#         if self.current_question < len(self.questions):
#             response = self.questions[self.current_question]
#             self.current_question += 1
#             return response
#         else:
#             return "Thank you for providing all the information. Our team will review and get back to you."

# interviewer = InterviewerAgent(
#     name="Interviewer",
#     system_message='''I will ask questions one by one. My first question would be 'How can I assist you today?' Then, going forward, I will ask 
#             another question related to the user's problem only, because my work is to collect all the information about the user's problem by asking 
#             questions. So that when my planner team works to solve the problem or plan the solution, it will have all the information given
#             by the user. I will also ask about the timeline for the completion of the problem.''',
#     llm_config=llm_config,
# )

# # ObserverAgent to monitor the conversation and signal when to stop
# class ObserverAgent(AssistantAgent):
#     def __init__(self, name, system_message, llm_config):
#         super().__init__(name, system_message, llm_config)
#         self.sufficient_data_flag = False

#     def handle_message(self, message, sender):
#         # Logic to determine if sufficient data has been collected
#         if "advertising goals" in message.lower():  # Example condition
#             self.sufficient_data_flag = True
#             interviewer.stop_interview = True
#             self.send_message("Sufficient data collected. Interviewer, please conclude the interview.", recipient=sender)
#         else:
#             self.send_message("Continue the interview.", recipient=sender)

# observer = ObserverAgent(
#     name="Observer",
#     system_message="I will monitor the conversation to ensure sufficient data is collected.",
#     llm_config=llm_config,
# )

# # Debugging: Print configurations to ensure they are correct
# print("User Proxy Agent:", user_proxy)
# print("Interviewer Agent:", interviewer)
# print("Observer Agent:", observer)
# print("LLM Config:", llm_config)

# # Function to start the conversation
# def start_interview():
#     try:
#         # Start conversation
#         interviewer.initiate_chat(
#             user_proxy,
#             message="How can I assist you today?",
#         )
#     except Exception as e:
#         print("Error during chat initiation:", e)

# # Start the interview process
# start_interview()


#-----------------------------------------------------------------------------------------
# from autogen import Agent, AssistantAgent, UserProxyAgent
# import os
# import requests

# # Set the correct Groq API key and base URL
# os.environ["GROQ_API_KEY"] = "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"
# os.environ["GROQ_API_BASE"] = "https://api.groq.com/openai/v1"  # Ensure this is correct

# # Verify environment variables
# print("GROQ_API_KEY:", os.environ.get("GROQ_API_KEY"))
# print("GROQ_API_BASE:", os.environ.get("GROQ_API_BASE"))

# import os
# import requests
# from autogen import Agent, AssistantAgent, UserProxyAgent


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

# # Configuration for the Groq model now uses a function to encapsulate logic
# def get_llm_config(api_key, api_base):
#     return {
#         "cache_seed": 48,
#         "config_list": [{
#             "model": "gemma-7b-it",
#             "api_key": api_key,
#             "base_url": api_base
#         }],
#     }
# class AssistantAgent:
#     def __init__(self, name, system_message, llm_config):
#         self.name = name
#         self.system_message = system_message
#         self.llm_config = llm_config
#         self.observers = []  # Observers like TriggerAgent

#     def add_observer(self, observer):
#         if observer not in self.observers:
#             self.observers.append(observer)

#     def notify_observers(self, message):
#         for observer in self.observers:
#             observer.handle_message(message, self)

#     def send_message(self, message, recipient):
#         print(f"{self.name} to {recipient.name}: {message}")
#         recipient.receive_message(message, self)
#         self.notify_observers(message)

#     def receive_message(self, message, sender):
#         print(f"Message received from {sender.name}: {message}")
#         self.notify_observers(message)

#     def initiate_chat(self, recipient, message):
#         print(f"Initiating chat with {recipient.name}")
#         interviewer.initiate_chat(recipient,message)

        

# class EnhancedUserProxyAgent(UserProxyAgent):
#     def __init__(self, name, system_message, code_execution_config):
#         super().__init__(name, system_message, code_execution_config)

#     def receive_message(self, message, sender):
#         # Implement handling of received messages
#         print(f"{self.name} received a message from {sender.name}: {message}")
#         # You could add additional logic here for the agent to process the message


# class TriggerAgent(AssistantAgent):
#     def __init__(self, name, system_message, llm_config, stop_trigger):
#         super().__init__(name, system_message, llm_config)
#         self.interaction_count = 0
#         self.stop_trigger = stop_trigger  # A callback to stop the interview

#     def handle_message(self, message, sender):
#         # Increment the interaction count each time a message is processed
#         self.interaction_count += 1
#         print(f"{self.name} noticed message: {message} (Count: {self.interaction_count})")

#         # Check if the interaction count reaches 2 (two questions and answers)
#         if self.interaction_count >= 4:  # 2 questions and 2 answers
#             self.stop_trigger()  # Call the stop function if criteria are met
#             self.send_message("Thank you for your responses. We have all the information we need.", sender)

# def stop_interview():
#     print("Stopping the interview as sufficient interactions have been made.")


# user_proxy = EnhancedUserProxyAgent(
#     name="User_proxy",
#     system_message="You are now interacting with the interview system.",
#     code_execution_config={"use_docker": False},
# )

# # AssistantAgent with detailed role
# interviewer = AssistantAgent(
#     name="Interviewer",
#     system_message=(
#        '''I will ask questions one by one. My first question would be 'How can I assist you today?' Then, going forward, I will ask 
#             another question related to the user's problem only, because my work is to collect all the information about the user's problem by asking 
#             questions. So that when my planner team works to solve the problem or plan the solution, it will have all the information given
#             by the user. I will also ask about the timeline for the completion of the problem.
#             I will ask questions like:
#              "How can I assist you today?",
#             "Tell me more about your product.",
#             "What are the key features of your product?",
#             "Who is your target audience?",
#             "What is your advertising budget?",
#             "What are your advertising goals?"'''
#     ),
#     llm_config=get_llm_config(os.environ['GROQ_API_KEY'], os.environ['GROQ_API_BASE'])
# )

# # Assuming 'interviewer' and 'user_proxy' are already defined

# trigger_agent = TriggerAgent(
#     name="TriggerAgent",
#     system_message="Monitoring the interaction count...",
#     llm_config=get_llm_config(os.environ['GROQ_API_KEY'], os.environ['GROQ_API_BASE']),
#     stop_trigger=stop_interview
# )

# # Add this trigger agent to the interviewer
# interviewer.add_observer(trigger_agent)

# def send_message(self, message, recipient):
#     print(f"{self.name}: {message}")
#     recipient.receive_message(message, self)
#     for agent in self.additional_agents:
#         agent.handle_message(message, recipient)  # Ensure agents handle messages to and from each other


# # Function to start the conversation
# def start_interview():
#     try:
#         interviewer.initiate_chat(
#             user_proxy,
#             message="How can I assist you today?"
#         )
#     except Exception as e:
#         print("Error during chat initiation:", e)

# start_interview()




from autogen import Agent, AssistantAgent, UserProxyAgent



# Function to print messages and save to file
def print_messages(recipient, messages, sender, config):
    if "callback" in config and config["callback"] is not None:
        callback = config["callback"]
        callback(sender, recipient, messages[-1])
    
    with open('result.txt', 'a') as file:
        file.write(f"{messages[-1]} \n")
    return False, None  # Ensure the agent communication flow continues

# UserProxyAgent to simulate user input
user_proxy = UserProxyAgent(
    name="User_proxy",
    system_message="You are now interacting with the interview system.",
    code_execution_config={"use_docker": False},
)

# # CoordinatorAgent to manage the conversation
# class CoordinatorAgent(AssistantAgent):
#     def __init__(self, name, system_message, llm_config):
#         super().__init__(name, system_message, llm_config)
#         self.questions_asked = []

#     def generate_next_question(self):
#         aspects = ["What", "Why", "When", "How"]
#         for aspect in aspects:
#             if aspect not in self.questions_asked:
#                 self.questions_asked.append(aspect)
#                 return f"{aspect} question about the problem"
#         return "Thank you for providing all the information."

#     def handle_message(self, message, sender):
#         next_question = self.generate_next_question()
#         self.send_message(next_question, recipient=sender)

# coordinator = CoordinatorAgent(
#     name="Coordinator",
#     system_message="I will manage the conversation to ensure all aspects of the problem are covered.",
#     llm_config=llm_config,
# )

# InterviewerAgent to ask questions and process responses
interviewer = AssistantAgent(
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
    llm_config=llm_config,
)

user_proxy.initiate_chat(
    interviewer,
    message="Please proceed with my interview",
)
