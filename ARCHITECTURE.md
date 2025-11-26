# REST/HTTP Pipeline Architecture

## System Architecture Diagram

```
┌──────────┐
│  Client  │
│ (Docker) │
└────┬─────┘
     │
     │ HTTP POST /process
     │ Port: 8061
     │
     ▼
┌─────────────────────────┐
│   Service 1             │
│   Text Input Service    │
│   (FastAPI)             │
└────────┬────────────────┘
         │
         │ HTTP POST /preprocess
         │ Port: 8062
         │
         ▼
┌─────────────────────────┐
│   Service 2             │
│   Preprocessing Service │
│   (FastAPI)             │
└────────┬────────────────┘
         │
         │ HTTP POST /analyze
         │ Port: 8063
         │
         ▼
┌─────────────────────────┐
│   Service 3             │
│   Analysis Service      │
│   (FastAPI)             │
└────────┬────────────────┘
         │
         │ HTTP POST /report
         │ Port: 8064
         │
         ▼
┌─────────────────────────┐
│   Service 4             │
│   Report Service        │
│   (FastAPI)             │
└─────────────────────────┘
```

## Data Flow

### 1. Client Request

- Input: Raw text string
- Request ID: Unique identifier for tracking
- Target: Service 1 (port 8061)
- Protocol: HTTP POST with JSON payload

### 2. Service 1 → Service 2

- Action: Forward text for preprocessing
- Data: Original text + request ID
- Protocol: HTTP POST /preprocess
- Endpoint: http://service2:8062/preprocess

### 3. Service 2 → Service 3

- Action: Forward cleaned text for analysis
- Data: Cleaned text + metadata
- Protocol: HTTP POST /analyze
- Endpoint: http://service3:8063/analyze

### 4. Service 3 → Service 4

- Action: Forward analysis results for reporting
- Data: Word frequencies, statistics
- Protocol: HTTP POST /report
- Endpoint: http://service4:8064/report

### 5. Response Chain

- Service 4 → Service 3 → Service 2 → Service 1 → Client
- Each service adds its processing results
- Final response includes complete pipeline results

## Network Architecture

```
┌─────────────────────────────────────────────────────┐
│          Docker Bridge Network: rest-network        │
│                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────┐ │
│  │Service 1 │  │Service 2 │  │Service 3 │  │S4  │ │
│  │:8061     │→ │:8062     │→ │:8063     │→ │:8064││
│  └────▲─────┘  └──────────┘  └──────────┘  └────┘ │
│       │                                             │
│  ┌────┴──────┐                                     │
│  │  Client   │                                     │
│  └───────────┘                                     │
│                                                     │
└─────────────────────────────────────────────────────┘
         │          │          │          │
         ▼          ▼          ▼          ▼
    localhost  localhost  localhost  localhost
      :8061     :8062     :8063     :8064
```

## Service Communication Pattern

**Sequential Delegation Pattern**

Each service:

1. Receives a request
2. Processes the data
3. Delegates to the next service (except Service 4)
4. Waits for response
5. Adds its own results
6. Returns combined response

This demonstrates:

- Service-to-service communication
- Request delegation
- Response aggregation
- Microservices architecture

## Technology Stack

- **Language**: Python 3.11
- **Web Framework**: FastAPI
- **HTTP Client**: httpx (async)
- **Serialization**: JSON
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Networking**: Docker Bridge Network

## Port Assignments

| Service   | Port | Purpose                | Environment Variable |
| --------- | ---- | ---------------------- | -------------------- |
| Service 1 | 8061 | Text input endpoint    | SERVICE1_URL         |
| Service 2 | 8062 | Preprocessing endpoint | SERVICE2_URL         |
| Service 3 | 8063 | Analysis endpoint      | SERVICE3_URL         |
| Service 4 | 8064 | Report endpoint        | SERVICE4_URL         |

All ports are:

- Exposed within Docker network
- Published to host machine
- Accessible for external testing

## Request/Response Format

### Service 1 Input

```json
{
  "text": "Your text here",
  "request_id": "unique-id-123"
}
```

### Service 1 Response

```json
{
  "status": "success",
  "message": "Pipeline completed",
  "word_count": 42,
  "report": "Analysis Report: ...",
  "top_words": [
    ["word", 5],
    ["another", 3]
  ]
}
```

### Inter-Service Communication

Each service passes data through HTTP POST requests with JSON payloads containing:

- Processed data from previous services
- Request ID for tracking
- Metadata about processing

## Async/Await Implementation

All services use:

- **FastAPI** with async endpoints
- **httpx.AsyncClient** for non-blocking HTTP calls
- **asyncio** for concurrent processing
- **uvicorn** as ASGI server

Benefits:

- Non-blocking I/O
- Better resource utilization
- Ability to handle multiple concurrent requests
- Improved throughput

## Error Handling

Each service implements:

- Try-catch blocks for network errors
- Timeout handling (60 seconds)
- Graceful error propagation
- Detailed error logging
- Health check endpoints

## Scalability Considerations

### Current Design

- 4 services in sequential pipeline
- One instance per service
- Synchronous communication (request-response)

### Possible Enhancements

1. **Horizontal Scaling**: Run multiple instances of each service
2. **Load Balancing**: Distribute requests across instances
3. **Async Processing**: Use message queues between services
4. **Caching**: Cache preprocessed/analyzed results
5. **Monitoring**: Add health checks and metrics collection

## Comparison with gRPC

| Aspect          | REST/HTTP             | gRPC                      |
| --------------- | --------------------- | ------------------------- |
| Protocol        | HTTP/1.1              | HTTP/2                    |
| Serialization   | JSON (text)           | Protocol Buffers (binary) |
| Message Size    | Larger (1-10KB)       | Smaller (100-500B)        |
| Latency         | Higher (50-200ms)     | Lower (5-50ms)            |
| Debugging       | Easy (human-readable) | Harder (binary format)    |
| Learning Curve  | Lower                 | Higher                    |
| Code Generation | Not needed            | Required                  |
| Browser Testing | Easy (curl/Postman)   | Difficult                 |

## Performance Characteristics

### Typical Metrics (REST/HTTP)

- **Single request latency**: 50-200ms
- **Throughput**: 5-20 requests/second
- **Message size**: 1-10KB per request
- **CPU usage**: Moderate
- **Memory usage**: Low

### Bottlenecks

- JSON serialization/deserialization
- HTTP overhead
- Network latency between services
- Processing time in each service
