import uuid
import tiktoken
import traceback
from datetime import time
from utils.logger import get_logger

logger = get_logger(__name__)

SUCCESS = "Success"
FAILURE = "Failure"
CHAT_ENCODING = "gpt-4"
CONTEXT_DELIMITER = "\n--------------\n"
EMBEDDING_ENCODING = "text-embedding-ada-002"

MIN_RETRY_DELAY = 1
RETRY_DELAY_FACTOR = 2

def generate_uuid():
    return uuid.uuid4()

def get_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def execute_with_retry(func, exception, *args, delay = MIN_RETRY_DELAY, max_retries=2):
    try:
        return func(*args)

    except:
        logger.error(traceback.format_exc())
        time.sleep(delay)

        if max_retries == 0:
            raise exception

        logger.info(f"Retrying after {delay * RETRY_DELAY_FACTOR} seconds")
        return execute_with_retry(func, exception, args, delay=delay * RETRY_DELAY_FACTOR, max_retries = max_retries - 1)

def create_message(role, content):
    return [ {
        "role": role,
        "content": content
    } ]
