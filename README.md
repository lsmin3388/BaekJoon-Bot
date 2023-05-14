# 백준 문제 풀이를 감지하고 출석 체크하는 디스코드 봇 제작

## 목차
- [작동 방식 고안](#--------)
- [명령어 선정](#------)
- [on_ready(self)](#on-ready-self-)
- [on_message(self, message)](#on-message-self--message-)
- [JSON 관리 :: Getter Setter](#JSON------getter-setter)
- [백준 웹사이트 크롤링(스크래핑) :: BaekJoon Crawling(Scraping)](#---------------------baekjoon-crawling-scraping-)
- [두 날짜 사이의 날짜 리스트 반환 :: return a list of dates between two dates](#----------------------return-a-list-of-dates-between-two-dates)
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
```python
async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        await self.change_presence(status=discord.Status.online, activity=discord.Game("!명령어"))
        if not os.path.isfile(JSON):
            with open(JSON, 'w') as f:
                data = dict()
                json.dump(data, f, indent="\t", ensure_ascii=False)
        if not os.path.isdir('dayDatas'):
            os.mkdir('dayDatas')`
```

---

## on_message(self, message)

---

## JSON 관리 :: Getter Setter

---

## 백준 웹사이트 크롤링(스크래핑) :: BaekJoon Crawling(Scraping)

---

## 두 날짜 사이의 날짜 리스트 반환 :: return a list of dates between two dates

---
