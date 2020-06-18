# Importing the major libraries 
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import email 
import base64
from urlextract import URLExtract
import git
import os

# Major Functions -

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


def get_msg_id(service, user_id, search_string):
    
    """
    Searches for messages and returns the msg_if of 
    the first message found with the search string
    """
    
    try:
        search_id = service.users().messages().list(userId=user_id, q=search_string).execute()
        number_results = search_id['resultSizeEstimate']
        
        final_list = []
        if number_results>0:
            message_ids = search_id['messages']
            
            for ids in message_ids:
                final_list.append(ids['id'])
            return (final_list[0])
        
    except(errors.HttpError, error):
        print('An error occured %s') % error
                
def get_url_from_msg_id(service, user_id, msg_id):
    
    """
    Returns the message body given the message id
    """
    extractor = URLExtract()
    
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
        content = message['payload']['parts'][0]['body']['data']
        msg_body = base64.urlsafe_b64decode(content).decode('utf-8')
        clean_str = " ".join(msg_body.split())
        url = extractor.find_urls(clean_str)
        repo_url = url[1][(url[1].find('=')+1):]
        return(repo_url)
            
    except(errors.HttpError, error):
        print('An error occured', error)

        
def find_str(s, char):
    
    """ A function used to find the index of a particular substring in a string """
    
    index = 0

    if char in s:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index:index+len(char)] == char:
                    return index

            index += 1

    return -1

def clone_repo(dir_to_clone, repo_url):
    
    # Get the repository name
    repo_name = repo_url[(repo_url.rfind('/')+1):]
    
    if os.path.isdir(dir_to_clone+repo_name):
        print('The directory already exists')
    else:
        git.Git(dir_to_clone).clone(repo_url)
        print('Sucessfully Cloned to the repository ', repo_name)


# User Id
user_id = 'me'

# Search String is the search parameter
search_string = 'https://ununu-p2p.github.io/website/'

# Calling the get_service method to recieve service object
service = get_service()

# Only get the body of the message with the first ID
msg_id = get_msg_id(service=service, user_id=user_id, search_string=search_string)

# Get the git repository url 
repo_url=get_url_from_msg_id(service=service, user_id=user_id, msg_id=msg_id)