#!/usr/bin/env python

import sys, os
import re
import urllib2, lxml.etree
from optparse import OptionParser
import pdb
import itertools
import operator
import csv
from operator import itemgetter

parser = OptionParser()
parser.add_option("-i", "--input", dest="input", default="./tmp/Draft Budget  Estimates for  FY 2015-16 Vol 1.pdf",
                help="Input pdf name", metavar="FILE")
parser.add_option("-o", "--output", dest="output", default="./tmp/",
                        help="Output path. Default is './tmp/'",metavar="FOLDER")
parser.add_option("-d", "--debug", dest="debug", default=False,
                        help="Debug",metavar="BOOLEAN")
(options, args) = parser.parse_args()

def remdash(string):
    return string.replace(u'\u2013',"-")
def trytext(el):
    textList = []
    text = el.text
    childText = None
    grandchildText = None
    children = el.getchildren()
    childLen = len(children)
    if childLen>0:
        child = children[0]
        childText = child.text
        grandchildren = child.getchildren()
        grandchildLen = len(grandchildren)
        if grandchildLen>0:
            grandchild = grandchildren[0]
            grandchildText = grandchild.text
    result = ""
    textList.append(text)
    textList.append(childText)
    textList.append(grandchildText)
    finalList = filter(None,textList)
    result = " ".join(finalList)
    output = remdash(result)
    if output=="":
        return None
    else:
        return output
    
def pdftoxml(pdfdata, options):
    """converts pdf file to xml file"""
    # lots of hacky Windows fixes c.f. original
    absDir = os.path.dirname(pdfdata)+"/"
    cmd = 'pdftohtml -xml -nodrm -zoom 1.5 -enc UTF-8 -noframes "'
    if options:
        cmd += options
    cmd += pdfdata
    cmd +=  '" "'
    cmd += absDir
    cmd +='output.xml"'
    cmd = cmd + " > NUL 2>&1" # can't turn off output, so throw away even stderr yeuch
    os.system(cmd)
    with open(absDir+'output.xml', 'r') as f:
        return f.read()

