import requests

OLLAMA_URL = "http://100.104.176.55:11434/api/generate"
MODEL = "phi3"

import requests
import json
import re

def extract_first_json(text):
    # Remove any code block markers and extra text
    clean_text = re.sub(r'```json\s*\n|\n\s*```', '', text).strip()

    # Try parsing the cleaned JSON
    try:
        return json.loads(clean_text)
    except json.JSONDecodeError:
        return {"error": "JSON decode error", "raw": clean_text}

def classify_ticket(description):
    prompt = (
        "You are a highly trained AI designed to classify IT helpdesk tickets who only speaks in JSON , Do not write normal text.:\n"
        "1. Return a JSON object with exactly two fields:\n"
        "   - \"severity\" (Low, Medium, High, Critical)\n"
        "   - \"department\" (IT, HR, Facilities, Finance)\n"
        "2. Classify based on the following guidelines:\n"
        "   - Severity:\n"
        "     - Low: Minor issue, typically not urgent.\n"
        "     - Medium: Noticeable issue affecting users but not critical.\n"
        "     - High: Major issue with significant impact on work or operations.\n"
        "     - Critical: An emergency-level issue requiring immediate attention.\n"
        "   - Department:\n"
        "     - IT: Technology-related issues (e.g., software, network, devices).\n"
        "     - HR: Employee relations, payroll, harassment, and work-life matters.\n"
        "     - Facilities: Office infrastructure, HVAC, lighting, physical space.\n"
        "     - Finance: Accounting, budgets, payroll, or financial tools.\n"
        'Your response must ONLY be in this form : {"severity":  ,"department": }\n'
        f"Ticket description: \"{description}\""
    )

    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": True
    }, stream=True)

    buffer = ""
    for chunk in response.iter_lines():
        if chunk:
            token = json.loads(chunk.decode()).get("response", "")
            buffer += token
            if "}" in token:
                break

    return extract_first_json(buffer) 

# test_descriptions = [
#     "Please update my contact number in the employee records.",
#     "My laptop is running slow and sometimes freezes during video calls.",
#     "The air conditioning in the server room has stopped working.",
#     "The internal network is completely down and no one can access email or shared drives.",
#     "There is a mismatch in the monthly budget reports sent by the accounting tool.",
#     "An employee has reported harassment from a colleague and is requesting immediate action.",
#     "We just discovered unauthorized transactions in the company’s payroll system.",
#     "The light in the pantry is flickering occasionally."
# ]

# for desc in test_descriptions:
#     print(f"\nDescription: {desc}")
#     result = classify_ticket(desc)
#     print("Result:", result)