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

## API Endpoints

- `GET /health`: Health check endpoint
- `POST /generate`: Generate AI response
  - Request body: `{"prompt": "Your prompt here"}`
  - Response: `{"generated_text": "AI generated response"}`

## License

MIT