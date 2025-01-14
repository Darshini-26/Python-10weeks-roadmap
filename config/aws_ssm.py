import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os

def pokemon_serveroverride(name, with_decryption=True, region_name=None):
    """
    Retrieves a parameter from AWS SSM Parameter Store.

    Args:
        name (str): The name of the parameter.
        with_decryption (bool): Whether to decrypt the parameter value (for SecureString).
        region_name (str): The AWS region name. If not provided, defaults to 'us-east-1'.

    Returns:
        str: The parameter value or None if not found.
    """
    print(f"Retrieving parameter: {name}")
    try:
        region_name = region_name or os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        ssm_client = boto3.client('ssm', region_name=region_name)

        # Fetch parameter from SSM
        response = ssm_client.get_parameter(
            Name=name,
            WithDecryption=with_decryption
        )

        # Retrieve the parameter value as a plain text string
        parameter_value = response['Parameter']['Value']

        # Return the raw parameter value (for plain text)
        return parameter_value
    except NoCredentialsError:
        raise RuntimeError("AWS credentials not found.")
    except PartialCredentialsError:
        raise RuntimeError("Incomplete AWS credentials.")
    except Exception as e:
        raise RuntimeError(f"Error retrieving SSM parameter: {e}")
