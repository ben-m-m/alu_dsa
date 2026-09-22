# Algorithm Time Complexity Analyzer

A Python tool for experimenting with, benchmarking, and visualizing algorithm time complexity.

The project provides two ways to study algorithm performance:

- **API mode** runs a benchmark and returns a generated complexity graph as a Base64-encoded image through Flask.
- **Live visualization mode** displays the graph interactively while the algorithm is tested with increasing input sizes.

This is an educational project. Its measurements help build intuition about algorithmic growth, but they are not a replacement for formal Big-O analysis or a professional benchmarking suite.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Running the Application](#running-the-application)
  - [API Mode](#api-mode)
  - [Live Visualization Mode](#live-visualization-mode)
- [Supported Algorithms](#supported-algorithms)
- [How the Benchmark Works](#how-the-benchmark-works)
- [API Reference](#api-reference)
- [Image Generation and Base64 Encoding](#image-generation-and-base64-encoding)
- [Understanding the Results](#understanding-the-results)
- [Benchmarking Limitations](#benchmarking-limitations)
- [Troubleshooting](#troubleshooting)
- [Development Workflow](#development-workflow)
- [Learning Workflow](#learning-workflow)
- [Future Improvements](#future-improvements)
- [Learning Goals](#learning-goals)

## Features

- Benchmarks searching, sorting, and data-structure operations.
- Measures execution time for increasing input sizes.
- Saves generated graphs as PNG files.
- Returns generated graphs as Base64-encoded images from the API.
- Supports interactive Matplotlib visualization.
- Provides a command-line interface for live experiments.
- Includes stack and queue operation benchmarks alongside classic algorithm examples.

## Project Structure

```text
alu_dsa/
├── algo_test.py
├── README.md
├── requirements.txt
├── tests/
│   ├── test_queue.py
│   └── test_stack.py
├── data_structures/
│   ├── __init__.py
│   ├── queue.py
│   └── stack.py
├── my_venv/
└── *.png                  # Generated benchmark graphs
```

The main application is [`algo_test.py`](algo_test.py). PNG files are generated when an API benchmark is run.

The repository currently also contains generated `merge_sort.png` and `unique_users.png` files. Other algorithm PNG files may appear after API benchmarks; generated images are not required source files.

## Requirements

- Python 3
- Flask
- Matplotlib
- Tkinter
- A graphical environment for live visualization

The project was developed in a Linux/Ubuntu environment.

Matplotlib uses the `TkAgg` backend. Tkinter and a graphical display are therefore needed for live visualization. The backend also supports saving generated figures as PNG files.

## Quick Start

From the project directory:

```bash
python -m venv my_venv
source my_venv/bin/activate
pip install -r requirements.txt
python algo_test.py
```

To open a live visualization instead:

```bash
python algo_test.py --live merge_sort
```

On Ubuntu, install Tkinter separately if necessary:

```bash
sudo apt install python3-tk
```

## Installation

1. Change to the project directory:

   ```bash
   cd /home/benzz/Documents/aluswe/Enterprise_web_dev/Data_structures_and_algorithms/alu_dsa
   ```

2. Activate the existing virtual environment, if available:

   ```bash
   source my_venv/bin/activate
   ```

3. Install the dependencies listed in `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

4. If Tkinter is not installed on Ubuntu, install it with:

   ```bash
   sudo apt install python3-tk
   ```

The appropriate Tkinter package may differ depending on the Python version and operating system.

## Running the Application

### API Mode

Start the Flask application with:

```bash
python algo_test.py
```

The service listens on port `5000` by default:

```text
http://127.0.0.1:5000
```

Use API mode when you want JSON output, Base64 image data, HTTP access, or future frontend integration.

### Live Visualization Mode

Run an algorithm directly with an interactive Matplotlib window:

```bash
python algo_test.py --live bubble_sort
```

The current live benchmark uses:

| Parameter | Value |
| --- | ---: |
| Minimum input size | 10 |
| Maximum input size | 1000 |
| Step | 10 |

Examples:

```bash
python algo_test.py --live linear_search
python algo_test.py --live binary_search
python algo_test.py --live unique_users
python algo_test.py --live bubble_sort
python algo_test.py --live insertion_sort
python algo_test.py --live merge_sort
python algo_test.py --live stack_push
python algo_test.py --live stack_pop
python algo_test.py --live queue_enqueue
python algo_test.py --live queue_dequeue
```

Live mode is useful for learning algorithms, comparing growth rates, and experimenting with implementations.

## Supported Algorithms

| Algorithm | Complexity | Main idea |
| --- | --- | --- |
| Linear search | `O(n)` | Checks elements sequentially |
| Binary search | `O(log n)` | Repeatedly halves a sorted search space |
| Unique users | `O(n)` average | Uses a set for membership checks |
| Bubble sort | `O(n^2)` | Repeatedly compares neighboring elements |
| Insertion sort | `O(n^2)` worst case | Inserts each item into a sorted section |
| Merge sort | `O(n log n)` | Divides the input and merges sorted halves |
| Stack push | `O(1)` amortized per push | Appends to the top of a stack |
| Stack pop | `O(1)` amortized per pop | Removes the most recent stack item |
| Queue enqueue | `O(1)` amortized per enqueue | Adds an item to the back of a queue |
| Queue dequeue | `O(1)` amortized per dequeue | Removes the front item from a queue |

### Algorithm Notes

- **Linear search:** The implementation creates an array and scans toward the end of the input. It is a simplified educational benchmark for linear growth, not a complete production search API.
- **Binary search:** The implementation creates a sorted generated array and uses a simplified target/index setup. Its search phase is `O(log n)`, although the benchmark also spends `O(n)` time creating the array. It is primarily intended to demonstrate logarithmic search behavior, not to serve as a general-purpose binary-search API.
- **Unique users:** The implementation generates `n` user records whose IDs are already unique. It checks a Python set and appends unseen users, demonstrating `O(1)` average membership checks and `O(n)` average overall processing; it does not measure duplicate removal from a duplicate-containing dataset.
- **Bubble sort:** Reverse-sorted input is used as an intentionally unfavorable input to demonstrate substantial `O(n^2)` work.
- **Insertion sort:** Reverse-sorted input represents a worst-case-style input and produces `O(n^2)` behavior.
- **Merge sort:** The implementation recursively divides the array, sorts both halves, and merges them. Its expected time complexity is `O(n log n)`.
- **Stack operations:** The stack implementation uses a Python list and measures repeated `push` and `pop` operations across increasing values of `n`. The benchmark reflects the cost of performing `n` stack operations, which is linear overall.
- **Queue operations:** The queue implementation uses a `deque` and measures repeated `enqueue` and `dequeue` calls. This demonstrates the near-constant-time behavior of queue operations at scale, while still producing a linear overall trend over `n` operations.

## How the Benchmark Works

The benchmark follows this process:

1. Select an algorithm.
2. Generate a sequence of input sizes.
3. Create an input for each size.
4. Start the timer.
5. Run the algorithm.
6. Stop the timer and store the elapsed time.
7. Plot input size against execution time.

In API mode, input sizes start at `n_min = 0` using the requested `step` and `n_max`. In live mode, the values are currently hard-coded to `n_min = 10`, `n_max = 1000`, and `n_step = 10`.

Input sizes are generated with:

```python
input_sizes = list(range(n_min, n_max + n_step, n_step))
```

Timing is measured with:

```python
start_time = time.time()
algorithm(n)
end_time = time.time()
elapsed_time = end_time - start_time
```

The graph uses input size `n` on the X-axis and execution time in seconds on the Y-axis.

## API Reference

### Endpoint

```text
GET /analyze
```

### Query Parameters

| Parameter | Required | Description | Example |
| --- | --- | --- | --- |
| `algo` | Yes | Algorithm to benchmark | `merge_sort` |
| `step` | Yes | Increase between input sizes | `10` |
| `n_max` | Yes | Maximum input size | `1000` |

The API does not currently accept `n_min`; it always starts at `n = 0`.

### Example Request

```text
http://127.0.0.1:5000/analyze?algo=merge_sort&step=10&n_max=1000
```

Using cURL:

```bash
curl "http://127.0.0.1:5000/analyze?algo=merge_sort&step=10&n_max=1000"
```

Stack and queue examples:

```bash
curl "http://127.0.0.1:5000/analyze?algo=stack_push&step=10&n_max=1000"
curl "http://127.0.0.1:5000/analyze?algo=queue_enqueue&step=10&n_max=1000"
```

### Example Response

```json
{
  "algorithm": "merge_sort",
  "step": 10,
  "n_max": 1000,
  "base64img": "iVBORw0KGgoAAAANSUhEUgAA..."
}
```

The complete Base64 value is much longer than the example shown above.

### Invalid Algorithms

If `algo` is not supported, the API returns HTTP `400 Bad Request`:

```json
{
  "error": "Unknown Algorithm",
  "available_algorithms": [
    "linear_search",
    "binary_search",
    "unique_users",
    "bubble_sort",
    "insertion_sort",
    "merge_sort",
    "stack_push",
    "stack_pop",
    "queue_enqueue",
    "queue_dequeue"
  ]
}
```

## Image Generation and Base64 Encoding

### Generated PNG Files

When an API benchmark runs, the graph is saved using the algorithm name:

```text
merge_sort.png
bubble_sort.png
linear_search.png
stack_push.png
queue_enqueue.png
```

The filename follows this pattern:

```python
filename = f"{algorithm_name}.png"
```

The graph is also written to an in-memory `BytesIO` buffer. The same image bytes are used both for the PNG file and for the Base64 response:

```python
image_buffer = BytesIO()
fig.savefig(image_buffer, format="png")
image_buffer.seek(0)
image_bytes = image_buffer.read()
filename = f"{algorithm_name}.png"
with open(filename, "wb") as image_file:
  image_file.write(image_bytes)
base64_image = base64.b64encode(image_bytes).decode("utf-8")
```

The implementation follows this flow:

1. Create an in-memory `BytesIO` buffer.
2. Save the Matplotlib figure to the buffer.
3. Call `seek(0)` so reading starts at the beginning of the buffer.
4. Read the PNG bytes once.
5. Reuse those same `image_bytes` to write the PNG file and create the Base64 string.

Base64 converts binary PNG data into text that can be transported inside JSON. A frontend can decode the value and display the image.

## Understanding the Results

The purpose of the graph is to answer this question:

> What happens to execution time as the input size becomes larger?

The expected growth rates can be ordered approximately as follows for large inputs:

```text
O(log n) < O(n) < O(n log n) < O(n^2)
```

For example:

- Linear search performs roughly proportional work as `n` increases.
- Binary search grows slowly because it repeatedly halves the search space.
- Merge sort grows faster than binary search but slower than quadratic algorithms.
- Bubble sort and insertion sort can become much slower as `n` grows.
- Stack and queue operations are usually close to constant per operation, so repeating them `n` times produces an overall linear trend.

A graph provides experimental evidence and intuition. It does not prove a Big-O classification by itself.

## Benchmarking Limitations

This is an educational benchmark. Results are affected by:

1. **Operating system activity:** Other applications and background services can consume CPU resources.
2. **Python runtime overhead:** Measurements include function calls, list creation, memory allocation, garbage collection, and interpreter overhead.
3. **Hardware differences:** Processor speed, memory, operating-system scheduling, and background processes affect results.
4. **Small inputs and timer resolution:** Very short execution times can be noisy relative to timer resolution and system scheduling.
5. **Single measurements:** The current implementation measures each input size once. More reliable benchmarks would repeat measurements and report an average, median, or minimum.
6. **Algorithm implementation details:** The graph represents this implementation in this environment, not pure mathematical operations.

For more reliable experiments, use larger inputs where appropriate and compare overall trends instead of individual points.

## Benchmark Parameters

The available parameters depend on the execution mode.

### API Mode

The caller can configure:

- `algo`
- `step`
- `n_max`

The API always starts at `n = 0`. There is no API parameter for `n_min`.

### Live Mode

The live mode values are currently hard-coded:

```text
n_min = 10
n_max = 1000
n_step = 10
```

Configurable live benchmark parameters are listed under [Future Improvements](#future-improvements), not currently available CLI options.

## Troubleshooting

### Port 5000 Is Already in Use

Find the process using the port:

```bash
sudo lsof -i :5000
```

Stop it using its process ID:

```bash
kill <PID>
```

Alternatively:

```bash
sudo fuser -k 5000/tcp
```

Then restart the application:

```bash
python algo_test.py
```

### The Live Graph Does Not Open

Live visualization uses the `TkAgg` Matplotlib backend. Install Tkinter and use an environment capable of displaying graphical windows:

```bash
sudo apt install python3-tk
```

### Unknown Algorithm Error

Use one of the exact supported names:

```text
linear_search
binary_search
unique_users
bubble_sort
insertion_sort
merge_sort
stack_push
stack_pop
queue_enqueue
queue_dequeue
```

For example, use `?algo=linear_search`, not `?algo='linear_search'`. Quotes become part of the query value.

## Development Workflow

When adding an algorithm:

1. Implement the algorithm.
2. Test it independently.
3. Analyze its complexity.
4. Add it to the `Algorithm` dictionary in [`algo_test.py`](algo_test.py).
5. Run it in live mode.
6. Run an API benchmark.
7. Inspect the generated PNG and API response.

The algorithm dictionary currently has this shape:

```python
Algorithm = {
    'linear_search': linear_search,
    'binary_search': binary_search,
    'unique_users': unique_users,
    'bubble_sort': bubble_sort,
    'insertion_sort': insertion_sort,
    'merge_sort': merge_sort,
    'stack_push': benchmark_stack_push,
    'stack_pop': benchmark_stack_pop,
    'queue_enqueue': benchmark_queue_enqueue,
    'queue_dequeue': benchmark_queue_dequeue,
}
```

After adding an entry such as `"my_algorithm": my_algorithm`, it can be selected through the command line and the `/analyze` endpoint.

## Learning Workflow

1. Understand the algorithm and the problem it solves.
2. Predict its complexity from its loops and recursion.
3. Run it in live mode.
4. Observe how the graph changes as `n` increases.
5. Compare it with an algorithm that has a different growth rate.
6. Revisit the implementation and connect the code to the measured behavior.

Useful experiments include:

```bash
# Linear versus binary search
python algo_test.py --live linear_search
python algo_test.py --live binary_search

# Bubble sort versus insertion sort
python algo_test.py --live bubble_sort
python algo_test.py --live insertion_sort

# Bubble sort versus merge sort
python algo_test.py --live bubble_sort
python algo_test.py --live merge_sort

# Stack versus queue operations
python algo_test.py --live stack_push
python algo_test.py --live queue_enqueue
```

Algorithms with the same Big-O complexity can still have different measured execution times because their implementations and constant factors differ.

## Future Improvements

- Add configurable live benchmark parameters such as minimum, maximum, and step values. These options do not currently exist.
- Repeat measurements and report averages, medians, or minimums.
- Measure memory complexity as well as time complexity.
- Plot multiple algorithms on the same graph.
- Build a frontend for the Flask API.
- Return algorithm metadata such as time complexity, space complexity, and measured execution time.
- Add selection sort, quick sort, heap sort, counting sort, tree traversal, graph traversal, breadth-first search, depth-first search, and Dijkstra's algorithm.
- Add more data-structure benchmarks for hash tables, linked lists, trees, and graphs.

## Learning Goals

This project provides practice with:

- Searching and sorting algorithms
- Recursion and divide-and-conquer techniques
- Lists, sets, dictionaries, and arrays
- Data structures such as stacks and queues
- Loops and nested functions
- Command-line arguments
- File handling and binary data
- Base64 encoding
- HTTP, query parameters, JSON, and status codes
- Matplotlib graphing and interactive visualization

The central mental model is:

```text
Algorithm
  -> Number of operations
  -> How operations change as n grows
  -> Effect on execution time
  -> Shape of the graph
```

The benchmark should support Big-O understanding, not replace it. The strongest learning comes from predicting the complexity first and then explaining how the observed graph relates to that prediction.
