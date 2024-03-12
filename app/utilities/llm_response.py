import requests
import json

def get_llm_response(prompt):
    """Stream the response of a POST request and concatenate the content."""
    DOCKER_SERVER_URL = "http://localhost:8080/completion"
    HEADERS = {
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream',
    }
    PAYLOAD = {
            "stream": True, 
            "n_predict": 500, 
            "temperature": 0.2, 
            "stop": ["</s>"],
            "prompt": prompt,
        }
    content_pieces = []

    response = requests.post(
        DOCKER_SERVER_URL, 
        data=json.dumps(PAYLOAD), 
        headers=HEADERS, 
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