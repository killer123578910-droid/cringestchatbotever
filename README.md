# Intent-Based Rental Room Chatbot

A Vietnamese intent-based chatbot designed to answer common questions about rental rooms. The project uses basic Natural Language Processing techniques to classify user messages and generate predefined responses.

The chatbot is provided through a Flask API, integrated with Telegram, and stores chat history in PostgreSQL.

## Features

* Vietnamese text processing with Underthesea
* Intent classification using TF-IDF and Cosine Similarity
* Predefined intents and responses stored in JSON
* Fallback handling for unknown messages
* REST API built with Flask
* Telegram Bot integration
* Chat history storage with PostgreSQL

## Tech Stack

* Python
* Flask
* Scikit-learn
* Underthesea
* PostgreSQL
* Flask-SQLAlchemy
* PyTelegramBotAPI

## How It Works

```text id="mbv6ck"
User Message
      ↓
Text Tokenization
      ↓
TF-IDF Vectorization
      ↓
Cosine Similarity
      ↓
Intent Classification
      ↓
Response Selection
```

The chatbot compares the user's message with predefined patterns and selects the intent with the highest similarity score. If the score is below a defined threshold, the chatbot returns a fallback response.

## Project Structure

```text id="buvjhd"
cringestchatbotever/
│
├── choicenrep/
│   ├── inputanas.py       # NLP and intent classification logic
│   ├── intents.json       # Chatbot intents and responses
│   └── naive_approach.py
│
├── app.py                 # Flask API and database integration
├── bot.py                 # Telegram Bot
├── test.py
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash id="v44o4s"
git clone https://github.com/killer123578910-droid/cringestchatbotever.git
cd cringestchatbotever
```

Create and activate a virtual environment:

```bash id="87dazp"
python -m venv venv
```

Windows:

```bash id="vbr5bn"
venv\Scripts\activate
```

Linux:

```bash id="kh8pb0"
source venv/bin/activate
```

Install dependencies:

```bash id="e6usj1"
pip install -r requirements.txt
```

## Configuration

Create a `.env` file:

```env id="d83zbn"
API=your_telegram_bot_token
sql_pw=your_postgresql_password
```

Make sure PostgreSQL is running and the database configuration matches `app.py`.

## Usage

Start the Flask API:

```bash id="dk1ccq"
python app.py
```

Then start the Telegram Bot in another terminal:

```bash id="k5z98n"
python bot.py
```

The Telegram bot sends user messages to the Flask API for processing and returns the generated response.

## API

### Chat Endpoint

```text id="8c4bqs"
POST /api/chat
```

Request:

```json id="h0g4h3"
{
    "message": "Giá phòng bao nhiêu?"
}
```

Response:

```json id="h8d3uk"
{
    "message": "..."
}
```

## Purpose

This project was built to practice:

* Basic Natural Language Processing
* Intent-based chatbot development
* TF-IDF and Cosine Similarity
* Flask API development
* Telegram Bot integration
* PostgreSQL database integration

## Limitations

This is a rule and similarity-based chatbot designed for learning purposes. It does not use Deep Learning or Large Language Models and works best with questions related to predefined intents.

## Future Improvements

* Add more intents and training patterns
* Improve Vietnamese text preprocessing
* Use sentence embeddings for semantic similarity
* Add confidence scoring
* Improve fallback responses
* Add a web interface
