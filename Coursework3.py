
name = raw_input('What is your name? ')
marks = []
grade = []
gps=[]
for i in range (1,4):
    score = input("What is "+str(i)+"th mark?: ")
    if score>=80:
    	grad="A"
    	gp=4
    elif score>=75 and score<80:
    	grad="B"
    	gp=3.5
    else:
    	grad="C"
    	gp=3

    marks = marks+[score]
    grade = grade+[grad]
    gps=gps+[gp]
   
print(name+" 's marks are")
print(marks)

print("and the respective grades are")
print(grade)

print("while the respective grade points are")
print(gps)

import math

tgpa=sum(gps)
gpa=tgpa/3

a=sum(marks)

av=a/4

print(name+"'s gross point average, GPA is")
print(float(gpa))

print(name+ "'s average score in the three subjects is")
print(float(av))

print(name+ "'s total score in the three subjects is"
print(a)


