import os
import requests
import json
import time  # Added for exponential backoff
from flask import Flask, request, jsonify
from urllib.parse import urlparse

app = Flask(__name__)

# --- Configuration ---
# IMPORTANT: REPLACE THIS PLACEHOLDER WITH YOUR ACTUAL KEY
GEMINI_API_KEY = "place ur key here" 

# Updated to the current recommended preview model for grounded generation
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent"

def call_gemini_api_with_retry(url, key, payload, max_retries=3):
    """
    Handles POST requests to the Gemini API with exponential backoff for retries.
    """
    headers = {'Content-Type': 'application/json'}
    url_with_key = f"{url}?key={key}"
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url_with_key, headers=headers, json=payload, timeout=30)
            response.raise_for_status()  # Raise exception for bad status codes (4xx or 5xx)
            return response
        except requests.exceptions.RequestException as e:
            # Check if this is the last attempt
            if attempt < max_retries - 1:
                # Calculate delay: 2^attempt seconds (1s, 2s, 4s)
                sleep_time = 2 ** attempt
                # print(f"API call failed (Attempt {attempt + 1}/{max_retries}). Retrying in {sleep_time}s...") # Suppressed console logging as per instructions
                time.sleep(sleep_time)
            else:
                # If it's the last attempt, raise the error
                raise e
    # Should be unreachable, but return None as a fallback
    return None


@app.route('/api/factcheck', methods=['POST'])
def fact_check_claim():
    """
    Handles POST requests to fact-check a claim using the Gemini API 
    with Google Search grounding and structured JSON output.
    """
    # NOTE: Corrected the placeholder check to match the initial value "key"
    if GEMINI_API_KEY == "key":
        return jsonify({"error": "API Key is missing. Please replace 'key' in app.py with your actual key."}), 500

    try:
        data = request.get_json()
        claim = data.get('claim')

        if not claim:
            return jsonify({"error": "Missing 'claim' in request body"}), 400

        # --- Gemini API Payload Configuration ---
        system_prompt = "You are a world-class fact-checker. Your task is to use the provided Google Search results to assess the accuracy of the user's claim and respond strictly in the requested JSON format. The accuracy_score should be your confidence (0-100) in the correctness of the verdict based on the supporting sources."
        
        payload = {
            "contents": [{"parts": [{"text": f"Fact-Check this claim: {claim}"}]}],
            # Enable Google Search grounding
            "tools": [{"google_search": {}}],
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            # Request structured JSON output
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": {
                    "type": "OBJECT",
                    "properties": {
                        "verdict": {"type": "STRING", "description": "The final conclusion, e.g., 'True', 'False', or 'Partially True'."},
                        "accuracy_score": {"type": "INTEGER", "description": "Confidence level in the verdict, from 0 to 100."},
                        "analysis": {"type": "STRING", "description": "A single, precise paragraph of analysis explaining the verdict based only on the retrieved information."}
                    },
                    "propertyOrdering": ["verdict", "accuracy_score", "analysis"]
                }
            }
        }

        # --- Call Gemini API with Retry Logic ---
        response = call_gemini_api_with_retry(API_URL, GEMINI_API_KEY, payload)
        
        gemini_result = response.json()
        
        # --- Process Gemini Result ---
        candidate = gemini_result.get('candidates', [None])[0]
        if not candidate:
            return jsonify({"error": "API returned an invalid or empty response."}), 500

        # Extract structured data
        json_text = candidate.get('content', {}).get('parts', [{}])[0].get('text')
        
        # Ensure the response is valid JSON before attempting to parse
        try:
            data = json.loads(json_text)
        except json.JSONDecodeError:
             app.logger.error(f"Failed to decode JSON from Gemini response: {json_text}")
             return jsonify({"error": "API returned malformed JSON structure.", "raw_response": json_text}), 500
        
        # Extract grounding sources
        sources = []
        grounding_metadata = candidate.get('groundingMetadata', {})
        if grounding_metadata and grounding_metadata.get('groundingAttributions'):
            for attr in grounding_metadata['groundingAttributions']:
                web = attr.get('web')
                if web and web.get('uri') and web.get('title'):
                    sources.append({
                        "title": web['title'],
                        "uri": web['uri'],
                        "hostname": urlparse(web['uri']).hostname if urlparse(web['uri']).hostname else "N/A"
                    })

        # Combine structured data and sources for the final response
        data['sources'] = sources
        
        return jsonify(data)

    except requests.exceptions.HTTPError as e:
        app.logger.error(f"HTTP Error calling Gemini API: {e}. Response: {e.response.text}")
        return jsonify({"error": "Failed to connect to the Gemini API.", "details": str(e)}), 500
    except Exception as e:
        app.logger.error(f"Internal Server Error: {e}")
        return jsonify({"error": "An unexpected server error occurred.", "details": str(e)}), 500

if __name__ == '__main__':
    # Use 0.0.0.0 to make the Flask app accessible externally (for deployment/testing)
    app.run(host='0.0.0.0', debug=True, port=5000)
