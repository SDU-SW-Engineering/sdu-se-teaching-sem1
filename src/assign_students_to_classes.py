#!/usr/bin/env python3

from openpyxl import load_workbook

from random import seed, randint

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

class2student = {}
teacher2class = {
  "Aslak": [1, 3, 5],
  "Peter": [2, 4, 6],
}

wb = load_workbook(filename=input_filename)
for sheet_name in sheet_names:
  sheet = wb[sheet_name]
  sheet["E1"].value = "Klasse"
  
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

wb.save(output_filename)

statlines = []
for teachername in teacher2class:
  for classname in teacher2class[teachername]:
    for studentname in class2student[classname]:
      statlines.append("%s,%s,%s" % (teachername, classname, studentname))

with open(stats_filename, "w") as fo:
  fo.writelines(map(lambda line: "%s\n"%line, statlines))

