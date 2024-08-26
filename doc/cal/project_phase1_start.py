import cal
from datetime import datetime

filename = "tables/project_phase1_start.tex"
headercolor = "blue!25"
window = {
  "begin": datetime.strptime("2024 September 1", "%Y %B %d"),
  "end":   datetime.strptime("2024 September 22", "%Y %B %d"),
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
    return True
  
  return False

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
      "alignment": "p{.6\\textwidth}",
      "title":     "Beskrivelse",
      "extractor": lambda e: escape("\n\n".join(e["description"])) if "description" in e else None,
      "blank":     "",
    },
    {
      "alignment": "l",
      "title":     "Date",
      "extractor": lambda e: prettyfy_date(e["date"][0] if type(e["date"])==list else e["date"]) if "date" in e else None,
      "blank":     "",
    },
  ]
  return cal.produce_table(cols, filterfun=filter_function, filename=filename)
