from discord import *
from asyncio import *
from random import *
from re import *
from discord.ext.commands import *
import os

#Variable
folder="DataBase\\"

#V-1:시작할때
f=open(folder+'dsToken.txt','r',encoding='utf-8')
token=f.readline()
client=Bot(command_prefix="!")

#V-2:채팅도중
badwards=["씨발","시부레","개같은","병진","병신","씹","년","시발","ㅅㅂ","ㅄ","ㅂㅅ","ㅇㅇㄴㅇ","!욕"\
    ,"미친","놈","ㄱㅅㄲ","ㄳㄲ","ㅆㅂ","야발","느금","ㄴㄱㅁ","ㅈㄲ","좆","뒤져","뒤저"\
        "ㅋㅋㄹㅃㅃ","야발","시부랄"]
logger=[]

#V-3:명령어 전용
lvl=0
formular="0"
value_a=0
value_b=0
value_c=0
following_name=[]
heros=[]
hp_min=95
hp_max=150
dmg_min=15
dmg_max=45
tsn=0
before_channel=""

#V-4:유저 관리
user_data=[]
max_warn=5
Maker="Terry#9339"
Maker_Name="Terry"

#V-5:Data Base
wardCnt=5889
DBward=[]
last_ward=""

#Fuction

#F-1:인자값 받기
def argSplit(arg, findArg):
    args=split(" ",arg)
    for i in range(len(args)):
        if args[i].find(findArg)==-1:
            final=None
        else:
            return (args[i][args[i].find(findArg)+len(findArg):])
    return ""

#Class

#C-1:게임-영웅
class Hero:
    def __init__(self, own, name, hp, dmg):
        self.own=own
        self.name=name
        self.base_hp=hp
        self.hp=hp
        self.dmg=dmg

    def Attack(self, Atk_Hero ,count):
        for i in range(count):
            Atk_Hero.hp-=self.dmg
            if Atk_Hero.hp<0:
                Atk_Hero.hp=0
                break

    def Respawn(self):
        self.hp=self.base_hp

#C-2:유저-데이터 베이스
def getBool(value):
    if value=="True" or value=="true" or value=="t":
        return True
    elif value=="False" or value=="false" or value=="f":
        return False
    else:
        return None
class Data:
    def __init__(self,name,lvl,warn,mute,perm,cmd):
        self.name=name
        self.lvl=lvl
        self.warn=warn
        self.mute=getBool(mute)
        self.perm=getBool(perm)
        self.cmd=getBool(cmd)

#M-1:데이터 베이스-불러오기
#DB-File
f=open(folder+"DB_user.txt",'r',encoding='utf-8')
f2=open(folder+"DBward.txt","r",encoding='utf-8')
datas=f.readlines()
for i in range(len(datas)):
    datas[i]=datas[i].replace("\n","")
    gets=split(":",datas[i])
    lvl_yet="%.3f"%(float(gets[1]))
    user_data.append(Data(gets[0], float(lvl_yet), int(gets[2]), gets[3], gets[4],gets[5]))

for i in range(wardCnt):
    wardTxt=str(f2.readline()).replace("\n","")
    DBward.append(wardTxt)

#F-2:데이터 베이스-입력
#DB-File
def Save():
    f=open(folder+"DB_user.txt",'w',encoding='utf-8')
    for i in range(len(user_data)):
        f.writelines("%s:%.3f:%d:%s:%s:%s\n"%(user_data[i].name,user_data[i].lvl,user_data[i].warn,\
            user_data[i].mute,user_data[i].perm,user_data[i].cmd))

#F-3:함수식-str=>int
def setValue(var_a):
    if var_a!="":
        try:
            test=eval(var_a)
            return var_a
        except Exception:
            return None

#F-4:레벨 여부
def Is_Level(name,min_lvl):
    for i in range(len(user_data)):
        if user_data[i].name==name:
            if user_data[i].lvl>=min_lvl:
                return True
            else:
                return False

#F-5:부방장 여부
def Is_Host(name):
    for i in user_data:
        if i.name==name:
            if i.perm==True:
                return True
            else:
                return False

#F-6:유저 찾기
def getName(name):
    for i in range(len(user_data)):
        if user_data[i].name==name:
            return i
    return None

#F-7:문자열 변환
def changeStr(text,ing,ed):
    result=""
    for i in text:
        for j in range(len(ed)):
            if i==ed[j]:
                i=ing[j]
                break
        result+=i
    return result

#F-8:가위바위보
def rsp(var1, var2):#var1 봇//var2 유저
    if var1=="묵" and var2=="찌":
        return "내가 이겼당~ ㅋㅋ"
    elif var1=="묵" and var2=="빠":
        return "내가 져써.."
    elif var1=="찌" and var2=="빠":
        return "응, 내가 이김!"
    elif var2=="묵" and var1=="찌":
        return "너가 이김.."
    elif var2=="묵" and var1=="빠":
        return "내가 이김 ㅋ"
    elif var2=="찌" and var1=="빠":
        return "그래.. 니가 이겼당.."
    elif var1==var2:
        return "비김"
    else:
        return None

#Discord Function

#DF-1:들어올때
@client.event
async def on_member_join(user):
    print(f"[On_Join] : {user}")

#DF-2:봇 시작할때
@client.event
async def on_ready():
    global lvl
    print("[On_Ready] : Connect")
    await client.change_presence(activity=Game("연산"))

