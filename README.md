# API Information Retrieval Website

A simple Flask-based website that retrieves information using an external API.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.venv\\Scripts\\activate
```
- Unix/MacOS:
```bash
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure .env:
- The project uses the following env variables: CHAT_GPT_API_KEY, HF_API_KEY. Those will be provided in the message accompanying the task submission

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Features

- The website provides weather information the way a granma could do it. A photo of a granma originating from the searched city is provided
- The website provides the weather stats for the current time: temperature, humidity, wind speed
- The website provides a generated image of the requested city at the local time of that city
- Below the picture there is also a 7-Day forecast
- The form accepts a single word (a city name) or a phrase like "What is the weather like in \<city\>?"
- If a non existent city is provided the website will say "I could not find the city"
- If multiple cities are provided the weather info will be given for the first on in the list
- The image is embedded as data/image base64
- You are more than welcome to try and hack the prompt
- Modern, responsive UI
- Real-time API data retrieval
- AI handling of requests
- Error handling
- Loading states
- Clean and intuitive interface

## Technicals

- The website is built using: 

    -- Javascript as a frontend with minified Bootstrap for CSS

    -- Python as a backend on Flask

    -- AI models ChatGPT-4o-mini for text and black-forest-labs/FLUX.1-schnell for image

    -- huggingface as an inference client
- The project can potentially be agentified with smolagents or llama_index