# Load Django, if you have it.
try:
    from django.conf import settings
    if not settings.configured:
        settings = None
except:
    settings = None


class QikLog(object):
    """
    A simplified logger that is preconfigured for a Django environment.

    from qiklog import QikLog
    logger = QikLog('latimes.whatever')
    logger.log.info('Info...')
    logger.log.debug('Info...')

    # Test the first var.
    # Make a __str__ and __repr__ functions
    """

    def __init__(self, logname=None, level='DEBUG',
        formatter='%(asctime)s|%(levelname)s|%(message)s'):

        if not logname:
            raise ValueError('first argument must be the name of logfile.')
        if not isinstance(logname, basestring):
            raise ValueError('first argument must be a string')

        # Import all the bizness
        import os
        import logging as l
        self.logging = l

        # Create the file handler
        self.logname = logname
        self.logdir = getattr(settings, 'LOG_DIRECTORY', os.path.dirname(__file__))
        self.logpath = os.path.join(self.logdir, self.logname)
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
        if getattr(settings, 'DEBUG', None):
            self.printer = self.logging.StreamHandler()
            self.printer.setLevel(self.logging.NOTSET)
            self.log = self.logging.getLogger(self.logname)
            self.log.addHandler(self.printer)



