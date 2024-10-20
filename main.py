import random
import time
from multiprocessing import Pool
import matplotlib.pyplot as plt


def generate_random_matrix(rows, cols):
    return [[random.randint(1, 1000) for _ in range(cols)] for _ in range(rows)]


def find_min_max(matrix):
    min_val = float('inf')
    max_val = float('-inf')
    for row in matrix:
        min_row = min(row)
        max_row = max(row)
        if min_row < min_val:
            min_val = min_row
        if max_row > max_val:
            max_val = max_row
    return min_val, max_val


def find_min_max_parallel(matrix):
    num_processes = 4  # Количество процессов
    pool = Pool(num_processes)

    # Разделяем матрицы
    submatrices = [matrix[i:i + len(matrix) // num_processes] for i in
                   range(0, len(matrix), len(matrix) // num_processes)]

    result = pool.map(find_min_max, submatrices)
    pool.close()
    pool.join()

    min_val = min(res[0] for res in result)
    max_val = max(res[1] for res in result)

    return min_val, max_val


if __name__ == '__main__':
    rows, cols = 1000, 1000  # Размеры матрицы
    matrix = generate_random_matrix(rows, cols)

    # Списки для хранения результатов
    sequential_times = []
    parallel_times = []

    for _ in range(10):
        start_time = time.time()
        min_val, max_val = find_min_max(matrix)
        sequential_times.append(time.time() - start_time)

        start_time = time.time()
        min_val_parallel, max_val_parallel = find_min_max_parallel(matrix)
        parallel_times.append(time.time() - start_time)

    print(f"Sequential Min: {min_val}, Max: {max_val}")
    print(f"Parallel Min: {min_val_parallel}, Max: {max_val_parallel}")

    # Рассчитываем среднее время выполнения
    avg_sequential_time = sum(sequential_times) / len(sequential_times)
    avg_parallel_time = sum(parallel_times) / len(parallel_times)

    print(f"Average Sequential Execution Time: {avg_sequential_time} seconds")
    print(f"Average Parallel Execution Time: {avg_parallel_time} seconds")

    # Рассчитываем ускорение и эффективность
    speedup = avg_sequential_time / avg_parallel_time
    efficiency = speedup / 4

    print(f"Speedup: {speedup:.2f}")
    print(f"Efficiency: {efficiency:.2f}")

    # Графики
    plt.plot(sequential_times, label='Sequential')
    plt.plot(parallel_times, label='Parallel')
    plt.xlabel('Iteration')
    plt.ylabel('Execution Time (seconds)')
    plt.legend()
    plt.show()
