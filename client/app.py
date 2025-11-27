import os
import asyncio
import httpx
import uuid
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SERVICE1_URL = os.getenv("SERVICE1_URL", "http://service1:8061")
DATASETS_DIR = "/app/datasets" if os.path.exists("/app/datasets") else os.path.join(os.path.dirname(__file__), '..', 'datasets')

async def run_pipeline(text: str, service1_url: str = SERVICE1_URL):
    """
    Run the complete pipeline by calling Service 1
    """
    logger.info("=" * 70)
    logger.info("CLIENT: Starting Pipeline Request")
    logger.info("=" * 70)
    
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"CLIENT: Request ID: {request_id}")
    logger.info(f"CLIENT: Text length: {len(text)} characters")
    logger.info(f"CLIENT: Text preview: {text[:100]}...")
    logger.info(f"CLIENT: Connecting to Service 1 at {service1_url}")
    
    try:
        async with httpx.AsyncClient() as client:
            request_data = {
                "text": text,
                "request_id": request_id
            }
            
            logger.info("CLIENT: Sending request to Service 1...")
            response = await client.post(
                f"{service1_url}/process",
                json=request_data,
                timeout=60.0
            )
            response.raise_for_status()
            
            result = response.json()
            
            logger.info("\nCLIENT: ===== Pipeline Complete =====")
            logger.info(f"CLIENT: Status: {result.get('status')}")
            logger.info(f"CLIENT: Message: {result.get('message')}")
            logger.info(f"CLIENT: Word Count: {result.get('word_count')}")
            
            if result.get('report'):
                logger.info("\nCLIENT: Report:")
                logger.info(result.get('report'))
            
            logger.info("=" * 70)
            
            return result
    
    except httpx.HTTPError as e:
        logger.error(f"\nCLIENT: ERROR - HTTP Error")
        logger.error(f"CLIENT: Details: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"\nCLIENT: ERROR - {str(e)}")
        raise

def load_dataset(filename: str) -> str:
    """Load text from a dataset file"""
    file_path = os.path.join(DATASETS_DIR, filename)
    
    if not os.path.exists(file_path):
        logger.error(f"Dataset file not found: {file_path}")
        logger.info(f"Available datasets in {DATASETS_DIR}:")
        if os.path.exists(DATASETS_DIR):
            for f in os.listdir(DATASETS_DIR):
                try:
                    file_size = os.path.getsize(os.path.join(DATASETS_DIR, f))
                    logger.info(f"  - {f} ({file_size:,} bytes)")
                except OSError:
                    pass # Ignore if it's not a file
        raise FileNotFoundError(f"Dataset file not found: {filename}")
    
    logger.info(f"Loading dataset: {filename}")
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    file_size = os.path.getsize(file_path)
    logger.info(f"Dataset loaded: {len(text)} characters ({file_size:,} bytes)")
    return text

async def main():
    """Main client function"""
    # Default to 'big.txt' if no command-line argument is given
    dataset_file = sys.argv[1] if len(sys.argv) > 1 else 'big.txt'
    
    try:
        test_text = load_dataset(dataset_file)
    except FileNotFoundError:
        # Error is already logged by load_dataset, so we can exit gracefully.
        return

    logger.info("CLIENT: Waiting for services to be ready...")
    # Increased sleep time for larger models or slower systems
    await asyncio.sleep(5)
    
    try:
        result = await run_pipeline(test_text)
        logger.info("\nCLIENT: Pipeline execution successful!")
        return result
    except Exception as e:
        logger.error(f"\nCLIENT: Pipeline execution failed: {str(e)}")
        # Exit with a non-zero status code to indicate failure, useful for scripting
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
