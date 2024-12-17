import logging
logging.basicConfig(level = logging.INFO)
import time

def timer(name: str = "Unnamed process"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            total_time = end_time - start_time
            logging.info(f"[[{name}]] - Total time cost: {total_time:.4f} seconds")
            return result
        return wrapper
    return decorator