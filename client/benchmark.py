import os
import asyncio
import httpx
import uuid
import time
import statistics
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SERVICE1_URL = os.getenv("SERVICE1_URL", "http://service1:8061")

async def run_single_test(session: httpx.AsyncClient, text: str, service1_url: str = SERVICE1_URL):
    """Run a single pipeline test and return the execution time."""
    request_id = str(uuid.uuid4())[:8]
    start_time = time.time()
    
    try:
        request_data = {"text": text, "request_id": request_id}
        response = await session.post(f"{service1_url}/process", json=request_data, timeout=60.0)
        response.raise_for_status()
        response_data = response.json()
        
        elapsed_time = time.time() - start_time
        return elapsed_time, True, response_data.get('word_count', 0)
    
    except Exception as e:
        elapsed_time = time.time() - start_time
        logger.error(f"\nError during test: {str(e)}")
        return elapsed_time, False, 0

async def run_benchmark(num_iterations=10):
    """Run benchmark with multiple iterations."""
    
    test_text = ("""
    FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
    The key features are: Fast, Fast to code, Fewer bugs, Intuitive, Easy, Short, Robust, Standards-based.
    This benchmark will compare its performance in a distributed pipeline against a gRPC implementation.
    REST/HTTP with JSON is often more verbose but easier to debug than binary protocols.
    """ * 5)
    
    logger.info("\n" + "=" * 70)
    logger.info("REST/HTTP DISTRIBUTED PIPELINE BENCHMARK")
    logger.info("=" * 70)
    logger.info(f"Test text length: {len(test_text)} characters")
    logger.info(f"Number of iterations: {num_iterations}")
    logger.info(f"Services: 4 (Input → Preprocessing → Analysis → Report)")
    logger.info(f"Protocol: REST/HTTP (FastAPI)")
    logger.info("=" * 70)
    
    async with httpx.AsyncClient() as session:
        # Warm-up run
        logger.info("\nPerforming warm-up run...")
        await run_single_test(session, test_text)
        await asyncio.sleep(1)
        
        # Benchmark runs
        logger.info(f"\nRunning {num_iterations} benchmark iterations...")
        times = []
        successes = 0
        
        for i in range(num_iterations):
            logger.info(f"  Iteration {i+1}/{num_iterations}...", end=' ')
            elapsed, success, word_count = await run_single_test(session, test_text)
            times.append(elapsed)
            
            if success:
                successes += 1
                logger.info(f"✓ {elapsed:.3f}s (words: {word_count})")
            else:
                logger.info(f"✗ {elapsed:.3f}s (failed)")
            
            if i < num_iterations - 1:
                await asyncio.sleep(0.5)
    
    # Calculate statistics
    logger.info("\n" + "=" * 70)
    logger.info("BENCHMARK RESULTS (REST/HTTP)")
    logger.info("=" * 70)
    logger.info(f"Total iterations: {num_iterations}")
    logger.info(f"Successful: {successes}")
    logger.info(f"Failed: {num_iterations - successes}")
    
    if successes > 0:
        logger.info(f"\nTiming Statistics:")
        logger.info(f"  Mean:     {statistics.mean(times):.3f}s")
        logger.info(f"  Median:   {statistics.median(times):.3f}s")
        logger.info(f"  Min:      {min(times):.3f}s")
        logger.info(f"  Max:      {max(times):.3f}s")
        
        if len(times) > 1:
            logger.info(f"  Std Dev:  {statistics.stdev(times):.3f}s")
        
        # Calculate throughput
        total_time = sum(times)
        throughput = num_iterations / total_time
        logger.info(f"\nThroughput: {throughput:.2f} requests/second")
        logger.info(f"Average latency: {statistics.mean(times)*1000:.1f}ms")
    
    logger.info("=" * 70)
    return times

async def main():
    # Check if custom iteration count provided
    num_iterations = 10
    if len(sys.argv) > 1:
        try:
            num_iterations = int(sys.argv[1])
        except ValueError:
            logger.error("Usage: python benchmark.py [num_iterations]")
            sys.exit(1)
    
    # Wait for services to be ready
    logger.info("Waiting for services to be ready...")
    await asyncio.sleep(5)
    
    # Run benchmark
    await run_benchmark(num_iterations)

if __name__ == "__main__":
    asyncio.run(main())
