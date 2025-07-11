**TIME-Stories-API**

A basic Flask application that scrapes the latest 6 stories from time.com using regular expressions. It uses only Python's built-in libraries and no external HTML parsers are required.

Features
- Returns the latest 6 headlines from time.com
- Uses regex to extract titles and URLs
- Lightweight and easy to run
- No external scraping libraries used

How to Run?
- Install Python 3 
- Create a virtual environment
On macOS/Linux:
python3 -m venv venv
- Activate The environment 
source venv/bin/activate
- Install Flask:
pip install flask
- Run the file:
python project.py
- Open in browser:
http://127.0.0.1:5000/getTimeStories
