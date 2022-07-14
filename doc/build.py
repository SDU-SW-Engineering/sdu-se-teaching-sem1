#!/usr/bin/env python3

from makeish import *
from subprocess import Popen, STDOUT, PIPE, run
import shutil
#import pdflatex
import subprocess

def system (command, logfile='makeish.log'):
    print('%s >> %s' % (command, logfile))
    p = Popen('%s >> %s' % (command, logfile), shell=True, stderr=STDOUT, stdout=PIPE)
    return_code = p.wait()
    return return_code

def systempipe (command, logfile='makeish.log'):
    p = Popen('%s >> %s 2>&1' % (command, logfile), shell=True, stderr=STDOUT, stdout=PIPE)
    return_code = p.wait()
    return return_code

document_prefix = "SDU SEST 2022 Semester 1"
document_names = {
  "Bogliste": {
    "source": "bogliste.tex",
    "topic": "Semester Information"
  },
  "Kontaktoplysninger": {
    "source": "contact.tex",
    "topic": "Semester Information"
  },
  "Project Description": {
    "source": "projectdescription.tex",
  },
  "Semesterhåndbog": {
    "source": "handbook.tex",
    "topic": "Semester Information"
  },
}

class RecipeTexDocument (Recipe):
  pattern = re.compile("(.+).pdf$")
  
  def __init__ (self, target):
    super(RecipeTexDocument, self).__init__(target)
  
  def build_linux(self):
    retcode = system(self.command_linux)
    if retcode==0:
      shutil.move(self.build_filename, self.target_filename)
    return "new" if retcode==0 else "error"

  def build_windows(self):
    try:
#     print(self.command)
     subprocess.run(self.command_windows)
    except subprocess.CalledProcessError:
     return "error"
    return "new"

  def extract_deps (self, mo):
    basename = mo.group(1)
    elements = basename.split(" - ")
    if not len(elements) == 2:
      print("Error: Format error in '%s'. Returning None!" % basename)
      return None
    rhs = elements[-1]
    if not rhs in document_names:
      print("Error: Unknown entry '%s'. Returning None!" % rhs)
      return None
    entry = document_names[rhs]
    input_filename = entry["source"]
    self.target_filename = "%s.pdf" % basename
    self.build_filename  = "%s.pdf" % input_filename[:-4]
    self.command_linux = "pdflatex -shell-escape %s" % (input_filename)
    self.command_windows = ['pdflatex', '-interaction=nonstopmode', input_filename]
    return ["shared.tex", input_filename]

add_recipe(RecipeTexDocument)
set_default(list(map(lambda key: ("%s - %s.pdf"%(document_prefix, key)).replace(" ", " "), document_names)))

main()

