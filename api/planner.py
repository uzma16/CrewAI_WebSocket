from pymongo import MongoClient
from datetime import datetime, timedelta
import json
from crewai_tools import BaseTool
from crewai import Agent, Task, Crew, Process
import os

# Set the OPENAI_API_KEY environment variable
os.environ['OPENAI_API_KEY'] = 'sk-proj-lG2Fk8i7e6nt5N9fNTovT3BlbkFJ74J0EJw5Vooi5pKyMgFT'


# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['Spark_AI']
conversations = db['Questions_Answer']
planner_collection = db['planner']

# Function to fetch user responses from MongoDB
def fetch_responses(username):
    document = conversations.find_one({"username": username})
    if document:
        responses = [msg.get('response', '') for msg in document['messages'] if 'response' in msg]
        print("Fetched responses:", responses)  # Debugging output
        return responses
    return []


def store_task_output_in_mongodb(task_output):
    try:
        print("Received output:", task_output)  # Debug output

        # Convert to dictionary if it's not already
        if isinstance(task_output, dict):
            task_data = task_output
        else:
            task_output_str = str(task_output).replace("'", '"')  # Replace single quotes for valid JSON
            task_data = json.loads(task_output_str)

        # Create the new plan object with the task data
        new_plan = task_data

        # Update the main document by pushing to the "Plans" array
        # If the main document doesn't exist, it will be created
        result = planner_collection.update_one(
            {"_id": "1234"},  # Unique identifier for the main document
            {"$push": {"Plans": new_plan}},  # Add new plan to the "Plans" array
            upsert=True  # If the document doesn't exist, create it
        )

        # Check the update operation results
        if result.modified_count > 0:
            print("Successfully updated the 'Plans' array in MongoDB.")
        else:
            print("Inserted a new 'main_plans_document' with the first plan.")
    except Exception as e:
        print(f"An error occurred: {e}")




from datetime import datetime, timedelta

class PlanningTool(BaseTool):
    name: str = "Planner"
    description: str = "Tool to decompose objectives into a series of scheduled tasks based on specified time frames."

    def _run(self, objective: str, time_frame: int) -> list:
        # Assuming `time_frame` is in days for simplicity
        return self.plan_tasks(objective, time_frame)

    def plan_tasks(self, objective, time_frame):
        # Define specific tasks as per the example provided
        tasks = [
            {
                "Date": (datetime.today() + timedelta(days=8)).strftime("%d %B %Y"),
                "Time_of_execution": "10:00",
                "task": "Create content about the user's product & post it on required platform"
            },
            {
                "Date": (datetime.today() + timedelta(days=14)).strftime("%d %B %Y"),
                "Time_of_execution": "10:00",
                "task": "Follow 5 accounts which look interested in your product."
            }
        ]
        # Optionally add more tasks or manipulate the time_frame to schedule further tasks
        return tasks


# Initialize Crew AI agent and tools
planner_agent = Agent(
    role='Planner',
    goal='Generate a detailed plan for given objectives within a specified timeframe.',
    # tools=[PlanningTool()],
    backstory="Expert in breaking down complex objectives into manageable tasks.",
    verbose=True,
    memory=True
)

# Function to initiate planning process using fetched responses
def initiate_planning_process(username, time_frame):
    responses = fetch_responses(username)
    combined_objective = ". ".join(responses).strip(". ")
    return combined_objective, time_frame

user_objective, user_time_frame = initiate_planning_process("uzma", 90)

# Define the task using fetched objectives
# planning_task = Task(
#     description="Create a detailed plan based on fetched user responses.", 
#     expected_output="Tasks structured in JSON",
#     tools=[PlanningTool()],
#     agent=planner_agent,
#     # callback=store_task_output_in_mongodb
# )



import json
from datetime import datetime, timedelta



# Assuming Task and planner_agent are properly defined elsewhere
planning_task = Task(
    description=(
        "Systematically analyze responses to identify and extract essential details required for strategic planning. "
        "Focus on objectives. Construct a comprehensive and actionable plan formatted as a structured JSON document. "
        "This plan should outline the project timelines, specify resource allocation needs, and map out task dependencies. "
        "Ensure that the plan is detailed enough to facilitate immediate implementation and future tracking."
    ),
    expected_output="""A set of scheduled tasks in a json format. The output should not have any text whatsoever, it should only be a json object.
    For example, if today's date is 11 May, 2024, the expected output shall be a json of the kind:
    [{
                "Date": Tommorow date,
                "Time_of_execution": "10:00",
                "task": "Create content about the user's product & post it on required platform"
            },
            {
                "Date": Day after tomorrow's date,
                "Time_of_execution": "10:00",
                "task": "Follow 5 accounts which look interested in your product."
            }]
    """,
    # tools=[PlanningTool()],
    agent=planner_agent
)



# Print to see the output (optional)
print("Planning Task Expected Output:")
print(planning_task.expected_output)

# Configure and execute the Crew AI system
planning_crew = Crew(
    agents=[planner_agent],
    tasks=[planning_task],
    process=Process.sequential
)

plan_result = planning_crew.kickoff()
if plan_result:
    store_task_output_in_mongodb(plan_result)
# print("Planning result:", plan_result)
