# 백준 문제 풀이를 감지하고 출석 체크하는 디스코드 봇 제작

## 목차
  * [작동 방식 고안](#작동-방식-고안)
  * [명령어 선정](#명령어-선정)
  * [on_ready(self)](#on_readyself)
  * [on_message(self, message)](#on_messageself-message)
  * [JSON 관리 :: Getter Setter](#json-관리--getter-setter)
  * [백준 웹사이트 크롤링(스크래핑) :: BaekJoon Crawling(Scraping)](#백준-웹사이트-크롤링스크래핑--baekjoon-crawlingscraping)
---
## 작동 방식 고안

개발에 앞서 가장 먼저 생각한 것은 프로그래밍 언어 선택입니다. 그 후보로는 **Java**와 **Python**이 있었습니다. 처음에는 **Java**가 더욱 끌려서 **Java**를 선택하려고 했지만, **Java**를 쓰기에는 Heavy 해지고, 대학교 수업에서 **Python**을 학습하는 중이기 때문에 복습할 겸 **Python**을 결국 선택하게 되었습니다.

일단 먼저 작동 방식을 생각해봅시다. 

1. 어떤 유저가 백준의 문제를 해결했는지, 총 몇 번 해결했고, 해결하지 않은 적은 몇 번 있는지 등 다양한 데이터를 저장해야만 합니다. 그래서 저는 이러한 데이터들을 손쉽게 관리하고자 **파이썬에서 제공하는 모듈인 JSON**을 이용하기로 결정했습니다.

2. 백준의 문제를 정말로 해결했는지, 거짓으로 적지는 않았는지, 예전에 풀었던 문제를 또 푼 건 아닌지조차 생각해야 합니다. 이를 위해서 백준의 웹사이트를 **크롤링**하기로 결정했습니다.

3. 그 외에도 사용자들이 편리하게 만들고자 **명령어를 다양하게 제공**하고, 유저들이 명령어를 입력하는 데에 있어서 어려움을 줄여주고자 **"도움말" 명령어도 포함**시킬 것입니다.

4. 디스코드 봇을 24시간으로 구동시켜야 하는데, 가정 컴퓨터는 24시간 계속 켜둘 수 없기 때문에 **호스팅**을 사용해야 합니다.

---
## 명령어 선정

다음은 선정한 명령어 모음입니다.

```
————————————————————————————————————————
    !명령어 :: 
        ㄴ 명령어 목록을 확인합니다.
    !백준가입 [실명] [백준아이디] :: 
        ㄴ 시스템에 유저id를 가입합니다. (최초 실행 시 한번만)
    !이름변경 [실명] :: 
        ㄴ 이름을 변경합니다.
    !백준아이디변경 [백준아이디] :: 
        ㄴ 백준아이디를 변경합니다.

——————————————————————————————————————————

    !백준 인증 [문제번호] :: 
        ㄴ 오늘의 백준을 인증합니다.
    !백준 확인 :: 
        ㄴ 본인의 정보를 확인합니다.
    !백준 확인 [유저아이디] :: 
        ㄴ 지정한 유저의 정보를 확인합니다.

——————————————————————————————————————————

    !백준 오늘안한사람 :: 
        ㄴ 오늘의 인증정보를 확인합니다.
    !백준 이때안한사람 [날짜(ex. 20230101)] :: 
        ㄴ 해당날짜의 인증정보를 확인합니다.
    !백준 이사이안한사람 [날짜1(ex. 20230101)] [날짜2(ex. 20240101)] :: 
        ㄴ 해당날짜 사이의 인증정보를 확인합니다.

——————————————————————————————————————————
```

---
## on_ready(self)

on_ready 함수는 봇의 최초 실행 시 실행되는 함수입니다.
해당 함수에서는 봇의 상태 표시 지정, json파일이 있는지(없으면 생성), dayDatas폴더가 있는지(없으면 생성)를 처리합니다.

```python
async def on_ready(self):
    print(f'Logged on as {self.user}!')
    await self.change_presence(status=discord.Status.online, activity=discord.Game("!명령어"))
    # 봇 상태 표시
    
    if not os.path.isfile(JSON): # JSON = 'userdatas.json'
        with open(JSON, 'w') as f:
            data = dict()
            json.dump(data, f, indent="\t", ensure_ascii=False)
            
    if not os.path.isdir('dayDatas'):
        os.mkdir('dayDatas')`
```

---
## on_message(self, message)

다음은 유저가 메시지를 보낼 때 처리되는 함수입니다. 명령어를 치는 경우보단 일반 대화를 치는 경우가 압도적으로 많기 때문에 불필요한 실행을 줄이고자 초반에서 명령어가 맞는지의 여부를 확인해야 합니다. 또한 명령어가 많은 만큼 if문을 잘 연계하여 명령어를 잘 처리해야만 합니다. 

```python
async def on_message(self, message):
    if message.author == self.user: return
    if len(message.content) >= 1 and message.content[0] != '!': return
    
    args = message.content.split()
    if len(args) < 1: return
        
    if args[0] in HELP: # HELP = ['!도움말', '!명령어', '!help', '!helps']
        ~~
    elif args[0] == '!백준가입':
        ~~~
    elif args[0] == '!이름변경':
        ~~~
    elif args[0] == '!백준아이디변경':
        ~~~
    elif args[0] == '!백준':
        ~~~
        if args[1] == '인증':
            ~~~
        elif args[1] == '확인':
            ~~~
        elif args[1] == '오늘안한사람':
            ~~~
        elif args[1] == '이때안한사람':
            ~~~
        elif args[1] == '이사이안한사람':
            ~~~
```

---
## JSON 관리 :: Getter Setter

백준봇은 저장해야 하는 유저 데이터가 많을뿐더러, 추후 업데이트하면서 데이터가 확장될 여지가 있습니다. 그래서 저는 JSON을 선택했고, JSON 파일을 쉽게 읽어오고자 Getter와 Setter 메소드를 만들었습니다.
</br></br>
먼저 JSON 파일을 읽어오는 방법은 json.load(PATH)를 이용하면 됩니다.

```python
with open(JSON, 'r') as f:
    data = json.load(f)
```

여기서 data는 딕셔너리 타입을 취하고 있습니다. 즉 이 딕셔너리를 가져와서 출력하거나 원하는 값으로 수정하면 됩니다.

```python
data['7923013']['userName'] = '홍길동'
data['2928932']['count'] = 5
```

</br></br></br>
딕셔너리 수정을 마치면 딕셔너리를 dump하여 json에 저장합니다.


```python
with open(JSON, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent="\t", ensure_ascii=False)
```
</br></br></br>
다음은 완성된 Getter/Setter 메소드입니다.

```python
def getter(self, id, key):
    with open(JSON, 'r') as f:
        data = json.load(f)

    return data[str(id)][key]

def getUserList(self):
    with open(JSON, 'r') as f:
        data = json.load(f)
    
    datas = list()
    for k in data:
        datas.append(k)

    return datas

def setter(self, id,  key, value):
    with open(JSON, 'r') as f:
        data = json.load(f)
    data[str(id)][key] = value

    with open(JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent="\t", ensure_ascii=False)
```

---
## 백준 웹사이트 크롤링(스크래핑) :: BaekJoon Crawling(Scraping)

백준의 출석체크를 직접 구현해봅시다. 

먼저 사용할 파이썬 패키지를 설치해야 합니다. 크롤링할 때 대표적으로 사용하는 requests와 BeautifulSoup를 설치하도록 합시다. 
</br>

```bash
pip install requests
pip install beautifulsoup
```
여기서 requests 패키지는 html 문서를 가져올 때, BeautifulSoup는 가져온 html 내용을 쉽게 가공하고 처리할 때 사용합니다.
</br></br></br>
다음으로 어떤 웹사이트를 크롤링할지 정해봅시다. 백준 웹사이트를 온 곳에 다 돌아본 결과 오늘 유저들이 문제를 풀었는지 확인하기 위해서는 "채점현황"을 긁어오는 것이 좋다고 생각했습니다. 왜냐하면 오늘 풀었는 문제인지 날짜 정보도 나오고, 문제를 성공적으로 해결했는지의 여부도 알 수 있었습니다. 또한 "https://www.acmicpc.net/status?user_id=유저아이디" 주소에서 유저아이디 부분만 바꿔서 request 하면 언제든지 긁어올 수 있기 때문에 이 주소를 사용하겠습니다.
</br>

```python
response = requests.get('https://www.acmicpc.net/status?user_id={}'.format(accountId), 
                                    headers={"User-Agent": "Mozilla/5.0"})
if response.status_code != 200:
    print('failed connect.')
    return
```
</br>
이렇게 적으면 response라는 변수에 get함수로 request 해서 받아온 값이 저장됩니다. 밑에 "!= 200"이라고 적혀있는 부분은 status_code가 200이 아니라면 성공적으로 서버로부터 데이터를 request 한 것이 아니라고 하더라구요. 그래서 넣어줬습니다.
</br></br></br>
그럼 이제 requests 패키지를 이용해 html 문서를 가져왔으니 BeautifulSoup 패키지를 이용해 가공 처리 해봅시다.
여기서부터 정말로 귀찮고 보기 싫지만.. 해당 사이트에 들어가서 요소 검사를 해봅시다.
</br></br></br>
<img width="60%" src="https://github.com/lsmin3388/BaekJoon-Bot/assets/67568334/21bcc972-8883-42c8-9b5a-028074687195"/>
</br></br>
우리가 가져올 것들은 사진에 표시된 3개의 td태그 입니다. 각각 3번째, 4번째, 9번째 td 태그임을 생각하고, 3번째 td에서 a 태그 안에 있는 href 값, 4번째 td에서 span 태그 안에 있는 data-color 값, 9번째 td에서 a 태그 안에 있는 data-original-title 값을 가져오도록 만듭시다.
</br></br></br>

```python
soup = BeautifulSoup(response.text, 'html.parser')

pbnumbers = soup.select('tbody > tr > td:nth-child(3) > a')
status = soup.select('tbody > tr > td:nth-child(4) > span')
datadate = soup.select('tbody > tr > td:nth-child(9) > a')
today = datetime.today().strftime("%Y%m%d")

problem_num = []
problem_yesno = []
problem_date = []
max_index = 0

for i, t in enumerate(datadate):
    psds = t['title'].split('-')
    day = psds[0] + psds[1] + psds[2][0:2]
    
    if day != today:
        max_index = i
        break

    problem_date.append(day)

for l in pbnumbers:
    problem_num.append(l['href'][9:])

    if len(problem_num) >= max_index: break

for s in status:
    problem_yesno.append(s['data-color'])

    if len(problem_yesno) >= max_index: break
```

잘 따라오셨으면 problem_num, problem_yesno, problem_date 리스트에 각각 문제번호, 풀었는지의 여부, 날짜 데이터가 저장될 것입니다. 이를 이용해서 마음대로 데이터를 사용하시면 되겠습니다.

다음은 크롤링한 데이터를 통해 출석체크를 확인하는 메소드입니다.

```python
def checkBaekJoon(self, accountId, pbnum):
    try:
        response = requests.get('https://www.acmicpc.net/status?user_id={}'.format(accountId), 
                                headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            print('failed connect.')
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')

        pbnumbers = soup.select('tbody > tr > td:nth-child(3) > a')
        status = soup.select('tbody > tr > td:nth-child(4) > span')
        datadate = soup.select('tbody > tr > td:nth-child(9) > a')
        today = datetime.today().strftime("%Y%m%d")

        problem_num = []
        problem_yesno = []
        problem_date = []
        max_index = 0

        for i, t in enumerate(datadate):
            psds = t['title'].split('-')
            day = psds[0] + psds[1] + psds[2][0:2]
            
            if day != today:
                max_index = i
                break

            problem_date.append(day)

        for l in pbnumbers:
            problem_num.append(l['href'][9:])

            if len(problem_num) >= max_index: break

        for s in status:
            problem_yesno.append(s['data-color'])

            if len(problem_yesno) >= max_index: break

        for i, v in enumerate(problem_num):
            if v == pbnum:
                if problem_yesno[i] == 'ac':
                    return True
    except Exception as e:
        print(e)
    return False
```


---
