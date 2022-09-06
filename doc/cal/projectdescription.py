import cal

filename = "tables/projectdescription.tex"

def escape (text):
  return text.replace("#", "\\#")

def build ():
  cols = [
  {
    "alignment": "r",
    "title":     "Date",
    "extractor": lambda e: (e["date"][0] if type(e["date"])==list else e["date"]) if "date" in e else None,
    "blank":     "",
  },
  {
    "alignment": "c",
    "title":     "Domain",
    "extractor": lambda e: e["key"] if "key" in e else None,
    "blank":     "",
  },
  {
    "alignment": "p{.6\\textwidth}",
    "title":     "Beskrivelse",
    "extractor": lambda e: escape("\n\n".join(e["description"])) if "description" in e else None,
    "blank":     "",
  },
]
  return cal.produce_table(cols, filterfun=None, filename=filename)
