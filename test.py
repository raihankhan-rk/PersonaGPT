import boto3
from langchain_community.llms import Bedrock
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
llm = Bedrock(model_id="anthropic.claude-v2", client=bedrock)
print(llm("Hello, world!"))