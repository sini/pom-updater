#!/usr/bin/env python

# brew install python
# pip install beautifulsoup4
# pip install lxml
# pip install pytidylib

import sys
import bs4
from tidylib import tidy_document

def update_platform_version(dep):
  print "Parsing platform " + dep.artifactId.string
  dep.version.string = "${platform.version}"

def update_rl_version(dep):
  print "Parsing rl " + dep.artifactId.string
  if not (dep.version.string == "${project.version}" or dep.version.string.startswith("[")):
    dep.version.string = "[" + dep.version.string + ",)"

def parse_dep(dep):
  if type(dep) != bs4.element.Tag:
    return
  if dep.groupId.string.startswith("com.rocketlawyer") or dep.groupId.string.startswith("com.rocketlawyer"):
    if any(dep.artifactId.string in s for s in ["rl-core", "persistence", "rl-protobuffers", "protobuffers"]):
      update_platform_version(dep)
    else:
      update_rl_version(dep)

def parse_parent(parent):
  print "Parsing parent..."
  if parent.groupId.string == "com.rocketlawyer.common" and parent.artifactId.string == "parent":
    parent.version.string = "2.1.1"
  return

def parse_pom(path):
  print "Processing pom file: " + path + "/pom.xml"

  f = open(path + "/pom.xml")
  doc = bs4.BeautifulSoup(f, "xml")
  f.close()

  if doc.project.parent:
    parse_parent(doc.project.parent)

  if doc.modules:
    for mod in doc.modules:
      if type(mod) != bs4.element.Tag:
        continue
      parse_pom(path + "/" + mod.string)

  if doc.dependencies:
    for dep in doc.dependencies:
      parse_dep(dep)

  f = open(path + "/pom.xml", "w")
  f.write(str(tidy_document(str(doc), options={'output_xml':1, 'indent':1, 'input_xml':1})[0]))
  f.close()
parse_pom(sys.argv[1])
