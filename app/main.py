from fastapi import FastAPI, HTTPException
from mangum import Mangum
from .models import GenerateRequest, GenerateResponse
from .ai_service import generate_text

app = FastAPI(title="GenAI API", version="1.0.0")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    try:
        generated_text = await generate_text(request.prompt)
        return GenerateResponse(generated_text=generated_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Handler for AWS Lambda
handler = Mangum(app)