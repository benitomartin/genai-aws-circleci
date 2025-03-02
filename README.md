# FastAPI GenAI Serverless API

A serverless API for generating AI responses using FastAPI, AWS Lambda, and CircleCI.

## Prerequisites

- Python 3.11.11
- AWS Account
- AWS CLI configured
- CircleCI Account
- OpenAI API Key

## Local Development

1. Create a virtual environment:
```bash
uv sync
source .venv/bin/activate
```

2. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

3. Run the development server:
```bash
uvicorn app.main:app --reload
```

## Testing

Run tests using pytest:
```bash
pytest
```

## Deployment

The application is automatically deployed to AWS Lambda when changes are pushed to the main branch.

### Required AWS Resources

1. AWS Lambda function
2. API Gateway
3. IAM role with appropriate permissions

### CircleCI Environment Variables

Set the following in CircleCI project settings:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`
- `AWS_LAMBDA_FUNCTION_NAME`
- `OPENAI_API_KEY`


First test the app.py with the get request


Then add the OpenAI and generate option. Test it with this


curl -X 'POST' 'http://127.0.0.1:8000/generate' \
-H 'Content-Type: application/json' \
-d '{"prompt": "Tell me a fun fact about AI"}'

curl -X POST https://dmfs4n6y6i.execute-api.eu-central-1.amazonaws.com/dev/generate \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Tell me a joke!"}'

Add Magnum to handle lambda


# Secrets


aws secretsmanager create-secret \
    --name openai/api_key \
    --description "OpenAI API Key for GenAI API (Staging)" \
    --secret-string '{"OPENAI_API_KEY":"YOUR_ACTUAL_API_KEY"}'


uv pip freeze > requirements.txt
