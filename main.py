from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import openai
from dotenv import load_dotenv
import os
import mangum  
import boto3   
import json

# Load environment variables
load_dotenv()


# Initialize FastAPI
app = FastAPI()

# Pydantic model to define expected structure of request
class PromptRequest(BaseModel):
    prompt: str

# Function to get OpenAI API key
def get_openai_api_key():
    # Check if running locally or in Lambda
    if os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
        # Running in Lambda, get key from AWS Secrets Manager
        secret_name = f"openai/api_key"
        
        try:
            # Create a Secrets Manager client
            session = boto3.session.Session()
            client = session.client(service_name='secretsmanager', region_name="eu-central-1")
            
            # Get the secret
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
            secret = get_secret_value_response['SecretString']
            secret_dict = json.loads(secret)
            
            return secret_dict.get("OPENAI_API_KEY")
        except Exception as e:
            print(f"Error retrieving secret: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to retrieve API key from Secrets Manager")
    else:
        # Running locally, get key from .env file
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="OPENAI_API_KEY not found in environment variables")
        return api_key

# Fetch the OpenAI API key and pass it to OpenAI client
api_key = get_openai_api_key()
openai.api_key = api_key  
client = OpenAI(api_key=api_key)  


@app.get("/")
async def root():
    return {"message": "Welcome to the GenAI API"}

@app.post("/generate")
async def generate_text(request: PromptRequest):

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[{"role": "user", "content": request.prompt}],
            max_tokens=200
        )
        return {"response": response.choices[0].message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create the handler for AWS Lambda
handler = mangum.Mangum(app)

# Run the app with uvicorn
if __name__ == "__main__":
    import uvicorn
    
    print("Starting the server...")
    
    uvicorn.run("__main__:app", host="127.0.0.1", port=8000, reload=True)

    ## This wouuld work as well but you need to run uvicorn app.main:app --reload in the
    ## terminal to start the server instead of uv run main.py

    # uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)


