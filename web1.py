#web1.py
#크롤링 작업을 위한 라이브러리
from bs4 import BeautifulSoup

#페이지 로딩
page = open("Chap09_test.html","rt",encoding="utf-8").read()

#전체 페이지를 bs4 객체로 변환
soup = BeautifulSoup(page,"html.parser")

#전체보기
# print(soup.prettify())

#<p>를 모두 검색하기
# print(soup.find_all("p"))

# print(soup.find_all("p", class_="outer-test"))

# print(soup.find_all("p", attrs={"class":"outer-text"}))

# print(soup.find_all(id="first"))

for tag in soup.find_all("p"):
    title = tag.text.strip()
    title = title.replace("\n","")
    print(title)

strA = "<<< python >>>"
result = strA.strip("<>") 
print(result)
strB = result.replace("python", "python javascript")
print(strB)
result = "spam ham egg banana" .split()
print(result)
print(":)".join(result))


import re

result = re.search(r"\d{4}", "올해는 2026년입니다.")
print(result.group())

result = re.search("apple", "this is apple")
print(result.group())

