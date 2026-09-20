# my_list = ["Emmanuel", "Joe", "Smith", "Jane", "Doe"]

# index = 0
# for name in my_list:
#     if name == "Smith":
#         print(f"Found {name} at index {index}")
#         #break
#     index += 1



#     len(my_list)

import time
import numpy as np
import matplotlib
matplotlib.use('TkAgg') # interactive backend
import matplotlib.pyplot as plt

import time
import numpy as np
import matplotlib
matplotlib.use('TkAgg')          # interactive backend
import matplotlib.pyplot as plt


# ---------------- algorithms: take an ARRAY ----------------

def linear_search(arr, target):
    for i, v in enumerate(arr):
        if v == target:
            return i
    return -1


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def selection_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


# ---------------- wrappers: take an INT n, build input, call algorithm ----------------

def make_input(n):
    return np.random.randint(0, 10**6, size=n).tolist()


def run_linear_search(n):
    return linear_search(make_input(n), -1)      # -1 absent → worst case


def run_bubble_sort(n):
    return bubble_sort(make_input(n))


def run_selection_sort(n):
    return selection_sort(make_input(n))


def run_insertion_sort(n):
    return insertion_sort(make_input(n))


# ---------------- visualizer ----------------

def time_complexity_visualizer_multi(algos, ranges):
    """
    algos:  list of wrapper functions
    ranges: list of (n_min, n_max, n_step) tuples
    """
    plt.ion()
    fig, ax = plt.subplots()
    ax.set_xlabel('Input Size (n)')
    ax.set_ylabel('Execution Time (seconds)')
    ax.set_title('Algorithm time complexity comparison')

    lines = []
    for algo in algos:
        line, = ax.plot([], [], 'o-', label=algo.__name__)
        lines.append(line)
    ax.legend()

    # compute all series first
    all_sizes, all_times = [], []
    for algo, (n_min, n_max, n_step) in zip(algos, ranges):
        sizes = list(range(n_min, n_max + n_step, n_step))
        times = []
        for n in sizes:
            t0 = time.time()
            algo(n)
            t1 = time.time()
            times.append(t1 - t0)
        all_sizes.append(sizes)
        all_times.append(times)

    # animate them together
    max_len = max(len(s) for s in all_sizes)
    for i in range(max_len):
        for line, sizes, times in zip(lines, all_sizes, all_times):
            k = min(i + 1, len(sizes))
            line.set_data(sizes[:k], times[:k])
        ax.relim()
        ax.autoscale_view()
        plt.draw()
        plt.pause(0.01)

    plt.ioff()
    plt.show()


# ---------------- driver ----------------

if __name__ == "__main__":
    time_complexity_visualizer_multi(
        [run_linear_search, run_bubble_sort, run_selection_sort, run_insertion_sort],
        [(100, 10000, 100), (100, 1000, 50), (100, 1000, 50), (100, 1000, 50)],
    )