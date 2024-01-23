import os
from crewai import Agent, Task, Crew, Process

import boto3
from langchain_community.llms import Bedrock

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

from langchain_community.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()

# Define your agents with roles and goals
mentor = Agent(
  role='Experienced Product Engineer',
  goal='Mentor a junior engineer',
  backstory="""You mentor students and professionals in hackathon.
  Your expertise lies in identifying the bug in the code and debugging it.
  You have a knack for helping out engineers with common tech related queries.
  actionable insights.""",
  verbose=True,
  allow_delegation=False,
  tools=[search_tool],
  llm=Bedrock(model_id="anthropic.claude-v2", client=bedrock)
  # You can pass an optional llm attribute specifying what mode you wanna use.
  # It can be a local model through Ollama / LM Studio or a remote
  # model like OpenAI, Mistral, Antrophic of others (https://python.langchain.com/docs/integrations/llms/)
  #
  # Examples:
  # llm=ollama_llm # was defined above in the file
  # llm=ChatOpenAI(model_name="gpt-3.5", temperature=0.7)
)

# writer = Agent(
#   role='Tech Content Strategist',
#   goal='Craft compelling content on tech advancements',
#   backstory="""You are a renowned Content Strategist, known for
#   your insightful and engaging articles.
#   You transform complex concepts into compelling narratives.""",
#   verbose=True,
#   allow_delegation=True,
#   # (optional) llm=ollama_llm
# )

# Create tasks for your agents
task1 = Task(
  description=f"""Following is a query of an engineer who's building a product at a hackathon.
  Help him out by providing actionable insights and code wherever necessary.
  If the query is out of your scope, say that you're not tuned to answer it.
  If the query is about a piece of code, use search tool to find the relevant code snippet.
  NOTE: Your final answer MUST be a concise yet factually correct.
  QUESTION:
  {input("Enter your query: ")}
  """,
  agent=mentor
)

# Instantiate your crew with a sequential process
crew = Crew(
  agents=[mentor],
  tasks=[task1],
  verbose=2, # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)