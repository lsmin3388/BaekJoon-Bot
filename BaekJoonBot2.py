import discord
from datetime import datetime, timedelta
import json
import os
import requests
from bs4 import BeautifulSoup

INIT = '[백준봇] '
JSON = 'userdatas.json'
HELP = ['!도움말', '!명령어', '!help', '!helps']

TOKEN = os.environ["DISCORD_TOKEN"]

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        await self.change_presence(status=discord.Status.online, activity=discord.Game("!명령어"))
        if not os.path.isfile(JSON):
            with open(JSON, 'w') as f:
                data = dict()
                json.dump(data, f, indent="\t", ensure_ascii=False)
        if not os.path.isdir('dayDatas'):
            os.mkdir('dayDatas')
    
    async def on_message(self, message):
        if message.author == self.user: return
        if len(message.content) >= 1 and message.content[0] != '!': return

        if message.content in HELP:
            
            msg = """```asciidoc
❔ 명령어 도움말 ❔
——————————————————————————————————————————

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
```"""
            await message.channel.send('{0} {1.author.mention}'.format(msg, message))
        

################################################################################


        elif message.content[0:5] == '!백준가입':
            
            args = message.content.split()

            if len(args) != 3:
                await message.channel.send(INIT + '명령어가 올바르지 않습니다.')
                await message.channel.send(INIT + '!백준가입 [본명] [백준아이디]')
                await message.channel.send(message.author.mention)
                return
            
            userName = args[1]
            userAccount = args[2]

            if not userName.isalpha() or not 2 <= len(userName) <= 4:
                await message.channel.send(INIT + '이름이 올바르지 않습니다. 2글자 이상 4글자 이하 한글 본명을 작성해주세요.')
                await message.channel.send(message.author.mention)
                return


            # 유저 확인 부분
            if self.checkUser(message.author.id):
                await message.channel.send(INIT + '이미 가입을 했습니다.')
                await message.channel.send(message.author.mention)
                return
                

            # 유저 아이디 추가 부분
            self.appendUser(message.author.id, userName, userAccount)

            await message.channel.send(INIT + '성공적으로 추가되었습니다.')
            await message.channel.send(message.author.mention)

#################################################################################

        elif message.content[0:5] == '!이름변경':
            args = message.content.split()

            if len(args) != 2:
                await message.channel.send(INIT + '명령어가 올바르지 않습니다.')
                await message.channel.send(INIT + '!이름변경 [본명]')
                await message.channel.send(message.author.mention)
                return
            
            if not self.checkUser(message.author.id):
                await message.channel.send(INIT + '백준가입부터 해주세요.')
                await message.channel.send(INIT + '!백준가입 [본명] [백준아이디]')
                await message.channel.send(message.author.mention)
                return
            
            if not args[1].isalpha() or not 2 <= len(args[1]) <= 4:
                await message.channel.send(INIT + '이름이 올바르지 않습니다. 2글자 이상 4글자 이하 한글 본명을 작성해주세요.')
                await message.channel.send(message.author.mention)
                return
            
            self.setter(message.author.id, 'userName', args[1])
            await message.channel.send(INIT + '이름이 "' + args[1] + '"으로 변경되었습니다.')
            await message.channel.send(message.author.mention)

#################################################################################

        elif message.content[0:8] == '!백준아이디변경':
            args = message.content.split()

            if len(args) != 2:
                await message.channel.send(INIT + '명령어가 올바르지 않습니다.')
                await message.channel.send(INIT + '!백준아이디변경 [백준아이디]')
                await message.channel.send(message.author.mention)
                return
            
            if not self.checkUser(message.author.id):
                await message.channel.send(INIT + '백준가입부터 해주세요.')
                await message.channel.send(INIT + '!백준가입 [본명] [백준아이디]')
                await message.channel.send(message.author.mention)
                return
            
            self.setter(message.author.id, 'userAccount', args[1])
            await message.channel.send(INIT + '백준아이디가 "' + args[1] + '"으로 변경되었습니다.')
            await message.channel.send(message.author.mention)
                


################################################################################


        else:
            if message.content[0:3] == '!백준':
                args = message.content.split()

                if args[0] != '!백준':
                    return
                
                if len(args) < 2:
                    await message.channel.send(INIT + '명령어가 올바르지 않습니다.')
                    await message.channel.send(INIT + '!명령어')
                    await message.channel.send(message.author.mention)
                    
                
                if not self.checkUser(message.author.id):
                    await message.channel.send(INIT + '백준가입부터 해주세요.')
                    await message.channel.send(INIT + '!백준가입 [본명] [백준아이디]')
                    await message.channel.send(message.author.mention)
                    return



