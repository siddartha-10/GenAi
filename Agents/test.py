from langchain.agents import load_tools
from langchain.chat_models import ChatOpenAI
import os
from crewai import Agent, Task, Crew, Process

os.environ["OPENAI_API_KEY"] = ""

llm = ChatOpenAI(temperature=0.0,model="gpt-3.5-turbo")
tools = load_tools(
    ["human"]
)


agent = Agent(
  role='Human',
  goal='Provide context when the Agents need me',
  backstory="I am a human, I am here to help the Agents",
  tools=tools
)

task1 = Task(
  description="""Give me a hook to write a story? and ask the human to give you a hook to write a story""",
  agent=agent
)

task2 = Task(
  description="""what is the name of the characters? you should ask the human to give you the name of the char""",
  agent=agent
)

task3 = Task(
    description="""Include the character names and involve them in your story.""",
    agent=agent,
)

crew = Crew(
  agents=[agent],
  tasks=[task1,task2,task3],
  verbose=3, # Crew verbose more will let you know what tasks are being worked on, you can set it to 1 or 2 to different logging levels
  process=Process.sequential # Sequential process will have tasks executed one after the other and the outcome of the previous one is passed as extra content into this next.
)

print(crew.kickoff())