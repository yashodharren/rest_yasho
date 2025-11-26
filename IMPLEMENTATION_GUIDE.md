# REST/HTTP Pipeline Implementation Guide

## Overview

This guide explains how the REST/HTTP distributed pipeline system is implemented using FastAPI and Docker Compose.

## Project Structure

```
rest_yasho/
├── README.md                    # Quick start guide
├── ARCHITECTURE.md              # System architecture
├── PROJECT_SUMMARY.md           # Project overview
├── IMPLEMENTATION_GUIDE.md      # This file
├── Makefile                     # Build automation
├── docker-compose.yml           # Service orchestration
├── client/
│   ├── app.py                  # Main client
│   ├── benchmark.py            # Performance benchmarking
│   ├── requirements.txt         # Dependencies
│   └── Dockerfile              # Container config
├── service1-input/
│   ├── app.py                  # Service 1
│   ├── requirements.txt         # Dependencies
│   └── Dockerfile              # Container config
├── service2-preprocess/
│   ├── app.py                  # Service 2
│   ├── requirements.txt         # Dependencies
│   └── Dockerfile              # Container config
├── service3-analysis/
│   ├── app.py                  # Service 3
│   ├── requirements.txt         # Dependencies
│   └── Dockerfile              # Container config
├── service4-report/
│   ├── app.py                  # Service 4
│   ├── requirements.txt         # Dependencies
│   └── Dockerfile              # Container config
└── datasets/
    └── sample.txt              # Sample test data
```

## Technology Stack

### Core Technologies

- **FastAPI**: Modern Python web framework with automatic API documentation
- **httpx**: Async HTTP client for inter-service communication
- **Uvicorn**: ASGI server for running FastAPI applications
- **Docker**: Containerization for consistent deployment
- **Docker Compose**: Orchestration of multiple containers

### Python Version

- Python 3.11 (slim image for smaller container size)

### Key Dependencies

```
fastapi==0.104.1          # Web framework
uvicorn==0.24.0           # ASGI server
httpx==0.25.1             # Async HTTP client
pydantic==2.5.0           # Data validation
```

## Service Implementation Details

### Service 1: Text Input (Port 8061)

**File**: `service1-input/app.py`

**Endpoints**:

- `GET /health` - Health check
- `POST /process` - Main entry point

**Functionality**:

- Receives text from client
- Forwards to Service 2 for preprocessing
- Waits for complete pipeline response
- Returns aggregated results

**Key Code**:

```python
@app.post("/process")
async def process_text(request: TextRequest) -> TextResponse:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SERVICE2_URL}/preprocess",
            json={"text": request.text, "request_id": request.request_id},
            timeout=60.0
        )
        return TextResponse(...)
```

### Service 2: Preprocessing (Port 8062)

**File**: `service2-preprocess/app.py`

**Endpoints**:

- `GET /health` - Health check
- `POST /preprocess` - Text preprocessing

**Functionality**:

- Receives raw text from Service 1
- Cleans text (lowercase, remove punctuation)
- Normalizes whitespace
- Forwards to Service 3 for analysis

**Text Cleaning Process**:

```python
def clean_text(text: str) -> str:
    text = text.lower()                           # Lowercase
    text = re.sub(r'[^a-z0-9\s]', '', text)     # Remove special chars
    text = re.sub(r'\s+', ' ', text).strip()     # Normalize whitespace
    return text
```

### Service 3: Analysis (Port 8063)

**File**: `service3-analysis/app.py`

**Endpoints**:

- `GET /health` - Health check
- `POST /analyze` - Text analysis

**Functionality**:

- Receives cleaned text from Service 2
- Tokenizes text into words
- Counts word frequencies
- Identifies top 10 words
- Forwards to Service 4 for report generation

**Analysis Process**:

```python
def analyze_text(text: str) -> tuple:
    words = text.split()                          # Tokenize
    word_count = len(words)
    word_freq = Counter(words)                    # Count frequencies
    top_words = word_freq.most_common(10)         # Top 10 words
    return word_count, top_words, dict(word_freq)
```

### Service 4: Report (Port 8064)

**File**: `service4-report/app.py`

**Endpoints**:

- `GET /health` - Health check
- `POST /report` - Report generation

**Functionality**:

- Receives analysis data from Service 3
- Generates formatted text report
- Includes statistics and top words
- Returns final response

**Report Format**:

```
======================================================================
TEXT ANALYSIS REPORT
======================================================================
Total Words: 1234
Unique Words: 567

Top 10 Most Frequent Words:
 1. word1              -   123 occurrences ( 9.97%)
 2. word2              -    98 occurrences ( 7.94%)
...
======================================================================
```

## Data Flow Through Pipeline

### Request Format

**Client → Service 1**:

```json
{
  "text": "Your text here",
  "request_id": "unique-id-123"
}
```

**Service 1 → Service 2**:

```json
{
  "text": "Your text here",
  "request_id": "unique-id-123"
}
```

**Service 2 → Service 3**:

```json
{
  "text": "cleaned text here",
  "request_id": "unique-id-123"
}
```

**Service 3 → Service 4**:

```json
{
    "analysis": {
        "word_count": 42,
        "top_words": [["word", 5], ["another", 3]],
        "word_frequencies": {"word": 5, "another": 3, ...},
        "unique_words": 20
    },
    "request_id": "unique-id-123"
}
```

### Response Format

**Service 4 → Service 3 → Service 2 → Service 1 → Client**:

```json
{
  "status": "success",
  "message": "Pipeline completed",
  "word_count": 42,
  "report": "======...",
  "top_words": [
    ["word", 5],
    ["another", 3]
  ]
}
```

