def sum():
    print "sum function with no arguments"
    a=2
    b=3
    c= a+b
    print "sum is {0}".format(c)
sum()

def summation(a,b):
    print "sum function with arguments"
    c=a+b
    print "sum is {0}".format(c)
summation(5 , 6)

def sumReturn(a,b):
    print "sum function with arguments"
    c=a+b
    return c

value =sumReturn(2 ,3)

#global variables
global_name = "allan"

def nameFun():
    print("global name is : "+global_name)
    local_name= "alex"
    print("local name is : "+ local_name)
    global me
    me ="locally defined global variable"
    print me

nameFun()

print me