# Terminal code to run 1,2,4 pipeline and benchmark code
```bash
#Build the Docker Images
docker compose -f docker-compose-parallel.yml build parallel-client

#Start the Services
docker compose -f docker-compose-parallel.yml up parallel-client

#Run the Pipeline Test
docker compose -f docker-compose-parallel.yml run --rm parallel-client python parallel_client.py

#Run the Performance Benchmark 
docker compose -f docker-compose-parallel.yml run --rm parallel-client python benchmark.py

#Stop and Remove All Containers
docker compose -f docker-compose-parallel.yml down
```

# Result pipeline 1,2,4
```bash
================================================================================
🚀 MASSIVE PARALLEL TEXT PROCESSING PIPELINE (REST)
================================================================================
This demonstrates:
• 4x instances of each service type
• Parallel processing of text chunks
• Load balancing across service instances
• Horizontal scaling performance
• Large file support
• Optimized chunking for different file sizes
================================================================================

Scanning for text files...
Found 1 .txt file(s):
  - big.txt (33,085,621 bytes, 32,443,332 chars, 5,478,475 words)


################################################################################
📄 PROCESSING: big.txt
📊 FILE SIZE: 33,085,621 bytes
################################################################################

============================================================
🧪 TESTING WITH 1 PARALLEL PIPELINES
============================================================

================================================================================
🚀 PARALLEL PIPELINE PROCESSING
================================================================================
Total text length: 32,443,332 characters
Number of parallel pipelines: 1
Service instances: 4x each service type
Timeout: 300 seconds
📊 Large file detected: 32,443,332 characters, using optimized chunking...
Split 32,443,332 characters into 1 chunks:
  Chunk 1: 5,478,475 words, 32,443,332 chars

Starting 1 parallel pipelines...

[Pipeline 0] Starting processing...
[Pipeline 0] Chunk size: 32,443,332 chars, 5,478,475 words
[Pipeline 0] ✓ Completed in 6.649s - 5,474,510 words

================================================================================
📊 PARALLEL PROCESSING RESULTS
================================================================================
Total processing time: 7.439s
Successful pipelines: 1/1
Failed pipelines: 0/1
Total words processed: 5,474,510
Average pipeline time: 6.649s

Pipeline Details:
  Pipeline 0: ✓ 6.649s, 5,474,510 words

Waiting 3 seconds before next test...

============================================================
🧪 TESTING WITH 2 PARALLEL PIPELINES
============================================================

================================================================================
🚀 PARALLEL PIPELINE PROCESSING
================================================================================
Total text length: 32,443,332 characters
Number of parallel pipelines: 2
Service instances: 4x each service type
Timeout: 300 seconds
📊 Large file detected: 32,443,332 characters, using optimized chunking...
Split 32,443,332 characters into 2 chunks:
  Chunk 1: 2,726,653 words, 16,221,666 chars
  Chunk 2: 2,751,822 words, 16,221,666 chars

Starting 2 parallel pipelines...

[Pipeline 0] Starting processing...
[Pipeline 0] Chunk size: 16,221,666 chars, 2,726,653 words

[Pipeline 1] Starting processing...
[Pipeline 1] Chunk size: 16,221,666 chars, 2,751,822 words
[Pipeline 0] ✓ Completed in 3.183s - 2,724,298 words
[Pipeline 1] ✓ Completed in 3.187s - 2,750,212 words

================================================================================
📊 PARALLEL PROCESSING RESULTS
================================================================================
Total processing time: 3.724s
Successful pipelines: 2/2
Failed pipelines: 0/2
Total words processed: 5,474,510
Average pipeline time: 3.185s
Parallel speedup: 1.71x

Pipeline Details:
  Pipeline 0: ✓ 3.183s, 2,724,298 words
  Pipeline 1: ✓ 3.187s, 2,750,212 words

Waiting 3 seconds before next test...

============================================================
🧪 TESTING WITH 4 PARALLEL PIPELINES
============================================================

================================================================================
🚀 PARALLEL PIPELINE PROCESSING
================================================================================
Total text length: 32,443,332 characters
Number of parallel pipelines: 4
Service instances: 4x each service type
Timeout: 300 seconds
📊 Large file detected: 32,443,332 characters, using optimized chunking...
Split 32,443,332 characters into 4 chunks:
  Chunk 1: 1,371,258 words, 8,110,833 chars
  Chunk 2: 1,355,396 words, 8,110,833 chars
  Chunk 3: 1,381,039 words, 8,110,833 chars
  Chunk 4: 1,370,783 words, 8,110,833 chars

Starting 4 parallel pipelines...

[Pipeline 0] Starting processing...
[Pipeline 0] Chunk size: 8,110,833 chars, 1,371,258 words

[Pipeline 1] Starting processing...
[Pipeline 1] Chunk size: 8,110,833 chars, 1,355,396 words

[Pipeline 2] Starting processing...
[Pipeline 2] Chunk size: 8,110,833 chars, 1,381,039 words

[Pipeline 3] Starting processing...
[Pipeline 3] Chunk size: 8,110,833 chars, 1,370,783 words
[Pipeline 1] ✓ Completed in 1.862s - 1,354,162 words
[Pipeline 3] ✓ Completed in 1.909s - 1,369,968 words
[Pipeline 0] ✓ Completed in 2.495s - 1,370,137 words
[Pipeline 2] ✓ Completed in 2.203s - 1,380,244 words

================================================================================
📊 PARALLEL PROCESSING RESULTS
================================================================================
Total processing time: 2.635s
Successful pipelines: 4/4
Failed pipelines: 0/4
Total words processed: 5,474,511
Average pipeline time: 2.117s
Parallel speedup: 3.21x

Pipeline Details:
  Pipeline 0: ✓ 2.495s, 1,370,137 words
  Pipeline 1: ✓ 1.862s, 1,354,162 words
  Pipeline 2: ✓ 2.203s, 1,380,244 words
  Pipeline 3: ✓ 1.909s, 1,369,968 words
```

