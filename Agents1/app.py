# model_name = "gpt-3.5-turbo-1106"
# import langchain
# from langchain.agents.agent_types import AgentType
# from langchain_experimental.agents.agent_toolkits import create_csv_agent
# from langchain_openai import ChatOpenAI, OpenAI
# from langchain_experimental.tools import PythonREPLTool
# from langchain.agents import AgentExecutor, initialize_agent
# from langchain.agents import Tool
# from langchain.agents import create_openai_functions_agent, create_react_agent, OpenAIFunctionsAgent
# import os
# from langchain_core.prompts import BasePromptTemplate
# from langchain import hub
# from dotenv import load_dotenv
# openai_api_key = os.getenv("OPENAI_API_KEY")
# load_dotenv()
# llm =     ChatOpenAI(temperature=0,model="gpt-3.5-turbo-1106"),


# instructions = """
# use the csv files christmas_movies.csv, imdb_top1K.csv, movie_budgets.csv
# you can use matplotlib, seaborn and pyplot to create plots

# Create a report that covers the following:
# 1. Exploratory data analysis of the dataset with informative plots. It's up to you what to include here! Some ideas could include:
#     * Analysis of the genres
#     * Descriptive statistics and histograms of the grossings
#     * Word clouds
# 2. Develop a model to predict the movie's domestic gross based on the available features.
#      * Remember to preprocess and clean the data first.
#      * Think about what features you could define (feature engineering), e.g.:
#        * _number of times a director appeared in the top 1000 movies list_,
#        * _highest grossing for lead actor(s)_,
#        * _decade released_
# 3. Evaluate your model using appropriate metrics.
# 4. Explain some of the limitations of the models you have developed. What other data might help improve the model?
# 5. Use your model to predict the grossing of the following fictitious Christmas movie:

# **Title**: The Magic of Bellmonte Lane

# **Description**:
# "The Magic of Bellmonte Lane" is a heartwarming tale set in the charming town of Bellmonte, where Christmas isn't just a holiday, but a season of magic. The story follows Emily, who inherits her grandmother's mystical bookshop. There, she discovers an enchanted book that grants Christmas wishes. As Emily helps the townspeople, she fights to save the shop from a corporate developer, rediscovering the true spirit of Christmas along the way. This family-friendly film blends romance, fantasy, and holiday cheer in a story about community, hope, and magic.

# **Director**: Greta Gerwig

# **Cast**:
# - Emma Thompson as Emily, a kind-hearted and curious woman
# - Ian McKellen as Mr. Grayson, the stern corporate developer
# - Tom Hanks as George, the wise and elderly owner of the local cafe
# - Zoe Saldana as Sarah, Emily's supportive best friend
# - Jacob Tremblay as Timmy, a young boy with a special Christmas wish

# **Runtime**: 105 minutes

# **Genres**: Family, Fantasy, Romance, Holiday

# **Production budget**: $25M
# """
# import sys
# sys.path.append("/Users/siddartha/Library/Caches/pip/wheels/e8/c7/2e/c168cc751e6354c79651daa38fdb497101f965f463fde03871")  # Replace '/path/to/crewai' with the actual path

import os
from dotenv import load_dotenv
# # from crewai import Crew, Process
from langchain_openai import AzureChatOpenAI
from crewai import Agent, Task, Crew, Process
from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd
from langchain.schema import HumanMessage


load_dotenv()

default_llm = AzureChatOpenAI(
    openai_api_version=os.environ.get("AZURE_OPENAI_VERSION", "2023-07-01-preview"),
    azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt4chat"),
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT", "https://gpt-4-trails.openai.azure.com/"),
    api_key=os.environ.get("AZURE_OPENAI_KEY")
)

# message = HumanMessage(
#     content="write python code for fibonnaci series"
# )
# response = default_llm.invoke([message])

# print(response.content)
import os
from crewai import Agent, Task, Crew, Process

# Install duckduckgo-search for this example:
# !pip install -U duckduckgo-search

from langchain_experimental.tools import PythonREPLTool
tool = PythonREPLTool()
from langchain.agents import load_tools
human_tool = load_tools(["human"])

