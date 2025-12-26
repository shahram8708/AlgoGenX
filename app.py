from flask import Flask, render_template, request, redirect, url_for, flash
import os
import base64
import json
import requests
from dotenv import load_dotenv
import markdown2

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

load_dotenv()

API_KEY = ""
PERPLEXITY_API_KEY = ""
SECRET_KEY = os.getenv("SECRET_KEY", "signature_secret")
ENDPOINT = "https://api.perplexity.ai/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        model_selected = request.form.get("modelSelect", "gemini").lower()

        sig1 = request.files.get("signature1")
        sig2 = request.files.get("signature2")

        if not sig1 or not sig2 or sig1.filename == "" or sig2.filename == "":
            flash("Both signature files are required.", "danger")
            return redirect(url_for("index"))

        if not (allowed_file(sig1.filename) and allowed_file(sig2.filename)):
            flash("Invalid file type. Please upload JPG or PNG images.", "danger")
            return redirect(url_for("index"))

        b64_1 = base64.b64encode(sig1.read()).decode("utf-8")
        b64_2 = base64.b64encode(sig2.read()).decode("utf-8")

        prompt_text = """I will provide you with two signature images. Your task is to analyze both signatures and determine whether they were made by the same person or by two different individuals. This verification is intended for high-stakes use in the banking sector, where signature-based fraud prevention is critical.

        Please ensure your analysis is as accurate as possible, considering all professional-level forensic signature analysis techniques, such as:
        – Line quality
        – Stroke order
        – Pen pressure consistency
        – Signature rhythm and speed
        – Angle and slant
        – Spacing and alignment
        – Signature proportions and size consistency
        – Natural variation vs. forgery indicators
        – Tremors, hesitation, and unnatural stops

        Also, compare the behavioral biometric elements of handwriting if detectable. If there are differences, explain whether they can be attributed to natural variation (as often seen in genuine signatures) or if they suggest deliberate forgery.

        Include the following in your response:

        A detailed comparison report

        A final conclusion: "Same Person" or "Different People"

        Confidence level (in percentage)

        Reasoning for your decision

        Highlight any areas of uncertainty or ambiguity

        Use best practices followed by forensic document examiners and handwriting experts in real-world financial institutions

        Assume this verification will be used as legal or compliance evidence, so accuracy, completeness, and professional explanation are critical. Analyze from every angle and cross-check with all known scientific and forensic signature verification methods.

        Only proceed if you are capable of checking with maximum reliability, minimizing false positives and false negatives, and clearly stating the level of certainty.
        
        Give your response with only the following:

        Match Status: "Same Person" or "Different People"

        Confidence Level: (percentage)

        Reasoning: (a short, clear summary of why you made the determination)

        Do not include any instructions, disclaimers, or explanations about your process. Only provide the core findings in a concise and professional tone suitable for forensic banking use."""

        if model_selected == "perplexity":
            endpoint = "https://api.perplexity.ai/chat/completions"
            headers = {
                "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "sonar-pro",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt_text},
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_1}"}},
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_2}"}}
                        ]
                    }
                ]
            }
        else:  
            endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={}".format(API_KEY)
            headers = {}  
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt_text},
                            {"inline_data": {"mime_type": "image/png", "data": b64_1}},
                            {"inline_data": {"mime_type": "image/png", "data": b64_2}},
                        ]
                    }
                ]
            }

        try:
            response = requests.post(endpoint, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            ai_data = response.json()
            if model_selected == "perplexity":
                ai_text = ai_data.get("choices", [{}])[0].get("message", {}).get("content", "No response.")
            else: 
                ai_text = (
                    ai_data.get("candidates", [{}])[0]
                    .get("content", {})
                    .get("parts", [{}])[0]
                    .get("text", "No response.")
                )

        except Exception as exc:
            flash(f"Error communicating: {exc}", "danger")
            return redirect(url_for("index"))

        html_report = markdown2.markdown(ai_text)

        return render_template(
            "result.html",
            report=html_report,
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
