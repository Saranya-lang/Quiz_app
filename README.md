# AI-Powered Quiz Generator

🧠 This is a Streamlit-based web app that generates customized quizzes using AI.  
Users enter their name, email, and a quiz topic, and receive a 20-question multiple-choice quiz with audio support and result emailing.

---

## Features

- Input your name, email, and desired quiz topic
- Automatically generates 20 multiple-choice questions (MCQs)
- Provides 4 answer options per question
- Includes a 5-minute timer for the quiz
- Sends quiz results to the user's email
- Supports audio generation for questions or options (if applicable)
- Built with Streamlit for an interactive web UI

---

## Getting Started

### Prerequisites

- Python 3.7 or higher
- An OpenAI API key for quiz generation
- SMTP email credentials to send quiz results

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Saranya-lang/quiz_app.git
   cd quiz_app
2. Create and activate a virtual environment:

bash

python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

3.Install dependencies:
  pip install -r requirements.txt

4.Create a .env file in the project root with the following environment variables:
  OPENAI_API_KEY=your_openai_api_key_here
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_EMAIL=your_email@example.com
SMTP_PASSWORD=your_email_password

Usage
Run the app locally with:
streamlit run app.py

