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

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

from System.Collections.Generic import *

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

TaskDialog.Show('Not working', "programming isn't done yet")

def getNames(z_element):
	z_elementname = []
	for e in z_element:
		z_elementname.append(e.Name)
	return z_elementname

def UnloadRevitLinks(location):
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

filepathstring = "C:\Revit Local Files\W3292-S16\W3292-S16_hazell.rvt"

links = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RvtLinks).WhereElementIsNotElementType().ToElements()
TaskDialog.Show("Number of nodes selected", "nodes - " + str(len(links)))

#makes display to select the link
options = sorted(getNames(links))
if options:
    selected_fromlist = SelectFromList.show(options)
    logger.debug('Selected symbols are: {}'.format(selected_fromlist))
    if selected_fromlist:
        if len(selected_fromlist)==1:
            for item in selected_fromlist:
                for l in links:
                    if item == l.Name:
                        selectedlink = l
                        TaskDialog.Show('Link: ', l.Name)
        else:
            TaskDialog.Show('pyRevit', 'You must select only one link.')
            sys.exit
else:
    TaskDialog.Show('pyRevit', 'You must select one item')



#transmit active file?

#NY Locations:
#central file at \\drawings\BIM central\...
#\\drawings\Milestones\transmission type... ( I am going to ignore for  a time and make a task dialog stating the file should be manually copied and renamed if needed)
#\\drawings\Model to Upload\today's date...

#DC Locations:
#central file at \\drawings\...
#\\drawings\Submissions
#\\drawings\Model to Upload



hostpathstring = ModelPathUtils.ConvertModelPathToUserVisiblePath(doc.GetWorksharingCentralModelPath())
linkpathstring = ModelPathUtils.ConvertModelPathToUserVisiblePath(selectedlink.PathName)
TaskDialog.Show("Link Location:", linkpathstring)
"""
dirpath, filename = os.path.split(filepathstring)
newpath = dirpath + "\Model to Transfer"
if not os.path.exists(newpath):
    os.makedirs(newpath)
    
filepathstring = shutil.copyfile(filepathstring, newpath + '\\' + filename)

dirpath, filename = os.path.split(filepathstring)

filepath = ModelPathUtils.ConvertUserVisiblePathToModelPath(filepathstring)


TransmissionData.WriteTransmissionData(filepath,UnloadRevitLinks(filepath))

TaskDialog.Show("File is Ready:", "Your file is ready to be sent outside our office: \n 1. Please rename the file if required. \n 2. The file should be manually copied to a milestones or submissions folder if this is a deadline submission.")
TaskDialog.Show("File is Ready:", '"'+dirpath+'"')
os.startfile('"'+dirpath+'"')
"""
