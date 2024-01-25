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
import sys
from crewai import Agent, Task
import os
from dotenv import load_dotenv
from crewai import Crew, Process
from langchain_openai import AzureChatOpenAI
from crewai.agent import Agent
from crewai.tools.agent_tools import AgentTools
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

from langchain.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()

# Define your agents with roles and goals
researcher = Agent(
  role='Senior Research Analyst',
  goal='Uncover cutting-edge developments in AI and data science',
  backstory="""You work at a leading tech think tank.
  Your expertise lies in identifying emerging trends.
  You have a knack for dissecting complex data and presenting
  actionable insights.""",
  verbose=True,
  allow_delegation=False,
  tools=[search_tool]
  # You can pass an optional llm attribute specifying what mode you wanna use.
  # It can be a local model through Ollama / LM Studio or a remote
  # model like OpenAI, Mistral, Antrophic of others (https://python.langchain.com/docs/integrations/llms/)
  #
  # Examples:
  # llm=ollama_llm # was defined above in the file
  # llm=ChatOpenAI(model_name="gpt-3.5", temperature=0.7)
)
writer = Agent(
  role='Tech Content Strategist',
  goal='Craft compelling content on tech advancements',
  backstory="""You are a renowned Content Strategist, known for
  your insightful and engaging articles.
  You transform complex concepts into compelling narratives.""",
  verbose=True,
  allow_delegation=True,
  # (optional) llm=ollama_llm
)

# Create tasks for your agents
task1 = Task(
  description="""Conduct a comprehensive analysis of the latest advancements in AI in 2024.
  Identify key trends, breakthrough technologies, and potential industry impacts.
  Your final answer MUST be a full analysis report""",
  agent=researcher
)

task2 = Task(
  description="""Using the insights provided, develop an engaging blog
  post that highlights the most significant AI advancements.
  Your post should be informative yet accessible, catering to a tech-savvy audience.
  Make it sound cool, avoid complex words so it doesn't sound like AI.
  Your final answer MUST be the full blog post of at least 4 paragraphs.""",
  agent=writer
)

# Instantiate your crew with a sequential process
crew = Crew(
  agents=[researcher, writer],
  tasks=[task1, task2],
  verbose=2, # You can set it to 1 or 2 to different logging levels
  llm=default_llm,
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)

