from app.config.aws_ssm import pokemon_serveroverride  # Import the function from aws_ssm.py

def get_database_url():
    """
    Retrieves the database URL from AWS SSM Parameter Store.

    Returns:
        str: The database URL retrieved from the SSM parameter store.
    """
    try:
        # Fetch the parameter value (which contains plain text)
        parameter_value = pokemon_serveroverride('/pokemon/serveroverride')

        # Parse the parameter value to find the DATABASE_URL
        for line in parameter_value.splitlines():
            if line.startswith('DATABASE_URL='):
                # Extract the value after "DATABASE_URL="
                database_url = line.split('=', 1)[1].strip()
                return database_url
        
        # Raise an error if DATABASE_URL isn't found
        raise RuntimeError("DATABASE_URL not found in the parameter value.")
    except Exception as e:
        raise RuntimeError(f"Error retrieving database URL: {e}")
