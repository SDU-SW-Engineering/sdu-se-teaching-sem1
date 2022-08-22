from os import listdir
import json5
from datetime import datetime
from functools import cmp_to_key

datadir = "cal"
data = []

#################################################################### query resolver

def produce_table (cols, filterfun=None, filename=None):
  lines = []
  
  entries = data
  if not filterfun==None:
    entries = list(filter(filterfun, data))
  
  # construct alignment string
  alignment = ""
  for col in cols:
    alignment += "|%s" % col["alignment"]
  alignment += "|"
  
  # produce contents: environment begin
  lines.append("\\begin{tabular}{%s}" % alignment)
  
  # produce contents: header
  lines.append("  \\hline")
  header = []
  for col in cols:
    header.append("\\emph{%s}" % col["title"])
  lines.append("  "+(" & ".join(header))+" \\\\")
  lines.append("  \\hline")
  
  # produce contents: entries
  for entry in entries:
    entryline = []
    for col in cols:
      extractor = col['extractor']
      extracted = extractor(entry)
      entryline.append(col['blank'] if extracted==None else extracted)
    lines.append("  "+(" & ".join(entryline))+" \\\\")
    lines.append("  \\hline")
  
  # produce contents: environment end
  lines.append("\\end{tabular}")
  
  # convert to string
  lines = list(map(lambda line: "%s\n"%line, lines))
  
  # option: export to file
  if filename!=None:
    with open(filename, "w") as fo:
      fo.writelines(lines)
  
  # return lines
  return lines

##################################################################### autoload data

def init ():
  global data
  
  filenames = list(filter(lambda f: f.endswith(".json"), listdir(datadir)))
  
  for filename in filenames:
    full_filename = "%s/%s"%(datadir, filename)
    print("Loading '%s' ..." % full_filename)
    with open(full_filename) as fo:
      lines = "".join(fo.readlines())
      contents = json5.loads(lines)
      
      for key in contents:
        entries = contents[key]
        for entry in entries:
#          print(entry)
          entry["key"] = key
          if type(entry["date"]) == list:
            entry["fromdate"] = datetime.strptime(entry["date"][0], "%Y %B %d")
            entry["todate"]   = datetime.strptime(entry["date"][1], "%Y %B %d")
          else:
            dt = datetime.strptime(entry["date"], "%Y %B %d")
            entry["fromdate"] = dt
            entry["todate"]   = dt
          entry["fromweek"] = int(entry["fromdate"].strftime("%V"))
          entry["toweek"]   = int(entry["todate"].strftime("%V"))
          data.append(entry)
  
  def compare (a, b):
    if a["fromdate"] != b["fromdate"]:
      return (a["fromdate"] - b["fromdate"]).total_seconds()
    if a["todate"] != b["todate"]:
      return (a["todate"] - b["todate"]).total_seconds()
    if a["key"] != b["key"]:
      return -1 if a["key"] < b["key"] else 1
    return 0
  
  data.sort(key=cmp_to_key(compare))

init()

#print(data)

#cols = [
#  {
#    "alignment": "r",
#    "title":     "Date",
#    "extractor": lambda e: (e["date"][0] if type(e["date"])==list else e["date"]) if "date" in e else None,
#    "blank":     "",
#  },
#  {
#    "alignment": "c",
#    "title":     "Domain",
#    "extractor": lambda e: e["key"] if "key" in e else None,
#    "blank":     "",
#  },
#  {
#    "alignment": "l",
#    "title":     "Description",
#    "extractor": lambda e: e["description"][0] if "description" in e else None,
#    "blank":     "",
#  },
#]
#produce_table(cols, filterfun=None, filename="sample_calendar_output.tex")
