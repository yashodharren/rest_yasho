import asyncio
import httpx
import sys
import time
import uuid
import os
import glob

sys.path.insert(0, '/app')

class ParallelPipelineClient:
    def __init__(self):
        self.service1_lb = 'http://service1-loadbalancer:8061'
        self.num_parallel_pipelines = 4

    def split_text_into_chunks(self, text, num_chunks):
        text_length = len(text)
        if text_length > 5 * 1024 * 1024:
            print(f"📊 Large file detected: {text_length:,} characters, using optimized chunking...")
            chunk_size = text_length // num_chunks
            chunks = []
            for i in range(num_chunks):
                start = i * chunk_size
                end = text_length if i == num_chunks - 1 else (i + 1) * chunk_size
                chunks.append(text[start:end])
        else:
            words = text.split()
            chunk_size = len(words) // num_chunks
            chunks = []
            for i in range(num_chunks):
                start = i * chunk_size
                end = len(words) if i == num_chunks - 1 else (i + 1) * chunk_size
                chunks.append(' '.join(words[start:end]))
        
        print(f"Split {text_length:,} characters into {num_chunks} chunks:")
        for i, chunk in enumerate(chunks):
            word_count = len(chunk.split())
            print(f"  Chunk {i+1}: {word_count:,} words, {len(chunk):,} chars")
        return chunks

    async def process_single_chunk(self, client, chunk_text, chunk_id, request_id_base):
        request_id = f"{request_id_base}_chunk{chunk_id}"
        print(f"\n[Pipeline {chunk_id}] Starting processing...")
        print(f"[Pipeline {chunk_id}] Chunk size: {len(chunk_text):,} chars, {len(chunk_text.split()):,} words")
        start_time = time.time()

        try:
            response = await client.post(
                f"{self.service1_lb}/process",
                json={"text": chunk_text, "request_id": request_id},
                timeout=300.0
            )
            response.raise_for_status()
            result = response.json()
            elapsed_time = time.time() - start_time
            print(f"[Pipeline {chunk_id}] ✓ Completed in {elapsed_time:.3f}s - {result.get('word_count', 0):,} words")
            return {
                'chunk_id': chunk_id,
                'success': True,
                'word_count': result.get('word_count', 0),
                'processing_time': elapsed_time,
                'status': result.get('status'),
                'message': result.get('message')
            }
        except (httpx.HTTPError, Exception) as e:
            elapsed_time = time.time() - start_time
            error_msg = f"HTTP Error: {str(e)}"
            print(f"[Pipeline {chunk_id}] ✗ Failed in {elapsed_time:.3f}s: {error_msg}")
            return {
                'chunk_id': chunk_id,
                'success': False,
                'error': error_msg,
                'processing_time': elapsed_time
            }

    async def process_parallel(self, text, num_parallel=None):
        num_parallel = num_parallel or self.num_parallel_pipelines
        print("\n" + "="*80)
        print("🚀 PARALLEL PIPELINE PROCESSING")
        print("="*80)
        print(f"Total text length: {len(text):,} characters")
        print(f"Number of parallel pipelines: {num_parallel}")
        print(f"Service instances: 4x each service type")
        print(f"Timeout: 300 seconds")

        chunks = self.split_text_into_chunks(text, num_parallel)
        request_id_base = str(uuid.uuid4())[:8]
        print(f"\nStarting {num_parallel} parallel pipelines...")
        overall_start = time.time()

        async with httpx.AsyncClient() as client:
            tasks = [self.process_single_chunk(client, chunk, i, request_id_base) for i, chunk in enumerate(chunks)]
            results = await asyncio.gather(*tasks)

        overall_time = time.time() - overall_start
        return self.aggregate_results(results, overall_time)

    def aggregate_results(self, results, total_time):
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        total_words = sum(r['word_count'] for r in successful)
        avg_time = sum(r['processing_time'] for r in results) / len(results) if results else 0

        print("\n" + "="*80)
        print("📊 PARALLEL PROCESSING RESULTS")
        print("="*80)
        print(f"Total processing time: {total_time:.3f}s")
        print(f"Successful pipelines: {len(successful)}/{len(results)}")
        print(f"Failed pipelines: {len(failed)}/{len(results)}")
        print(f"Total words processed: {total_words:,}")
        print(f"Average pipeline time: {avg_time:.3f}s")

        speedup = (avg_time * len(results)) / total_time if total_time > 0 and len(successful) > 1 else 0
        if speedup:
            print(f"Parallel speedup: {speedup:.2f}x")

        print("\nPipeline Details:")
        for result in sorted(results, key=lambda x: x['chunk_id']):
            status = "✓" if result['success'] else "✗"
            words = f"{result.get('word_count', 0):,} words" if result['success'] else "N/A"
            print(f"  Pipeline {result['chunk_id']}: {status} {result['processing_time']:.3f}s, {words}")
        
        if failed:
            print("\nFailures:")
            for fail in failed:
                print(f"  Pipeline {fail['chunk_id']}: {fail['error']}")
        return {
            'total_time': total_time,
            'successful_count': len(successful),
            'failed_count': len(failed),
            'total_words': total_words,
            'speedup': speedup
        }

def read_text_files(datasets_path='/app/datasets'):
    if not os.path.exists(datasets_path):
        print(f"WARNING: Datasets directory '{datasets_path}' not found!")
        return []
    
    txt_files = glob.glob(os.path.join(datasets_path, '*.txt'))
    if not txt_files:
        print(f"WARNING: No .txt files found in '{datasets_path}'")
        return []

    print(f"Found {len(txt_files)} .txt file(s):")
    text_files = []
    for file_path in txt_files:
        try:
            file_size = os.path.getsize(file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            if content:
                word_count = len(content.split())
                print(f"  - {os.path.basename(file_path)} ({file_size:,} bytes, {len(content):,} chars, {word_count:,} words)")
                text_files.append({'filename': os.path.basename(file_path), 'content': content, 'file_size': file_size})
            else:
                print(f"  - {os.path.basename(file_path)} (EMPTY - skipping)")
        except Exception as e:
            print(f"  - ERROR reading {os.path.basename(file_path)}: {str(e)}")
    return text_files

async def main():
    client = ParallelPipelineClient()
    print("\n" + "="*80)
    print("🚀 MASSIVE PARALLEL TEXT PROCESSING PIPELINE (REST)")
    print("="*80)
    print("This demonstrates:")
    print("• 4x instances of each service type")
    print("• Parallel processing of text chunks")
    print("• Load balancing across service instances")
    print("• Horizontal scaling performance")
    print("• Large file support")
    print("• Optimized chunking for different file sizes")
    print("="*80)

    print("\nScanning for text files...")
    text_files = read_text_files('/app/datasets')
    if not text_files:
        print("No text files found!")
        return

    for file_info in text_files:
        print(f"\n\n{'#'*80}")
        print(f"📄 PROCESSING: {file_info['filename']}")
        print(f"📊 FILE SIZE: {file_info['file_size']:,} bytes")
        print(f"{'#'*80}")

        for parallelism in [1, 2, 4]:
            print(f"\n{'='*60}")
            print(f"🧪 TESTING WITH {parallelism} PARALLEL PIPELINES")
            print(f"{'='*60}")
            await client.process_parallel(file_info['content'], parallelism)
            if parallelism < 4:
                print("\nWaiting 3 seconds before next test...")
                await asyncio.sleep(3)

if __name__ == '__main__':
    asyncio.run(main())
