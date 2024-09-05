from channels.generic.websocket import AsyncJsonWebsocketConsumer
from dotenv import load_dotenv


# import os
# load_dotenv()
import json
from .modules.agent import InterviewAgent, ResumableGroupChatManager
from autogen import Agent, AssistantAgent, UserProxyAgent, GroupChat
from datetime import datetime
import uuid


from pymongo import MongoClient

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['Spark_AI']
conversations = db['Questions_Answer']

class interviewConsumer(AsyncJsonWebsocketConsumer):
    agent = InterviewAgent()
    user_proxy = agent.user_proxy()
    interviewer = agent.interviewer()

    async def connect(self):
        if self.scope['user']:
            user = "uzma"
            await self.channel_layer.group_add(
                    f"user_{user}",
                    self.channel_name
            )
            await self.accept()
            initial = self.user_proxy.initiate_chat(
                self.interviewer,
                message="Please proceed with my interview",
            )
            info = str(initial.chat_history[1]['content']).split(".")
            respond = info[1]
            await self.send(text_data=respond)

            conversations.insert_one({
                "_id": str(uuid.uuid4()),
                "username": user,
                "messages": [{"content": initial.chat_history[1]['content']}],
                "started_at": datetime.now()  # Assuming timestamp is available in the scope
            })
        else:
            await self.close(code=1008, reason="Unauthorized")

    async def disconnect(self, close_code):
        await super().disconnect(close_code)

    async def receive(self, **kwargs):
        message = kwargs.get("text_data")
        group_chat = GroupChat(
            agents=[
                self.interviewer, self.user_proxy
            ],
            messages=[]
        )
        manager = ResumableGroupChatManager(
            name="Manager",
            groupchat=group_chat,
            llm_config=self.agent.llm_config,
            history=group_chat.messages
        )
        await self.user_proxy.a_initiate_chat(
            manager,
            message=message,
        )
        await self.send_json({
            "response": group_chat.messages[-1],
            "history": group_chat.messages,
        })

        # Update the MongoDB document with new messages
        conversations.update_one(
            {"username": "uzma"},
            {"$push": {"messages": {"content": group_chat.messages[-1], "response": message}}}
        )




# from channels.generic.websocket import AsyncJsonWebsocketConsumer
# import json
# from datetime import datetime
# from pymongo import MongoClient

# from .modules.agent import InterviewAgent, ResumableGroupChatManager
# from autogen import GroupChat
# from asgiref.sync import sync_to_async

# # MongoDB setup
# client = MongoClient('mongodb://localhost:27017/')
# db = client['Spark_AI']
# conversations = db['Questions_Answer']

# class interviewConsumer(AsyncJsonWebsocketConsumer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.agent = InterviewAgent()
#         self.user_proxy = self.agent.user_proxy()
#         self.interviewer = self.agent.interviewer()
#         self.session_id = None  # To track the session-specific document in MongoDB

#     async def connect(self):
#         if self.scope['user']:
#             user = "unravler"
#             await self.channel_layer.group_add(
#                     f"user_{user}",
#                     self.channel_name
#             )
#             await self.accept()

#             # Convert the synchronous initiate_chat method to async
#             initiate_chat_async = sync_to_async(self.user_proxy.initiate_chat)
#             initial_response = await initiate_chat_async(
#                 self.interviewer,
#                 message="Please proceed with my interview",
#             )
#             info = str(initial_response.chat_history[1]['content']).split(".")
#             respond = info[1]
#             await self.send(text_data=respond)

#             # MongoDB insertion code remains the same
#             conversations.insert_one({
#                 "username": user,
#                 "messages": [{"content": initial_response.chat_history[1]['content']}],
#                 "started_at": datetime.now()
#             })
#         else:
#             await self.close(code=1008, reason="Unauthorized")
#     async def disconnect(self, close_code):
#         # Optionally update the document with session end time or other metadata
#         conversations.update_one(
#             {"_id": self.session_id},
#             {"$set": {"ended_at": datetime.now()}}
#         )
#         await super().disconnect(close_code)

#     async def receive(self, **kwargs):
#         message = kwargs.get("text_data")
#         group_chat = GroupChat(
#             agents=[self.interviewer, self.user_proxy],
#             messages=[]
#         )
#         manager = ResumableGroupChatManager(
#             name="Manager",
#             groupchat=group_chat,
#             llm_config=self.agent.llm_config,
#             history=group_chat.messages
#         )
#         await self.user_proxy.a_initiate_chat(
#             manager,
#             message=message,
#         )
#         await self.send_json({
#             "response": group_chat.messages[-1],
#             "history": group_chat.messages,
#         })

#         # Update the MongoDB document with new messages
#         conversations.update_one(
#             {"_id": self.session_id},
#             {"$push": {"messages": {"sent": message, "response": group_chat.messages[-1]}}}
#         )
