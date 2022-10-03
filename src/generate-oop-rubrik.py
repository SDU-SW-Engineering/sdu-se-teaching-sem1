#!/usr/bin/env python3

from openpyxl import load_workbook, Workbook
from openpyxl.comments import Comment
from openpyxl.styles import PatternFill, Font

input_filename = "Lister SI1-OOP19 med klasser.xlsx"
output_filename = "SDU SE OOP 2022 - Pointgivende Aktivitet 1.xlsx"

sheet_names = [
  "Software Engineering",
  "Software teknologi",
  "Spiludvikling og Læringsteknolo",
]

classcount = 6
author = "Aslak Johansen"

syntax_guide = '''
Giv følgende bedømmelse:
0: Besvarelsen indeholder intet der minder om Javakode.
1: Besvarelsen indeholder spor af Javakode med mange og betydelige fejl.
2: Besvarelsen indeholder en del korrekt Javakode med nogle fejl og mangler.
3: Besvarelsen indeholder mest syntaktisk korrekt Javakode med få eller mest ubetydelige fejl.
4: Besvarelsen indeholder syntaktisk korrekt java.
'''

rowi   = [4]*classcount
sheeti = []

iwb = load_workbook(filename=input_filename)
owb = Workbook()

# generate sheets
for i in range(classcount):
  name = 'Klasse %u'%(i+1)
  owb.create_sheet(title = name)
  sheet = owb[name]
  
  sheet["A3"].font = Font(b=True)
  sheet["A3"].value = "Fornavn"
  sheet["B3"].font = Font(b=True)
  sheet["B3"].value = "Efternavn"
  sheet.merge_cells(range_string="C1:I1")
  sheet["C1"].font = Font(b=True)
  sheet["C1"].fill = PatternFill("solid", fgColor="AAFFAA")
  sheet["C1"].value = "Opgave 9"
  sheet["C2"].font = Font(b=True)
  sheet["C2"].fill = PatternFill("solid", fgColor="CCFF88")
  sheet["C3"].font = Font(b=True)
  sheet["C3"].fill = PatternFill("solid", fgColor="CCFF88")
  sheet["C3"].value = "Syntaks"
  sheet["C3"].comment = Comment(syntax_guide, author)
  sheet.merge_cells(range_string="D2:H2")
  sheet["D2"].font = Font(b=True)
  sheet["D2"].fill = PatternFill("solid", fgColor="88FFCC")
  sheet["D2"].value = "Besvarelse"
  sheet["D3"].font = Font(b=True)
  sheet["D3"].fill = PatternFill("solid", fgColor="88FFCC")
  sheet["D3"].value = "for(int i;i<10;i++)"
  sheet["D3"].comment = Comment("Erklæring af en for-løkke med initialisering af en int variabel ved navn \"i\" til værdien 0 og en continuation condition der tester om denne værdi er mindre end 10 og et update-statement der tæller værdien op med én for hvert gennemløb.\n\n0 eller 1", author)
  sheet["E3"].font = Font(b=True)
  sheet["E3"].fill = PatternFill("solid", fgColor="88FFCC")
  sheet["E3"].value = "print(i)"
  sheet["E3"].comment = Comment("Udskrivelse af værdien for variablen \"i\" i bodyen.\n\n0 eller 1", author)
  sheet["F3"].font = Font(b=True)
  sheet["F3"].fill = PatternFill("solid", fgColor="88FFCC")
  sheet["F3"].value = "int i=i"
  sheet["F3"].comment = Comment("Erklæring af en ny variabel af typen int i bodyen intialiseret til den værdi variablen \"i\" har.\n\n0 eller 1", author)
  sheet["G3"].font = Font(b=True)
  sheet["G3"].fill = PatternFill("solid", fgColor="88FFCC")
  sheet["G3"].value = "print(++j)"
  sheet["G3"].comment = Comment("Tæller den nye variabel op med én og udskriver dens værdi.\n\n0 eller 1", author)
  sheet["H3"].font = Font(b=True)
  sheet["H3"].fill = PatternFill("solid", fgColor="88FFCC")
  sheet["H3"].value = "Sum"
  sheet["I3"].font = Font(b=True)
  sheet["I2"].fill = PatternFill("solid", fgColor="AAFFAA")
  sheet["I3"].fill = PatternFill("solid", fgColor="AAFFAA")
  sheet["I3"].value = "Resultat"
  sheet.merge_cells(range_string="J1:P1")
  sheet["J1"].font = Font(b=True)
  sheet["J1"].fill = PatternFill("solid", fgColor="AAAAFF")
  sheet["J1"].value = "Opgave 10"
  sheet["J2"].font = Font(b=True)
  sheet["J2"].fill = PatternFill("solid", fgColor="CC88FF")
  sheet["J3"].font = Font(b=True)
  sheet["J3"].fill = PatternFill("solid", fgColor="CC88FF")
  sheet["J3"].value = "Syntaks"
  sheet["J3"].comment = Comment(syntax_guide, author)
  sheet.merge_cells(range_string="K2:O2")
  sheet["K2"].font = Font(b=True)
  sheet["K2"].fill = PatternFill("solid", fgColor="88CCFF")
  sheet["K2"].value = "Besvarelse"
  sheet["K3"].font = Font(b=True)
  sheet["K3"].fill = PatternFill("solid", fgColor="88CCFF")
  sheet["K3"].value = "int getLargerNumber (int arg)"
  sheet["K3"].comment = Comment("Erklæring af en metode ved navn \"getLargerNumber\", der returnerer en \"int\" og tager en \"int\" som argument.\n\n0 eller 1", author)
  sheet["L3"].font = Font(b=True)
  sheet["L3"].fill = PatternFill("solid", fgColor="88CCFF")
  sheet["L3"].value = "print(arg)"
  sheet["L3"].comment = Comment("Udskriver værdien af argumentet.\n\n0 eller 1", author)
  sheet["M3"].font = Font(b=True)
  sheet["M3"].fill = PatternFill("solid", fgColor="88CCFF")
  sheet["M3"].value = "arg++"
  sheet["M3"].comment = Comment("Øger værdien af argumentet med én.\n\n0 eller 1", author)
  sheet["N3"].font = Font(b=True)
  sheet["N3"].fill = PatternFill("solid", fgColor="88CCFF")
  sheet["N3"].value = "return(42)"
  sheet["N3"].comment = Comment("Returnerer den nye værdi.\n\n0 eller 1", author)
  sheet["O3"].font = Font(b=True)
  sheet["O3"].fill = PatternFill("solid", fgColor="88CCFF")
  sheet["O3"].value = "Sum"
  sheet["P2"].font = Font(b=True)
  sheet["P2"].fill = PatternFill("solid", fgColor="AAAAFF")
  sheet["P3"].font = Font(b=True)
  sheet["P3"].fill = PatternFill("solid", fgColor="AAAAFF")
  sheet["P3"].value = "Resultat"
  
  sheeti.append(sheet)

