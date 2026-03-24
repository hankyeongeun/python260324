
# ================================================================
# 파이썬 상속(Inheritance) 학습 프로그램
# ================================================================
# 설명: 사람(Person)을 기본으로 하고, 직원(Employee)과 매니저(Manager)로 확장하는 예제
# 마치 동물 클래스가 있고, 그 안의 강아지, 고양이처럼 상속받는 것과 같습니다!

# ================================================================
# 🎁 Person 클래스 - 모든 사람의 기본 정보를 담는 블록박스
# ================================================================
# "클래스"는 붕어빵 틀과 같고, 만들어진 개체는 붕어빵입니다!
# Person 클래스는 모든 '사람'이 가져야할 공통 정보와 기능을 정의합니다.

class Person:
    # __init__은 "생성자"라고 불리며, 새로운 사람이 태어날 때 호출됩니다!
    # 마치 "아기가 태어나면서 이름을 지어주는 것처럼"
    def __init__(self, id, name):
        # self는 "자기 자신"을 의미합니다. (대명사처럼 생각하세요!)
        # self.id - 각 사람마다 다른 아이디 번호를 저장합니다 (주민등록번호처럼!)
        self.id = id
        # self.name - 각 사람의 이름을 저장합니다
        self.name = name

    # printInfo()는 "정보 출력" 메서드입니다. 버튼을 누르면 정보가 나타나는 것처럼!
    def printInfo(self):
        # format()을 사용해서 id와 name을 예쁘게 출력합니다
        print("ID: {0}, Name: {1}".format(self.id, self.name))


# ================================================================
# 🏢 Manager 클래스 - 매니저는 Person(사람)의 특별한 버전입니다!
# ================================================================
# "상속"은 자식이 부모의 특징을 물려받는 것처럼, 
# Manager가 Person의 id와 name을 자동으로 받아서 사용합니다!
# Person의 모든 것을 가지고 있으면서, "title(직급)"이라는 새로운 정보를 추가합니다!

class Manager(Person):
    # (Person) 이 부분이 "상속"을 의미합니다!
    # "Manager는 Person을 상속받습니다" = "매니저는 사람의 특징을 물려받습니다"
    
    # Manager만의 특별한 생성자입니다
    def __init__(self, id, name, title):
        # id와 name은 부모인 Person에서 받아오라는 뜻입니다!
        # super()는 "부모님"을 의미합니다! super().__init__은 부모님의 생성자를 호출!
        super().__init__(id, name)
        # title은 Manager만이 가질 수 있는 직급입니다!
        # 예: "개발팀장", "CTO" 등등
        self.title = title

    # Manager의 정보를 출력하는 메서드입니다
    # 부모의 printInfo()를 "오버라이드"(덮어쓰기)했습니다!
    # 더 많은 정보를 출력하도록 변경했어요!
    def printInfo(self):
        # id, name, title 3가지 정보를 모두 출력합니다!
        print("ID: {0}, Name: {1}, Title: {2}".format(self.id, self.name, self.title))


# ================================================================
# 👨‍💻 Employee 클래스 - 직원은 Person(사람)의 또 다른 특별한 버전입니다!
# ================================================================
# Employee도 Manager처럼 Person을 상속받습니다!
# Person의 id와 name을 물려받고, "skill(기술)"이라는 새로운 정보를 추가합니다!
# 예: "Python", "Java", "JavaScript" 등의 프로그래밍 언어를 배웠어요!

class Employee(Person):
    # (Person) 이 부분이 "상속"을 의미합니다!
    # "Employee는 Person을 상속받습니다" = "직원은 사람의 특징을 물려받습니다"
    
    # Employee만의 특별한 생성자입니다
    def __init__(self, id, name, skill):
        # id와 name은 부모인 Person에서 받아오라는 뜻입니다!
        super().__init__(id, name)
        # skill은 Employee만이 가질 수 있는 기술 정보입니다!
        # 예: "Python", "Java" 등의 프로그래밍 언어
        self.skill = skill

    # Employee의 정보를 출력하는 메서드입니다
    # 부모의 printInfo()를 "오버라이드"(덮어쓰기)했습니다!
    def printInfo(self):
        # id, name, skill 3가지 정보를 모두 출력합니다!
        print("ID: {0}, Name: {1}, Skill: {2}".format(self.id, self.name, self.skill))


# ================================================================
# 🧪 테스트 코드 - 위에서 만든 클래스들이 잘 작동하는지 테스트합니다!
# ================================================================
# 마치 장난감을 만든 후 "이 장난감이 제대로 작동하는지 확인하는 것"처럼!

# 📌 테스트 1️⃣ : Person 객체를 만들고 정보를 출력합니다 (첫 번째 테스트)
print("=== 테스트 1: Person 객체 기본 생성 및 출력 ===")
# p1은 "전우치"라는 아이디가 1번인 사람 객체입니다
# Person(아이디, 이름) 이렇게 정보를 입력해서 새로운 사람을 만듭니다!
p1 = Person(1, "전우치")
# 만든 사람 p1의 정보를 출력합니다! (버튼을 누르는 것처럼!)
p1.printInfo()

