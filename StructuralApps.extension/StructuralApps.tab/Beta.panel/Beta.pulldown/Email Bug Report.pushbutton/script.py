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

# __doc__ = 'Emails a Bug Report'
# import os

# import csv
# from subprocess import Popen

# import sys
# from Autodesk.Revit.UI import *
# from System.Collections.Generic import List

# uidoc = __revit__.ActiveUIDocument
# doc = __revit__.ActiveUIDocument.Document

# import clr
# clr.AddReference('RevitAPI') 
# clr.AddReference('RevitAPIUI') 
# from Autodesk.Revit.DB import * 

# dialog = TaskDialog("Decision");
# dialog.MainContent = "Export all text elements from the model?";
# dialog.CommonButtons = TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No;


# result = TaskDialog.Show(dialog)

# if result == TaskDialogResult.Yes:
    # textnotes = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TextNotes).WhereElementIsNotElementType().ToElementIds()
# else:
    # curview = uidoc.ActiveGraphicalView
    # textnotes = FilteredElementCollector(doc, curview.Id).OfCategory(BuiltInCategory.OST_TextNotes).WhereElementIsNotElementType().ToElementIds()

# file_path = "c:\Temp\export.csv"
# directory = os.path.dirname(file_path)

# try:
    # os.stat(directory)
# except:
    # os.mkdir(directory)  
    
# with open(file_path, 'wb') as csvfile:
        # spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # fieldnames = ['TextNoteID', 'View', 'Text']
        # writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # writer.writeheader()
        # for t in textnotes:
            # try:    
                # writer.writerow({'TextNoteID': t.ToString(), 'Text': doc.GetElement(t).Text, 'View':doc.GetElement(doc.GetElement(t).OwnerViewId).Name  })
            # except:
                # writer.writerow({'TextNoteID': t.ToString(), 'Text': "---Text did not export: the text note contains unsupported characters---", 'View':doc.GetElement(doc.GetElement(t).OwnerViewId).Name  })
                # pass
# p = Popen(file_path, shell=True)

# # Import smtplib for the actual sending function
# import smtplib

# # Import the email modules we'll need
# from email.mime.text import MIMEText

# textfile = "c:\Temp\emailtest.txt"

# # Open a plain text file for reading.  For this example, assume that
# # the text file contains only ASCII characters.
# fp = open(textfile, 'rb')
# # Create a text/plain message
# msg = MIMEText(fp.read())
# fp.close()

# me = "hazell@silman.com"
# you = "hazell@silman.com"


# # me == the sender's email address
# # you == the recipient's email address
# msg['Subject'] = 'The contents of %s' % textfile
# msg['From'] = me
# msg['To'] = you

# # Send the message via our own SMTP server, but don't include the
# # envelope header.
# s = smtplib.SMTP('localhost')
# s.sendmail(me, [you], msg.as_string())
# s.quit()

 #!/usr/bin/python

from urllib import quote
import webbrowser

def mailto(recipients, subject, body):
    "recipients: string with comma-separated emails (no spaces!)"
    webbrowser.open("mailto:%s?subject=%s&body=%s" %
        (recipients, quote(subject), quote(body)))

body_template = """SilmanApps Developer,
I was trying to use:    .......[insert tool name here]......
Here's what happened:   .......[describe why you think a bug happened].......

Here's an image:        .......[if you got a warning include image here].....

Thanks,
"""

def gen(email):
    mailto(email, "SilmanApps Bug Report", body_template % locals())

gen("hazell@silman.com")