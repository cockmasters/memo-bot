import logging


def start_logging():
    open('log.log', 'w').close()
    logging.basicConfig(handlers=(logging.FileHandler('log.log'), logging.StreamHandler()),
                        level=logging.INFO
                        )
