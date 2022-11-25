#!/usr/bin/env python3

from openpyxl import load_workbook

src_sheet_names = [
  "Software Engineering",
  "Software teknologi",
  "Spiludvikling og Læringsteknolo",
]

eduname2line = {
  "Software Engineering":            "Software Engineering",
  "Software teknologi":              "Softwareteknologi",
  "Spiludvikling og Læringsteknolo": "Spiludvikling og Læringsteknologi",
}

def groups2thold (groups):
  for group in groups:
    if len(group)==2 and group[0]=="T":
      return group
  return -1

def groups2group (groups):
  for group in groups:
    if group.startswith("Gruppe "):
      return group
  return -1

def load_datafile (filename, students=None):
  if students==None: students = []
  
  with open(filename) as fo:
    lines = fo.readlines()
  
  for line in lines:
    elements = line.split("\t")
    name   = elements[1]
    email  = elements[2]
    role   = elements[3].strip()
    groups = elements[4].split(", ")
    thold  = groups2thold(groups)
    group  = groups2group(groups)
    
    if not role in ["Studerende", "Student"]: continue
    
    student = {
      "name":  name,
      "email": email,
      "role":  role,
      "thold": thold,
      "group": group,
    }
    students.append(student)
  
  return students

def load_student_lines (filename):
  global name2line
  
  wb = load_workbook(filename=filename)
  
  for sheet_name in src_sheet_names:
    line = eduname2line[sheet_name]
    sheet = wb[sheet_name]
    
    for row in range(2, 200):
      if sheet["A%d"%row].value==None:
        
        break
      
      gname = sheet["B%d"%row].value
      fname = sheet["C%d"%row].value
      name = "%s %s" % (gname, fname)
      
      name2line[name] = line

oop_students = []
load_datafile("oop1.data", oop_students)
load_datafile("oop2.data", oop_students)

sem_students = []
load_datafile("sem1.data", sem_students)
load_datafile("sem2.data", sem_students)

name2line = {}
load_student_lines("Lister SI1-OOP19 med klasser.xlsx")

#print(oop_students)
#print(sem_students)
#print(name2line)

