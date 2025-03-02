import sys
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
import mangum  
import boto3   
import json
from loguru import logger

# Load environment variables
load_dotenv()

# Configure Loguru
logger.remove()
logger.add(
    sys.stdout,
    level="DEBUG",
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{module}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
)

# Initialize FastAPI
app = FastAPI()

# Pydantic model to define expected structure of request
class PromptRequest(BaseModel):
    """Model for request validation."""
    prompt: str


def get_openai_api_key():
    """
    Retrieve OpenAI API Key from AWS Secrets Manager or environment variables.

    Returns:
        str: OpenAI API key.
    
    Raises:
        HTTPException: If retrieval from Secrets Manager fails or key is missing.
    """
    # Check if running locally or in Lambda
    if os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
        # Running in Lambda, get key from AWS Secrets Manager
        secret_name = "openai/api_key"
        
        try:
            # Create a Secrets Manager client
            session = boto3.session.Session()
            client = session.client(service_name='secretsmanager', region_name="eu-central-1")
            
            # Get the secret API Key
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
            secret = get_secret_value_response['SecretString']
            secret_dict = json.loads(secret)
            
            api_key = secret_dict.get("OPENAI_API_KEY")
            if not api_key:
                raise KeyError("OPENAI_API_KEY not found in Secrets Manager.")
            
            logger.info("Successfully retrieved OpenAI API key from AWS Secrets Manager.")
            return api_key
        except Exception as e:
            logger.error(f"Error retrieving OpenAI API key: {e}")
            raise HTTPException(status_code=500, detail="Failed to retrieve API key from Secrets Manager")
    else:
        # Running locally, get key from .env file
        api_key = os.environ.get("OPENAI_API_KEY")

        if not api_key:
            logger.error("OPENAI_API_KEY not found in environment variables.")
            raise HTTPException(status_code=500, detail="OPENAI_API_KEY not found in environment variables")

        logger.info("Successfully retrieved OpenAI API key from .env file.")
        return api_key

def get_openai_client():
    """
    Creates and returns an OpenAI client instance.
    
    Returns:
        OpenAI: An initialized OpenAI client.
        
    Raises:
        HTTPException: If client initialization fails.
    """
    try:
        api_key = get_openai_api_key()
        return OpenAI(api_key=api_key)
    except HTTPException as e:
        logger.error(f"Failed to initialize OpenAI client: {e.detail}")
        raise  HTTPException(status_code=500, detail="Failed to initialize OpenAI client: " + str(e.detail))


@app.get("/")
async def root():
    """Root endpoint to confirm API is running."""
    logger.info("Root endpoint accessed.")
    return {"message": "Welcome to the GenAI API"}

@app.post("/generate")
async def generate_text(request: PromptRequest, client: OpenAI = Depends(get_openai_client)):
    """
    Generate AI response using OpenAI API.

    Args:
        request (PromptRequest): User prompt input.

    Returns:
        dict: AI-generated response.

    Raises:
        HTTPException: If OpenAI API request fails.
    """
    if not client:
        logger.error("OpenAI API client not initialized.")
        raise HTTPException(status_code=500, detail="OpenAI API client not initialized.")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[{"role": "user", "content": request.prompt}],
            max_tokens=200
        )

        if not response.choices:
            raise ValueError("No response received from OpenAI API.")
        
        logger.info("Generated response for prompt")
        return {"response": response.choices[0].message.content}


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create the handler for AWS Lambda
handler = mangum.Mangum(app)

# Run the app with uvicorn
if __name__ == "__main__":
    logger.info("Starting FastAPI server...")
    
    import uvicorn
      
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


