import boto3
from botocore.exceptions import NoCredentialsError



def upload_to_s3(file_name: str, bucket_name: str, object_name: str = None) -> str:
    """
    Upload a file to an S3 bucket.

    Args:
        file_name (str): The path to the file to upload.
        bucket_name (str): The name of the S3 bucket.
        object_name (str, optional): The S3 object name. Defaults to the file name.

    Returns:
        str: The S3 URL of the uploaded file.

    Raises:
        Exception: If the upload fails.
    """
    s3_client = boto3.client('s3')

    if object_name is None:
        object_name = file_name

    try:
        s3_client.upload_file(file_name, bucket_name, object_name)
        return f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
    except FileNotFoundError:
        raise Exception("The file was not found")
    except NoCredentialsError:
        raise Exception("AWS credentials not available")
