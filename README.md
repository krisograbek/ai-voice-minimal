# Flask + ReactJS Full Stack Application

This application utilizes OpenAI's API to transcribe audio inputs from the user, generate text-based responses, and synthesize these responses back into audio. It features a ReactJS frontend for user interaction and a Flask backend for handling the audio processing and API communication.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.8 or higher
- Node.js and npm
- An OpenAI API key

## Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

## Setting up the Backend

Navigate to the backend directory and create a virtual environment:

```bash
cd path/to/your/backend
python -m venv venv
```

**Activate the virtual environment:**
On Windows: `venv\Scripts\activate`
On macOS/Linux: `source venv/bin/activate`

**Install the required Python dependencies:**

```bash
pip install -r requirements.txt
```

**Create a .env file based on the provided .env.example. Replace `OPENAI_API_KEY` with your actual OpenAI API key.**

## Setting up the Frontend

Navigate to the frontend directory:

```bash
cd path/to/your/frontend
```

**Install the required npm packages:**

```bash
npm install
```

## Running the Application

### Starting the Backend Server

Ensure your virtual environment is activated, then run:

```bash
python app.py
```

This will start the Flask server on http://localhost:5000/.

## Starting the Frontend Application

Open a new terminal window, navigate to the frontend directory, and run:

```bash
npm start
```

This will start the React application and open it in your default web browser at http://localhost:3000/.

## Using the Application

Once both servers are running, go to http://localhost:3000/ in your browser.
Click on the microphone icon to start recording your message.
Click the stop icon to end the recording. The application will then transcribe your message, generate a response, and synthesize this response into audio.
Listen to the synthesized response through the audio player that appears.
