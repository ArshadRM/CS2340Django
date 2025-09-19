import requests
import re

# Login
login_url = 'http://127.0.0.1:8000/accounts/login/'
session = requests.Session()
session.get(login_url)
csrftoken = session.cookies['csrftoken']
login_data = {
    'username': 'admin',
    'password': 'admin',
    'csrfmiddlewaretoken': csrftoken
}
session.post(login_url, data=login_data)

# Create petition
create_petition_url = 'http://127.0.0.1:8000/petitions/create/'
session.get(create_petition_url)
csrftoken = session.cookies['csrftoken']
petition_data = {
    'movie_title': 'The Matrix',
    'description': 'Please add this movie to the store.',
    'csrfmiddlewaretoken': csrftoken
}
response = session.post(create_petition_url, data=petition_data)

# Check if the petition was created
petitions_url = 'http://127.0.0.1:8000/petitions/'
response = session.get(petitions_url)
if 'The Matrix' in response.text:
    print('Petition created successfully')
else:
    print('Failed to create petition')

# Vote on the petition
# First, get the petition id
petitions_url = 'http://127.0.0.1:8000/petitions/'
response = session.get(petitions_url)
# a simple way to get the petition id from the html
petition_id_match = re.search(r'href="/petitions/(\d+)/"', response.text)
if petition_id_match:
    petition_id = petition_id_match.group(1)

    vote_url = f'http://127.0.0.1:8000/petitions/{petition_id}/vote/'

    # Vote
    session.get(vote_url)
    csrftoken = session.cookies['csrftoken']
    vote_data = { 'csrfmiddlewaretoken': csrftoken }
    response = session.post(vote_url, data=vote_data)

    # Check if the vote was successful
    show_petition_url = f'http://127.0.0.1:8000/petitions/{petition_id}/'
    response = session.get(show_petition_url)
    if 'Unvote' in response.text:
        print('Voted successfully')
    else:
        print('Failed to vote')

    # Unvote
    session.get(vote_url)
    csrftoken = session.cookies['csrftoken']
    vote_data = { 'csrfmiddlewaretoken': csrftoken }
    response = session.post(vote_url, data=vote_data)
    response = session.get(show_petition_url)
    if 'Vote' in response.text:
        print('Unvoted successfully')
    else:
        print('Failed to unvote')
else:
    print("Could not find petition id")
