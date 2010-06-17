from django.conf import settings


class QikLog(object):
    """
    A simplified logger that is preconfigured for our Django environment.

    from qiklog import QikLog
    logger = QikLog('latimes.whatever', 'debug')
    logger.log.info('...')
    """

    def __init__(self, logname, level='DEBUG',
        formatter='%(asctime)s|%(levelname)s|%(message)s'):

        # Import all the bizness
        import os
        import logging as l
        import logging.handlers as h
        self.logging = l

        # Create the file handler
        self.logname = logname
        self.logpath = os.path.join(settings.LOG_DIRECTORY, self.logname)
        self.logfile = self.logging.FileHandler(self.logpath)
        self.formatter = self.logging.Formatter(formatter)
        self.logfile.setFormatter(self.formatter)
        
        # Create the log handler
        self.log = self.logging.getLogger(self.logname)

        # Attach the file handler
        self.log.addHandler(self.logfile)

        # Set the debug level
        self.level = getattr(self.logging, level.upper())
        self.log.setLevel(self.level)

        # Turn on console stream and lower debug level if in development mode
        if settings.DEBUG:
            self.printer = self.logging.StreamHandler()
            self.printer.setLevel(self.logging.NOTSET)
            self.log = self.logging.getLogger(self.logname)
            self.log.addHandler(self.printer)



