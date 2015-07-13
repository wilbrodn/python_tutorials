data=[]
name="Sophie"
while True:
	name=raw_input("Please enter ur user name?")
	if name=="Sophie":
		print("Thank you %s" %name)
		dat=input("Enter data for variable 1")
	else:
		print("unrecognised user")
		break

	data=data+[dat]
print("this is sophie's data")
print(data)

