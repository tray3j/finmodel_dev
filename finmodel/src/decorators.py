#####################################################################################################################################################
# DECORATORS                                                                                                    
#####################################################################################################################################################

# Standard library imports
import time
import logging
import functools
import inspect

# # Third party library imports
# --- NONE ---

# Local application imports
# --- NONE ---

# instantiating the logger
logger = logging.getLogger(__name__) 
logger.setLevel(logging.DEBUG) 
formatter = logging.Formatter('%(asctime)s:   %(message)s')
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s: %(message)s') # alt format


# # for writing to a log file 
# file_handler = logging.FileHandler(os.path.join(write_read_path, 'log.txt'))
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

# for dev stream to terminal
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


# ====================================================================================================================================================
def log(func):

    @functools.wraps(func) 
    def log_wrapper(*args, **kwargs): 
        start = time.time() 
        stack_depth = len(inspect.stack()) 
        logger.info(f'{f"{func.__module__}":<16s}   {(int(stack_depth/2))*str("-")}↘   {func.__name__} CALLED')
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            logger.exception(f'{f"{func.__module__}":<16s}   {(int(stack_depth/2))*str("-")}↗   {func.__name__} EXCEPTION: {str(e)}')
            end = time.time()
            logger.info(f'{f"{func.__module__}":<16s}   {(int(stack_depth/2))*str("-")}↗   {func.__name__} RUNTIME: {end-start:.4f} seconds')
            # raise e
        else:
            end = time.time()
            logger.info(f'{f"{func.__module__}":<16s}   {(int(stack_depth/2))*str("-")}↗   {func.__name__} RUNTIME: {end-start:.4f} seconds ')
            return result 

    return log_wrapper