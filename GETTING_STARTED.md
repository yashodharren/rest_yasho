# Getting Started with REST/HTTP Pipeline

## Quick Start (5 minutes)

### Prerequisites

- Docker & Docker Compose installed
- Git (optional)

### Step 1: Build Services

```bash
cd rest_yasho
make build
```

### Step 2: Start Services

```bash
make up
```

You should see:

```
✅ REST SERVICES ARE RUNNING!

🌐 SERVICE ENDPOINTS:
  Service 1 (Input):       http://localhost:8061
  Service 2 (Preprocess):  http://localhost:8062
  Service 3 (Analysis):    http://localhost:8063
  Service 4 (Report):      http://localhost:8064
```

### Step 3: Run Test

```bash
make test
```

You should see output like:

```
CLIENT: Starting Pipeline Request
CLIENT: Request ID: abc12345
CLIENT: Text length: 1234 characters
CLIENT: Forwarding to Service 2...
...
CLIENT: Pipeline Complete
CLIENT: Word Count: 42
```

### Step 4: Stop Services

```bash
make down
```

## Detailed Commands

### Building

```bash
make build              # Build all Docker images
make rebuild            # Force rebuild (no cache)
```

### Running

```bash
make up                 # Start all services
make down               # Stop all services
make restart            # Restart services
make status             # Check service status
```

### Testing

```bash
make test               # Run single test
make benchmark          # Run 20 iterations (performance test)
make benchmark NUM=50   # Run 50 iterations
```

### Debugging

```bash
make logs               # View all service logs (live)
make logs-service1      # View Service 1 logs only
make logs-service2      # View Service 2 logs only
make logs-service3      # View Service 3 logs only
make logs-service4      # View Service 4 logs only
```

### Maintenance

```bash
make clean              # Stop and clean up
make help               # Show all commands
```

## Understanding the Pipeline

### What Happens When You Run `make test`

1. **Client sends request to Service 1**

   - Text: "FastAPI is a modern..."
   - Request ID: "abc12345"

2. **Service 1 processes**

   - Receives text
   - Forwards to Service 2
   - Waits for response

3. **Service 2 preprocesses**

   - Cleans text (lowercase, remove punctuation)
   - Forwards to Service 3

4. **Service 3 analyzes**

   - Tokenizes text
   - Counts word frequencies
   - Identifies top words
   - Forwards to Service 4

5. **Service 4 generates report**

   - Creates formatted report
   - Returns to Service 3

6. **Response flows back**

   - Service 3 → Service 2 → Service 1 → Client

7. **Client displays results**
   - Word count
   - Top words
   - Full report

## Local Development (Without Docker)

### Terminal 1: Service 1

```bash
cd service1-input
pip install -r requirements.txt
python app.py
```

### Terminal 2: Service 2

```bash
cd service2-preprocess
pip install -r requirements.txt
python app.py
```

### Terminal 3: Service 3

```bash
cd service3-analysis
pip install -r requirements.txt
python app.py
```

### Terminal 4: Service 4

```bash
cd service4-report
pip install -r requirements.txt
python app.py
```

### Terminal 5: Client

```bash
cd client
pip install -r requirements.txt
python app.py
```

## Testing Individual Services

### Using curl

**Test Service 1**:

```bash
curl -X POST http://localhost:8061/process \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello world",
    "request_id": "test-123"
  }'
```

**Test Service 2**:

```bash
curl -X POST http://localhost:8062/preprocess \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello World!",
    "request_id": "test-123"
  }'
```

**Test Health Check**:

```bash
curl http://localhost:8061/health
curl http://localhost:8062/health
curl http://localhost:8063/health
curl http://localhost:8064/health
```

### Using Python

```python
import httpx
import asyncio

async def test():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8061/process",
            json={
                "text": "Hello world",
                "request_id": "test-123"
            }
        )
        print(response.json())

asyncio.run(test())
```

## Performance Benchmarking

### Run Benchmark

```bash
make benchmark
```

### Output Example

