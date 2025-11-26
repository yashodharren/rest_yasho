# REST/HTTP Parallel Pipeline with Load Balancers

## Overview

This is a **parallel, horizontally-scalable** version of the REST/HTTP pipeline that uses load balancers to distribute requests across multiple instances of each service.

## Architecture

### Sequential vs Parallel

**Sequential (Original)**:

```
Client → Service1 → Service2 → Service3 → Service4 → Response
(1 instance each)
```

**Parallel (New)**:

```
                    ┌─→ Service1a ─┐
                    ├─→ Service1b ─┤
Client → LB1 ─────→ ├─→ Service1c ─┤ → LB2 → ... → Response
                    └─→ Service1d ─┘
(4 instances per service, 1 load balancer per service)
```

## Load Balancer Design

### How Load Balancers Work

Each load balancer:

1. **Receives requests** from the previous service
2. **Routes to instances** using round-robin algorithm
3. **Handles failures** by trying next instance
4. **Tracks statistics** for monitoring
5. **Returns response** to caller

### Round-Robin Algorithm

```python
# Simple round-robin distribution
current_index = 0
instance = instances[current_index]
current_index = (current_index + 1) % len(instances)
```

Each request goes to the next instance in sequence, cycling through all instances.

### Failure Handling

If an instance fails:

1. Load balancer catches the error
2. Tries the next instance
3. Continues until success or all instances fail
4. Returns error if all instances fail

## Architecture Overview

### Services & Ports

**Load Balancers** (Entry points):

- Service 1 LB: Port 8061
- Service 2 LB: Port 8062
- Service 3 LB: Port 8063
- Service 4 LB: Port 8064

**Service 1 Instances**:

- service1a: Port 8051
- service1b: Port 8055
- service1c: Port 8057
- service1d: Port 8059

**Service 2 Instances**:

- service2a: Port 8052
- service2b: Port 8056
- service2c: Port 8058
- service2d: Port 8060

**Service 3 Instances**:

- service3a: Port 8053
- service3b: Port 8065
- service3c: Port 8067
- service3d: Port 8069

**Service 4 Instances**:

- service4a: Port 8054
- service4b: Port 8066
- service4c: Port 8068
- service4d: Port 8070

### Total Containers

- 4 services × 4 instances = 16 service instances
- 4 load balancers = 4 containers
- 1 client = 1 container
- **Total: 21 containers**

## Quick Start

### Build Parallel Setup

```bash
make build-parallel
```

### Start Parallel Services

```bash
make up-parallel
```

You should see:

```
✅ PARALLEL SERVICES ARE RUNNING!

🌐 LOAD BALANCERS:
  Service 1: localhost:8061
  Service 2: localhost:8062
  Service 3: localhost:8063
  Service 4: localhost:8064

🔧 SERVICE INSTANCES:
  Service1: 8051, 8055, 8057, 8059
  Service2: 8052, 8056, 8058, 8060
  Service3: 8053, 8065, 8067, 8069
  Service4: 8054, 8066, 8068, 8070
```

### Run Test

```bash
make test-parallel
```

### Run Benchmark

```bash
make benchmark-parallel
```

### View Logs

```bash
make logs-parallel
```

### Stop Services

```bash
make down-parallel
```

## Commands Reference

### Parallel Operations

```bash
make build-parallel         # Build all parallel services
make up-parallel            # Start all parallel services
make test-parallel          # Run pipeline test
make benchmark-parallel     # Run performance benchmark
make logs-parallel          # View all logs
make down-parallel          # Stop all services
make clean-parallel         # Clean up
make restart-parallel       # Restart services
```

## How Requests Flow Through Parallel System

### Example Request Path

1. **Client sends request** to Service 1 Load Balancer (Port 8061)

   ```
   POST http://service1-loadbalancer:8061/process
   ```

2. **Service 1 LB routes** to Service 1 instance (round-robin)

   ```
   → service1a:8051 (or b, c, d)
   ```

3. **Service 1 instance** processes and calls Service 2 LB

   ```
   POST http://service2-loadbalancer:8062/preprocess
   ```

4. **Service 2 LB routes** to Service 2 instance

   ```
   → service2a:8052 (or b, c, d)
   ```

5. **Service 2 instance** processes and calls Service 3 LB

   ```
   POST http://service3-loadbalancer:8063/analyze
   ```

6. **Service 3 LB routes** to Service 3 instance

   ```
   → service3a:8053 (or b, c, d)
   ```

7. **Service 3 instance** processes and calls Service 4 LB

   ```
   POST http://service4-loadbalancer:8064/report
   ```

8. **Service 4 LB routes** to Service 4 instance

   ```
   → service4a:8054 (or b, c, d)
   ```

9. **Service 4 instance** generates report and returns

10. **Response flows back** through the chain

## Load Balancer Implementation

### Load Balancer Class

