"""
Copyright Silman 2017

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

import os
import datetime
from Autodesk.Revit.DB import * 
from Autodesk.Revit.UI import *

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


doclocations = []

#this is a text file that lists all the models to open
filename = "C:\\Temp\\NCMVersioning\\file_list_fullall.txt"

#this is the folder where the exported data file will live
folder = "C:\\Temp\\NCMVersioning\\"

#open the text file and extract each line as a doclocation to run
with open(filename, 'r') as settingsfile:
    for line in settingsfile:
        doclocations.append(line.rstrip())

print("Running on " + str(len(doclocations)) + " files.")

uiapp = __revit__.Application

#set open options to detached
opt = OpenOptions()
opt.DetachFromCentralOption = DetachFromCentralOption.DetachAndPreserveWorksets
    

#for each document run the following code
i = 0
for doclocation in doclocations:
    i = i+1
    print str(i) + " - " + doclocation
    #convert string path to revit model path 
    filepath = ModelPathUtils.ConvertUserVisiblePathToModelPath(doclocation)
    #using the copied file, unload the links
    transSettings = UnloadRevitLinks(filepath)
    TransmissionData.WriteTransmissionData(filepath,transSettings)
    #try background open
    doc = uiapp.OpenDocumentFile(filepath, opt)
    
    #repeated commands for any file
    cl_dims = FilteredElementCollector(doc)
    cl_dims2 = FilteredElementCollector(doc)
    allbeams = cl_dims.OfCategory(BuiltInCategory.OST_StructuralFraming).WhereElementIsNotElementType().ToElements()
    allcolumns = cl_dims2.OfCategory(BuiltInCategory.OST_StructuralColumns).WhereElementIsNotElementType().ToElements()
    file_name = doclocation
    mtime = os.path.getmtime(file_name)
    ctime = os.path.getctime(file_name)
    formattedmodifieddatestamp = datetime.date.fromtimestamp(mtime)
    formattedcreateddatestamp = datetime.date.fromtimestamp(ctime)
    print len(allbeams)
    print len(allcolumns)
    filename = folder + "automatereport.txt"
    with open(filename, 'a') as file:
        file.writelines("DateTime Modified:, " + str(formattedmodifieddatestamp) + ", DateTime Created:, " + str(formattedcreateddatestamp) + ", Number of Columns:, " + str(len(allcolumns)) + ", Number of Beams:, " + str(len(allbeams)) + " , FileLocation:, " + doclocation + "\n")
        
    #call another python script.  here's a sample
    """import subprocess
    subprocess.call("test1.py", shell=True)"""
    #close Revit background file
    doc.Close(False)

