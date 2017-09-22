"""


Copyright (c) 2014-2017 Timon Hazell

You can redistribute this file and/or modify
it under the terms of the GNU General Public License version 3, as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

"""

import os
import csv
from subprocess import Popen

import clr
import glob, os

from urllib import urlopen
import json

urlweb = urlopen('http://www.dynamopackages.com/packages').read()
urlpage = json.loads(urlweb)

print urlpage.get('content').get('versions')[urlpage.get('content')#.get('num_versions')-1].get('full_dependency_ids').get('name')
#urlpage.get('content')[0].get('versions')[urlpage.get('content').get('num_versions')-1].get('full_dependency_ids').get('name')