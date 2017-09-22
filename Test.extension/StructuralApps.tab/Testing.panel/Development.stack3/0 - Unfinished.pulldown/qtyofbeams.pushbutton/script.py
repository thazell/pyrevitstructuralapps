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

__doc__ = 'Searches Project for Overriden Dimensions'

doc = __revit__.ActiveUIDocument.Document

from Autodesk.Revit.DB import * 


cl_dims = FilteredElementCollector(doc)
cl_dims2 = FilteredElementCollector(doc)
allbeams = cl_dims.OfCategory(BuiltInCategory.OST_StructuralFraming).WhereElementIsNotElementType().ToElements()
allcolumns = cl_dims2.OfCategory(BuiltInCategory.OST_StructuralColumns).WhereElementIsNotElementType().ToElements()

print len(allbeams)
print len(allcolumns)
filename = "C:\\Temp\\WilsonVersioning\\automatereport.txt"

with open(filename, 'a') as file:
    file.writelines("Number of Columns:, " + str(len(allcolumns)) + ", " + "Number of Beams:, " + str(len(allbeams)))

    
    
    
#call another python script.  here's a sample
"""import subprocess
subprocess.call("test1.py", shell=True)"""