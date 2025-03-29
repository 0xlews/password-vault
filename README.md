# Password Vault

A simple learning project for exploring account discovery and API integration.

## What's This?

This is a proof of concept I built while learning about Flask and API integrations. It's basically a sandbox for experimenting with the Hunter API to discover accounts associated with email addresses.

## Core Functionality

- Basic account discovery using Hunter API
- Simple web interface built with Flask
- Local database for storing discovered accounts
- Categorisation of discovered accounts

## Tech Stack

- Python + Flask
- SQLite + SQLAlchemy
- Basic HTML/CSS

## Getting Started

### Prerequisites

- Python 3.8+
- Hunter API key (free tier works for testing)

### Installation

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your Hunter API key:
   ```
   HUNTER_API_KEY=your_hunter_api_key
   ```
4. Run with: `python app.py`

## Project Structure

The project is organised in a standard Flask structure with separate files for routes, models, and services.

## Testing

Run the basic tests with:
```
python tests/test_hunter.py
```

### Learning Goals

I created this project to:
- Understand more about APIs
- Flask development

### Future Plans

I'm planning to expand this concept by integrating additional APIs:
- Have I Been Pwned (HIBP) paid API for breach detection
- Additional email verification services
- Other account discovery methods
- Better categorisation of discovered accounts

The architecture is designed to be modular so I can easily add new API integrations as I learn more.

## License

MIT