import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Service 1 - Text Input")

# Configuration
SERVICE2_URL = os.getenv("SERVICE2_URL", "http://service2-loadbalancer:8062")
SERVICE_PORT = int(os.getenv("SERVICE_PORT", 8051))

class TextRequest(BaseModel):
    text: str
    request_id: str

class TextResponse(BaseModel):
    status: str
    message: str
    word_count: int
    report: str = ""
    top_words: list = []

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "service1"}

@app.post("/process")
async def process_text(request: TextRequest) -> TextResponse:
    """
    Main endpoint: receives text from client and orchestrates pipeline
    """
    logger.info(f"[Service 1] Received request {request.request_id}")
    logger.info(f"[Service 1] Text length: {len(request.text)} characters")
    
    try:
        # Forward to Service 2
        logger.info(f"[Service 1] Forwarding to Service 2 at {SERVICE2_URL}")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICE2_URL}/preprocess",
                json={
                    "text": request.text,
                    "request_id": request.request_id
                },
                timeout=60.0
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"[Service 1] Received response from Service 2")
            
            return TextResponse(
                status=result.get("status", "success"),
                message=result.get("message", "Pipeline completed"),
                word_count=result.get("word_count", 0),
                report=result.get("report", ""),
                top_words=result.get("top_words", [])
            )
    
    except httpx.HTTPError as e:
        logger.error(f"[Service 1] HTTP Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Service 2 error: {str(e)}")
    except Exception as e:
        logger.error(f"[Service 1] Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    logger.info(f"[Service 1] Starting on port {SERVICE_PORT}")
    uvicorn.run(app, host="0.0.0.0", port=SERVICE_PORT)
