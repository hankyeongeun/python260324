# 블럭 주석 처리: ctrl + /

score = int(input("점수를 입력:"))

if 90<= score <= 100:
    grade="A"
elif 80 <= score <90:
    grade = "B"
elif 70 <= score <80:
    grade = "C"
else:
    grade = "D"
print("등급은 ", grade)



value = 5

while value > 0:
    print(value)
    value -=1

lst = [100, 3.14, "apple"]
for item in lst:
    print(item)

colors = {"apple":"red", "banana":"yellow", "grape":"purple"}
for item in colors.items():
   print(item)

   print("-------range() -------")
   print(list(range(10)))
   print(list(range(200,2027)))
   print(list(range(1,32)))
   print(list(range(10,0,-1)))

   print("list comprehension---")
   lst = [1,2,3,4,5,6,7,8,9,10]
   print([i**2 for i in lst if i>5])
   tp= ("apple", "banana")
   print([len(i) for i in tp])



print("---- filtering -----")
lst = [10,25,30]
itemL = filter(None, lst)
for item in itemL:
    print

# def getBiggerThan20(x):
#     return x>20

itemL = filter(lambda x: x > 20,lst)
for item in itemL:
    print(item)