#################################################################################



                if args[1] == '인증':
                    
                    if len(args) != 3:
                        await message.channel.send(INIT + '다시 입력해주세요.  (!백준 인증 [문제번호])')
                        await message.channel.send(message.author.mention)
                        return

                    # 이미 인증했던 문제번호 중복할 경우

                    for key, value in self.getter(message.author.id, "questNum").items():
                        if args[2] == value:
                            await message.channel.send(INIT + '이미 ' + key + ' 날짜로 인증된 문제번호입니다.')
                            await message.channel.send(message.author.mention)
                            return
                        
                    await message.channel.send(INIT + '백준아이디 ' + self.getter(message.author.id, 'userAccount') + '으로 확인중입니다...')

                    if not self.checkBaekJoon(self.getter(message.author.id, 'userAccount'), args[2]):
                        await message.channel.send(INIT + '오늘 해결한 적이 없는 문제입니다.')
                        await message.channel.send(INIT + '인증을 실패했습니다.')
                        await message.channel.send(message.author.mention)
                        return
                    
                    today = datetime.today().strftime("%Y%m%d")
                    questNum = self.getter(message.author.id, "questNum")

                    if questNum.get(today) is None:
                        count = self.getter(message.author.id, 'count') + 1
                        self.setter(message.author.id, 'count', count)

                    questNum[today] = args[2]

                    with open(JSON, 'r') as f:
                        json_data = json.load(f)

                    json_data[str(message.author.id)]["questNum"] = questNum

                    with open(JSON, 'w') as f:
                        json.dump(json_data, f, indent="\t", ensure_ascii=False)

                    with open('dayDatas/'+today+'.txt', 'a+') as f:
                        f.write(str(message.author.id) + '\n')
                        
                    await message.channel.send(INIT + '성공적으로 ' + today + ' 날짜의 백준 인증정보가 업데이트(수정) 되었습니다.')
                    await message.channel.send(message.author.mention)


#################################################################################


                elif args[1] == '확인':
                    if len(args) == 2:

                        questNum = self.getter(message.author.id, 'questNum')

                        questNumStr = ''
                        for key, value in questNum.items():
                            questNumStr += '        ㄴ 날짜: ' + key + ', 문제번호: ' + value + '\n'
                        msg = f"""```asciidoc
📢 {message.author.name}님의 정보 📢
——————————————————————————————————————————
    
    이름: {self.getter(message.author.id, 'userName')}
    백준아이디: {self.getter(message.author.id, 'userAccount')}
    고유번호: {message.author.id}
    해결한 문제 수: {self.getter(message.author.id, 'count')}
    해결한 문제 종류: 
{questNumStr}
——————————————————————————————————————————
```"""
                        await message.channel.send('{0} {1.author.mention}'.format(msg, message))
                        
                    elif len(args) == 3:

                        if not self.checkUser(args[2]):
                            await message.channel.send(INIT + '해당 유저는 아직 가입하지 않았습니다.')
                            await message.channel.send(message.author.mention)
                            return
                        
                        questNum = self.getter(args[2], 'questNum')

                        questNumStr = ''
                        for key, value in questNum.items():
                            questNumStr += '        ㄴ 날짜: ' + key + ', 문제번호: ' + value + '\n'

                        msg = f"""```asciidoc
📢 {args[2]}님의 정보 📢
——————————————————————————————————————————

    이름: {self.getter(args[2], 'userName')}
    백준아이디: {self.getter(args[2], 'userAccount')}
    고유번호: {args[2]}
    해결한 문제 수: {self.getter(args[2], 'count')}
    해결한 문제 종류: 
{questNumStr}
——————————————————————————————————————————
            ```"""
                        await message.channel.send('{0} {1.author.mention}'.format(msg, message))
                    else:
                        await message.channel.send(INIT + '명령어가 올바르지 않습니다.')
                        await message.channel.send(INIT + '!백준 확인')
                        await message.channel.send(message.author.mention)
                        return
                    
#################################################################################


                elif args[1] == '오늘안한사람':

                    today = datetime.today().strftime("%Y%m%d")
                    yesList = ''
                    noList = ''

                    with open('dayDatas/' + today + '.txt', 'r') as f:
                        datas = f.readlines()

                    datas = list(map(lambda s: s.strip(), datas))

                    for d in self.getUserList():
                        if d in datas:
                            yesList += f'    {d}({self.getter(d, "userName")})\n'
                        else:
                            noList += f'    {d}({self.getter(d, "userName")})\n'
                    
                    msg = f"""```asciidoc
——————————————————————————————————————————

⭕️ 오늘 한 사람 ⭕️

——————————————————————————————————————————

{yesList}
——————————————————————————————————————————

❌ 오늘 안한 사람 ❌

——————————————————————————————————————————

{noList}
——————————————————————————————————————————
```"""
                    await message.channel.send('{0} {1.author.mention}'.format(msg, message))



