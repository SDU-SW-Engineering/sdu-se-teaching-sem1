import cal

filename = "tables/projectdescription.tex"

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
    "alignment": "l",
    "title":     "Description",
    "extractor": lambda e: e["description"][0] if "description" in e else None,
    "blank":     "",
  },
]
  return cal.produce_table(cols, filterfun=None, filename=filename)