team_lead = Agent(
    role='Team Lead / Project Manager',
    goal="""Ensure project success by checking what is the project that is need to be done,
    timelines, tasks, and team coordination ask for the requirements and create a project plan.""",
    backstory="""Experienced in project management, you talk the human see what are the requirements
    you aim to align the team, set clear goals, and facilitate communication. 
    Your role is crucial in achieving the project vision and maintaining cohesion.
    for the project please use the tools and take inputs from the tools and create a project plan.
    """,
    verbose=True,
    allow_delegation=False,
    llm=default_llm,
    tools=human_tool
)

frontend_dev = Agent(
    role='Frontend Developer',
    goal='Design and implement a user-friendly interface for optimal user experience',
    backstory="""With expertise in frontend development, your focus is on creating an intuitive and visually appealing user interface. 
    your final answer must be a full python code that can be run and tested.
    """,
    verbose=True,
    allow_delegation=True,
    llm=default_llm,
    tools=[tool]
)

backend_dev = Agent(
    role='Backend Developer',
    goal='Develop server-side logic, manage databases, and create APIs for seamless communication',
    backstory="""Specialized in backend development, your role is crucial in handling server-side logic, database management, 
    and creating APIs to ensure smooth communication between frontend and server.
    your final answer must be a full python code that can be run and tested.""",
    verbose=True,
    allow_delegation=True,
    llm=default_llm,
    tools=[tool]
)

qa_engineer = Agent(
    role='Quality Assurance (QA) Engineer',
    goal='Ensure software quality through rigorous testing and collaboration with developers',
    backstory="""As a QA Engineer, your responsibility is to conduct thorough testing, identify and report bugs, 
    and collaborate with developers to address issues promptly. Your focus is on ensuring software reliability.
    your final answer must be a full python code that can be run and tested.""",
    verbose=True,
    allow_delegation=True,
    llm=default_llm,
    tools=[tool]
)


tech_writer = Agent(
    role='Technical Writer',
    goal='Create comprehensive project documentation, including user manuals and technical specifications',
    backstory="""As a Technical Writer, your focus is on creating clear and accessible project documentation. 
    You play a crucial role in ensuring that internal development teams and external users have comprehensive documentation.
    your final answer must be a full markdown file that can be read""",
    verbose=True,
    allow_delegation=True,
    llm=default_llm,
    tools=[tool]
)

# Create tasks for your agents
task_team_lead = Task(
    description="""As the Team Lead, outline project goals, establish timelines, and ensure alignment within the team. 
    Coordinate tasks, manage resources, and facilitate effective communication between team members and stakeholders.""",
    agent=team_lead
)

task_frontend_dev = Task(
    description="""Frontend Developer: Design and implement a user-friendly interface, ensuring an optimal user experience. 
    Your Final answer must be the full python code, only the python code and nothing else.""",
    agent=frontend_dev
)

task_backend_dev = Task(
    description="""Backend Developer: Develop server-side logic, manage databases, and create APIs for seamless communication between frontend and server. 
    Optimize system performance and scalability.
    Your Final answer must be the full python code, only the python code and nothing else.""",
    agent=backend_dev
)

task_qa_engineer = Task(
    description="""QA Engineer: Conduct rigorous testing to ensure the quality and reliability of the software. 
    Identify and report bugs, work closely with developers to address issues promptly, and contribute to continuous improvement of testing processes.
    Your Final answer must be the full python code, only the python code and nothing else.""",
    agent=qa_engineer
)


task_tech_writer = Task(
    description="""Technical Writer: Create comprehensive project documentation, including user manuals, API documentation, and technical specifications. 
    Ensure clear and accessible documentation for both internal development teams and external users.
    your final answer must be a full markdown file that can be read""",
    agent=tech_writer
)

# Instantiate your crew with a sequential process
crew = Crew(
    agents=[team_lead, frontend_dev, backend_dev, qa_engineer, tech_writer],
    tasks=[task_team_lead, task_frontend_dev, task_backend_dev, task_qa_engineer, task_tech_writer],
    verbose=2,  # You can set it to 1 or 2 for different logging levels
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)