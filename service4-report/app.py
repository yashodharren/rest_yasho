import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Service 4 - Report")

# Configuration
SERVICE_PORT = int(os.getenv("SERVICE_PORT", 8054))

class ReportRequest(BaseModel):
    analysis: dict
    request_id: str

class ReportResponse(BaseModel):
    status: str
    message: str
    word_count: int
    report: str
    top_words: list = []

def generate_report(analysis: dict) -> str:
    """
    Generate a formatted text report from analysis data
    """
    word_count = analysis.get("word_count", 0)
    top_words = analysis.get("top_words", [])
    unique_words = analysis.get("unique_words", 0)
    
    # Build report
    report_lines = [
        "=" * 70,
        "TEXT ANALYSIS REPORT",
        "=" * 70,
        f"Total Words: {word_count}",
        f"Unique Words: {unique_words}",
        ""
    ]
    
    if top_words:
        report_lines.append("Top 10 Most Frequent Words:")
        report_lines.append("-" * 70)
        for i, (word, count) in enumerate(top_words, 1):
            percentage = (count / word_count * 100) if word_count > 0 else 0
            report_lines.append(f"{i:2d}. {word:20s} - {count:5d} occurrences ({percentage:5.2f}%)")
    
    report_lines.append("=" * 70)
    
    report = "\n".join(report_lines)
    logger.info(f"[Service 4] Generated report with {len(top_words)} top words")
    
    return report

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "service4"}

@app.post("/report")
async def generate_request_report(request: ReportRequest) -> ReportResponse:
    """
    Final service: generate formatted report from analysis data
    """
    logger.info(f"[Service 4] Received request {request.request_id}")
    
    try:
        analysis = request.analysis
        word_count = analysis.get("word_count", 0)
        top_words = analysis.get("top_words", [])
        
        # Generate report
        report = generate_report(analysis)
        
        logger.info(f"[Service 4] Report generated successfully")
        
        return ReportResponse(
            status="success",
            message="Report generated successfully",
            word_count=word_count,
            report=report,
            top_words=top_words
        )
    
    except Exception as e:
        logger.error(f"[Service 4] Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    logger.info(f"[Service 4] Starting on port {SERVICE_PORT}")
    uvicorn.run(app, host="0.0.0.0", port=SERVICE_PORT)
