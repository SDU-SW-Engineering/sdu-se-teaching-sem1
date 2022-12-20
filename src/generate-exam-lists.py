#!/usr/bin/env python3

from openpyxl import load_workbook
from functools import cmp_to_key

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

oop_dates = [
  "Mandag den 16. Januar, 2023",
  "Tirsdag den 17. Januar, 2023",
  "Onsdag den 18. Januar, 2023",
  "Torsdag den 19. Januar, 2023",
  "Fredag den 20. Januar, 2023",
]

oop_line_order = [
  "Spiludvikling og Læringsteknologi",
  "Software Engineering",
  "Softwareteknologi",
]

group2size = {}
classes = ["1", "2", "3", "4"]

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

def load_group_sizes (students):
  global group2size
  
  for student in students:
    group = student["group"]
    
    if not group in group2size:
      group2size[group] = 0
    
    group2size[group] += 1

def import_groups (oop_students, sem_students):
  name2group = {}
  
  for entry in sem_students:
    name2group[entry['name']] = entry["group"]
  
  for entry in oop_students:
    name = entry["name"]
    entry["group"] = name2group[name] if name in name2group else "-1"

def generate_line2index ():
  line2index = {}
  
  for i in range(len(oop_line_order)):
    line = oop_line_order[i]
    line2index[line] = i
  
  return line2index

def sort_students (students):
  def compare (s1, s2):
    def strcmp (s1, s2):
      return -1 if s1<s2 else (0 if s1==s2 else 1)
    
    n1 = s1["name"]
    n2 = s2["name"]
    
    # primary
    l1 = name2line[n1] if n1 in name2line else ""
    l2 = name2line[n2] if n2 in name2line else ""
    if l1 != l2:
      return strcmp(line2index[l1], line2index[l2])
    
    # secondary
    if s1["group"] != s2["group"]:
      return strcmp(s1["group"], s2["group"])
    
    # tertiary
    return strcmp(n1, n2)
  
  students.sort(key=cmp_to_key(compare))

def generate_oop_schedules ():
    pass

def print_class_times ():
  for classname in classes:
    count = 0
    groups = []
    
    for student in sem_students:
      if student["thold"] == "T"+classname:
        count += 1
        if not student["group"] in groups:
          groups.append(student["group"])
    
    print("Class %s: %2d students in %d groups => %3d min / %1d h %s" % (classname, count, len(groups), 20*count, 20*count/60, list(map(lambda group: group2size[group]*20, groups))))

oop_students = []
load_datafile("oop1.data", oop_students)
load_datafile("oop2.data", oop_students)

sem_students = []
load_datafile("sem1.data", sem_students)
load_datafile("sem2.data", sem_students)

name2line = {}
load_student_lines("Lister SI1-OOP19 med klasser.xlsx")

load_group_sizes(sem_students)

import_groups(oop_students, sem_students)
line2index = generate_line2index()
sort_students(oop_students)

generate_oop_schedules()

#print(oop_students)
#print(sem_students)
#print(name2line)
#print(group2size)
print_class_times()

