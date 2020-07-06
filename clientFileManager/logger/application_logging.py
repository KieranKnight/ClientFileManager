import time
import logging

class BaseLogger(object):
    def __init__(self, name='logger', level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        stream_handler = logging.StreamHandler()
        self.logger.addHandler(stream_handler)

        formatter = logging.Formatter('%(asctime)s :: %(name)s :: %(levelname)s >> %(message)s')
        stream_handler.setFormatter(formatter)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, error):
        self.logger.warning(msg)


class ApplicationLogger(BaseLogger):
    def __init__(self, name='Client File Manager Logging'):
        super(ApplicationLogger, self).__init__(name)


class IntegrateLogger(BaseLogger):
    def __init__(self, location, name='Integrate Logging'):
        super(IntegrateLogger, self).__init__(name)
        timestr = time.strftime("%Y%m%d_%H%M%S")
        file_handler = logging.FileHandler('integrateFiles_{}'.format(timestr), 'w')
        self.logger.addHandler(file_handler)
