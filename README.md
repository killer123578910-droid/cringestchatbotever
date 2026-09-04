# Intent-Based Rental Room Chatbot

A Vietnamese intent-based chatbot designed to answer common questions about rental rooms. The project uses basic Natural Language Processing techniques to classify user messages and generate predefined responses.

The chatbot is deployed on Render and can be accessed through Telegram.

## Live Demo

Chat with the bot on Telegram:

**Telegram Bot:** [@h_advbot](https://t.me/h_advbot)

## Features

* Vietnamese text processing with Underthesea
* Intent classification using TF-IDF and Cosine Similarity
* Predefined intents and responses stored in JSON
* Fallback handling for unknown messages
* REST API built with Flask
* Telegram Bot integration
* Chat history storage with PostgreSQL
* Deployed using Render

## Tech Stack

* Python
* Flask
* Scikit-learn
* Underthesea
* PostgreSQL
* Flask-SQLAlchemy
* PyTelegramBotAPI
* Render

## How It Works

```text
Telegram User
      ↓
Telegram Bot
      ↓
Flask API
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
      ↓
Telegram Response
```

The chatbot compares the user's message with predefined patterns and selects the intent with the highest similarity score. If the similarity score is below a defined threshold, the chatbot returns a fallback response.

## Project Structure

```text
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

## Usage

The chatbot is publicly available through Telegram:

**https://t.me/h_advbot**

Users can send messages related to rental rooms, including:

* Greetings
* Room information
* Rental prices
* Services and utilities
* Amenities
* Deposit and rental terms

The chatbot processes the message, identifies the most relevant intent, and returns a predefined response.

## Local Installation

Clone the repository:

```bash
git clone https://github.com/killer123578910-droid/cringestchatbotever.git
cd cringestchatbotever
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment.

Windows:

```bash
venv\Scripts\activate
```

Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file:

```env
API=your_telegram_bot_token
sql_pw=your_postgresql_password
```

Make sure your PostgreSQL database configuration matches the application settings.

## Running Locally

Start the Flask application:

```bash
python app.py
```

The Telegram bot can then be started with:

```bash
python bot.py
```

## API

### Chat Endpoint

```text
POST /api/chat
```

Example request:

```json
{
    "message": "Giá phòng bao nhiêu?"
}
```

Example response:

```json
{
    "message": "..."
}
```

## Deployment

The application is deployed using Render.

The deployed backend handles chatbot requests and communicates with the Telegram bot.

## Purpose

This project was built to practice:

* Basic Natural Language Processing
* Vietnamese text processing
* Intent-based chatbot development
* TF-IDF and Cosine Similarity
* Flask API development
* Telegram Bot integration
* PostgreSQL database integration
* Cloud deployment with Render

## Limitations

This project uses a similarity-based intent classification approach and is designed for learning purposes.

It does not use Deep Learning or Large Language Models. The chatbot works best with messages related to predefined intents and patterns.


