''' script that reads students marks from a file
    computes their grades and gets total and averge score
    remove the pass key word after writing your code for each function
'''

# open file function that opens files
marks=[]
def open_file ():
    file_name=open("C:\Users\wilbrodn\Desktop\marks.txt", "r")
    marks=file_name.readlines()
    return marks
    #returns marks list

# computes grade  for each mark in the list
def grade(marks_list):
    if marks_list>=80 and marks_list<=100:
        grade="A"
        point=5
        comment="Excellent"
    elif marks_list>=75 and marks_list<80:
        grade="B"
        point=4.5
        comment="Very Good"
    elif marks_list>=65 and marks_list<75:
        grade="C"
        point=4
        comment="Good"
    elif marks_list>=60 and marks_list<65:
        grade="D"
        point=3.5
        comment="Fair"
    elif marks_list>=50 and marks_list<60:
        grade="E"
        point=3
        comment="Pass"
    else:
        grade="F"
        point=2
        comment="Fail"
    return [grade, point, comment]
    # returns list of computed grade

# computes average of grades or marks
def average (total,no):
    n= total/no
    return n

def total(dff):
    t=0
    for b in dff:
        t=t+int(b)
    return t


# main function that puts all functions together

def main():
    print("A PROGRAM THAT EXTRACTS STUDENTS MARKS FROM A FILE AND COMPUTES THEIR GRADES AND AVERAGE")
    print("========================================================================================")
    print(" ")
    print(" ")

    data = open_file()
    marki=[]
    names=[]
    markz=[]
    z=[]
    gra=[]
    poi=[]
    com=[]

    for i in data:
        nm=i.split(" ")
        name=nm[0]
        mar=nm[1]
        marki=marki+[mar]
        names=names+[name]
    print("The students names are:")
    print names
    print(" ")
    print("Their respective marks are:")
    print marki
    print(" ")
    for y in marki:
        z=grade(int(y))
        gra=gra+[z[0]]
        poi=poi+[z[1]]
        com=com+[z[2]]
    print("Their respective grades are:")
    print gra
    print(" ")
    print("Their respective points are:")
    print poi
    print(" ")
    print("And their respective comments are:")
    print com
    tm=total(marki)
    
    print(" ")
    print(" ")
    print(" ")
    print("The average score of all the students is:")
    av=average(tm,3)
    print av
    print("===")

main()
