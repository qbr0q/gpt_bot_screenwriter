import requests
import time
from config import FOLDER_ID

def create_new_token():
    """Создание нового токена"""
    metadata_url = "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token"
    headers = {"Metadata-Flavor": "Google"}
    response = requests.get(metadata_url, headers=headers)
    return response.json()

a = create_new_token()
print(a, type(a))


def ask_gpt(question):
    iam_token = '< твой IAM-токен >'

    headers = {
        'Authorization': f'Bearer {iam_token}',
        'Content-Type': 'application/json'
    }
    data = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "200"
        },
        "messages": [
            {
                "role": "user",
                "text": question
            }
        ]
    }
    response = requests.post("https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
                             headers=headers,
                             json=data)
    if response.status_code == 200:
        answer = response.json()["result"]["alternatives"][0]["message"]["text"]
        return answer
    else:
        raise RuntimeError(
            f'Invalid response received: code: {response.status_code},'
            f' message: {response.text}'
        )