import os
import logging
from collections import Counter
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Service 3 - Analysis")

# Configuration
SERVICE4_URL = os.getenv("SERVICE4_URL", "http://service4-loadbalancer:8064")
SERVICE_PORT = int(os.getenv("SERVICE_PORT", 8053))

class AnalysisRequest(BaseModel):
    text: str
    request_id: str

class AnalysisResponse(BaseModel):
    status: str
    message: str
    word_count: int
    report: str = ""
    top_words: list = []

def analyze_text(text: str) -> tuple:
    """
    Analyze text: tokenize and count word frequencies
    Returns: (word_count, top_words_list, word_frequencies_dict)
    """
    # Tokenize text
    words = text.split()
    word_count = len(words)
    
    # Count frequencies
    word_freq = Counter(words)
    
    # Get top 10 words
    top_words = word_freq.most_common(10)
    
    logger.info(f"[Service 3] Word count: {word_count}")
    logger.info(f"[Service 3] Unique words: {len(word_freq)}")
    logger.info(f"[Service 3] Top words: {top_words[:5]}")
    
    return word_count, top_words, dict(word_freq)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "service3"}

@app.post("/analyze")
async def analyze_request(request: AnalysisRequest) -> AnalysisResponse:
    """
    Analyze text: perform word frequency analysis and forward to Service 4
    """
    logger.info(f"[Service 3] Received request {request.request_id}")
    logger.info(f"[Service 3] Text length: {len(request.text)} characters")
    
    try:
        # Analyze text
        word_count, top_words, word_freq = analyze_text(request.text)
        
        # Prepare analysis data for Service 4
        analysis_data = {
            "word_count": word_count,
            "top_words": top_words,
            "word_frequencies": word_freq,
            "unique_words": len(word_freq)
        }
        
        # Forward to Service 4
        logger.info(f"[Service 3] Forwarding to Service 4 at {SERVICE4_URL}")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICE4_URL}/report",
                json={
                    "analysis": analysis_data,
                    "request_id": request.request_id
                },
                timeout=60.0
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"[Service 3] Received response from Service 4")
            
            return AnalysisResponse(
                status=result.get("status", "success"),
                message=result.get("message", "Analysis completed"),
                word_count=result.get("word_count", word_count),
                report=result.get("report", ""),
                top_words=result.get("top_words", top_words)
            )
    
    except httpx.HTTPError as e:
        logger.error(f"[Service 3] HTTP Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Service 4 error: {str(e)}")
    except Exception as e:
        logger.error(f"[Service 3] Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    logger.info(f"[Service 3] Starting on port {SERVICE_PORT}")
    uvicorn.run(app, host="0.0.0.0", port=SERVICE_PORT)
