# Load Django, if you have it.

try:
    from django.conf import settings
except:
    settings = None


class QikLog(object):
    """
    A simplified logger that is preconfigured for a Django environment.

    from qiklog import QikLog
    logger = QikLog('latimes.whatever')
    logger.log.info('Info...')
    logger.log.debug('Debug...')
    """

    def __init__(self, logname=None, level='DEBUG',
        formatter='%(asctime)s|%(levelname)s|%(message)s',
        force_debug_mode=False):

        if not logname:
            raise ValueError('first argument must be the name of logfile.')
        if not isinstance(logname, basestring):
            raise ValueError('first argument must be a string')

        # Import all the bizness
        import os
        import sys
        import logging as l
        self.log = l

        # Create the file handler
        self.logname = logname
        self.logdir = getattr(settings,
            'LOG_DIRECTORY',
            os.path.join(os.path.dirname(__file__), 'logs')
        )
        # If settings.LOG_DIRECTORY doesn't exist,
        # try to create it. OSError.errno == 17 means
        # the directory exists, which is hunky dory.
        # If not 17 or an OSError, raise the original.
        try:
            os.makedirs(self.logdir)
        except OSError, e:
            if e.errno == 17:
                pass
            else:
                raise e
        self.logpath = os.path.join(self.logdir, self.logname)
        
        # Set the debug level
        self.level = getattr(self.log, level.upper())
        
        # If we're in debug mode, configure to print to stdout
        if getattr(settings, 'DEBUG', None) and not force_debug_mode:
            self.log.basicConfig(
                stream=sys.stdout,
                format=formatter,
                level=self.log.NOTSET,
            )
        # If we're not in debug, print to the log file
        else:
            self.log.basicConfig(
                filename=self.logpath,
                format=formatter,
                level=self.level,
            )
    
    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.__str__())
    
    def __str__(self):
        return self.__unicode__().encode("utf-8")
    
    def __unicode__(self):
        return unicode(self.logname)


