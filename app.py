from flask import Flask, render_template, request
import base64
import requests
from markdown import markdown

app = Flask(__name__)

# OpenAI API Key
api_key = ""

# Function to encode the image from URL
def encode_image_from_url(image_url):
    response = requests.get(image_url)
    return base64.b64encode(response.content).decode('utf-8')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image_url = request.form['image_url']
        prompt = request.form['prompt']  # New line to get user's prompt
        base64_image = encode_image_from_url(image_url)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "gpt-4-vision-preview",
            "max_tokens": 4096,  # Increase max_tokens to accommodate longer responses
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt  # Use the user's prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        result = response.json()

        return render_template('index.html', image_url=image_url, result=result, user_prompt=prompt)

    return render_template('index.html')

# Add the markdown filter to Jinja environment
app.jinja_env.filters['markdown'] = markdown

if __name__ == '__main__':
    app.run(debug=True)