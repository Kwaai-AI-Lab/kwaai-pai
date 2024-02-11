import requests
import json

def stream_response_and_concatenate(url, payload):
    """Stream the response of a POST request and concatenate the content."""
    headers = {
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream',
    }

    content_pieces = []

    response = requests.post(
        url, 
        data=json.dumps(payload), 
        headers=headers, 
        stream=True
    )

    if response.status_code == 200:
        try:
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith('data:'):
                        data_json = json.loads(decoded_line[5:])
                        content_pieces.append(data_json['content'])
        except KeyboardInterrupt:
            print("Stream stopped by user.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print(f"Failed to get a proper response, status code: {response.status_code}")

    complete_content = "".join(content_pieces)
    return complete_content

url = "http://localhost:8080/completion"
payload = {
    "stream": True,
    "n_predict": 500,
    "temperature": 0.2,
    "stop": ["</s>"],
    "prompt": "Write an email draft to scheule a meeting with John"
}

complete_content = stream_response_and_concatenate(url, payload)

print(complete_content)