import logging

def getLogger(    
        LOG_FORMAT     = '%(asctime)s %(levelname)-8s %(message)s',
        LOG_NAME       = '',
        LOG_FILE_INFO  = r'C:\Users\Julie\Desktop\HeatherData\logs\file.log',
        LOG_FILE_ERROR = r'C:\Users\Julie\Desktop\HeatherData\logs\error.log',
        LOG_FILE_DEBUG = r'C:\Users\Julie\Desktop\HeatherData\logs\debug.log'):

    log           = logging.getLogger(LOG_NAME)
    log_formatter = logging.Formatter(LOG_FORMAT)


    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)
    log.addHandler(stream_handler)
    
    file_handler_debug = logging.FileHandler(LOG_FILE_DEBUG)
    file_handler_debug.setFormatter(log_formatter)
    file_handler_debug.setLevel(logging.DEBUG)
    log.addHandler(file_handler_debug)


    file_handler_info = logging.FileHandler(LOG_FILE_INFO)
    file_handler_info.setFormatter(log_formatter)
    file_handler_info.setLevel(logging.INFO)
    log.addHandler(file_handler_info)

    file_handler_error = logging.FileHandler(LOG_FILE_ERROR)
    file_handler_error.setFormatter(log_formatter)
    file_handler_error.setLevel(logging.ERROR)
    log.addHandler(file_handler_error)

    log.setLevel(logging.DEBUG)

    return log