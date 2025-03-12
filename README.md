# Building a serverless GenAI API with FastAPI, AWS, and CircleCI

![Image](https://github.com/user-attachments/assets/ebda21bc-fa26-49e3-bfc1-039e9ca2dd18)

This project provides a serverless API for generating AI responses using OpenAI's API. It leverages FastAPI for the web framework, AWS Lambda an API Gateway for serverless deployment, and CircleCI for continuous integration and deployment.

The project has been developed as part of the following  [blog](https://circleci.com/blog/building-a-serverless-genai-api/)

## Project Structure

- `main.py`: Main application code for FastAPI.
- `build-sam.sh`: Script to build the Lambda deployment package.
- `template.yaml`: AWS SAM template for deploying the application.
- `test/`: Directory containing test cases.
- `.circleci/config.yml`: CircleCI configuration for CI/CD.
- `Makefile`: Makefile for running common tasks.
- `pyproject.toml`: Project dependencies and configuration.

## Setup

**Clone the repository:**

```sh
git clone https://github.com/yourusername/genai-aws-circleci.git
cd genai-aws-circleci
```

**Install dependencies:**

```sh
uv sync
```

**Set up environment variables:**

Create a `.env` file in the root directory and add your OpenAI API key:

```sh
OPENAI_API_KEY=your_openai_api_key
```

## Running Locally

To run the application locally, use the following command:

```sh
uv run main.py
```

The API will be available at http://127.0.0.1:8000.

## Testing

To run the tests, use the following command:

```sh
uv run pytest
```

## Deployment

### Using AWS SAM

**Build the Lambda deployment package:**

```sh
chmod +x build-sam.sh
./build-sam.sh
```

**Deploy using AWS SAM:**

```sh
sam build
sam deploy --stack-name sam-app --resolve-s3 --capabilities CAPABILITY_IAM --region eu-central-1
```

**Testing Endpoint**

```sh
curl -X POST https://znhxj2t415.execute-api.eu-central-1.amazonaws.com/dev/generate \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Tell me a joke!"}'
```

### Using CircleCI

The project is configured to use CircleCI for continuous integration and deployment. The `.circleci/config.yml` file contains the necessary steps to build, test, and deploy the application on the CircleCI platform.
