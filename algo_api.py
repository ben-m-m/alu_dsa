import base64
import io
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
SNAPSHOT_DIR = Path(__file__).parent / "snapshots"


@app.after_request
def allow_local_frontend(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


def run_linear_search(n):
    values = list(range(n))
    target = -1
    for value in values:
        if value == target:
            return value
    return -1


def run_bubble_sort(n):
    values = list(range(n, 0, -1))
    for end in range(n - 1, 0, -1):
        for index in range(end):
            if values[index] > values[index + 1]:
                values[index], values[index + 1] = values[index + 1], values[index]
    return values


def run_binary_search(n):
    values = list(range(n))
    target = -1
    low, high = 0, len(values) - 1
    while low <= high:
        middle = (low + high) // 2
        if values[middle] == target:
            return middle
        if values[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1


def run_nested_loops(n):
    total = 0
    for outer in range(n):
        for inner in range(n):
            total += outer + inner
    return total


def run_selection_sort(n):
    values = list(range(n, 0, -1))
    for index in range(n - 1):
        smallest = index
        for candidate in range(index + 1, n):
            if values[candidate] < values[smallest]:
                smallest = candidate
        values[index], values[smallest] = values[smallest], values[index]
    return values


def run_insertion_sort(n):
    values = list(range(n, 0, -1))
    for index in range(1, n):
        value = values[index]
        position = index - 1
        while position >= 0 and values[position] > value:
            values[position + 1] = values[position]
            position -= 1
        values[position + 1] = value
    return values


ALGORITHMS = {
    "linear_search": run_linear_search,
    "bubble_sort": run_bubble_sort,
    "binary_search": run_binary_search,
    "nested_loops": run_nested_loops,
    "selection_sort": run_selection_sort,
    "insertion_sort": run_insertion_sort,
}


def parse_integer(value, name):
    try:
        return int(value.strip().strip("'").strip('"').replace(",", ""))
    except (AttributeError, ValueError):
        raise ValueError(f"{name} must be an integer")


def create_snapshot(algo, step, n_max):
    sizes = list(range(0, n_max + 1, step))
    if sizes[-1] != n_max:
        sizes.append(n_max)

    times = []
    for size in sizes:
        started = time.perf_counter()
        algo(size)
        times.append(time.perf_counter() - started)

    figure, axis = plt.subplots()
    axis.plot(sizes, times, "o-", label=algo.__name__)
    axis.set_xlabel("Input Size (n)")
    axis.set_ylabel("Execution Time (seconds)")
    axis.set_title("Algorithm time complexity comparison")
    axis.legend()
    figure.tight_layout()

    SNAPSHOT_DIR.mkdir(exist_ok=True)
    snapshot_path = SNAPSHOT_DIR / f"{algo.__name__}.png"
    image = io.BytesIO()
    figure.savefig(image, format="png")
    figure.savefig(snapshot_path, format="png")
    plt.close(figure)
    return snapshot_path, image.getvalue()


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/analyze")
def analyze():
    algorithm_name = request.args.get("algo", "").strip().strip("'").strip('"')
    if algorithm_name not in ALGORITHMS:
        return jsonify({
            "error": "Unsupported algorithm",
            "supported_algorithms": sorted(ALGORITHMS),
        }), 400

    try:
        step = parse_integer(request.args.get("step"), "step")
        n_max = parse_integer(request.args.get("n_max"), "n_max")
        if step <= 0 or n_max < 0:
            raise ValueError("step must be positive and n_max must be non-negative")
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    snapshot_path, image_bytes = create_snapshot(ALGORITHMS[algorithm_name], step, n_max)
    return jsonify({
        "algo": algorithm_name,
        "step": step,
        "n_max": n_max,
        "snapshot": str(snapshot_path),
        "image_base64": base64.b64encode(image_bytes).decode("ascii"),
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