# 📌 테스트 2️⃣ : Person 객체를 또 만들어서 정보를 출력합니다 (두 번째 테스트)
print("\n=== 테스트 2: Person 객체 다양한 데이터 ===")
# 이번엔 아이디가 2번이고 이름이 "김순신"인 사람을 만듭니다
# \n은 "줄을 바꾼다"는 뜻입니다 (엔터를 치는 것처럼!)
p2 = Person(2, "김순신")
# 새로운 사람 p2의 정보를 출력합니다!
p2.printInfo()

# 📌 테스트 3️⃣ : Manager 객체를 만들고 정보를 출력합니다 (세 번째 테스트)
print("\n=== 테스트 3: Manager 객체 생성 및 출력 ===")
# m1은 아이디 101번, 이름 "이순신", 직급은 "개발팀장"인 매니저입니다
# Manager(아이디, 이름, 직급) 이렇게 정보를 입력합니다!
m1 = Manager(101, "이순신", "개발팀장")
# 만든 매니저 m1의 정보를 출력합니다!
m1.printInfo()

# 📌 테스트 4️⃣ : Manager 객체를 또 만들어서 정보를 출력합니다 (네 번째 테스트)
print("\n=== 테스트 4: Manager 객체 다양한 데이터 ===")
# 이번엔 아이디 102번, 이름 "세종대왕", 직급은 "CTO"인 매니저입니다
m2 = Manager(102, "세종대왕", "CTO")
# 새로운 매니저 m2의 정보를 출력합니다!
m2.printInfo()

# 📌 테스트 5️⃣ : Employee 객체를 만들고 정보를 출력합니다 (다섯 번째 테스트)
print("\n=== 테스트 5: Employee 객체 생성 및 출력 ===")
# e1은 아이디 201번, 이름 "강감찬", 기술은 "Python"인 직원입니다
# Employee(아이디, 이름, 기술) 이렇게 정보를 입력합니다!
e1 = Employee(201, "강감찬", "Python")
# 만든 직원 e1의 정보를 출력합니다!
e1.printInfo()

# 📌 테스트 6️⃣ : Employee 객체를 또 만들어서 정보를 출력합니다 (여섯 번째 테스트)
print("\n=== 테스트 6: Employee 객체 다양한 기술 ===")
# 이번엔 아이디 202번, 이름 "을지문덕", 기술은 "Java"인 직원입니다
e2 = Employee(202, "을지문덕", "Java")
# 새로운 직원 e2의 정보를 출력합니다!
e2.printInfo()

# 📌 테스트 7️⃣ : Manager가 정말 Person을 상속받았는지 확인합니다 (일곱 번째 테스트)
print("\n=== 테스트 7: 상속 확인 - Manager는 Person의 인스턴스인가? ===")
# isinstance() 함수는 "이 객체가 이 클래스의 인스턴스인가?"를 확인합니다
# "이 케이크는 케이크 틀로 만든 것인가?" 이렇게 확인하는 것처럼!
# True(맞다) 또는 False(틀렸다)라는 답이 나옵니다!
print("isinstance(m1, Person):", isinstance(m1, Person))  # m1이 Person인가? → True (상속받았으니까!)
print("isinstance(m1, Manager):", isinstance(m1, Manager))  # m1이 Manager인가? → True (Manager로 만들었으니까!)

# 📌 테스트 8️⃣ : Employee가 정말 Person을 상속받았는지 확인합니다 (여덟 번째 테스트)
print("\n=== 테스트 8: 상속 확인 - Employee는 Person의 인스턴스인가? ===")
# 마찬가지로 e1이 Person인지, Employee인지 확인합니다!
print("isinstance(e1, Person):", isinstance(e1, Person))  # e1이 Person인가? → True (상속받았으니까!)
print("isinstance(e1, Employee):", isinstance(e1, Employee))  # e1이 Employee인가? → True (Employee로 만들었으니까!)

# 📌 테스트 9️⃣ : 여러 사람을 리스트에 넣고 하나씩 출력합니다 (아홉 번째 테스트)
print("\n=== 테스트 9: 여러 객체를 리스트에 저장하고 순회 ===")
# people은 여러 사람들을 담은 상자(리스트)입니다!
# [항목1, 항목2, 항목3, ...] 이렇게 여러 개를 넣을 수 있어요!
people = [p1, m1, e1, m2, e2]
# for문으로 리스트의 각 사람을 하나씩 꺼냅니다!
# "바구니에서 하나씩 꺼내는 것처럼!" - 반복 공부할 때 유용합니다!
for person in people:
    # 리스트에 있는 각 사람의 정보를 출력합니다!
    person.printInfo()

# 📌 테스트 🔟 : 만든 객체의 멤버 변수에 직접 접근해서 확인합니다 (열 번째 테스트)
print("\n=== 테스트 10: 멤버 변수 직접 접근 확인 ===")
# 점(.)을 사용하면 객체 안의 정보(멤버 변수)에 직접 접근할 수 있습니다!
# 마치 "상자를 열어서 안의 물건을 꺼내는 것처럼!"
print(f"p1.id = {p1.id}, p1.name = {p1.name}")  # p1의 아이디와 이름을 직접 꺼내서 출력!
print(f"m1.id = {m1.id}, m1.name = {m1.name}, m1.title = {m1.title}")  # m1의 아이디, 이름, 직급을 출력!
print(f"e1.id = {e1.id}, e1.name = {e1.name}, e1.skill = {e1.skill}")  # e1의 아이디, 이름, 기술을 출력!   