import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import os

def feedback_discord_webhook(content):
    url = os.environ['DISCORD_SMOKER_URL']

    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "content": content,
        "username": "Fictitious Data Smoker Smuggler",
        "allowed_mentions": {
            "parse": ["everyone"]
        }
    })

    try:
        response = requests.post(url, data=payload,  headers=headers)
        print(response.text)

        if response.status_code != 200:
            print(response.text)
            return False

    except Exception as e:
        print(e)
        print("Error sending feedback to Discord")



def make_request(url):

    try:
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(e)
        return None


def get_workers_number():
    return ThreadPoolExecutor()._max_workers


if __name__ == '__main__':

    ok = 0
    error = 0
    workers = get_workers_number()
    doc_type = ['person', 'company']
    
    doc_type = doc_type[random.choice(range(len(doc_type)))]

    url = f'https://data4tests.herokuapp.com/api/{doc_type}'
    urls = []

    for i in range(workers * 5 if doc_type == 'person' else workers * 2):
        urls.append(url)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_url = {executor.submit(make_request, url): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            data = future.result()
            if data is not None:
                ok += 1
            else:
                error += 1
        
    print(f'OK: {ok}')
    print(f'ERROR: {error}')
    print(f'Total: {ok + error}')

    messages = [
        f'Went to buy some cigarretes.\nIn the middle way i found {ok} {doc_type if ok > 1 else doc_type+"s"} data.',
        f'Went out again to buy cigars.\nAnd I found an opportunity to stole {ok} {doc_type if ok > 1 else doc_type+"s"} data.\nI alreay stored it in you db.'
    ]

    messages_error = [ f'Had to smoke {error} cigars on this little trip.',
    f"Now I want to see who is gonna pay back for {error} cigars i had to smoke on this trip."]

    feedback_discord_webhook(random.choice(messages))
    if error > 0:
        feedback_discord_webhook(random.choice(messages))