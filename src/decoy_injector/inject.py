import boto3
import json
import argparse
from utils import generate_fake_decoys

lambda_client = boto3.client('lambda')

def inject_decoys(function_name):
    # Fetch current configuration
    response = lambda_client.get_function_configuration(FunctionName=function_name)
    current_env = response.get('Environment', {}).get('Variables', {})

    # Generate new fake decoy values
    decoys = generate_fake_decoys()
    updated_env = {**current_env, **decoys}

    # Inject into Lambda environment
    lambda_client.update_function_configuration(
        FunctionName=function_name,
        Environment={'Variables': updated_env}
    )

    print(f"[+] Injected decoys into {function_name}:")
    print(json.dumps(decoys, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inject decoy secrets into AWS Lambda functions.")
    parser.add_argument('--function', required=True, help="Name of the target Lambda function")

    args = parser.parse_args()
    inject_decoys(args.function)
