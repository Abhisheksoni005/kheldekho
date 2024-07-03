import logging

def get_logger(name):

    log_file = 'app.log'
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    logging.basicConfig(
        filename=log_file,
        filemode='a',
        level=logging.INFO,
        format=log_format,
    )

    logging.getLogger("openai").disabled = True
    logging.getLogger('py4j.java_gateway').disabled = True
    logging.getLogger("azure.core.pipeline.policies.http_logging_policy").disabled = True

    return logging.getLogger(name)