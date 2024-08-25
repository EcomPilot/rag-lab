import threading
from typing import Callable, List, Any, Tuple

def parallel_for(func: Callable[..., Any], args_list: List[Tuple], num_threads: int = 3) -> List[Any]:
    """
    Executes a function in parallel using multiple threads and collects the return values.

    **Parameters:**
    - func (Callable[..., Any]): The function to execute. It should accept multiple arguments.
    - args_list (List[Tuple]): A list of tuples, each containing the arguments to pass to the function.
    - num_threads (int): The number of threads to use for parallel execution.

    **Returns:**
    - List[Any]: A list of return values from the function.
    """
    results = [None for _ in range(len(args_list))]
    lock = threading.Lock()

    def worker(start_index, end_index):
        for i in range(start_index, end_index):
            result = func(*args_list[i])
            with lock:
                results[i] = result

    # Split args_list into chunks for each thread
    chunk_size = len(args_list) // num_threads
    threads = []

    for i in range(num_threads):
        start_index = i * chunk_size
        end_index = len(args_list) if i == num_threads - 1 else (i + 1) * chunk_size
        thread = threading.Thread(target=worker, args=(start_index, end_index))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results


# Example usage
if __name__ == "__main__":
    def add(a, b):
        return a + b

    args = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]
    results = parallel_for(add, args, 3)
    print(args)