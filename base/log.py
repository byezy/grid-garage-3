import contextlib
import functools
import os
import inspect
import logging


APPDATA_PATH = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "GridGarage")
LOG_FILE = os.path.join(APPDATA_PATH, "gridgarage.log")


def make_tuple(ob):

    return ob if isinstance(ob, (list, tuple)) else [ob]


def debug(message):

    message = make_tuple(message)

    for msg in message:
        try:
            logging.getLogger("gridgarage").debug(msg)
        except:
            print "DEBUG: " + str(msg)


def info(message):

    message = make_tuple(message)

    for msg in message:
        try:
            logging.getLogger("gridgarage").info(msg)
        except:
            print "INFO: " + str(msg)


def warn(message):

    message = make_tuple(message)

    for msg in message:
        try:
            logging.getLogger("gridgarage").warn(msg)
        except:
            print "WARN: " + str(msg)


def error(message):

    message = make_tuple(message)

    for msg in message:
        try:
            logging.getLogger("gridgarage").error(msg)
        except:
            print "ERROR: " + str(msg)


class ArcStreamHandler(logging.StreamHandler):
    """ Logging handler to log messages to ArcGIS """

    def __init__(self, messages):

        logging.StreamHandler.__init__(self)

        self.messages = messages

    def emit(self, record):
        """ Emit the record to the ArcGIS messages object

        Args:
            record (): The message record

        Returns:

        """

        msg = self.format(record)
        msg = msg.replace("\n", ", ").replace("\t", " ").replace("  ", " ")
        lvl = record.levelno

        if lvl in [logging.ERROR, logging.CRITICAL]:
            self.messages.addWarningMessage(msg)

        elif lvl == logging.WARNING:
            self.messages.addWarningMessage(msg)

        else:
            self.messages.addMessage(msg)

        return


def configure_logging(arc_messages):

    if not os.path.exists(LOG_FILE):

        if not os.path.exists(APPDATA_PATH):
            arc_messages.AddMessage("Creating app data path {}".format(APPDATA_PATH))
            os.makedirs(APPDATA_PATH)

        arc_messages.AddMessage("Creating log file {}".format(LOG_FILE))
        open(LOG_FILE, 'a').close()

    logger = logging.getLogger('gridgarage')

    if len(logger.handlers):  # then this has already been done for this logger instance
        return

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(fmt="%(asctime)s.%(msecs)03d %(levelname)s %(module)s %(funcName)s %(lineno)s %(message)s", datefmt="%Y%m%d %H%M%S")

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.debug("FileHandler added")

    ah = ArcStreamHandler(arc_messages)
    ah.setLevel(logging.INFO)
    logger.addHandler(ah)
    logger.debug("ArcLogHandler added")

    logger.debug("Logging configured")

    return


@contextlib.contextmanager
def error_trap(context):

    """ A context manager that traps and logs exception in its block.
        Usage:
        with error_trapping('optional description'):
            might_raise_exception()
        this_will_always_be_called()
    """

    idx = getattr(context, "__name__", None)
    if not idx:
        idx = getattr(context, "name", None)
    if not idx:
        idx = inspect.getframeinfo(inspect.currentframe())[2]

    _in = "IN context= " + idx
    _out = "OUT context= " + idx

    try:
        debug(_in)
        yield
        debug(_out)
    except Exception as e:
        error(str(e))
        raise e

    return


def log_error(f):
    """ A decorator to trap and log exceptions """

    @functools.wraps(f)
    def log_wrap(*args, **kwargs):

        debug(str(dir(f)))

        with error_trap(f):

            return f(*args, **kwargs)

    return log_wrap