#DF-3:메세지 받을때
@client.event
async def on_message(msg):
    global before_channel
    global formular
    global value_a, value_b, value_c
    global following_name
    global heros
    global hp_max,hp_min
    global dmg_max,dmg_min
    global user_data
    global last_ward
    global tsn

    #code1 : 텍스트 설정
    text=msg.content
    name=str(msg.author)
    ID=str(msg.author)
    name=name[:name.find("#")]
    user_num=getName(name)
    if name!="F(bot)":
        #명령어와 인자 구분
        if text.find(" ")!=-1:
            empty=text.find(" ")
            cmd=text[:empty]
            arg=text[empty+1:]
        else:
            cmd=text
            arg=None

        #데이터 베이스
        exist_bool=False
        for i in range(len(user_data)):
            if user_data[i].name==name:
                #기본 레벨 상승
                user_data[i].lvl+=(randint(1,15))*0.001
                #추가 레벨 상승
                if len(text)<100:
                    user_data[i].lvl+=len(text)*0.0001
                else:
                    user_data[i].lvl+=0.01
                exist_bool=True
                break
            else:
                exist_bool=False

        #데이터가 없다면=>데이터 생성
        #DB-File
        if exist_bool==False:
            user_data.append(Data(name,0,0,False,False,True))
            print(f"[Add_Data] : {name}")
            user_num=len(user_data)-1

        #로그
        channel=str(msg.channel).replace(":","_")
        if before_channel!=channel:
            print(f"\n[{channel}]")
            before_channel=channel
        print(f"{name} >> {text}")

        #커맨드
        if user_data[user_num].cmd==False:
            print(f"[Command_Cancle] : {name}")
            return 0

        #공지 채팅
        if str(msg.channel).find("공지")!=-1:
            if ID!=Maker and Is_Host(name)==False:
                print(f"[Channel_Cancle] : {name}")
                await msg.delete()
                return 0
        
        #따라하기
        for i in following_name:
            if i==name:
                await msg.channel.send(text)

        #욕 감지
        finded=False
        for i in badwards:
            for j in i:
                if text.find(j)!=-1:
                    finded=True
                else:
                    finded=False
                    break
            if finded==True:
                await msg.channel.send("__**욕설**__ 감지!!")
                break
        #저장
        Save()

        #뮤트 처리
        if ID!=Maker:
            for i in range(len(user_data)):
                if user_data[i].name==name:
                    if user_data[i].mute==True:
                        await msg.delete()
                        print(f"[Mute_Cancle] : {name}")
                        return 0
        #code2 : 대화
        if text=="넌 왜나와":
            await msg.channel.send("나 불렀자나요!")
            await msg.add_reaction("😠")
        if text=="함수봇":
            await msg.channel.send("무슨 일이오")
            await msg.add_reaction("🍀")
        if text=="앙" or text=="앙?" or text=="야":
            await msg.channel.send("앙?")
        if text=="선":
            await msg.channel.send("넘네")
        if text=="넘네":
            await msg.channel.send("선")
        if text=="자기야":
            await msg.channel.send("웅?")
        if text=="무야호":
            await msg.channel.send("무야호~~!")
            await msg.add_reaction("😮")
        elif text.find("갈게")!=-1 or text.find("ㅂㅂ")!=-1 or text.find("ㅃ")!=-1:
            await msg.channel.send("안녕히가세요!")
            await msg.add_reaction("🤗")
        elif text.find("잔다")!=-1 or text.find("잘게")!=-1:
            await msg.channel.send("{0}님 제 꿈꿔요♥!".format(name))
            await msg.add_reaction("😘")
        if text=="!help" or text=="!도움말":
            embed=Embed(title="도움말",color=0x0F73FF)
            embed.add_field(name="!embed name:[text] value:[text]",value="임베드를 생성합니다",inline=False)
            embed.add_field(name="!rect x:[value] y:[value] txt:[text]",value="사각형을 출력합니다.",inline=False)
            embed.add_field(name="!clab cnt:[value]",value="박수를 칩니다.",inline=False)
            embed.add_field(name="!calc [식]",value="식을 계산합니다.",inline=False)
            txt1="미지수 a,b,c가 포함이 가능합니다.\n"
            txt1+="!for set:[식] -> 식을 설정합니다.\n"
            txt1+="!for a:[value] -> a의 값을 설정합니다.\n"
            txt1+="!for b:[value] -> b의 값을 설정합니다.\n"
            txt1+="!for c:[value] -> b의 값을 설정합니다.\n"
            txt1+="ex)!for set:-3b*c/2a\n"
            txt1+="ex)!for a:2 b:5 c:2"  
            embed.add_field(name="!for",value=txt1,inline=False)
            embed.add_field(name="!run",value="!for을 계산합니다.",inline=False)
            embed.add_field(name="!split txt:[text] arg:[text]",value="txt를 arg로 분할합니다.",inline=False)
            embed.add_field(name="!follow b:[true/false]",value="봇이 따라할 여부를 결정합니다.",inline=False)
            embed.add_field(name="!hero name:[text]",value="랜덤한 HP,DMG를 가진 히어로를 생성합니다.",inline=False)
            embed.add_field(name="!h atk:[name]",value="[name]을가진 히어로를 공격합니다.",inline=False)
            embed.add_field(name="!hp min:[value] max:[value]",value="히어로의 hp최소/최대치를 변경합니다.",inline=False)
            embed.add_field(name="!dmg min:[value] max:[value]",value="히어로의 dmg최소/최대치를 변경합니다.",inline=False)
            embed.add_field(name="!info",value="자신의 정보를 출력합니다.",inline=False)
            embed.add_field(name="!admin",value="자신의 계급을 알수있습니다.",inline=False)
            await msg.channel.send(embed=embed)
        if text.find("안녕")!=-1 or text.find("하이")!=-1 or text.find("ㅎㅇ")!=-1:
            if ID==Maker:
                await msg.channel.send("제작자다!")
                await msg.add_reaction("☘")
            elif Is_Host(name):
                await msg.channel.send("부방장이다!")
            elif name=="히공" or name=="heegong":
                await msg.channel.send("히공 바보!")
            elif name=="Kiddie":
                await msg.channel.send("어이쿠!")
                await msg.add_reaction("😋")
            else:
                await msg.channel.send("{0}님이당!".format(name))
        elif text.find("ㅇㅈ?")!=-1 or text.find("히공 바보")!=-1 :
            await msg.channel.send("인정!!")
        elif text.find("ㅗㅜㅑ")!=-1:
            await msg.channel.send("ㅗㅜㅑ...")
            await msg.add_reaction("☺")
        elif (text.find("호")!=-1 and (text.find("롤")!=-1 or text.find("로")!=-1)) or (text.find("ㅎ")!=-1 and text.find("ㄹ")!=-1):
            await msg.channel.send("호로롤롤롤롤롤로로롤")
        elif text.find("5번")!=-1:
            await msg.channel.send("어, fuXk해 fuXk")
        elif text.find("4번")!=-1:
            r1=randint(0,4)
            if r1==0:
                result="은 개인주의야"
            elif r1==1:
                result="은 독신주의야"
            elif r1==2:
                result="한국말 못알아 듣는척해"
            elif r1==3:
                result="팀버려?"
            elif r1==4:
                result="X나 이기적인 4번!"
            await msg.channel.send(result)
        elif text.find("3번")!=-1:
            r1=randint(0,4)
            if r1==0:
                result="너 X발 뭐해!"
            elif r1==1:
                result="입닫아! 입 냄새나!"
            elif r1==2:
                result="놀러왔어?"
            elif r1==3:
                result="반으로 죽일거야"
            elif r1==4:
                result="니 엉덩이 자랑하고 싶냐?"
            await msg.channel.send(result)
        elif text.find("6번")!=-1:
            r1=randint(0,1)
            if r1==0:
                result="버섯"
            elif r1==1:
                result="니가 아브배우야? shut up!"
            await msg.channel.send(result)
        if randint(0,50)==0:
            if text.find("ㅋ")!=-1 or text.find("ㄷ")!=-1:
                if text.find("ㅋ")!=-1:
                    return_txt="ㅋ"
                elif text.find("ㄷ")!=-1:
                    return_txt="ㄷ"
                result=""
                for i in text:
                    if i==return_txt:
                        result+=return_txt
                if len(result)>1:
                    if len(result)<200:
                        await msg.channel.send(result)
                    else:
                        result=return_txt*20
                        await msg.channel.send(result)
        if text.find("히히")!=-1:
            await msg.channel.send("공공")
        elif text.find("힘들어")!=-1 or text.find("슬퍼")!=-1:
            await msg.channel.send("힘내 ㅠㅠ")
        if randint(0,50)==0:
            if text.find("대")!=-1 or text.find("머")!=-1:
                result=""
                before=[i for i in text]
                for i in range(len(before)):
                    if before[i]=="대":
                        before[i]="머"
                    elif before[i]=="머":
                        before[i]="대"
                    result+=before[i]
                await msg.channel.send(result)
            elif text.find("에엑따")!=-1 or text.find("히익")!=-1 or text.find("힉")!=-1 or text.find("에?")!=-1:
                await msg.channel.send("히익?")

        #code3 : 명령어-No Arg
        if text=="!admin":#권력 테스트
            if ID==Maker or Is_Level(name, 70):
                await msg.channel.send(f"**{name}**님이 **관리자**가 되었습니다.")
                await msg.add_reaction("😂")
            elif Is_Host(name):
                await msg.channel.send(f"**{name}**님이 **부방장**이 되었습니다.")
            elif Is_Level(name, 15):
                await msg.channel.send("**{0}**님이 **관리자 권한**을 해킹했습니다.".format(name))
            else:
                await msg.channel.send("**{0}**님이 **관리자 권한**을 노렸습니다.".format(name))
                await msg.add_reaction("😡")
        if cmd=="!run":#함수 실행
            try:
                forResult=""
                formularB=formular.replace("+"," + ")
                formularB=formularB.replace("-"," - ")
                formularB=formularB.replace("*"," * ")
                formularB=formularB.replace("/"," / ")
                formularB=formularB.replace("^"," ** ")
                forSplit=split(" ",formularB)
                for i in range(len(forSplit)):
                    if forSplit[i]=="a":
                        forSplit[i]="1a"
                    if forSplit[i]=="b":
                        forSplit[i]="1b"
                    if forSplit[i]=="c":
                        forSplit[i]="1c"
                    if forSplit[i]=="ac":
                        forSplit[i]="1ac"
                    if forSplit[i]=="ab":
                        forSplit[i]="1ab"
                    forResult+=forSplit[i]
                formularB=forResult
                formularB=formularB.replace("a",("*{0}".format(value_a)))
                formularB=formularB.replace("b",("*{0}".format(value_b)))
                formularB=formularB.replace("c",("*{0}".format(value_c)))
                if formularB[0]!="+" and formularB[0]!="-" and formularB[0]!="(" and formularB[0]!="{" and formularB[0]!="[":
                    a=int(formularB[0])
                if formularB.find(",")!=-1 or formularB.find(":")!=-1 or formularB.find("'")!=-1 or formularB.find('"')!=-1:
                    a=int(formularB[len(formularB)+1])
                result=eval(formularB)
                await msg.channel.send("{0} = {1}".format(formular,result))
            except Exception:
                await msg.channel.send("연산 오류!!")
        if cmd=="!hero":#게임-영웅:생성
            if arg==None:
                await msg.channel.send("사용법 : !hero name:[text]")
        if cmd=="!id":#아이디 출력
            await msg.channel.send(msg.author.id)
        if cmd=="!info" or cmd=="!정보":#정보 출력
            for i in user_data:
                if i.name==name:
                    rank="Unknown"
                    if i.lvl>=67.5 and i.lvl<70:
                        rank="__전설__"
                    elif i.lvl>=65 and i.lvl<67.5:
                        rank="쿼크"
                    elif i.lvl>=62.5 and i.lvl<65:
                        rank="전자"
                    elif i.lvl>=60 and i.lvl<62.5:
                        rank="원자핵"
                    elif i.lvl>=57.5 and i.lvl<60:
                        rank="원자"
                    elif i.lvl>=55 and i.lvl<57.5:
                        rank="분자"
                    elif i.lvl>=52.5 and i.lvl<55:
                        rank="__DNA__"
                    elif i.lvl>=50 and i.lvl<52.5:
                        rank="세포"
                    elif i.lvl>=47.5 and i.lvl<50:
                        rank="Known"
                    elif i.lvl>=45 and i.lvl<47.5:
                        rank="고래"
                    elif i.lvl>=42.5 and i.lvl<45:
                        rank="지배자"
                    elif i.lvl>=40 and i.lvl<42.5:
                        rank="__마스터__"
                    elif i.lvl>=37.5 and i.lvl<40:
                        rank="MVP"
                    elif i.lvl>=35 and i.lvl<37.5:
                        rank="VIP"
                    elif i.lvl>=32.5 and i.lvl<35:
                        rank="__다이아__"
                    elif i.lvl>=30 and i.lvl<32.5:
                        rank="채팅 장관"
                    elif i.lvl>=27.5 and i.lvl<30:
                        rank="__플레티넘__"
                    elif i.lvl>=25 and i.lvl<27.5:
                        rank="판사"
                    elif i.lvl>=22.5 and i.lvl<25:
                        rank="__골드__"
                    elif i.lvl>=20 and i.lvl<22.5:
                        rank="변호사"
                    elif i.lvl>=17.5 and i.lvl<20:
                        rank="시장"
                    elif i.lvl>=15 and i.lvl<17.5:
                        rank="__실버__"
                    elif i.lvl>=10 and i.lvl<15:
                        rank="경찰"
                    elif i.lvl>=7.5 and i.lvl<10:
                        rank="__브론즈__"
                    elif i.lvl>=5 and i.lvl<7.5:
                        rank="시민"
                    elif i.lvl>=2.5 and i.lvl<5:
                        rank="고수"
                    elif i.lvl>=1 and i.lvl<2.5:
                        rank="중수"
                    elif i.lvl>=0.5 and i.lvl<1:
                        rank="하수"
                    elif i.lvl<0.5:
                        rank="입문자"
                    embed=Embed(title="INFO",color=0xEFFF77)
                    embed.add_field(name="이름",value=f"**{i.name}**",inline=False)
                    embed.add_field(name="레벨",value="**%.3f**"%(i.lvl),inline=False)
                    embed.add_field(name="경고",value="**%d**"%(i.warn),inline=False)
                    embed.add_field(name="랭크",value="**%s**"%(rank),inline=False)
                    embed.add_field(name="부방장",value="**%s**"%(i.perm),inline=False)
                    embed.add_field(name="커맨드",value="**%s**"%(i.cmd),inline=False)
                    embed.set_thumbnail(url=msg.author.avatar_url)
                    if i.lvl>=45:
                        embed.set_image(url="https://cdn.discordapp.com/attachments/744881719336763462/752442570726047744/Master.png")
                    await msg.channel.send(embed=embed)
                    return 0
        if cmd=="!제작":#제작 지원
            embed=Embed(title="제작 및 도움",color=0x2AFF00)
            embed.add_field(name="코드 작성(제작)/기획",value="Terry",inline=False)
            embed.add_field(name="도움",value="히공\n파이떤\n김민욱",inline=False)
            embed.add_field(name="테스트",value="Terry\n평범한 리눅서\ncyalume\n정의석\n해에킹\n기상모두",inline=False)
            embed.add_field(name="언어",value="Python",inline=False)
            embed.set_image(url="https://i.pinimg.com/236x/ed/66/63/ed666327dd3ce274d94f2b3547155891.jpg")
            await msg.channel.send(embed=embed)
        if cmd=="!부방장":#부방장 출력
            result=""
            for i in user_data:
                if i.perm==True:
                    result+=f"{i.name}\n"
            embed=Embed(title="부방장 목록",description=result,color=0xFF7F00)
            await msg.channel.send(embed=embed)
        elif cmd==("!ms"):#뮤트 리스트
            result=""
            for i in range(len(user_data)):
                if user_data[i].mute==True:
                    result+=f"{user_data[i].name}\n"
            embed=Embed(title="Mute List",description=result,color=0xFF1459)
            await msg.channel.send(embed=embed)
        elif cmd=="!data":#데이터 축력
            embed=Embed(title="User Data", color=0xE6BFFF)
            for i in user_data:
                value="LV : %.3f"%(i.lvl)
                value+=f"\n경고 : {i.warn}\n뮤트 : {i.mute}\n부방장 : {i.perm}\n커맨드 : {i.cmd}"
                embed.add_field(name=f"이름 : {i.name}",value=value,inline=True)
            await msg.channel.send(embed=embed)
        elif cmd=="!dice":#주사위
            result=randint(1,6)
            await msg.channel.send(f"난수 : {result}")
        elif cmd=="!cs":
            result=""
            for i in range(len(user_data)):
                if user_data[i].cmd==False:
                    result+=f"{user_data[i].name}\n"
            embed=Embed(title="Cmd False List",description=result,color=0xFF1459)
            await msg.channel.send(embed=embed)
         #code4 : 명령어-Arg
        if arg!=None:
            arg+=" "
            if cmd=="!embed":#임베드 생성
                name=argSplit(arg, "name:")
                value=argSplit(arg, "value:").replace("[]"," ")
                colorValue=randint(0,6)
                if colorValue==0:
                    color=0xFF0000
                elif colorValue==1:
                    color=0x00FF00
                elif colorValue==2:
                    color=0x0000FF
                elif colorValue==3:
                    color=0xFF00FF
                elif colorValue==4:
                    color=0xFFFF00
                elif colorValue==5:
                    color=0x00FFFF
                elif colorValue==6:
                    color=0x999999
                embed=Embed(title=name,description=value,color=color)
                await msg.channel.send(embed=embed)
            elif cmd=="!rect":#사각형 출력
                text=""
                try:
                    x=int(argSplit(arg, "x:"))
                except ValueError:
                    x=1
                try:
                    y=int(argSplit(arg, "y:"))
                except ValueError:
                    y=1
                txt=argSplit(arg, "txt:")
                if txt=="":
                    txt="■"
                if x>20 or y>20 or x<1 or y<1:
                    await msg.channel.send("x또는 y는 20이하, 1이상이여야 해요!")
                    return 0
                for j in range(y):
                    for i in range(x):
                        text+=txt
                    text+="\n"
                try:
                    await msg.channel.send(text)
                except Exception:
                    await msg.channel.send("에러!")
            if cmd=="!clab":#박수
                try:
                    count=int(argSplit(arg,"cnt:"))
                except:
                    count=2
                if count>300 or count<1:
                    await msg.channel.send("cnt는 300이하, 1이상이여야 해요!")
                    return 0
                text=""
                for i in range(count):
                    text+="짝"
                try:
                    await msg.channel.send(text)
                except Exception:
                    await msg.channel.send("에러!")
            if cmd=="!calc":#계산
                try:
                    if arg[0]!="+" and arg[0]!="-" and arg[0]!="(" and arg[0]!="{" and arg[0]!="[":
                        a=int(arg[0])
                    if arg.find(",")!=-1 or arg.find(":")!=-1 or arg.find("'")!=-1 or arg.find('"')!=-1:
                        a=int(arg[len(arg)+1])
                    arg=arg.replace("^","**")
                    result=eval(arg)
                except Exception:
                    result="연산 오류!"
                await msg.channel.send("{0}".format(result))
            if cmd=="!for":#식 설정
                if arg!=None:
                    sets=argSplit(arg,"set:")
                    var_a=argSplit(arg,"a:").replace("^","**")
                    var_b=argSplit(arg,"b:").replace("^","**")
                    var_c=argSplit(arg,"c:").replace("^","**")
                    if sets!="":
                        formular=sets
                        await msg.channel.send("식 = {0}".format(formular))
                    if var_a!="":
                        before_a=setValue(var_a)
                        if before_a==None:
                            await msg.channel.send("값이 이상해요!")
                        else:
                            value_a=before_a
                            await msg.channel.send("a = {0}".format(value_a))
                    if var_b!="":
                        before_b=setValue(var_b)
                        if before_b==None:
                            await msg.channel.send("값이 이상해요!")
                        else:
                            value_b=before_b
                            await msg.channel.send("b = {0}".format(value_b))
                    if var_c!="":
                        before_c=setValue(var_c)
                        if before_c==None:
                            await msg.channel.send("값이 이상해요!")
                        else:
                            value_c=before_c
                            await msg.channel.send("c = {0}".format(value_c))
            elif cmd=="!split":#텍스트 나누기
                try:
                    splited=argSplit(arg,"txt:")
                    spliting=argSplit(arg,"arg:")
                    result=split(spliting,splited)
                    await msg.channel.send(result)
                except Exception:
                    await msg.channel.send("예상치 못한 에러에요!")
            elif cmd=="!follow":#따라하기
                TFbool=argSplit(arg, "b:")
                target=""
                if ID==Maker or Is_Host(name):
                    target=argSplit(arg, "target:").replace("[]"," ")
                nameF=name
                if target!="":
                    nameF=target
                if target=="all":
                    following_name=[]
                    await msg.channel.send("따라하기 목록을 초기화했어요!")
                if target=="show":
                    txt=""
                    if following_name==[]:
                        txt="아무도 없어요!"
                    else:
                        for i in following_name:
                            txt+=("%s//"%(i))
                    await msg.channel.send("{0}".format(txt))
                if TFbool=="true":
                    following_name.append(nameF)
                    await msg.channel.send("{0}님을 따라할게요!".format(nameF))
                if TFbool=="false":
                    for i in range(len(following_name)):
                        if following_name[i]==nameF:
                            del(following_name[i])
                            await msg.channel.send("{0}님을 그만 따라할게요!".format(nameF))
                            return 0
                    await msg.channel.send("{0}님은 따라하기 목록에 없어요!".format(nameF))
            elif cmd=="!Game" or cmd=="!game":#~하는중 설정//LEVEL:15
                if ID==Maker or Is_Level(name,15):
                    game=argSplit(arg,"name:").replace("[]"," ")
                    await msg.channel.send("'**{0}** 하는 중'으로 변경했어요!".format(game))
                    await client.change_presence(activity=Game(game))
                else:
                    await msg.channel.send("{0}님은 **권한**이 없어요!".format(name))
            elif cmd=="!hero":#게임-영웅-생성
                get_own=argSplit(arg,"own:")
                get_name=argSplit(arg,"name:")
                get_hp=argSplit(arg,"hp:")
                get_dmg=argSplit(arg,"dmg:")
                if ID!=Maker or get_own=="":
                    get_own=name
                if ID!=Maker or get_hp=="":
                    get_hp=randint(hp_min,hp_max)
                if ID!=Maker or get_dmg=="":
                    get_dmg=randint(dmg_min,dmg_max)
                for i in range(len(heros)):
                    if heros[i].own==get_own:
                        await msg.channel.send("{0}님의 영웅을 삭제했어요!".format(name))
                        del(heros[i])
                        break
                for i in range(len(heros)):
                    if heros[i].name==get_name:
                        await msg.channel.send("{0}은 이미 있는 이름이에요!".format(get_name))
                        return 0
                try:
                    heros.append(Hero(get_own,get_name,int(get_hp),int(get_dmg)))
                    await msg.channel.send(f"**{get_own}**님의 영웅을 만들었어요!\nHP : **{get_hp}** // DMG : **{get_dmg}** // Name : **{get_name}**")
                except Exception:
                    await msg.channel.send("연산 오류!")
                    
            elif cmd=="!h":#공격
                if heros==[]:
                    await msg.channel.send("영웅이 없어요!")
                    return 0
                num=[None,None]
                atk_hero=argSplit(arg, "atk:")
                by=argSplit(arg, "by:")
                cnt=argSplit(arg,"cnt:")
                if ID!=Maker or cnt=="":
                    cnt=1
                else:
                    try:
                        cnt=int(cnt)
                    except ValueError:
                        cnt=1
                if ID!=Maker or by=="":
                    by=name
                for i in range(len(heros)):
                    if heros[i].own==by:
                        num[0]=i
                    if heros[i].own==atk_hero or heros[i].name==atk_hero:
                        num[1]=i
                if num[0]==None:
                    await msg.channel.send("당신의 영웅이 없어요!")
                    return 0
                if num[1]==None:
                    await msg.channel.send(f"{atk_hero}라는 영웅이 없어요!")
                    return 0
                if  heros[num[0]].hp<=0:
                    await msg.channel.send(f"{heros[num[0]].name}님은 이미 죽었어요!")
                    return 0
                if  heros[num[1]].hp<=0:
                    await msg.channel.send(f"{heros[num[1]].name}님은 이미 죽었어요!")
                    return 0
                hp_before=heros[num[1]].hp
                heros[num[0]].Attack(heros[num[1]],cnt)
                await msg.channel.send(f"**{heros[num[0]].name}**님이 **{heros[num[1]].name}**님을 공격하였습니다.\n**{heros[num[1]].name}** : **{hp_before}** → **{heros[num[1]].hp}**")
            elif cmd=="!hp":
                get_min=argSplit(arg,"min:")
                get_max=argSplit(arg,"max:")
                if get_min!="":
                    try:
                        get_min=int(get_min)
                    except ValueError:
                        get_min=hp_min
                else:
                    get_min=hp_min
                if get_max!="":
                    try:
                        get_max=int(get_max)
                    except ValueError:
                        get_max=hp_max
                else:
                    get_max=hp_max
                if get_min<=0 or get_max<=0:
                    await msg.channel.send("min과 max는 1이상이어야 해요!")
                    return 0
                hp_min=get_min
                hp_max=get_max
                await msg.channel.send(f"HP 설정 => [최소:**{hp_min}**//최대:**{hp_max}**]")
            elif cmd=="!dmg":
                get_min=argSplit(arg,"min:")
                get_max=argSplit(arg,"max:")
                if get_min!="":
                    try:
                        get_min=int(get_min)
                    except ValueError:
                        get_min=dmg_min
                else:
                    get_min=dmg_min
                if get_max!="":
                    try:
                        get_max=int(get_max)
                    except ValueError:
                        get_max=dmg_max
                else:
                    get_max=dmg_max
                if get_min<=0 or get_max<=0:
                    await msg.channel.send("min과 max는 1이상이어야 해요!")
                    return 0
                dmg_min=get_min
                dmg_max=get_max
                await msg.channel.send(f"DMG 설정 => [최소:**{dmg_min}**//최대:**{dmg_max}**]")
            elif cmd=="!hs":
                target=argSplit(arg,"name:")
                if target=="all":
                    txt=""
                    for i in heros:
                        txt+=f"{i.name}//"
                    await msg.channel.send(txt)
                else:
                    num=None
                    for i in range(len(heros)):
                        if target==heros[i].name:
                            num=i
                    if num==None:
                        await msg.channel.send(f"{target}이라는 영웅이 없어요.")
                        return 0
                    await msg.channel.send(f"**{heros[num].name}**[**{heros[num].own}**] => HP : **{heros[num].hp}** // DMG : **{heros[num].dmg}**")
            elif cmd=="!경고" or cmd=="!warn":#경고//Perm:Host
                if ID==Maker or Is_Host(name):
                    warn_value=argSplit(arg,"value:")
                    warn_name=argSplit(arg,"name:").replace("[]"," ")
                    if warn_value=="":
                        warn_value=1
                    else:
                        try:
                            warn_value=int(warn_value)
                        except Exception:
                            await msg.channel.send("정수를 입력하세요!")
                            return 0
                    if name!=Maker_Name:
                        if warn_name==Maker_Name or  Is_Host(warn_name):
                            await msg.channel.send("방장/부방장에게는 경고를 금지합니다.")
                            return 0
                    if warn_name!="":
                        for i in range(len(user_data)):
                            if user_data[i].name==warn_name:
                                before_warn=user_data[i].warn
                                user_data[i].warn+=warn_value
                                if user_data[i].warn<0:
                                    user_data[i].warn=0
                                if user_data[i].warn>50:
                                    user_data[i].warn=50
                                await msg.channel.send(f"**{warn_name}**의 경고 => **{before_warn}** → **{user_data[i].warn}**")
                                Save()
                                if user_data[i].warn>=max_warn:
                                    await msg.channel.send(f"**{warn_name}**님의 경고가 **{max_warn}** 이상입니다!")
                                return 0
                        await msg.channel.send(f"**{warn_name}**님은 존재하지 않습니다!")
                    elif warn_name=="":
                        await msg.channel.send("사용법 -> !경고 name:[name] value:[value]")
            elif cmd=="!mute" or cmd=="!뮤트":#뮤트//Perm:Host
                if ID==Maker or Is_Host(name):
                    get_name=argSplit(arg, "name:").replace("[]"," ")
                    get_bool=argSplit(arg, "b:")
                    if get_name=="":
                        await msg.channel.send("사용법 -> !mute name:[name] b:[t/f]")
                        return 0

                    if name!=Maker_Name:
                        if get_name==Maker_Name or Is_Host(get_name):
                            await msg.channel.send("방장/부방장에게는 뮤트를 금지합니다.")
                            return 0
                    if get_bool=="t" or get_bool=="true":
                        get_bool=True
                    elif get_bool=="f" or get_bool=="false":
                        get_bool=False
                    else:
                        await msg.channel.send("사용법 -> !mute name:[name] b:[t/f]")
                        return 0
                    for i in range(len(user_data)):
                        if user_data[i].name==get_name:
                            user_data[i].mute=get_bool
                            await msg.channel.send(f"**{user_data[i].name}**님의 뮤트는 **{user_data[i].mute}**입니다.")
                            Save()
                            return 0
                    await msg.channel.send(f"**{get_name}**님이라는 유저 이름 또는 유저 데이터가 존재하지 않습니다.")
                    return 0
                else:
                    await msg.channel.send(f"**{name}**님은 권한이 없거든요!")
                    return 0
            elif cmd=="!perm":#부방장 설정//Perm:Maker
                if ID==Maker:
                    get_name=argSplit(arg, "name:").replace("[]"," ")
                    get_bool=argSplit(arg, "b:")
                    if get_name=="":
                        await msg.channel.send("사용법 -> !perm name:[name] b:[t/f]")
                        return 0
                    if get_name==Maker:
                        await msg.channel.send("제작자는 부방장이 되지 못합니다.")
                        return 0

                    if get_bool=="t" or get_bool=="true":
                        get_bool=True
                    elif get_bool=="f" or get_bool=="false":
                        get_bool=False
                    else:
                        await msg.channel.send("사용법 -> !perm name:[name] b:[t/f]")
                        return 0
                    
                    for i in range(len(user_data)):
                        if user_data[i].name==get_name:
                            user_data[i].perm=get_bool
                            await msg.channel.send(f"**{user_data[i].name}**님의 부방장 여부는 **{user_data[i].perm}**")
                            Save()
                            return 0
                    await msg.channel.send(f"**{get_name}**님이라는 유저 이름 또는 유저 데이터가 존재하지 않습니다.")
                    return 0
            elif cmd=="!eval":#명령어//Perm:Maker
                if ID==Maker:
                    try:
                        await msg.channel.send(eval(arg))
                    except:
                        await msg.channel.send("에러!")
                else:
                    await msg.channel.send(f"{name}님은 권한이 없어요!")
            elif cmd=="!exec":#명령어//Perm:Maker
                if ID==Maker:
                    try:
                        await msg.channel.send(exec(arg))
                    except:
                        pass
                else:
                    await msg.channel.send(f"{name}님은 권한이 없어요!")
            elif cmd=="!say":#말하게 하기//Perm:Maker
                if ID==Maker:
                    try:
                        await msg.delete()
                        await msg.channel.send(arg)
                    except:
                        await msg.channel.send("에러!")
                else:
                    await msg.channel.send(f"{name}님은 권한이 없어요!")
            elif cmd=="!tri":
                txt1=argSplit(arg,"txt:").replace("[]"," ")
                txt2=""
                try:
                    value_h=int(argSplit(arg,"h:"))
                except Exception:
                    await msg.channel.send("에러!")
                    return 0
                if value_h<1 or value_h>20:
                    await msg.channel.send("높이는 1이상 20이하여야합니다.")
                    return 0
                if txt2=="":
                    txt2="\n"
                if len(txt1)>10 or len(txt2)>10:
                    await msg.channel.send("txt의 길이는 10자 이하여야합니다")
                    return 0
                result=""
                for i in range(value_h):
                    for j in range(i):
                        result+=txt1
                    result+=txt2
                await msg.channel.send(result)
            elif cmd=="!find":
                num=argSplit(arg,"name:")
                if num=="":
                    await msg.channel.send("사용법 : !find name:[name]")
                    return 0
                num=getName(num)
                await msg.channel.send(f"{num}")
            elif cmd=="!cmd":
                getN=argSplit(arg,"name:").replace("[]"," ")
                cmdBool=getBool(argSplit(arg,"b:"))
                if getN=="" or cmdBool==None:
                    await msg.channel.send("사용법 : !cmd name:[name] b:[t/f]")
                    return 0
                num=getName(getN)
                if num==None:
                    await msg.channel.send(f"**{getN}**님의 데이터가 없습니다.")
                    return 0
                if ID!=Maker:
                    if Is_Host(getN)==True or getN==Maker:
                        await msg.channel.send(f"**방장/부방장**의 커맨드는 조작할수 없습니다.")
                        return 0
                user_data[num].cmd=cmdBool
                await msg.channel.send(f"**{getN}**님의 커맨드는 **{cmdBool}**")
            elif cmd=="!r":
                rsp_bot=randint(0,2)
                if rsp_bot==0:
                    rsp_bot="묵"
                elif rsp_bot==1:
                    rsp_bot="찌"
                elif rsp_bot==2:
                    rsp_bot="빠"
                arg=arg.replace(" ","")
                result=rsp(rsp_bot,arg)
                if result==None:
                    await msg.channel.send("연산 에러!")
                    return 0
                await msg.channel.send(f"{rsp_bot}\n{result}")
            elif cmd=="!a":
                arg=arg.replace(" ","")
                last_char=arg[len(arg)-1]
                if last_ward!=arg[0] and last_ward!='':
                    await msg.channel.send(f"마지막 단어는 '{last_ward}' 인데요?")
                    return 0
                if len(arg)<2:
                    await msg.channel.send(f"단어는 2글자 이상이 되야해요!!")
                    return 0
                passBool=False
                for i in DBward:
                    if i==arg:
                        passBool=True
                        break
                if passBool==False:
                    await msg.channel.send("처음 들어보는 단어에요...")
                    return 0
                for i in DBward:
                    if i[0]==last_char:
                        if len(i)<2:
                            pass
                        elif i.find("하다")!=-1:
                            pass
                        elif i[len(i)-1]=="다":
                            pass
                        elif i.find("되다")!=-1:
                            pass
                        else:
                            await msg.channel.send(f"{i}")
                            last_ward=i[len(i)-1]
                            return 0
                await msg.channel.send("제가 졌어요 ㅠㅠ")
                last_ward=""
            elif cmd=="!b":
                arg=arg.replace(" ","")
                if arg=="reset":
                    tsn=0
                    return 0
                if arg=="show":
                    await msg.channel.send(f"[10진수 : {tsn}]   [16진수 : {hex(tsn)}]")
                    return 0

                num=str(tsn)
                if num.find("3")!=-1 or num.find("6")!=-1 or num.find("9")!=-1:
                    if arg=="짝" or arg=="ㅉ" or arg=="w":
                        tsn+=1
                    else:
                        await msg.channel.send("'짝'이라고 해야죠!")
                    return 0
                            
                if arg==hex(tsn):
                    tsn+=1
                    await msg.add_reaction("👍")
                    if tsn==369:
                        await msg.channel.send("게임 끝!! 369도달!!")
                        tsn=0
                        return 0
                else:
                    await msg.channel.send("틀렸어요!")
                    return 0
            elif cmd=="!encode":
                try:
                    await msg.channel.send(arg.encode("utf-8"))
                except Exception:
                    await msg.channel.send("인코딩중 오류가 났습니다")
            elif cmd=="!decode":
                try:
                    await msg.channel.send(bytes(arg).decode("utf-8"))
                except Exception:
                    await msg.channel.send("디코딩중 오류가 났습니다")
            Save()
                
client.run(token)
