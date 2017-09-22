"""Reloads/Updates to the Current Release from a Network Location"""

from pyrevit.coreutils.logger import get_logger
from pyrevit.loader.sessionmgr import load_session

# noinspection PyUnresolvedReferences
logger = get_logger(__commandname__)




# re-load pyrevit session.
logger.info('Reloading....')

import subprocess

p = subprocess.Popen(r'start cmd /c "\\dcfs\engineering\Revit\Revit Development\PyRevit\ManagementScripts\InstallTestingExtension.bat"', shell=True)

p.wait()


load_session()

print 'done'