#################################################################################


                elif args[1] == '이때안한사람':
                    if len(args) != 3:
                        await message.channel.send(INIT + '명령어가 올바르지 않습니다.')
                        await message.channel.send(INIT + '!백준 이때안한사람 [날짜(ex. 20230101)]')
                        await message.channel.send(message.author.mention)
                        return
                    
                    day = args[2]

                    if not os.path.isfile('dayDatas/' + day + '.txt'):
                        await message.channel.send(INIT + '아무도 백문문제 인증을 하지 않았습니다.')
                        await message.channel.send(message.author.mention)
                        return
                        

                    yesList = ''
                    noList = ''

                    with open('dayDatas/' + day + '.txt', 'r') as f:
                        datas = f.readlines()

                    datas = list(map(lambda s: s.strip(), datas))

                    for d in self.getUserList():
                        if d in datas:
                            yesList += f'    {d}({self.getter(d, "userName")})\n'
                        else:
                            noList += f'    {d}({self.getter(d, "userName")})\n'
                    
                    msg = f"""```asciidoc
——————————————————————————————————————————

⭕️ '{day}' 한 사람 ⭕️

——————————————————————————————————————————

{yesList}
——————————————————————————————————————————

❌ '{day}' 안한 사람 ❌

——————————————————————————————————————————

{noList}
——————————————————————————————————————————
```"""
                    await message.channel.send('{0} {1.author.mention}'.format(msg, message))



#################################################################################


                elif args[1] == '이사이안한사람':
                    if len(args) != 4:
                        await message.channel.send(INIT + '명령어가 올바르지 않습니다.')
                        await message.channel.send(INIT + '!백준 이사이안한사람 날짜1(ex. 20230101)] [날짜2(ex. 20240101)]')
                        await message.channel.send(message.author.mention)
                        return
                    
                    if len(args[2]) != 8 or len(args[3]) != 8:
                        await message.channel.send(INIT + '명령어가 올바르지 않습니다.')
                        await message.channel.send(INIT + '!백준 이사이안한사람 날짜1(ex. 20230101)] [날짜2(ex. 20240101)]')
                        await message.channel.send(message.author.mention)
                        return
                    
                    try:
                        await message.channel.send(INIT + '계산중입니다. 잠시만 기다려주세요....')
                        userCheckList = {string : 0 for string in self.getUserList()}
                        count = 0
                        for date in self.date_range(args[2], args[3]):
                            if os.path.isfile('dayDatas/' + date + '.txt'):
                                count += 1
                                with open('dayDatas/' + date + '.txt', 'r') as f:
                                    datas = f.readlines()

                                datas = list(map(lambda s: s.strip(), datas))

                                for d in self.getUserList():
                                    if d in datas:
                                        userCheckList[d] += 1

                        for user, yesnum in userCheckList.items():
                            await message.channel.send(INIT + f'{self.getter(user, "userName")}님이 푼 문제 개수: {yesnum}/{count} ({count-yesnum}문제 안품)')
                        await message.channel.send(message.author.mention)

                    except Exception as e:
                        await message.channel.send(INIT + '오류가 발생했습니다.')
                        await message.channel.send(INIT + '명령어를 다시 확인해주세요.')
                        await message.channel.send(message.author.mention)
                        print(e)

                else:
                    await message.channel.send(INIT + '존재하지 않는 명령어입니다.')
                    await message.channel.send(INIT + '!명령어')
                    await message.channel.send(message.author.mention)

################################################################################

    # Check UserData #

    def checkUser(self, id):
        with open(JSON, 'r') as f:
            json_data = json.load(f)
            for data in json_data:
                if str(id) == data:
                    return True
        return False
    
    # Append UserData #

    def appendUser(self, id, name, userAccount, count=0, questNum=dict()):

        with open(JSON, 'r') as f:
            data = json.load(f)

        data[str(id)] = {"userName": name, "userAccount": userAccount,"userId": str(id), "count": count, "questNum": questNum}

        with open(JSON, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent="\t", ensure_ascii=False)

    # Getter #

    def getter(self, id, key):
        with open(JSON, 'r') as f:
            data = json.load(f)

        return data[str(id)][key] # key = "userName", "userAccount", "id", "count", "questNum"
    
    def getUserList(self):
        with open(JSON, 'r') as f:
            data = json.load(f)
        
        datas = list()
        for k in data:
            datas.append(k)

        return datas
    
    # Setter # 

    def setter(self, id,  key, value):
        with open(JSON, 'r') as f:
            data = json.load(f)
        data[str(id)][key] = value

        with open(JSON, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent="\t", ensure_ascii=False)

    # BaekJoon Web Parsing #

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
    
    # Date Range -> List type return #

    def date_range(self, start, end):
        try:
            start = datetime.strptime(start, "%Y%m%d")
            end = datetime.strptime(end, "%Y%m%d")
            dates = [(start + timedelta(days=i)).strftime("%Y%m%d") for i in range((end-start).days+1)]
            return dates
        except Exception as e:
            print(e)
            return []

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)