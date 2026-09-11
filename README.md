# RAG Telegram Chatbot

A Telegram chatbot built with Retrieval-Augmented Generation (RAG). Users can provide their own text data, which is embedded and stored in PostgreSQL with pgvector. Relevant context is retrieved and passed to an LLM to generate responses.

## Demo

Telegram: [@h_advbot](https://t.me/h_advbot)

## Features

* RAG-based question answering
* User-provided text and `.txt` file ingestion
* Text chunking and vector embeddings
* PostgreSQL + pgvector similarity search
* User-specific context retrieval
* Gemma LLM via OpenRouter
* Telegram Bot integration
* Chat history storage
* Render deployment

## Architecture

```text
Telegram
   ↓
Flask Webhook
   ↓
Query Embedding
   ↓
PostgreSQL + pgvector
   ↓
Retrieve Relevant Context
   ↓
Prompt + Gemma LLM
   ↓
Response
```

## Tech Stack

* Python
* Flask
* LangChain
* PostgreSQL + pgvector
* NVIDIA Nemotron Embeddings
* Gemma
* OpenRouter
* PyTelegramBotAPI
* Render

## Commands

```text
/start
```
show instructions.

```text
/input your text
```

Add text to the vector database.

Send a `.txt` file with `/input` to add file content.

```text
/delete
```

Clear the vector database.



After adding context, simply send a question to the bot.

## Project Structure

```text
cringestchatbotever/
├── rag_engine/
│   ├── get_rep.py
│   └── rag_preprocess.py
├── choicenrep/
├── context/
├── app.py
├── extensions.py
├── requirements.txt
└── README.md
```

## Purpose

A personal learning project focused on practical RAG development, including embeddings, vector search, LLM integration, PostgreSQL, Telegram bots, and deployment.
