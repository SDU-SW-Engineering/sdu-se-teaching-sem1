#!/usr/bin/env python3

from openpyxl import load_workbook

from random import seed, randint

GROUPS_PER_CLASS = 5

seed(10)

def permute_list (old_list):
  new_list = []
  
  while len(old_list)>0:
    i = randint(0,len(old_list)-1)
    new_list.append(old_list[i])
    old_list = old_list[:i] + old_list[i+1:]
  
  return new_list

input_filename  = 'Lister SI1-OOP19.xlsx'
output_filename = 'Lister SI1-OOP19 med klasser.xlsx'
stats_filename  = 'Lister SI1-OOP19 med klasser.txt'
tex_filename    = 'Lister SI1-OOP19 med klasser.tex'

sheet_names = [
  "Software Engineering",
  "Software teknologi",
  "Spiludvikling og Læringsteknolo",
]

classes = {
  "Software Engineering": [1, 2],
  "Software teknologi": [3, 4],
  "Spiludvikling og Læringsteknolo": [5, 6],
}

student2sheet = {}
student2row = {}
class2student = {}
student2group = {}
teacher2class = {
  "Aslak": [1, 3, 5],
  "Peter": [2, 4, 6],
}
group2room = {
  "1.1": "Ø27-507-2",
  "1.2": "Ø27-508-2",
  "1.3": "Ø27-512a-2",
  "1.4": "Ø27-512-2",
  "1.5": "Ø27-601a-2",
  "2.1": "Ø30-508-2",
  "2.2": "Ø30-508a-2",
  "2.3": "Ø31-508-2",
  "2.4": "Ø31-508a-2",
  "2.5": "Ø31-508b-2",
  "3.1": "Ø27-605-2",
  "3.2": "Ø32-511-2",
  "3.3": "Ø32-512-2",
  "3.4": "Ø32-512a-2",
  "3.5": "Ø32-600-2",
  "4.1": "Ø32-600a-2",
  "4.2": "Ø32-601-2",
  "4.3": "Ø32-602-2",
  "4.4": "Ø32-602a-2",
  "4.5": "Ø32-603-2",
}

# load
wb = load_workbook(filename=input_filename)

# insert classes
for sheet_name in sheet_names:
  sheet = wb[sheet_name]
  sheet["E1"].value = "Klasse"
  if sheet_name!="Spiludvikling og Læringsteknolo":
    sheet["F1"].value = "Gruppe"
  
  rows = []
  for row in range(2, 200):
    if sheet["A%d"%row].value==None:
      break
    
    rows.append(row)
  
  rows = permute_list(rows)
  for rowi in range(len(rows)):
    row = rows[rowi]
    
    classname = classes[sheet_name][rowi%len(classes[sheet_name])]
    studentname = "%s %s" % (sheet["B%d" % row].value, sheet["C%d" % row].value)
    
    sheet["E%d" % row].value = classes[sheet_name][rowi%len(classes[sheet_name])]
    
    if not classname in class2student:
      class2student[classname] = []
    class2student[classname].append(studentname)
    student2sheet[studentname] = sheet
    student2row[studentname] = row

# insert groups
for teachername in teacher2class:
  for classname in teacher2class[teachername]:
    groups = []*GROUPS_PER_CLASS
    index = 0
    for studentname in class2student[classname]:
      sheet = student2sheet[studentname]
      row   = student2row[studentname]
      group = "%d.%d" % (classname, (index%GROUPS_PER_CLASS)+1)
      student2group[studentname] = group
      if not classname in classes["Spiludvikling og Læringsteknolo"]:
        sheet["F%d" % row].value = group
      index += 1

# store
wb.save(output_filename)

# stat file creation
statlines = []
for teachername in teacher2class:
  for classname in teacher2class[teachername]:
    for studentname in class2student[classname]:
      groupname = student2group[studentname]
      statlines.append("%s,%s,%s,%s" % (teachername, classname, groupname, studentname))
with open(stats_filename, "w") as fo:
  fo.writelines(map(lambda line: "%s\n"%line, statlines))

# tex file creation
texlines = []
texlines.append("\\documentclass{article}")
texlines.append("\\usepackage[utf8]{inputenc}")
texlines.append("\\title{Software Educations 1st Semester Grouping}")
texlines.append("\\begin{document}")
texlines.append("\\maketitle")
texlines.append("Hver gruppe er blevet tildelt et grupperum alle Tirsdage kl 8-18 fra uge 37 (2022) til og med uge 4 (2023).")
texlines.append("")
texlines.append("\\textbf{Bemærk:} Hvis jeres gruppe ikke er repræsenteret i grupperummet senest 8:30 giver I afkald på grupperumsgarantien og andre har ret til at tage det i brug. På dette tidspunkt er det op til tilfældigheder om I får adgang til det i løbet af dagen.")
for education in classes:
  if education=="Spiludvikling og Læringsteknolo": continue
  texlines.append("\\section{%s}"%education)
  for classname in classes[education]:
    texlines.append("\\subsection{Klasse %s}"%classname)
    students = class2student[classname]
    
    # produce mapping
    group2students = {}
    for studentname in students:
      group = student2group[studentname]
      if not group in group2students:
        group2students[group] = []
      group2students[group].append(studentname)
    
    groups = sorted(group2students.keys())
    for groupname in groups:
      grouproom = group2room[groupname]
      texlines.append("\\subsubsection{Gruppe %s (grupperum %s)}"% (groupname,grouproom))
      texlines.append("\\begin{enumerate}")
      for studentname in group2students[groupname]:
        texlines.append("  \\item %s" % studentname)
      texlines.append("\\end{enumerate}")
      
texlines.append("\\end{document}")
with open(tex_filename, "w") as fo:
  fo.writelines(map(lambda line: "%s\n"%line, texlines))

