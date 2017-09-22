"""
Copyright (c) 2014-2016 Gui Talarico
Written for pyRevit
TESTED API: 2015 | 2016

Copyright (c) 2014-2017 Ehsan Iran-Nejad
Python scripts for Autodesk Revit
TESTED API: 2015 | 2016

Copyright (c) 2014-2017 Timon Hazell
Python scripts for Autodesk Revit
TESTED API: 2015 | 2016

This file is part of pyRevit repository at https://github.com/eirannejad/pyRevit

pyRevit is a free set of scripts for Autodesk Revit: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 3, as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See this link for a copy of the GNU General Public License protecting this package.
https://github.com/eirannejad/pyRevit/blob/master/LICENSE
"""

# Original Code by dp-stuff.org
# http://dp-stuff.org/revit-view-underlay-property-python-problem/


from Autodesk.Revit.UI import TaskDialog

from scriptutils.userinput import SelectFromList
from scriptutils import logger, this_script
import os
import clr
import shutil
import datetime

from os.path import basename

from System.Collections.Generic import *

import Autodesk
from Autodesk.Revit.DB import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

#TaskDialog.Show('Not working', "programming isn't done yet")


def UnloadRevitLinksandFlagasTransmitted(location):
#  This method will set all Revit links to be unloaded the next time the document at the given location is opened. 
#  The TransmissionData for a given document only contains top-level Revit links, not nested links.
#  However, nested links will be unloaded if their parent links are unloaded, so this function only needs to look at the document's immediate links. 
    # access transmission data in the given Revit file
    transData = TransmissionData.ReadTransmissionData(location);
    if not transData is None:
        # collect all (immediate) external references in the model
        externalReferences = transData.GetAllExternalFileReferenceIds();
        # find every reference that is a link
        for refId in externalReferences:
            extRef = transData.GetLastSavedReferenceData(refId)
            if (extRef.ExternalFileReferenceType == ExternalFileReferenceType.RevitLink):
                # we do not want to change neither the path nor the path-type
                # we only want the links to be unloaded (shouldLoad = false)
                transData.SetDesiredReferenceData(refId, extRef.GetPath(), extRef.PathType, False);
        # make sure the IsTransmitted property is set 
        transData.IsTransmitted = True
        # modified transmission data must be saved back to the model
        return transData
    else:
        Autodesk.Revit.UI.TaskDialog.Show("Unload Links", "The document does not have any transmission data")


#transmit active file?

#NY Locations:
#central file at \\drawings\BIM central\...
#\\drawings\Milestones\transmission type... ( I am going to ignore for  a time and make a task dialog stating the file should be manually copied and renamed if needed)
#\\drawings\Model to Upload\today's date...

#DC Locations:
#central file at \\drawings\...
#\\drawings\Submissions
#\\drawings\Model to Upload
#\\drawings\BIM for Exchange


filepathstring = ModelPathUtils.ConvertModelPathToUserVisiblePath(doc.GetWorksharingCentralModelPath())
dirpath, filename = os.path.split(filepathstring)
newpath = dirpath + "\Model to Upload"
if not os.path.exists(newpath):
    os.makedirs(newpath)
    

#add date and time to and central file name subdirectory
today = datetime.datetime.today()
currenttime =  today.strftime('%Y-%m-%d_%H.%M.%S')
    #W3252-S16-CENTRAL_2017-07-06_18.30.40
filenameonly, file_extension = os.path.splitext(filename)
    #W3252-S16-CENTRAL_currenttime
newsubdirectoryname = filenameonly + "_" + currenttime
newsubdirectory = newpath + '\\' + newsubdirectoryname
if not os.path.exists(newsubdirectory):
    os.makedirs(newsubdirectory)

newfilepath = newsubdirectory + '\\' + filename


#copy the central file to the path
shutil.copyfile(filepathstring, newfilepath)

#using the copied file, unload the links and set detach flag
filepath = ModelPathUtils.ConvertUserVisiblePathToModelPath(newfilepath)
transSettings = UnloadRevitLinksandFlagasTransmitted(filepath)
TransmissionData.WriteTransmissionData(filepath,transSettings)

TaskDialog.Show("File is Ready:", "Your file is ready to be sent outside our office: \n 1. Please rename the file if required. \n 2. The file should be manually copied to a milestones or submissions folder if this is a deadline submission.")
TaskDialog.Show("File is Ready:", '"'+newfilepath+'"')
os.startfile('"'+newsubdirectory+'"')
