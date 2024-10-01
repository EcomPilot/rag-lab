from enum import Enum
import threading
from typing import Callable, List, Any, Tuple
from loguru import logger
import os
from tqdm import tqdm


class OnError(Enum):
    exit_system = "exit_system"
    return_none = "return_none"
    raise_exception = "raise_exception"


def parallel_for(func: Callable[..., Any], args_list: Tuple[List], num_threads: int = 3, on_error = OnError.exit_system.value) -> List[Any]:
    """
    Executes a function in parallel using multiple threads and collects the return values.

    **Parameters:**
    - func (Callable[..., Any]): The function to execute. It should accept multiple arguments.
    - args_list (Tuple[List]): A Tuple of List, each containing the arguments to pass to the function.
    - num_threads (int): The number of threads to use for parallel execution. Default is 3.
    - on_error (str): The error handling strategy. Options are 'exit_system', 'return_none', and 'raise_exception'. Default is 'exit_system'.

    **Returns:**
    - List[Any]: A list of return values from the function. If `on_error` is 'return_none' and an error occurs, the corresponding entry will be None.
    """
    results = [None for _ in range(len(args_list))]
    lock = threading.Lock()

    def worker(start_index, end_index):
        try:
            for i in tqdm(range(start_index, end_index)):
                result = func(*args_list[i])
                with lock:
                    results[i] = result
        except Exception as ex:
            logger.error(ex)
            if on_error == OnError.exit_system.value:
                os._exit(1)
            elif on_error == OnError.return_none.value:
                with lock:
                    results[i] = None
            else:
                raise ex

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
        # raise Exception("test ex")
        return a + b

    args = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]
    results = parallel_for(add, args, 3)
    print(args)