```
======================================================================
REST/HTTP DISTRIBUTED PIPELINE BENCHMARK
======================================================================
Test text length: 2500 characters
Number of iterations: 20
Services: 4 (Input → Preprocessing → Analysis → Report)
Protocol: REST/HTTP (FastAPI)
======================================================================

Running 20 benchmark iterations...
  Iteration 1/20... ✓ 0.125s (words: 42)
  Iteration 2/20... ✓ 0.118s (words: 42)
  ...

======================================================================
BENCHMARK RESULTS (REST/HTTP)
======================================================================
Total iterations: 20
Successful: 20
Failed: 0

Timing Statistics:
  Mean:     0.122s
  Median:   0.120s
  Min:      0.115s
  Max:      0.135s
  Std Dev:  0.006s

Throughput: 163.93 requests/second
Average latency: 122.0ms
======================================================================
```

## Understanding the Output

### Timing Statistics

- **Mean**: Average request time
- **Median**: Middle value (50th percentile)
- **Min/Max**: Best/worst case times
- **Std Dev**: Consistency (lower is better)

### Performance Metrics

- **Throughput**: Requests per second
- **Latency**: Average time per request (in milliseconds)
- **Success Rate**: Percentage of successful requests

## Troubleshooting

### Issue: "Connection refused"

**Solution**:

```bash
# Wait for services to start
sleep 15

# Check if services are running
make status

# View logs
make logs
```

### Issue: "Port already in use"

**Solution**:

```bash
# Stop existing services
make down

# Wait a moment
sleep 5

# Start again
make up
```

### Issue: "Service X is unhealthy"

**Solution**:

```bash
# View logs for that service
make logs-service1  # Replace 1 with service number

# Rebuild and restart
make clean
make build
make up
```

### Issue: High latency or timeouts

**Solution**:

```bash
# Check system resources
docker stats

# Check service logs for errors
make logs

# Restart services
make restart
```

## Comparing with gRPC

The `grpc_arman` folder contains the gRPC implementation. To compare:

```bash
# Build and test gRPC
cd ../grpc_arman
make build
make up
make benchmark

# Build and test REST
cd ../rest_yasho
make build
make up
make benchmark
```

**Key Differences**:

- gRPC uses binary Protocol Buffers (faster)
- REST uses JSON (easier to debug)
- gRPC uses HTTP/2 (more efficient)
- REST uses HTTP/1.1 (more compatible)

## Project Documentation

- **README.md** - Quick start and overview
- **ARCHITECTURE.md** - Detailed system design
- **PROJECT_SUMMARY.md** - Project overview
- **IMPLEMENTATION_GUIDE.md** - Implementation details
- **GETTING_STARTED.md** - This file

## Next Steps

1. **Understand the Architecture**

   - Read ARCHITECTURE.md
   - Study the service implementations

2. **Modify Services**

   - Add new endpoints
   - Change text processing logic
   - Add new services

3. **Performance Optimization**

   - Add caching
   - Implement connection pooling
   - Add load balancing

4. **Production Deployment**
   - Add monitoring
   - Implement logging aggregation
   - Set up CI/CD pipeline

## Common Modifications

### Add a New Service

1. Create new directory: `service5-custom/`
2. Create `app.py` with FastAPI endpoints
3. Create `requirements.txt` with dependencies
4. Create `Dockerfile`
5. Update `docker-compose.yml`
6. Update service chain in previous service

### Change Text Processing

Edit `service2-preprocess/app.py`:

```python
def clean_text(text: str) -> str:
    # Add your custom processing here
    text = text.lower()
    # Add more logic...
    return text
```

### Add New Analysis

Edit `service3-analysis/app.py`:

```python
def analyze_text(text: str) -> tuple:
    words = text.split()
    # Add your custom analysis here
    # Return results
    return word_count, top_words, word_freq
```

## Learning Resources

### FastAPI

- Official Docs: https://fastapi.tiangolo.com/
- Tutorial: https://fastapi.tiangolo.com/tutorial/

### Docker

- Official Docs: https://docs.docker.com/
- Tutorial: https://docs.docker.com/get-started/

### Async Python

- asyncio Docs: https://docs.python.org/3/library/asyncio.html
- httpx Docs: https://www.python-httpx.org/

## Support

For issues:

1. Check service logs: `make logs`
2. Review ARCHITECTURE.md
3. Check individual service implementations
4. Verify Docker is running: `docker ps`

## Summary

You now have a complete REST/HTTP distributed pipeline system with:

- ✅ 4 microservices
- ✅ FastAPI endpoints
- ✅ Docker containerization
- ✅ Performance benchmarking
- ✅ Comprehensive documentation

Happy coding! 🚀
