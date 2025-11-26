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

--- Run 1/10 ---
  Time: 5.649s
  Success: 1/1
  Words processed: 5,474,510
  Waiting 2 seconds...

--- Run 2/10 ---
  Time: 5.161s
  Success: 1/1
  Words processed: 5,474,510
  Waiting 2 seconds...

--- Run 3/10 ---
  Time: 5.437s
  Success: 1/1
  Words processed: 5,474,510
  Waiting 2 seconds...

--- Run 4/10 ---
  Time: 5.543s
  Success: 1/1
  Words processed: 5,474,510
  Waiting 2 seconds...

--- Run 5/10 ---
  Time: 4.907s
  Success: 1/1
  Words processed: 5,474,510
  Waiting 2 seconds...

--- Run 6/10 ---
  Time: 5.240s
  Success: 1/1
  Words processed: 5,474,510
  Waiting 2 seconds...

--- Run 7/10 ---
  Time: 7.453s
  Success: 1/1
  Words processed: 5,474,510
  Waiting 2 seconds...

--- Run 8/10 ---
  Time: 4.640s
  Success: 1/1
  Words processed: 5,474,510
  Waiting 2 seconds...

--- Run 9/10 ---
  Words processed: 5,474,510
  Waiting 2 seconds...

--- Run 10/10 ---
  Time: 5.085s
  Success: 1/1
  Words processed: 5,474,510


############################################################
🧪 TESTING 2 PARALLEL PIPELINE(S)
############################################################

--- Run 1/10 ---
  Time: 2.916s
  Success: 2/2
  Words processed: 5,474,510
  Waiting 2 seconds...

--- Run 2/10 ---
  Time: 2.668s
  Success: 2/2
  Words processed: 5,474,510
  Waiting 2 seconds...

--- Run 3/10 ---
  Time: 2.730s
  Success: 2/2
  Words processed: 5,474,510
  Waiting 2 seconds...

--- Run 4/10 ---
  Time: 2.757s
  Success: 2/2
  Words processed: 5,474,510
  Waiting 2 seconds...

--- Run 5/10 ---
  Time: 2.362s
  Success: 2/2
  Words processed: 5,474,510
  Waiting 2 seconds...

--- Run 6/10 ---
  Time: 2.543s
  Success: 2/2
  Words processed: 5,474,510
  Waiting 2 seconds...

--- Run 7/10 ---
  Time: 2.791s
  Success: 2/2
  Words processed: 5,474,510
  Waiting 2 seconds...

--- Run 8/10 ---
  Time: 2.529s
  Success: 2/2
  Words processed: 5,474,510
  Waiting 2 seconds...

--- Run 9/10 ---
  Time: 2.526s
  Success: 2/2
  Words processed: 5,474,510
  Waiting 2 seconds...

--- Run 10/10 ---
  Time: 2.367s
  Success: 2/2
  Words processed: 5,474,510


############################################################
🧪 TESTING 4 PARALLEL PIPELINE(S)
############################################################

--- Run 1/10 ---
  Time: 1.739s
  Success: 4/4
  Words processed: 5,474,511
  Waiting 2 seconds...

--- Run 2/10 ---
  Time: 1.559s
  Success: 4/4
  Words processed: 5,474,511
  Waiting 2 seconds...

--- Run 3/10 ---
  Time: 1.637s
  Success: 4/4
  Words processed: 5,474,511
  Waiting 2 seconds...

--- Run 4/10 ---
  Time: 1.685s
  Success: 4/4
  Words processed: 5,474,511
  Waiting 2 seconds...

--- Run 5/10 ---
  Time: 1.573s
  Success: 4/4
  Words processed: 5,474,511
  Waiting 2 seconds...

--- Run 6/10 ---
  Time: 1.690s
  Success: 4/4
  Words processed: 5,474,511
  Waiting 2 seconds...

--- Run 7/10 ---
  Time: 1.736s
  Success: 4/4
  Words processed: 5,474,511
  Waiting 2 seconds...

--- Run 8/10 ---
  Time: 1.601s
  Success: 4/4
  Words processed: 5,474,511
  Waiting 2 seconds...

--- Run 9/10 ---
  Time: 1.629s
  Success: 4/4
  Words processed: 5,474,511
  Waiting 2 seconds...

--- Run 10/10 ---
  Time: 1.685s
  Success: 4/4
  Words processed: 5,474,511

================================================================================
📊 COMPREHENSIVE BENCHMARK RESULTS
================================================================================
File: big.txt (32,443,332 chars)
Configuration: 10 runs per pipeline type
================================================================================

🏆  REST PERFORMANCE COMPARISON:
┌────────────┬────────────┬────────────┬────────────┬────────────┬────────────┐
│ Pipelines  │  Avg Time  │  Best Time │ Worst Time │ Success %  │ Speedup    │
├────────────┼────────────┼────────────┼────────────┼────────────┼────────────┤
│     1      │    5.382s  │    4.640s  │    7.453s  │   100.0%   │     1.00x  │
│     2      │    2.619s  │    2.362s  │    2.916s  │   100.0%   │     2.05x  │
│     4      │    1.653s  │    1.559s  │    1.739s  │   100.0%   │     3.26x  │
└────────────┴────────────┴────────────┴────────────┴────────────┴────────────┘

📈 DETAILED RESULTS:

    • Worst time: 7.453s
    • Success rate: 100.0%
    • Individual times: ['5.649s', '5.161s', '5.437s', '5.543s', '4.907s', '5.240s', '7.453s', '4.640s', '4.702s', '5.085s']

  2 Pipeline(s):
    • Average time: 2.619s
    • Best time: 2.362s
    • Worst time: 2.916s
    • Success rate: 100.0%
    • Individual times: ['2.916s', '2.668s', '2.730s', '2.757s', '2.362s', '2.543s', '2.791s', '2.529s', '2.526s', '2.367s']

  4 Pipeline(s):
    • Average time: 1.653s
    • Best time: 1.559s
    • Worst time: 1.739s
    • Success rate: 100.0%
    • Individual times: ['1.739s', '1.559s', '1.637s', '1.685s', '1.573s', '1.690s', '1.736s', '1.601s', '1.629s', '1.685s']

💡 PERFORMANCE ANALYSIS:
  • 2 pipelines vs 1: 2.05x faster
  • 4 pipelines vs 1: 3.26x faster
  • 4 pipelines vs 2: 1.58x faster
================================================================================