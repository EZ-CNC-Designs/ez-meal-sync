import gpsoauth

def mastertoken_generator(email_address: str, oauth_token_id: str)-> str:
    """Generates a master token to be used in for Google Keep's API.
    Takes the users email address and an oauth token and returns a master token."""
    
    email = email_address
    android_id = '0123456789abcdef' # Generic id as it is irrelevant
    oauth_token = oauth_token_id

    # Exchange the OAuth token for a master token
    master_response = gpsoauth.exchange_token(email, oauth_token, android_id)

    # Print the master response
    # print(f"Master response: {master_response}")

    if 'Token' in master_response:
        master_token = master_response['Token']
        print(f"Master Token: {master_token}")
        return master_token
    else:
        print("Error: No master token found")
        return None
