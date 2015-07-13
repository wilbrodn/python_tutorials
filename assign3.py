def exam_scores():
 
    print("A PROGRAM THAT ANALYSES STUDENTS MARKS PERFORMANCE")
    print("==================================================")
    print(" ")
    print(" ")
    print(" ")
    
    
    again="yes"
    while True:
        std=raw_input ("What is the name of the students?: ")
        score=[]
        grading=[]
        points=[]
        comments=[]
        n=input("Please enter the number subjects you are going to enter: ")
        total=0
        tpoints=0
        for y in range(0,int(n)):
            z=int(y)+1
            mark=input("The mark for subject {} is?:".format(z))

            if mark<0 or mark>100:
                print("please enter the marks between 0 and 100")
                mark=input()

            elif mark>=80 and mark<=100:
                grade="A"
                point=5
                comment="Excellent"
            elif mark>=75 and mark<80:
                grade="B"
                point=4.5
                comment="Very Good"
            elif mark>=65 and mark<75:
                grade="C"
                point=4
                comment="Good"
            elif mark>=60 and mark<65:
                grade="D"
                point=3.5
                comment="Fair"
            elif mark>=50 and mark<60:
                grade="E"
                point=3
                comment="Pass"
            else:
                grade="F"
                point=2
                comment="Fail"
            total=total+mark
            tpoints=tpoints+point
            grading=grading+[grade]
            score=score+[mark]
            points=points+[point]
            comments=comments+[comment]
        average=total/n
        apoint=tpoints/n


        print("THE SUMMARY FOR "+std+" IS AS FOLLOWS:")
        print("=====================================")
        print(std+"'s entered marks are:")
        print(score)
        print(std+"'s respective grading are:")
        print(grading)
        print(std+"'s respective points for each grade are:")
        print(points)
        print(std+"'s respective comments are:")
        print(comments)

        print("The average mark of " +std+ " is")
        print(average)
        print("And the total and average points are {} and {}, respectively".format(tpoints,apoint))
        print(" ")
        print("===========================================================================================================")
        print(" ")
        print(" ")
        print(" ")

        again=raw_input("Are you going to enter for another student?: (Please type yes to enter for more or any other key to exit)")
        if again=="yes":
            print("The program is restarting")
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("")
            print("")
            print("")

        else:
            print("Program exits, bye!")
            exit()
    return apoint

exam_scores()