# Result benchmark

```bash

================================================================================
🚀 COMPREHENSIVE PIPELINE BENCHMARK
================================================================================
📁 Found 1 dataset file(s):
  - big.txt (32,443,332 chars, ~5,478,475 words)
📄 Using: big.txt
📊 File size: 32,443,332 characters
🔢 Testing pipelines: 1, 2, and 4 parallel pipelines
🔄 Runs per configuration: 3
================================================================================


############################################################
🧪 TESTING 1 PARALLEL PIPELINE(S)
############################################################

--- Run 1/3 ---
  Time: 5.376s
  Success: 1/1
  Words processed: 5,474,510
  Waiting 2 seconds...

--- Run 2/3 ---
  Time: 5.860s
  Success: 1/1
  Words processed: 5,474,510
  Waiting 2 seconds...
  Words processed: 5,474,510
  Waiting 2 seconds...
  Waiting 2 seconds...


--- Run 3/3 ---
  Time: 6.867s
  Time: 6.867s
  Success: 1/1
  Words processed: 5,474,510
  Success: 1/1
  Words processed: 5,474,510

  Words processed: 5,474,510




############################################################
🧪 TESTING 2 PARALLEL PIPELINE(S)
############################################################

--- Run 1/3 ---
  Time: 3.739s
  Success: 2/2
  Words processed: 5,474,510
  Waiting 2 seconds...

--- Run 2/3 ---
  Time: 4.529s
  Success: 2/2
  Words processed: 5,474,510
  Waiting 2 seconds...

--- Run 3/3 ---
  Time: 3.195s
  Success: 2/2
  Words processed: 5,474,510


############################################################
🧪 TESTING 4 PARALLEL PIPELINE(S)
############################################################

--- Run 1/3 ---
  Time: 2.413s
  Success: 4/4
  Words processed: 5,474,511
  Waiting 2 seconds...

--- Run 2/3 ---
  Time: 1.923s
  Success: 4/4
  Words processed: 5,474,511
  Waiting 2 seconds...

--- Run 3/3 ---
  Time: 2.056s
  Success: 4/4
  Words processed: 5,474,511

================================================================================
📊 COMPREHENSIVE BENCHMARK RESULTS
================================================================================
File: big.txt (32,443,332 chars)
Configuration: 3 runs per pipeline type
================================================================================

🏆 PERFORMANCE COMPARISON:
┌────────────┬────────────┬────────────┬────────────┬────────────┬────────────┐
│ Pipelines  │  Avg Time  │  Best Time │ Worst Time │ Success %  │ Speedup    │
├────────────┼────────────┼────────────┼────────────┼────────────┼────────────┤
│     1      │    6.034s  │    5.376s  │    6.867s  │   100.0%   │     1.00x  │
│     2      │    3.821s  │    3.195s  │    4.529s  │   100.0%   │     1.58x  │
│     4      │    2.131s  │    1.923s  │    2.413s  │   100.0%   │     2.83x  │
└────────────┴────────────┴────────────┴────────────┴────────────┴────────────┘

📈 DETAILED RESULTS:

  1 Pipeline(s):
    • Average time: 6.034s
    • Best time: 5.376s
    • Worst time: 6.867s
    • Success rate: 100.0%
    • Individual times: ['5.376s', '5.860s', '6.867s']

  2 Pipeline(s):
    • Average time: 3.821s
    • Best time: 3.195s
    • Worst time: 4.529s
    • Success rate: 100.0%
    • Individual times: ['3.739s', '4.529s', '3.195s']

  4 Pipeline(s):
    • Average time: 2.131s
    • Best time: 1.923s
    • Worst time: 2.413s
    • Success rate: 100.0%
    • Individual times: ['2.413s', '1.923s', '2.056s']

💡 PERFORMANCE ANALYSIS:
  • 2 pipelines vs 1: 1.58x faster
  • 4 pipelines vs 1: 2.83x faster
  • 4 pipelines vs 2: 1.79x faster
```