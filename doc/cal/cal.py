from os import listdir
import json5
from datetime import datetime
from functools import cmp_to_key

datadir = "cal"
data = []

#################################################################### helpers

def parse_date (text):
  return datetime.strptime(text, "%Y %B %d")

#################################################################### query resolver

def produce_table (cols, filterfun=None, filename=None, headlines=None):
  lines = []
  
  colcount = len(cols)
  
  entries = data
  if not filterfun==None:
    entries = list(filter(filterfun, data))
  
  # preprocess headlines
  if headlines != None:
    for headline in headlines:
      headline["date"] = parse_date(headline["date"])
    headlines.sort(key=cmp_to_key(lambda a, b: (a["date"] - b["date"]).total_seconds()))
  
  # construct alignment string
  alignment = ""
  for col in cols:
    alignment += "|%s" % col["alignment"]
  alignment += "|"
  
  # produce contents: environment begin
  lines.append("\\begin{longtable}{%s}" % alignment)
  
  # produce contents: header
  lines.append("  \\hline")
  header = []
  for col in cols:
    header.append("\\emph{%s}" % col["title"])
  lines.append("  "+(" & ".join(header))+" \\\\")
  lines.append("  \\hline")
  
  # produce contents: entries
  for entry in entries:
    rowcolor = "\\rowcolor{%s}" % entry["fillcolor"] if "fillcolor" in entry else ""
    if headlines != None:

      while len(headlines)>0 and entry["fromdate"]>headlines[0]["date"]:

        headline = headlines[0]   # extract head
        headlines = headlines[1:] # remove head
        cellcolor = "\\cellcolor{%s}" % headline["fillcolor"] if "fillcolor" in headline else ""
        lines.append("  \\multicolumn{%i}{|l|}{%s%s} \\\\" % (colcount, cellcolor, headline["title"]))
#        lines.append("  \\multicolumn{%i}*{%s%s} \\\\" % (colcount, headline["title"]))
        lines.append("  \\hline")
    entryline = []
    for col in cols:
      extractor = col['extractor']
      extracted = extractor(entry)
      entryline.append(col['blank'] if extracted==None else extracted)
    lines.append(("  %s"%rowcolor)+(" & ".join(entryline))+" \\\\")
    lines.append("  \\hline")
  
  # produce contents: environment end
  lines.append("\\end{longtable}")
  
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
    with open(full_filename) as fo:
      lines = "".join(fo.readlines())
      contents = json5.loads(lines)
      
      for key in contents:
        entries = contents[key]
        for entry in entries:
#          print(entry)
          entry["key"] = key
          if type(entry["date"]) == list:
            entry["fromdate"] = parse_date(entry["date"][0])
            entry["todate"]   = parse_date(entry["date"][1])
          else:
            dt = parse_date(entry["date"])
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
