import cal

filename = "tables/semesterplan.tex"
headercolor = "blue!25"


def escape (text):
  return text.replace("#", "\\#")

def prettyfy_date (text):
  parts = text.split(" ")
  return "%s %s" % (parts[1][:3], parts[2])

def filter_function (entry):
  if not (entry["key"] in ["OOP", "COS", "SDA"]): return True
  
  return "fillcolor" in entry

def build ():
  cols = [
#    {
#      "alignment": "l",
#      "title":     "Fase",
#      "extractor": lambda e: e["phase"] if "phase" in e else None,
#      "blank":     "",
#    },
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
      "extractor": lambda e: escape("\n\n".join(e["description"])) if "description" in e else None,
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
  headlines = [
#    {
#      "date":  "2023 August 7",
#      "title": "Før semesterstart (uge 32-34)",
#      "fillcolor": headercolor,
#    },
    {
      "date":  "2024 August 31",
      "title": "Projektstart (uge 36-38)",
      "fillcolor": headercolor,
    },
    {
      "date":  "2024 September 23",
      "title": "Problemanalysefase (Uge 39-40)",
      "fillcolor": headercolor,
    },
    {
      "date":  "2024 October 6",
      "title": "Gennemførselsfase - programudvikling (41-48)",
      "fillcolor": headercolor,
    },
    {
      "date":  "2024 December 1",
      "title": "Afleveringsfase (49-50)",
      "fillcolor": headercolor,
    },
    {
      "date":  "2025 January 1",
      "title": "Eksamen og refleksion",
      "fillcolor": headercolor,
    },
  ]
  return cal.produce_table(cols, filterfun=filter_function, filename=filename, headlines=headlines)