```python
class LoadBalancer:
    def __init__(self, instances: List[str]):
        self.instances = instances
        self.current_index = 0
        self.instance_stats = {...}

    async def route_request(self, request_data: dict) -> dict:
        # Round-robin routing
        instance = self.instances[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.instances)

        # Try to send request
        try:
            response = await client.post(f"http://{instance}/endpoint", ...)
            return response.json()
        except:
            # Try next instance on failure
            ...
```

### Statistics Tracking

Each load balancer tracks:

- Number of requests per instance
- Number of errors per instance
- Success/failure rates

Access via:

```bash
curl http://localhost:8061/stats
```

## Performance Benefits

### Horizontal Scaling

- **4 instances per service** = 4x processing capacity
- Requests distributed across instances
- Better resource utilization

### Load Distribution

- **Round-robin** ensures even distribution
- No instance gets overloaded
- Improved throughput

### Fault Tolerance

- **Instance failure handling** - requests rerouted
- **Automatic failover** to healthy instances
- **Graceful degradation** - system continues with fewer instances

## Comparison: Sequential vs Parallel

### Sequential Setup

```
make build      # Build 4 services
make up         # Start 4 containers
make test       # Test
```

### Parallel Setup

```
make build-parallel      # Build 4 services + 4 LBs + 4×4 instances
make up-parallel         # Start 21 containers
make test-parallel       # Test with load balancing
```

## Monitoring Load Balancers

### Check Load Balancer Stats

```bash
# Service 1 LB stats
curl http://localhost:8061/stats

# Service 2 LB stats
curl http://localhost:8062/stats

# Service 3 LB stats
curl http://localhost:8063/stats

# Service 4 LB stats
curl http://localhost:8064/stats
```

### Example Output

```json
{
  "instances": [
    "service1a:8051",
    "service1b:8055",
    "service1c:8057",
    "service1d:8059"
  ],
  "stats": {
    "service1a:8051": { "requests": 5, "errors": 0 },
    "service1b:8055": { "requests": 5, "errors": 0 },
    "service1c:8057": { "requests": 5, "errors": 0 },
    "service1d:8059": { "requests": 5, "errors": 0 }
  }
}
```

## Troubleshooting

### Services Won't Start

```bash
# Check logs
make logs-parallel

# Check specific service
docker logs rest-service1a

# Rebuild
make clean-parallel
make build-parallel
make up-parallel
```

### High Latency

- Check if all instances are running: `docker ps`
- Monitor load balancer stats
- Check system resources

### Load Imbalance

- Verify round-robin is working: `curl http://localhost:8061/stats`
- Check for instance failures
- Review load balancer logs

## Docker Compose Configuration

### Service Definition Example

```yaml
service1a:
  build:
    context: .
    dockerfile: service1-input/Dockerfile
  ports:
    - "8051:8051"
  environment:
    - SERVICE_PORT=8051
    - INSTANCE_ID=a
    - SERVICE2_URL=http://service2-loadbalancer:8062
  networks:
    - rest-network
```

### Load Balancer Definition Example

```yaml
service1-loadbalancer:
  build:
    context: .
    dockerfile: service1-loadbalancer/Dockerfile
  ports:
    - "8061:8061"
  environment:
    - SERVICE_PORT=8061
  networks:
    - rest-network
  depends_on:
    - service1a
    - service1b
    - service1c
    - service1d
```

## Performance Expectations

### Throughput Improvement

- **Sequential**: 5-20 requests/second
- **Parallel**: 15-60+ requests/second (3-4x improvement)

### Latency

- **Sequential**: 50-200ms per request
- **Parallel**: 50-200ms per request (same, but more concurrent)

### Resource Usage

- **Sequential**: 4 containers
- **Parallel**: 21 containers (more memory/CPU needed)

## Advanced Topics

### Adding More Instances

To add a 5th instance to Service 1:

1. Add `service1e` to `docker-compose-parallel.yml`
2. Update `SERVICE1_INSTANCES` in `service1-loadbalancer/app.py`
3. Rebuild and restart

### Custom Load Balancing Algorithm

Replace round-robin with:

- **Least connections**: Route to instance with fewest active requests
- **Weighted**: Give more requests to powerful instances
- **Random**: Randomly select instance

### Monitoring & Metrics

Add Prometheus metrics:

- Request count per instance
- Error rate per instance
- Response time per instance
- Load balancer health

## Comparison with gRPC Parallel

The REST parallel implementation follows the same pattern as the gRPC parallel version:

- 4 instances per service
- 1 load balancer per service
- Round-robin distribution
- Failure handling

Key differences:

- REST uses HTTP/JSON instead of gRPC/protobuf
- REST load balancers are simpler (no protobuf code generation)
- REST easier to debug (human-readable JSON)

## Summary

The parallel setup provides:

- ✅ **Horizontal scaling** with multiple instances
- ✅ **Load balancing** across instances
- ✅ **Fault tolerance** with automatic failover
- ✅ **Better throughput** with concurrent processing
- ✅ **Easy monitoring** with statistics endpoints
- ✅ **Simple round-robin** distribution algorithm

**Ready for production-scale testing!** 🚀
