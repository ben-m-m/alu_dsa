import argparse
import time
# import numpy as np
import matplotlib
matplotlib.use('TkAgg') #interactive backend
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify
import base64
from io import BytesIO
from data_structures.stack import Stack
from data_structures.queue import Queue
import sqlalchemy

engine = sqlalchemy.create_engine('sqlite://algodatabase.db', echo=True)

with engine.connect() as conn:
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS analysis
    id INT PRIMARY KEY
    algorithm VARCHAR(100) NOT NULL
    step INT NOT NULL
    n_max INT NOT NULL
    """))

    conn.commit()

def time_complexity_visualizer(algorithm, algorithm_name, n_min, n_max, n_step):
    times = []
    input_sizes = list(range(n_min, n_max + n_step, n_step))
    # plt.ion() #Turn on interactive mode
    fig, ax = plt.subplots()

    ax.set_xlabel('Input Size(n)')
    ax.set_ylabel('Execution Time(seconds)')
    ax.set_title(f'{algorithm_name} Time Complexity visualization')

    for n in input_sizes:
        start_time = time.time()
        algorithm(n)
        end_time = time.time()
        times.append(end_time - start_time)

    #graph plotting
    ax.plot(input_sizes, times, 'o-')

    image_buffer = BytesIO()

    fig.savefig( image_buffer, format='png')

    image_buffer.seek(0)
    image_bytes = image_buffer.read()
    filename = f'{algorithm_name}.png'
    with open(filename, 'wb') as image_file:
        image_file.write(image_bytes)

    # image_buffer.seek(0)

    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    plt.close(fig)
    return base64_image

def live_complexity_visualizer(algorithm, algorithm_name, n_min, n_max, n_step):
    times = []
    input_sizes = list(range(n_min, n_max + n_step, n_step))
    plt.ion()

    fig, ax = plt.subplots()

    ax.set_xlabel('Input Size(n)')
    ax.set_ylabel('Execution Time(seconds)')
    ax.set_title(f'{algorithm_name} Time Complexity - Live')

    line, = ax.plot([], [], 'o-') #Initialize empty line

    for n in input_sizes:
        start_time = time.time()
        algorithm(n)
        end_time = time.time()
        times.append(end_time - start_time)

        line.set_data(input_sizes[:len(times)], times)
        ax.relim()
        ax.autoscale_view()
        plt.draw()
        plt.pause(0.01)

    plt.ioff()
    plt.show()


def unique_users(n):
    users = []
    for k in range(n):
        users.append({'id':k})

    unique_users = []
    seen_ids = set()

    for user in users:
        user_id = user['id']

        if user_id not in seen_ids:
            unique_users.append(user)
            seen_ids.add(user_id)
    return unique_users

def linear_search(n):
    arr = list(range(n))
    target = n - 1
    for i in range(len(arr)):
        if i == target:
            return 1

def binary_search(n):
    arr = list(range(n))
    target = n - 1
    left_index = 0
    right_index = len(arr) - 1
    while left_index <= right_index:
        mid_index = int((left_index + right_index) / 2)

        if mid_index == target:
            return target
        if mid_index < target:
            left_index = mid_index + 1
        else:
            right_index = mid_index - 1

    return -1       #search is empty.

def bubble_sort(n):
    arr = list(range(n, 0, -1))

    for i in range(n):
        for j in range(n-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def insertion_sort(n):
    arr = list(range(n, 0, -1))

    for i in range(1, n):
        current = arr[i]
        j = i -1

        while j >= 0 and arr[j] > current:
            arr[j+1] = arr[j]
            j -= 1

        arr[j+1] = current

    return arr

def merge_sort(n):
    arr = list(range(n, 0, -1))

    def sort(arr):
        if len(arr) <= 1:
            return arr

        mid = int(len(arr) / 2)

        left = sort(arr[:mid])
        right = sort(arr[mid:])

        merged_arr = []

        i = 0
        j = 0

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                merged_arr.append(left[i])
                i += 1
            else:
                merged_arr.append(right[j])
                j += 1

        merged_arr.extend(left[i:])
        merged_arr.extend(right[j:])

        return merged_arr
    return sort(arr)

# def nested_loops(n):
#     arr = list(range(n))
#     target = n - 1
#     for outer_index in range(arr):
#         for inner_index in range(arr):


def benchmark_stack_push(n):
    stack = Stack()
    start_time = time.time()

    for i in range(n):
        stack.push(i)

    end_time = time.time()
    return end_time - start_time

def benchmark_stack_pop(n):
    stack = Stack()

    for i in range(n):
        stack.push(i)

    start_time = time.time()

    for i in range(n):
        stack.pop()

    end_time = time.time()
    return end_time - start_time

def benchmark_queue_enqueue(n):
    queue = Queue()

    start_time = time.time()

    for i in range(n):
        queue.enqueue(i)

    end_time = time.time()
    return end_time - start_time

def benchmark_queue_dequeue(n):
    queue = Queue()

    for i in range(n):
        queue.enqueue(i)

    start_time = time.time()

    for i in range(n):
        queue.dequeue()

    end_time = time.time()
    return end_time - start_time


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
    'queue_dequeue': benchmark_queue_dequeue
}

app = Flask(__name__)
@app.route('/analyze')
def analyze():
    algo = request.args.get('algo')
    step = request.args.get('step', type=int)
    n_max = request.args.get('n_max', type=int)

    if algo is None or step is None or n_max is None:
        return jsonify({
            "error": "missing parameters",
            "usage": "/analyze?algo=bubble_sort&step=10&n_max=1000",
            "available_algorithms": sorted(Algorithm.keys())
        }), 400

    if step <= 0 or n_max <= 0:
        return jsonify({
            "error": "step an n_max must be > 0"
        })

    if algo not in Algorithm:
        return jsonify({
            "error": 'Unknown Algorithm',
            "available_algorithms": list(Algorithm.keys())
        }), 400

    algorithm = Algorithm[algo]
    base64img = time_complexity_visualizer(algorithm, algo, 0, n_max, step)
    

    return jsonify({
        'algorithm': algo,
        'step': step,
        'n_max': n_max,
        'base64img': base64img
    })

@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    algo = data.get('algo')
    step = data.get('step')
    n_max = data.get('n_max')


    if algo is None or step is None or n_max is None:
        return jsonify({
         "Error": "missing fields",
         "Available Algorithms": sorted(Algorithm.keys())
        }), 400

    try:
        step = int(step)
        n_max = int(n_max)
    except (TypeError, ValueError):
        return jsonify({
            "error": "step and n_max must be integers"
        }), 400
    
    if step <= 0 or n_max <= 0:
        return jsonify({
            "error": "step and n_max must be integers"
        })
    
    if algo not in Algorithm:
        return jsonify({
            "error": 'Unknown Algorithm',
            "available_algorithms": list(Algorithm.keys())
        }), 400
    
    algorithm = Algorithm[algo]
    base64img = time_complexity_visualizer(algorithm, algo, 0, n_max, step)
        
    
    return jsonify({
        'algorithm': algo,
        'step': step,
        'n_max': n_max,
        'base64img': base64img
    }), 201

# time_complexity_visualizer(unique_users, 10, 1000, 10)
# time_complexity_visualizer(binary_search, 10, 10000, 10)
#time_complexity_visualizer(linear_search, 10, 1000, 10)


"""
function to view in flsk app or live 
"""

def main():
    parser = argparse.ArgumentParser( description="Algorithm time complexity Analyzer")

    parser.add_argument('--live', help='Run live visualization for an algorithm')

    args = parser.parse_args()

    if args.live:
        if args.live not in Algorithm:
            print(f"Unknown algorithm: {args.live}")
            print("Available algorithms:")
            for algorithm in Algorithm:
                print(f" - {algorithm}")
            return

        live_complexity_visualizer(Algorithm[args.live], args.live, 10, 1000, 10)

    else:
        app.run(debug=True)


if __name__ == "__main__":
    main()


# binary_search	O(log n)
# linear_search	O(n)
# insertion_sort	O(n²)
# bubble_sort	O(n²)
# merge_sort	O(n log n)