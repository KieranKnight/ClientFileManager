# -*- coding: utf-8 -*-

################################################################################
## Client File Manager TOOL - Ingesting client files into a production pipeline
##  with tracking, logging and configuration overrides.
##
## File : application_logging.py
## Description : A simple logging system for the application and saving the 
##      integrated files into a log.
##
## Created by: Kieran Knight
## Email: kieransknight@gmail.com
## 
################################################################################

# Python Modules
import os
import time
import logging

class BaseLogger(object):
    """
    Simple base logging system.
    Where the logger is setup.
    """
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

    def error(self, msg):
        self.logger.warning(msg)


class ApplicationLogger(BaseLogger):
    """
    The application logger. This class is the logging
    setup that shows all messages linked to the UI processes

    Args:
        BaseLogger ([type]): [description]
    """
    def __init__(self, name='Client File Manager Logging'):
        super(ApplicationLogger, self).__init__(name)


class IntegrateLogger(BaseLogger):
    """
    The integration logger. This class
    will be where the logging to the saved files run

    Args:
        BaseLogger (Class): Base logger that instantiates the logging setup
    """
    def __init__(self, location, name='Integrate Logging'):
        super(IntegrateLogger, self).__init__(name)

        timestr = time.strftime("%Y%m%d_%H%M%S")  # time stamp format

        # adding the filehandler to the logger on where the file will be placed
        file_handler = logging.FileHandler(
            '{location}/integrateFiles_{date}.txt'.format(location=location, date=timestr), 'w')
        self.logger.addHandler(file_handler) 

    def completed_files(self, completed):
        """
        Passing all completed files to the writing method to be written to the log.
        
        Arguments:
            completed (list): A list of completed integration files
        """
        self.logger.info('\n\n**** Successful Integration ****')
        self.write_integration(completed, self.completed_files)

    def failed_files(self, failed):
        """
        Passing all failed files to the writing method to be written to the log.
        
        Arguments:
            failed (list): A list of failed integration files
        """
        self.logger.info('\n\n**** Failed Integration ****')
        self.write_integration(failed, self.failed_files)

    def ignored_files(self, ignored):
        """
        Passing all ignored files to the writing method to be written to the log.
        
        Arguments:
            ignored (list): A list of ignored integration files
        """
        self.logger.info('\n\n**** Ignored Integration ****')
        self.write_integration(ignored, self.ignored_files)

    def write_integration(self, items, method_instance):
        """
        Writing the integration data log to a file in the specified
        output location.

        Args:
            items (list): A list of items that have either been completed, failed or ignored.
            method_instance (bound method): The method the processed list is coming from.
        """
        for item in items:
            _from = item.item_contents.file_path
            _to = os.path.join(
                str(item.location.currentText()),
                str(item.sequence.currentText()),
                str(item.shot.currentText()),
                str(item.option.currentText()),
                str(item.filename.text())
            )
            if isinstance(method_instance, type(self.completed_files)):
                self.logger.info('{start} >> Copied To >> {end}'.format(start=_from, end=_to))
            
            elif isinstance(method_instance, type(self.failed_files)):
                self.error.info('{start} >> Failed To Copy To >> {end}'.format(start=_from, end=_to))
            
            elif isinstance(method_instance, type(self.ignored_files)):
                self.warning.info('{start} >> Was Set To Ignore and was not processed'.format(start=_from))
        

