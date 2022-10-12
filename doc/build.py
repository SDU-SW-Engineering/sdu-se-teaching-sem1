#!/usr/bin/env python3

from makeish import *
import cal.projectdescription as projectdescription
import cal.semesterplan as semesterplan
import cal.project_phase1_start as project_phase1_start
import cal.project_phase2_analyse as project_phase2_analyse
import cal.project_phase3_programudvikling as project_phase3_programudvikling

from subprocess import Popen, STDOUT, PIPE, run
import shutil
import subprocess
import sys

# local imports
import cal

def system (command, logfile='makeish.log'):
    print('%s >> %s' % (command, logfile))
    p = Popen('%s >> %s' % (command, logfile), shell=True, stderr=STDOUT, stdout=PIPE)
    return_code = p.wait()
#    print("return code: "+str(return_code))
    return return_code

def system_win (command, logfile='makeish.log'):
    #print('%s >> %s' % (command, logfile))
    p = Popen(command, shell=False)
    return_code = p.wait()
    return return_code

def systempipe (command, logfile='makeish.log'):
    p = Popen('%s >> %s 2>&1' % (command, logfile), shell=True, stderr=STDOUT, stdout=PIPE)
    return_code = p.wait()
    return return_code

document_prefix = "SDU SEST 2022 Semester 1"
document_names = {
  "Project Description": {
    "source": "projectdescription.tex",
    "dependencies": {
      projectdescription.filename: lambda: projectdescription.build(),
    },
  },
  "Krav til Projektaflevering": {
    "source": "project_handin_requirements.tex",
  },
  "Semester Plan": {
    "source": "semesterplan.tex",
    "dependencies": {
      semesterplan.filename: lambda: semesterplan.build(),
    },
  },
  "Semester Handbook": {
    "source": "handbook.tex",
    "includetoc": False,
  },
  "Book List": {
    "source": "bogliste.tex",
  },
  "Indkaldelse til Midtvejsevaluering (Grupperepræsentantmøde)": {
    "source": "midwayeval.tex",
  },
  "Kontaktoplysninger": {
    "source": "contact.tex",
  },
  "ProOnline Literature": {
    "source": "kursuslitteratur.tex",
  },
  "Semester Project": {
    "source": "semesterprojekt.tex",
  },
  "Semester Project Fase 1 Projektstart": {
    "source": "project_phase1_start.tex",
    "dependencies": {
      project_phase1_start.filename: lambda: project_phase1_start.build(),
    },
  },
  "Semester Project Fase 2 Problemanalyse": {
    "source": "project_phase2_analyse.tex",
    "dependencies": {
      project_phase2_analyse.filename: lambda: project_phase2_analyse.build(),
    },
  },
  "Semester Project Fase 3 Programudvikling": {
    "source": "project_phase3_programudvikling.tex",
    "dependencies": {
      project_phase3_programudvikling.filename: lambda: project_phase3_programudvikling.build(),
    },
  },
  "ProOnline Course Material": {
    "source": "kursusmaterialer.tex",
  },
  "ProOnline Course Explanation": {
    "source": "kursusbeskrivelse.tex",
  },
  "ProOnline Course Handbook": {
    "source": "kursushandbook.tex",
  },
  "ProOnline Agreement Example": {
    "source": "samarbejdeEksempel.tex",
  },
  "ProOnline Problem Formulation": {
    "source": "problemformuleringer.tex",
  },
  "ProOnline Project Problems": {
    "source": "projektproblemer.tex",
  },
  "ProOnline Project Foundation": {
    "source": "projektgrundlag.tex",
  },
   "ProOnline Reference Technique": {
    "source": "referatteknik.tex",
  },
   "ProOnline Rubric Example": {
    "source": "rubriceksempel.tex",
  },
}

class RecipeTexTable (Recipe):
  pattern = re.compile("tables/(.+).tex$")
  
  def __init__ (self, target):
    super(RecipeTexTable, self).__init__(target)
  
  def extract_deps (self, mo):
    filename = mo.group(0)
    print("EXTRACT_DEPS filename="+filename)
    for key in document_names:
      entry = document_names[key]
      if "dependencies" in entry and filename in entry["dependencies"]:
        self.builder = entry["dependencies"][filename]
        return []
    
    return None
  
  def build_python (self):
    self.builder()
  
  def build_linux (self):
    self.build_python()
  
  def build_windows (self):
    self.build_python()

class RecipeTexDocument (Recipe):
  pattern = re.compile("(.+).pdf$")
  
  def __init__ (self, target):
    super(RecipeTexDocument, self).__init__(target)
  
  def build_linux (self):
    for _ in range(2):
      retcode = system(self.command_linux)
      if retcode==0:
        shutil.move(self.build_filename, self.target_filename)
      if retcode!=0: return "error"
    return "new"
  
  def build_windows (self):
    for _ in range(2):
      try:
       retcode = system_win(self.command_win)
       #print(self.command_win)
       print(" ".join(self.command_win))
       #subprocess.run(self.command_win)
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
    deps = list(entry["dependencies"].keys()) if "dependencies" in entry else []
    input_filename = entry["source"]
    self.target_filename = "%s.pdf" % basename
    self.build_filename  = "%s.pdf" % input_filename[:-4]
    title = elements[1]
    subtitle = elements[0]
    includetoc = entry["includetoc"] if "includetoc" in entry else False
    tocwrapper = "\\newcommand\\tableofcontentswrapper[0]{%s}" % ("\\tableofcontents" if includetoc else "")
    latexcode = "\"\\newcommand\\documenttitle[0]{%s} \\newcommand\\documentsubtitle[0]{%s} %s \\input{%s}\"" % (title, subtitle, tocwrapper, input_filename)
    
    self.command_linux = "pdflatex -shell-escape %s" % (latexcode) #  -interaction=nonstopmode
    self.command_win = ['pdflatex', '-interaction=nonstopmode', latexcode]
    
    if sys.platform=="win32":
      print(self.command_win)
      print(latexcode)
      print(latexcode.replace("\\\\", "\\"))
      print(" ".join(self.command_win))
    
    
    return ["shared.tex", input_filename]+deps

add_recipe(RecipeTexTable)
add_recipe(RecipeTexDocument)
set_default(list(map(lambda key: ("%s - %s.pdf"%(document_prefix, key)).replace(" ", " "), document_names)))

main()

