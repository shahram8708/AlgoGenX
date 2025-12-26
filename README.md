# AlgoGenX

AlgoGenX is a Flask-based web application for AI-driven signature comparison and verification. It allows users to upload two signature images, sends them to an AI model for forensic-style analysis, and returns a structured verification report rendered as formatted HTML.

The system is designed around a simple web workflow with validation, AI communication, Markdown-to-HTML conversion, and a clean Bootstrap-based interface.

---

## Features

* Upload two signature images (PNG or JPG/JPEG)
* Validates file type before processing
* Converts uploaded images to Base64 for secure transmission
* Sends request to AI model using HTTP API
* Receives a narrative forensic analysis report
* Renders the AI response using Markdown2
* Displays result in a formatted HTML report page
* Flash messaging for errors and status feedback
* dotenv support for configuration
* Minimal, user-friendly web interface

---

## Tech Stack

**Backend**

* Flask
* Requests
* python-dotenv
* markdown2

**Frontend**

* HTML / Jinja Templates
* Bootstrap 5
* Custom CSS and simple JavaScript

All dependencies are listed in `requirements.txt`.

---

## Project Structure

```
AlgoGenX/
│
├── app.py                     # Main Flask application
├── requirements.txt           # Dependencies
│
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── scripts.js
│
└── templates/
    ├── index.html             # Upload form UI
    └── result.html            # Verification result page
```

---

## Installation

1. Extract or clone the project.
2. Ensure Python is installed.
3. Install dependencies:

```
pip install -r requirements.txt
```

---

## Configuration

Environment variables are loaded using `python-dotenv`.

The application expects the following values to be configured inside `app.py` or through environment variables:

* `SECRET_KEY` (used for Flask session security)
* AI API key(s) for communicating with the remote model

The application defines:

```
API_KEY = ""
PERPLEXITY_API_KEY = ""
ENDPOINT = "https://api.perplexity.ai/chat/completions"
```

Update these values with valid credentials.

---

## Running the Application

Start the Flask server:

```
python app.py
```

By default it runs in debug mode.

Open the application in a browser:

```
http://localhost:5000
```

---

## Usage

1. Open the homepage.
2. Upload two signature image files.
3. Submit the form.
4. The system:

   * Validates both files
   * Converts them to Base64
   * Sends them to the configured AI endpoint
   * Receives and processes the response
5. A formatted verification report is displayed.

Only the following file types are accepted:

* `.png`
* `.jpg`
* `.jpeg`

---

## Routes

| Route | Method     | Description                                         |
| ----- | ---------- | --------------------------------------------------- |
| `/`   | GET / POST | Upload form, processing logic, and result rendering |

---

## Notes

* Both signature files are required; the system will not proceed otherwise.
* Invalid image formats will be rejected.
* The application relies on external AI services; valid API credentials and internet connectivity are required.
* Returned AI text is converted from Markdown to HTML before rendering.

---

## Troubleshooting

* If uploads fail, ensure files are valid PNG/JPG formats.
* Verify API credentials and endpoint.
* Check server logs for request or response issues.
* Ensure `.env` or configuration values are correctly set.

---

## License

This repository does not include a license file.
