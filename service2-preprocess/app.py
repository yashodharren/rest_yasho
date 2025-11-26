import os
import logging
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Service 2 - Preprocessing")

# Configuration
SERVICE3_URL = os.getenv("SERVICE3_URL", "http://service3-loadbalancer:8063")
SERVICE_PORT = int(os.getenv("SERVICE_PORT", 8052))

class PreprocessRequest(BaseModel):
    text: str
    request_id: str

class PreprocessResponse(BaseModel):
    status: str
    message: str
    word_count: int
    report: str = ""
    top_words: list = []

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and punctuation
    text = re.sub(r'[^a-z0-9\s]', '', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "service2"}

@app.post("/preprocess")
async def preprocess_text(request: PreprocessRequest) -> PreprocessResponse:
    """
    Preprocess text: clean and normalize, then forward to Service 3
    """
    logger.info(f"[Service 2] Received request {request.request_id}")
    logger.info(f"[Service 2] Original text length: {len(request.text)} characters")
    
    try:
        # Clean text
        cleaned_text = clean_text(request.text)
        logger.info(f"[Service 2] Cleaned text length: {len(cleaned_text)} characters")
        
        # Forward to Service 3
        logger.info(f"[Service 2] Forwarding to Service 3 at {SERVICE3_URL}")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICE3_URL}/analyze",
                json={
                    "text": cleaned_text,
                    "request_id": request.request_id
                },
                timeout=60.0
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"[Service 2] Received response from Service 3")
            
            return PreprocessResponse(
                status=result.get("status", "success"),
                message=result.get("message", "Preprocessing completed"),
                word_count=result.get("word_count", 0),
                report=result.get("report", ""),
                top_words=result.get("top_words", [])
            )
    
    except httpx.HTTPError as e:
        logger.error(f"[Service 2] HTTP Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Service 3 error: {str(e)}")
    except Exception as e:
        logger.error(f"[Service 2] Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    logger.info(f"[Service 2] Starting on port {SERVICE_PORT}")
    uvicorn.run(app, host="0.0.0.0", port=SERVICE_PORT)
