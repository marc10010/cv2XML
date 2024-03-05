import os
from dotenv import load_dotenv
import boto3
from langchain.llms.bedrock import Bedrock

textOnDocument = ""
region = os.getenv('AWS_DEFAULT_REGION', 'eu-west-3')
language = "spanish"
region_bedrock = "eu-central-1"
load_dotenv()

# Configuración de Bedrock
bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name=region_bedrock,
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID_BEDROCK'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY_BEDROCK')
)
modelID = "anthropic.claude-v2:1"
llm = Bedrock(
    model_id=modelID,
    client=bedrock_client,
    model_kwargs={"max_tokens_to_sample": 2200, "temperature": 1}
)
# Configuración de textract
textract_client = boto3.client(
    'textract',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_DEFAULT_REGION')
)
# Configuración de S3
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=region
)