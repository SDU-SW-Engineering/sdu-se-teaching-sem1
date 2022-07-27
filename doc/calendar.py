from os import listdir
import json5
from datetime import datetime
from functools import cmp_to_key

datadir = "calendar"
data = []

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

print(data)
