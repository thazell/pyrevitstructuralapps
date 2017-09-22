from pyrevit.coreutils.logger import get_logger
from pyrevit.loader.sessionmgr import load_session

# noinspection PyUnresolvedReferences
logger = get_logger(__commandname__)

__doc__ = 'Searches the script folders and creates buttons for new scripts or extensions.'


# re-load pyrevit session.
logger.info('Reloading....')
load_session()
