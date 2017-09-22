"""Reloads/Updates to the Current Release from a Network Location"""
import subprocess

p = subprocess.Popen(r'start cmd /c "\\dcfs\engineering\Revit\Revit Development\PyRevit\InstallSilmanAppsExtension.bat"', shell=True, stdout=subprocess.PIPE)

p.wait()
from pyrevit.coreutils.logger import get_logger
from pyrevit.loader.sessionmgr import load_session

# noinspection PyUnresolvedReferences
logger = get_logger(__commandname__)

# re-load pyrevit session.
logger.info('Reloading....')

load_session()

print 'done'