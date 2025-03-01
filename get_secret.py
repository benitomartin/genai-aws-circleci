import boto3
import json
import os
from fastapi import HTTPException
from botocore.exceptions import ClientError

def retrieve_secret(secret_name: str, region_name: str = "eu-central-1"):
    """
    Retrieve a secret from AWS Secrets Manager.

    :param secret_name: The name of the secret in Secrets Manager.
    :param region_name: The AWS region where the secret is stored (default is "eu-central-1").
    :return: The secret value if found, or raises an exception.
    """
    try:
        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager', region_name=region_name)

        # Get the secret value
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        # print(get_secret_value_response)
        # Check if the secret is a string or binary and process accordingly
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            # print(secret)

            secret_dict = json.loads(secret)
            # print(secret_dict.get("OPENAI_API_KEY"))
            # print("Hello")

            return secret_dict.get("OPENAI_API_KEY")
        else:
            raise HTTPException(status_code=500, detail="Secret is in binary format, which is not supported in this implementation.")

    except ClientError as e:
        # Handle specific AWS service errors
        print(f"Error retrieving secret from Secrets Manager: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve API key from Secrets Manager")
    except Exception as e:
        # Generic exception handling
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve API key from Secrets Manager")

# Example Usage:
if __name__ == "__main__":
    secret_name = "openai/api_key"  # Replace with the actual secret name in your Secrets Manager
    try:
        api_key = retrieve_secret(secret_name)
        print(f"Retrieved OpenAI API Key: {api_key}")
    except HTTPException as e:
        print(f"Error: {e.detail}")
