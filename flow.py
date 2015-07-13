'''     program flow
        string formatiing https://docs.python.org/2/library/string.html#formatspec
'''
age = input("my age: ")

if age > 24 and not age >30:
    print("age is greater than 24")
    b=age + 7
    print(b)

if age < 24:
    print(" you are still young")
else:
    print("you are old")

name = raw_input("my name :")
if name == "allan"  and age > 24:
    print("hi "+ name)
elif name=="mary":
    print("hi mary")
else:
    print("you are not allan or mary")

i =0;
while i <3:
    print "counting to 3 from  %d "%i
    print "counting to 3 from ,i"
    print "counting to 3 from" + str(i)
    print "counting to 3 from {0}".format(i)
    i=i+1
#break and continue statements
while True:
    print("please type your name")
    user = input()
    if user == name:
        print("thank you  %s" %user)
        break
    else:
        print("Your name is "+ name +" are you a new user");