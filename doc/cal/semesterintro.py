import cal
from datetime import datetime
import re

filename = "tables/intro-next-steps.tex"
headercolor = "blue!25"
window = {
  "begin": datetime.strptime("2023 September 4", "%Y %B %d"),
  "end":   datetime.strptime("2023 September 10", "%Y %B %d"),
}

def escape (text):
  return text.replace("#", "\\#")

def prettyfy_date (text):
  parts = text.split(" ")
  return "%s %s" % (parts[1][:3], parts[2])

def filter_function (entry):
  print(entry)
  
  if entry["fromdate"]<window["begin"]: return False
  if entry["todate"]>window["end"]: return False
  
  if entry["key"]=="ProOnline": return True
  if entry["key"]=="Projekt":
    if "Vejledning" in entry["description"][0]: return True
  
  return False

# make the entry be compatible with beamer
def preprocess (description):
  mapper = lambda line: re.sub("begin{itemize}\[[^\]]*\]", "begin{itemize}", line)
#  mapper = lambda line: line.replace("\\\\begin{itemize}[noitemsep,leftmargin=*,topsep=0pt,partopsep=0pt]", "\\\\begin{itemize")
  new = list(map(mapper, description))
  print(str(description)+" -> "+str(new))
  return new

def build ():
  cols = [
    {
      "alignment": "r",
      "title":     "Uge",
      "extractor": lambda e: str(e["fromweek"]) if "fromweek" in e else None,
      "blank":     "",
    },
    {
      "alignment": "l",
      "title":     "Aktivitet",
      "extractor": lambda e: e["key"] if "key" in e else None,
      "blank":     "",
    },
    {
      "alignment": "p{.4\\textwidth}",
      "title":     "Beskrivelse",
      "extractor": lambda e: escape("\n\n".join(preprocess(e["description.summary"]))) if "description.summary" in e else (escape("\n\n".join(preprocess(e["description"]))) if "description" in e else None),
      "blank":     "",
    },
    {
      "alignment": "l",
      "title":     "Date",
      "extractor": lambda e: prettyfy_date(e["date"][0] if type(e["date"])==list else e["date"]) if "date" in e else None,
      "blank":     "",
    },
    {
      "alignment": "p{.2\\textwidth}",
      "title":     "Semesterteam",
      "extractor": lambda e: e["team"] if "team" in e else None,
      "blank":     "",
    },
  ]
  return cal.produce_table(cols, filterfun=filter_function, filename=filename)