## Async/Await Implementation

All services use asynchronous programming for non-blocking I/O:

```python
# Async endpoint
@app.post("/process")
async def process_text(request: TextRequest):
    # Non-blocking HTTP call
    async with httpx.AsyncClient() as client:
        response = await client.post(...)
        return response.json()
```

**Benefits**:

- Non-blocking I/O operations
- Better resource utilization
- Ability to handle multiple concurrent requests
- Improved throughput

## Docker Configuration

### Dockerfile Structure

Each service has a similar Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY service1-input/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY service1-input/app.py .

EXPOSE 8061

CMD ["python", "app.py"]
```

**Key Points**:

- Uses slim image for smaller size
- Installs dependencies in separate layer for caching
- Exposes service port
- Runs app.py as entry point

### Docker Compose Configuration

```yaml
services:
  service1:
    build:
      context: .
      dockerfile: service1-input/Dockerfile
    ports:
      - "8061:8061"
    environment:
      - SERVICE2_URL=http://service2:8062
    networks:
      - rest-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8061/health"]
```

**Key Features**:

- Service-to-service communication via service names
- Health checks for readiness
- Docker bridge network for inter-service communication
- Environment variables for configuration

## Environment Variables

Each service uses environment variables for configuration:

| Variable     | Service   | Default              | Purpose            |
| ------------ | --------- | -------------------- | ------------------ |
| SERVICE2_URL | Service 1 | http://service2:8062 | Service 2 endpoint |
| SERVICE3_URL | Service 2 | http://service3:8063 | Service 3 endpoint |
| SERVICE4_URL | Service 3 | http://service4:8064 | Service 4 endpoint |
| SERVICE_PORT | All       | 8061-8064            | Service port       |
| SERVICE1_URL | Client    | http://service1:8061 | Service 1 endpoint |

## Error Handling

Each service implements error handling:

```python
try:
    # Process request
    response = await client.post(...)
    return TextResponse(...)
except httpx.HTTPError as e:
    logger.error(f"HTTP Error: {str(e)}")
    raise HTTPException(status_code=500, detail=f"Service error: {str(e)}")
except Exception as e:
    logger.error(f"Error: {str(e)}")
    raise HTTPException(status_code=500, detail=str(e))
```

**Error Handling Features**:

- Try-catch blocks for network errors
- Timeout handling (60 seconds)
- Graceful error propagation
- Detailed error logging
- HTTP status codes for client feedback

## Logging

All services use Python's logging module:

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"[Service 1] Received request {request_id}")
logger.error(f"[Service 1] Error: {str(e)}")
```

**Log Format**:

- Service name in brackets for easy identification
- Request ID for request tracking
- Appropriate log levels (INFO, ERROR, etc.)

## Performance Considerations

### Optimization Strategies

1. **Connection Pooling**: httpx.AsyncClient reuses connections
2. **Timeout Management**: 60-second timeout prevents hanging requests
3. **Async I/O**: Non-blocking operations improve throughput
4. **Health Checks**: Docker health checks ensure service readiness

### Bottlenecks

1. **JSON Serialization**: Text-based format is slower than binary
2. **HTTP Overhead**: More overhead than gRPC
3. **Network Latency**: Between-service communication adds latency
4. **Processing Time**: Text cleaning and analysis take time

## Testing

### Unit Testing (Local)

```bash
# Test individual service
cd service1-input
python app.py

# In another terminal
curl -X POST http://localhost:8061/process \
  -H "Content-Type: application/json" \
  -d '{"text": "test text", "request_id": "123"}'
```

### Integration Testing (Docker)

```bash
make build
make up
make test
```

### Performance Testing

```bash
make benchmark
```

## Deployment

### Local Development

```bash
# Terminal 1: Service 1
cd service1-input && python app.py

# Terminal 2: Service 2
cd service2-preprocess && python app.py

# Terminal 3: Service 3
cd service3-analysis && python app.py

# Terminal 4: Service 4
cd service4-report && python app.py

# Terminal 5: Client
cd client && python app.py
```

### Docker Deployment

```bash
make build
make up
make test
```

## Troubleshooting

### Services Won't Start

```bash
# Check logs
make logs

# Check specific service
make logs-service1

# Rebuild from scratch
make clean
make build
make up
```

### Connection Refused

- Wait 10-15 seconds for services to start
- Check service logs for errors
- Verify Docker network: `docker network ls`

### High Latency

- Check system resources (CPU, memory)
- Monitor service logs for processing delays
- Verify network connectivity

## Comparison with gRPC

| Aspect          | REST/HTTP  | gRPC             |
| --------------- | ---------- | ---------------- |
| Protocol        | HTTP/1.1   | HTTP/2           |
| Serialization   | JSON       | Protocol Buffers |
| Message Size    | Larger     | Smaller          |
| Latency         | Higher     | Lower            |
| Debugging       | Easy       | Harder           |
| Learning Curve  | Lower      | Higher           |
| Code Generation | Not needed | Required         |

## Future Enhancements

1. **Horizontal Scaling**: Multiple instances per service
2. **Load Balancing**: Distribute requests across instances
3. **Caching**: Cache intermediate results
4. **Message Queues**: Decouple services with async queues
5. **Monitoring**: Add metrics and tracing
6. **API Gateway**: Single entry point for all services

## References

- FastAPI Documentation: https://fastapi.tiangolo.com/
- httpx Documentation: https://www.python-httpx.org/
- Docker Documentation: https://docs.docker.com/
- Docker Compose Documentation: https://docs.docker.com/compose/