def main():
    #Before writing, try pdftohtml NAME.pdf -xml NAME.xml
    #Requires Poppler for windows in your path
    #http://blog.alivate.com.au/poppler-windows/
    basename = os.path.basename(options.input)
    inputname, inputextension = os.path.splitext(basename)
    sys.stdout.write("Reading "+basename+"... This may take a while....")
    xmldata = pdftoxml(options.input,False)
    root = lxml.etree.fromstring(xmldata)
    pages = list(root)
    output = []
    pageLen = len(pages)
    #Cascade these down...
    ministry = ""
    vote = ""
    department = ""
    budgetType = ""
    programme = ""
    econOutput = ""
    #Cascade this up...
    sector = 0
    sectors = []
    for i in range(0,pageLen):
        page = pages[i]
        elLen = len(page)
        for j in range(0,elLen):
            el = page[j]
            if el.tag == "text":
                left = int(el.attrib['left'])
                right = int(el.attrib['left'])+int(el.attrib['width'])
                top = int(el.attrib['top'])
                font = int(el.attrib['font'])
                if j==elLen-1:
                    sector+=1
                    try:
                        sectors.append(str.split(el.text,"- ")[1])
                    except:
                        sectors.append("Unknown Sector")
                if font==1:
                    if trytext(el)!=None:
                        ministry = trytext(el)
                elif font==2 or font==15:
                    if trytext(el)!=None:
                        vote = trytext(el)
                elif font==4 or font==17:
                    if trytext(el)!=None:
                        department = trytext(el)
                elif font==5:            
                    if trytext(el)!=None:
                        budgetType = trytext(el)
                elif font==6:
                    if trytext(el)!=None:
                        programme = trytext(el)
                elif (font==7 or font==10) and trytext(el)[:7]=="Output:":
                    if trytext(el)!=None:
                        econOutput = trytext(el)
                elif font==11:
                    if j<elLen-6:
                        el2 = page[j+1]
                        font2 = int(el2.attrib['font'])
                        el3 = page[j+2]
                        font3 = int(el3.attrib['font'])
                        el4 = page[j+3]
                        font4 = int(el4.attrib['font'])
                        el5 = page[j+4]
                        font5 = int(el5.attrib['font'])
                        el6 = page[j+5]
                        font6 = int(el6.attrib['font'])
                        el7 = page[j+6]
                        font7 = int(el7.attrib['font'])
                        #Pattern is 11 11 12 11 11 12 9/20 for:
                        #wage non-wage total wageEst non-wageEst totalEst econFunc
                        if font2==11 and font3==12 and font4==11 and font5==11 and font6==12 and (font7==9 or font7==20):
                            #Wage 2014/15
                            obj = {}
                            obj['year']="2014/15 Approved Budget"
                            obj['Government']="Central Government"
                            obj['sectorId']=sector
                            obj['Vote']=vote
                            obj['Ministry']=ministry
                            obj['Budget Type']=budgetType
                            obj['Department']=department
                            obj['Programme']=programme
                            obj['Budget']=trytext(el)
                            obj['Budget Function']="Wage" if obj['Budget Type']=="Recurrent Budget Estimates" else "GOU"
                            obj['Economic Function']=trytext(el7)
                            obj['Output']=econOutput
                            obj['ofWhich']=""
                            output.append(obj)
                            #Non-Wage 2014/15
                            obj = {}
                            obj['year']="2014/15 Approved Budget"
                            obj['Government']="Central Government"
                            obj['sectorId']=sector
                            obj['Vote']=vote
                            obj['Ministry']=ministry
                            obj['Budget Type']=budgetType
                            obj['Department']=department
                            obj['Programme']=programme
                            obj['Budget']=trytext(el2)
                            obj['Budget Function']="Non Wage" if obj['Budget Type']=="Recurrent Budget Estimates" else "External Fin."
                            obj['Economic Function']=trytext(el7)
                            obj['Output']=econOutput
                            obj['ofWhich']=""
                            output.append(obj)
                            #Wage 2015/16
                            obj = {}
                            obj['year']="2015/16 Draft Estimates"
                            obj['Government']="Central Government"
                            obj['sectorId']=sector
                            obj['Vote']=vote
                            obj['Ministry']=ministry
                            obj['Budget Type']=budgetType
                            obj['Department']=department
                            obj['Programme']=programme
                            obj['Budget']=trytext(el4)
                            obj['Budget Function']="Wage" if obj['Budget Type']=="Recurrent Budget Estimates" else "GOU"
                            obj['Economic Function']=trytext(el7)
                            obj['Output']=econOutput
                            obj['ofWhich']=""
                            output.append(obj)
                            #Non-Wage 2015/16
                            obj = {}
                            obj['year']="2015/16 Draft Estimates"
                            obj['Government']="Central Government"
                            obj['sectorId']=sector
                            obj['Vote']=vote
                            obj['Ministry']=ministry
                            obj['Budget Type']=budgetType
                            obj['Department']=department
                            obj['Programme']=programme
                            obj['Budget']=trytext(el5)
                            obj['Budget Function']="Non Wage" if obj['Budget Type']=="Recurrent Budget Estimates" else "External Fin."
                            obj['Economic Function']=trytext(el7)
                            obj['Output']=econOutput
                            obj['ofWhich']=""
                            output.append(obj)
                #of which columns
                elif font==14:
                    if j<elLen-7:
                        el2 = page[j+1]
                        font2 = int(el2.attrib['font'])
                        el3 = page[j+2]
                        font3 = int(el3.attrib['font'])
                        el4 = page[j+3]
                        font4 = int(el4.attrib['font'])
                        el5 = page[j+4]
                        font5 = int(el5.attrib['font'])
                        el6 = page[j+5]
                        font6 = int(el6.attrib['font'])
                        el7 = page[j+6]
                        font7 = int(el7.attrib['font'])
                        el8 = page[j+7]
                        font8 = int(el8.attrib['font'])
                        #pattern is 14 14 13 8/19 14 14 14 13
                        #for wageEst nonWageEst totalEst EconFunc Other? wage nonWage total
                        if font2==14 and font3==13 and (font4==8 or font4==19) and font5==14 and font6==14 and font7==14 and font8==13:
                            #Find of last font 9/20 for 'of which'
                            ofWhich = el.getprevious()
                            ofWhichFont = int(ofWhich.attrib['font'])
                            while ofWhichFont!=9 and ofWhichFont!=20:
                                ofWhich = ofWhich.getprevious()
                                ofWhichFont = int(ofWhich.attrib['font'])
                            #Wage 2014/15
                            obj = {}
                            obj['year']="2014/15 Approved Budget"
                            obj['Government']="Central Government"
                            obj['sectorId']=sector
                            obj['Vote']=vote
                            obj['Ministry']=ministry
                            obj['Budget Type']=budgetType
                            obj['Department']=department
                            obj['Programme']=programme
                            obj['Budget']=trytext(el6)
                            obj['Budget Function']="Wage" if obj['Budget Type']=="Recurrent Budget Estimates" else "GOU"
                            obj['Economic Function']=trytext(el4)
                            obj['Output']=econOutput
                            obj['ofWhich']=trytext(ofWhich)
                            output.append(obj)
                            #Non-Wage 2014/15
                            obj = {}
                            obj['year']="2014/15 Approved Budget"
                            obj['Government']="Central Government"
                            obj['sectorId']=sector
                            obj['Vote']=vote
                            obj['Ministry']=ministry
                            obj['Budget Type']=budgetType
                            obj['Department']=department
                            obj['Programme']=programme
                            obj['Budget']=trytext(el7)
                            obj['Budget Function']="Non Wage" if obj['Budget Type']=="Recurrent Budget Estimates" else "External Fin."
                            obj['Economic Function']=trytext(el4)
                            obj['Output']=econOutput
                            obj['ofWhich']=trytext(ofWhich)
                            output.append(obj)
                            #Wage 2015/16
                            obj = {}
                            obj['year']="2015/16 Draft Estimates"
                            obj['Government']="Central Government"
                            obj['sectorId']=sector
                            obj['Vote']=vote
                            obj['Ministry']=ministry
                            obj['Budget Type']=budgetType
                            obj['Department']=department
                            obj['Programme']=programme
                            obj['Budget']=trytext(el)
                            obj['Budget Function']="Wage" if obj['Budget Type']=="Recurrent Budget Estimates" else "GOU"
                            obj['Economic Function']=trytext(el4)
                            obj['Output']=econOutput
                            obj['ofWhich']=trytext(ofWhich)
                            output.append(obj)
                            #Non-Wage 2015/16
                            obj = {}
                            obj['year']="2015/16 Draft Estimates"
                            obj['Government']="Central Government"
                            obj['sectorId']=sector
                            obj['Vote']=vote
                            obj['Ministry']=ministry
                            obj['Budget Type']=budgetType
                            obj['Department']=department
                            obj['Programme']=programme
                            obj['Budget']=trytext(el2)
                            obj['Budget Function']="Non Wage" if obj['Budget Type']=="Recurrent Budget Estimates" else "External Fin."
                            obj['Economic Function']=trytext(el4)
                            obj['Output']=econOutput
                            obj['ofWhich']=trytext(ofWhich)
                            output.append(obj)
    #Add sectors in by sectorId
    for obj in output:
        obj['MTEF Sector'] = sectors[obj['sectorId']]
        del obj['sectorId']
    if options.debug:
        pdb.set_trace()
    keys = output[0].keys()
    with open(options.output+inputname+".csv", 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(output)
    sys.stdout.write("\n")
    print("Done.")

main()