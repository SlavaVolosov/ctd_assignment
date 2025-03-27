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

4. Configure the API:
- Open `app.py` and replace the `API_URL` with your desired API endpoint
- If the API requires authentication, create a `.env` file and add your API key:
```
API_KEY=your_api_key_here
```

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

- Modern, responsive UI
- Real-time API data retrieval
- AI handling of requests
- Error handling
- Loading states
- Clean and intuitive interface

## Customization

- Modify the API endpoint in `app.py`
- Adjust the UI in `templates/index.html`
- Customize styles in `static/style.css`
- Update the data display logic in `static/script.js` 