import json
from google import genai

QUIZ_PROMPT = """
Create a quiz from the supplied transcript using this exact JSON structure:
{
  "title": "A concise title",
  "description": "A summary with at most 150 characters",
  "questions": [
    {
      "question_title": "Question text",
      "question_options": ["A", "B", "C", "D"],
      "answer": "The exact correct option"
    }
  ]
}
Create exactly 10 questions with exactly 4 distinct options each.
Each question must have exactly one correct answer.
Return valid JSON without explanations or code fences.
Transcript:
"""


def generate_quiz_data(transcript):
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=f"{QUIZ_PROMPT}\n{transcript}",
    )
    return json.loads(response.text)