for sheet_name in sheet_names:
  sheet = iwb[sheet_name]
  
  for row in range(2, 200):
    if sheet["A%d"%row].value==None:
      break
    
    gname = sheet["B%d"%row].value
    fname = sheet["C%d"%row].value
    lname = sheet["C%d"%row].value
    clsname = sheet["E%d"%row].value
    grpname = sheet["F%d"%row].value
    i = int(clsname)-1
    
    osheet = sheeti[i]
    orow   = rowi[i]
    rowi[i] += 1
    
    osheet["A%d"%orow].value = gname
    osheet["B%d"%orow].value = fname
    osheet["C%d"%orow].fill = PatternFill("solid", fgColor="CCFF88")
    for letter in ["D", "E", "F", "G", "H"]:
      osheet["%s%d"%(letter, orow)].fill = PatternFill("solid", fgColor="88FFCC")
    osheet["H%d"%orow].value = "=sum(D%d:G%d)"%(orow, orow)
    osheet["I%d"%orow].fill = PatternFill("solid", fgColor="AAFFAA")
    osheet["I%d"%orow].value = "=ceiling(((C%u*25)*0.5 + (H%u*25)*0.5)*15/100, 1)"%(orow, orow)
    osheet["J%d"%orow].fill = PatternFill("solid", fgColor="CC88FF")
    for letter in ["K", "L", "M", "N", "O"]:
      osheet["%s%d"%(letter, orow)].fill = PatternFill("solid", fgColor="88CCFF")
    osheet["O%d"%orow].value = "=sum(K%d:N%d)"%(orow, orow)
    osheet["P%d"%orow].fill = PatternFill("solid", fgColor="AAAAFF")
    osheet["P%d"%orow].value = "=ceiling(((J%u*25)*0.5 + (O%u*25)*0.5)*15/100, 1)"%(orow, orow)

owb.remove(owb['Sheet'])
owb.save(output_filename)

