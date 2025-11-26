import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import asyncio
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Service 1 - Load Balancer")

class TextRequest(BaseModel):
    text: str
    request_id: str

class TextResponse(BaseModel):
    status: str
    message: str
    word_count: int
    report: str = ""
    top_words: list = []

class LoadBalancer:
    def __init__(self, instances: List[str]):
        self.instances = instances
        self.current_index = 0
        self.instance_stats = {instance: {'requests': 0, 'errors': 0} for instance in instances}
        logger.info(f"[Load Balancer 1] Initialized with {len(instances)} instances:")
        for instance in instances:
            logger.info(f"  - {instance}")
    
    async def route_request(self, request_data: dict) -> dict:
        """Route request to available instance using round-robin"""
        start_index = self.current_index
        attempts = 0
        
        request_id = request_data.get('request_id', 'unknown')
        text_size = len(request_data.get('text', ''))
        logger.info(f"[Load Balancer 1] Routing request {request_id} ({text_size} chars)")
        
        while attempts < len(self.instances):
            instance = self.instances[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.instances)
            
            logger.info(f"[Load Balancer 1] → Sending to {instance}")
            self.instance_stats[instance]['requests'] += 1
            
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"http://{instance}/process",
                        json=request_data,
                        timeout=60.0
                    )
                    response.raise_for_status()
                    result = response.json()
                    logger.info(f"[Load Balancer 1] ✓ Success from {instance}")
                    return result
            
            except httpx.HTTPError as e:
                self.instance_stats[instance]['errors'] += 1
                logger.error(f"[Load Balancer 1] ✗ Error from {instance}: {str(e)}")
                attempts += 1
                continue
            except Exception as e:
                self.instance_stats[instance]['errors'] += 1
                logger.error(f"[Load Balancer 1] ✗ Unexpected error from {instance}: {str(e)}")
                attempts += 1
                continue
        
        error_msg = f"All Service 1 instances failed after {attempts} attempts"
        logger.error(f"[Load Balancer 1] 💥 {error_msg}")
        raise HTTPException(status_code=503, detail=error_msg)

# Initialize load balancer with service instances
SERVICE1_INSTANCES = [
    "service1a:8051",
    "service1b:8055",
    "service1c:8057",
    "service1d:8059"
]

lb = LoadBalancer(SERVICE1_INSTANCES)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "service1-loadbalancer"}

@app.post("/process")
async def process_text(request: TextRequest) -> TextResponse:
    """
    Load balancer endpoint: routes requests to Service 1 instances
    """
    logger.info(f"[Load Balancer 1] Received request {request.request_id}")
    
    try:
        result = await lb.route_request({
            "text": request.text,
            "request_id": request.request_id
        })
        
        return TextResponse(
            status=result.get("status", "success"),
            message=result.get("message", "Pipeline completed"),
            word_count=result.get("word_count", 0),
            report=result.get("report", ""),
            top_words=result.get("top_words", [])
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Load Balancer 1] Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    """Get load balancer statistics"""
    return {
        "instances": lb.instances,
        "stats": lb.instance_stats
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("SERVICE_PORT", 8061))
    logger.info(f"[Service 1 Load Balancer] Starting on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
