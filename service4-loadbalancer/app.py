import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Service 4 - Load Balancer")

class ReportRequest(BaseModel):
    analysis: dict
    request_id: str

class ReportResponse(BaseModel):
    status: str
    message: str
    word_count: int
    report: str
    top_words: list = []

class LoadBalancer:
    def __init__(self, instances: List[str]):
        self.instances = instances
        self.current_index = 0
        self.instance_stats = {instance: {'requests': 0, 'errors': 0} for instance in instances}
        logger.info(f"[Load Balancer 4] Initialized with {len(instances)} instances:")
        for instance in instances:
            logger.info(f"  - {instance}")
    
    async def route_request(self, request_data: dict) -> dict:
        """Route request to available instance using round-robin"""
        start_index = self.current_index
        attempts = 0
        
        request_id = request_data.get('request_id', 'unknown')
        logger.info(f"[Load Balancer 4] Routing request {request_id}")
        
        while attempts < len(self.instances):
            instance = self.instances[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.instances)
            
            logger.info(f"[Load Balancer 4] → Sending to {instance}")
            self.instance_stats[instance]['requests'] += 1
            
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"http://{instance}/report",
                        json=request_data,
                        timeout=60.0
                    )
                    response.raise_for_status()
                    result = response.json()
                    logger.info(f"[Load Balancer 4] ✓ Success from {instance}")
                    return result
            
            except httpx.HTTPError as e:
                self.instance_stats[instance]['errors'] += 1
                logger.error(f"[Load Balancer 4] ✗ Error from {instance}: {str(e)}")
                attempts += 1
                continue
            except Exception as e:
                self.instance_stats[instance]['errors'] += 1
                logger.error(f"[Load Balancer 4] ✗ Unexpected error from {instance}: {str(e)}")
                attempts += 1
                continue
        
        error_msg = f"All Service 4 instances failed after {attempts} attempts"
        logger.error(f"[Load Balancer 4] 💥 {error_msg}")
        raise HTTPException(status_code=503, detail=error_msg)

# Initialize load balancer with service instances
SERVICE4_INSTANCES = [
    "service4a:8054",
    "service4b:8066",
    "service4c:8068",
    "service4d:8070"
]

lb = LoadBalancer(SERVICE4_INSTANCES)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "service4-loadbalancer"}

@app.post("/report")
async def generate_request_report(request: ReportRequest) -> ReportResponse:
    """
    Load balancer endpoint: routes requests to Service 4 instances
    """
    logger.info(f"[Load Balancer 4] Received request {request.request_id}")
    
    try:
        result = await lb.route_request({
            "analysis": request.analysis,
            "request_id": request.request_id
        })
        
        return ReportResponse(
            status=result.get("status", "success"),
            message=result.get("message", "Report generated"),
            word_count=result.get("word_count", 0),
            report=result.get("report", ""),
            top_words=result.get("top_words", [])
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Load Balancer 4] Error: {str(e)}")
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
    port = int(os.getenv("SERVICE_PORT", 8064))
    logger.info(f"[Service 4 Load Balancer] Starting on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
