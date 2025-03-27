from dotenv import load_dotenv
import os
import json
from openai import OpenAI
from huggingface_hub import InferenceClient
import base64
from io import BytesIO
    
# Load environment variables
load_dotenv()

CHAT_GPT_MODEL = os.getenv('CHAT_GPT_MODEL') or 'gpt-4o-mini'
if not CHAT_GPT_MODEL:
    raise ValueError("CHAT_GPT_MODEL not found in .env file. Please add your model to the .env file.") 

CHAT_GPT_API_KEY = os.getenv('CHAT_GPT_API_KEY')
if not CHAT_GPT_API_KEY:
    raise ValueError("CHAT_GPT_API_KEY not found in .env file. Please add your API key to the .env file.") 

HF_API_KEY = os.getenv('HF_API_KEY')
if not HF_API_KEY:
    raise ValueError("HF_API_KEY not found in .env file. Please add your API key to the .env file.") 

FLUX_MODEL = os.getenv('FLUX_MODEL') or 'black-forest-labs/FLUX.1-schnell'
if not FLUX_MODEL:
    raise ValueError("FLUX_MODEL not found in .env file. Please add your model to the .env file.") 

client = OpenAI(api_key=CHAT_GPT_API_KEY)

# Extracts the city name from the request and converts it to the coordinates
def get_coordinates_from_request(query):
    """Use ChatGPT to get coordinates for a city name"""

    prompt = f"Please provide the latitude, longitude coordinates, city name and local time in the city location for the city of {query}. Return the result in JSON format like in example: {{\"latitude\": \"23.41\", \"longitude\": \"45.34\", \"city_name\": \"London\", \"local_time\":\"2023-10-01T12:00:00+03:00\"}} without any additional text. If the city does not exist reply {{\"error\": \"I could not find the city\"}} without any explanation or additional information. If more than one cities are listed return the result only for the first one. Remember, return the result in JSON format like in example: {{\"latitude\": \"23.41\", \"longitude\": \"45.34\", \"city_name\": \"London\", \"local_time\":\"2023-10-01T12:00:00+03:00\"}} without any additional text"
    messages = [
        {"role": "system", "content": "You are a helpful assistant that provides city coordinates in the format 'latitude,longitude' without any additional text."},
        {
            "role": "user", 
            "content": prompt
        }]
    try:
        completion = client.chat.completions.create(
            model=CHAT_GPT_MODEL,
            messages=messages
        )
        reply = completion.choices[0].message.content
        city_data = json.loads(reply)
        return city_data
    except Exception as e:
        raise Exception(f"Error getting coordinates: {str(e)}")

# AI recommendations for the weather
def get_recommendations(current_weather, city_name):
    """Use ChatGPT to get recommendations for the weather conditions"""

    prompt = f"Please look at the weather stats {current_weather} for the city of {city_name} and give recommendations on the clothes without bullet points in the form of text. Make sure the city exists, double check. Do not hallucinate non existing cities. If the city does not exist reply 'None' without any explanation or additional information"
    messages = [
        {"role": "system", "content": "You are a helpful assistant that analyzes current weather for the city and gives recommendations on the clothes for the weather without bullet points in the form of text in one paragraph. The temperature, distance and speed units must be given both in metric and imperial units. You must sound like a mom and use current slang, emojis and be extremely friendly and loving"},
        {
            "role": "user", 
            "content": prompt
        }]
    try:
        completion = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=messages
        )
        return completion.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error getting coordinates: {str(e)}")

# City image at current time
flux_client = InferenceClient(model=FLUX_MODEL, api_key=HF_API_KEY)
def get_image(prompt):
    image_data = flux_client.text_to_image(f"{prompt}. Don't hesitate to add details in the prompt to make the image look better, like 'high-res, photorealistic', etc.")
    data = BytesIO()
    image_data.save(data, "JPEG")
    data64 = base64.b64encode(data.getvalue()).decode('utf-8')
    return f"data:image/jpeg;base64,{data64}"

def get_granma_image(city):
    # client = InferenceClient(model=FLUX_MODEL, api_key=HF_API_KEY)
    image_data = flux_client.text_to_image(f"Create an image of a kind elderly granma-like lady from ${city}, 100px")
    data = BytesIO()
    image_data.save(data, "JPEG")
    data64 = base64.b64encode(data.getvalue()).decode('utf-8')
    # print(data64)
    return f"data:image/jpeg;base64,{data64}"
