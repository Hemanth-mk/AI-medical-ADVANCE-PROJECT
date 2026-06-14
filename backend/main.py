from fastapi import FastAPI
from pydantic import BaseModel, Field
import google.generativeai as genai



from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load Gemini model
model = genai.GenerativeModel(
    "models/gemini-flash-lite-latest"
)

# Create FastAPI app
app = FastAPI()

# Input schema
class Query(BaseModel):
    question: str

# API endpoint
@app.post("/ask")

def ask_ai(query: Query):

    try:

        response = model.generate_content(
            query.question
        )

        return {
            "response": response.text
        }

    except Exception as e:

        return {
            "response": str(e)
        }