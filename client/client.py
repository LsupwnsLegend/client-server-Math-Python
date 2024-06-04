from tkinter import *
from tkinter import font
import random
import math

from socket import *
import json

class Client:
    def __init__(self, ip, port):
        self.cli = socket(AF_INET, SOCK_STREAM)
        self.cli.connect(
            (ip, port)
        )

    def connect(self):
        try:
            msg = self.cli.recv(1024).decode('utf-8')
        except Exception as e:
            print(f'ERROR: {str(e)}')
            exit()

        if msg == 'YOU ARE CONNECTED!':
            print(msg)
        else:
            exit()

    def sender(self, text):
        print('Отправляю запрос')
        self.cli.send(text.encode('utf-8'))
        while self.cli.recv(1024).decode('utf-8') != 'GETTED':
            self.cli.send(text.encode('utf-8'))

    def listen(self, req):
        if req:
            if req == 'disconnect':
                self.sender(req)
                print(self.cli.recv(1024).decode('utf-8'))
                self.cli.close()
            else:
                self.sender(req)

def StartWindow():
    global widgets
    for w in widgets:
        w.destroy()
        
    btnStart = Button(root, text = 'Начать игру', font=font2, bg="#99ff99", border = 0, height=2, width=15, command = lambda: ChangeDificulty())
    btnStart.pack(pady = [HEIGHT//3, 100])
    
    btnScore = Button(root, text = 'Профиль', font=font2, bg="#cccccc", border = 0, height=2, width=15, command = lambda: Profile())
    btnScore.pack()
    
    widgets.append(btnStart)
    widgets.append(btnScore)

def ChangeDificulty():
    global widgets
    for w in widgets:
        w.destroy()

    btnBack = Button(root, text='↶', font=font3, border = 0, command = lambda: StartWindow())
    btnBack.pack(anchor = 'nw')
        
    dificult = Label(root, text = "Выберите сложность", font=font2, border = 0)
    dificult.pack(pady = 50)
    
    btnEasy = Button(root, text = 'Легкая', font=font2, bg="#99ff99", border = 0, height=2, width=15, command = lambda: ChangeMode(0))
    btnEasy.pack(pady = 25)
    
    btnMedium = Button(root, text = 'Средняя', font=font2, bg="#ffebb8", border = 0, height=2, width=15, command = lambda: ChangeMode(1))
    btnMedium.pack(pady = 25)
    
    btnHard = Button(root, text = 'Сложная', font=font2, bg="#ff9494", border = 0, height=2, width=15, command = lambda: ChangeMode(2))
    btnHard.pack(pady = 25)

    widgets.append(btnBack)
    widgets.append(dificult)
    widgets.append(btnEasy)
    widgets.append(btnMedium)
    widgets.append(btnHard)

def ChangeMode(dificultyGame):
    global widgets
    for w in widgets:
        w.destroy()

    btnBack = Button(root, text='↶', font=font3, border = 0, command = lambda: ChangeDificulty())
    btnBack.pack(anchor = 'nw')

    mod = Label(root, text = "Выберите режим", font=font2, border = 0)
    mod.pack(pady = 50)
    
    btnPlus = Button(root, text = 'Сложение', font=font2, bg="#99ff99", border = 0, height=2, width=15, command = lambda: lesgo(dificultyGame, 0))
    btnPlus.pack(pady = 25)
    
    btnMinus = Button(root, text = 'Вычитание', font=font2, bg="#99ff99", border = 0, height=2, width=15, command = lambda: lesgo(dificultyGame, 1))
    btnMinus.pack(pady = 25)
    
    btnMultiply = Button(root, text = 'Умножение', font=font2, bg="#ffebb8", border = 0, height=2, width=15, command = lambda: lesgo(dificultyGame, 2))
    btnMultiply.pack(pady = 25)
    
    btnDivision = Button(root, text = 'Деление', font=font2, bg="#ffebb8", border = 0, height=2, width=15, command = lambda: lesgo(dificultyGame, 3))
    btnDivision.pack(pady = 25)

    widgets.append(btnBack)
    widgets.append(mod)
    widgets.append(btnPlus)
    widgets.append(btnMinus)
    widgets.append(btnMultiply)
    widgets.append(btnDivision)

def lesgo(dificultyGame, modeGame):
    global widgets, dificulty, mode
    for w in widgets:
        w.destroy()

    dificulty = dificultyGame
    mode = modeGame

    question = ''
    
    label = Label(root, text = "Решите пример", font = font2, border = 0)
    label.pack(pady = 50)
    
    questionLabel = Label(root, text = '', font=font2, border = 0, height=2, width=15)
    questionLabel.pack(pady = 25)
    
    labelAns = Label(root, text = "Ваш ответ: ", font = font2, border = 0)
    labelAns.pack(pady = 25)
    
    entry = Entry(root, font = font2, border = 0, background = '#cccccc')
    entry.pack(pady = 10)

    ap1 = random.randint(int(math.pow(10, dificulty)), int(math.pow(10, dificulty+2)))
    ap2 = random.randint(int(math.pow(10, dificulty)), int(math.pow(10, dificulty+2)))

    if modeGame == 0:
        question = f'{ap1} + {ap2} = ?'
        questionLabel["text"] = question
        
    elif modeGame == 1:
        question = f'{ap1} - {ap2} = ?'
        questionLabel["text"] = question
        
    elif modeGame == 2:
        ap1 = random.randint(int(math.pow(10, dificulty)), int(math.pow(10, dificulty+1)))
        ap2 = random.randint(int(math.pow(10, dificulty)), int(math.pow(10, dificulty+1)))
        question = f'{ap1} × {ap2} = ?'
        questionLabel["text"] = question

    elif modeGame == 3:
        ap1 = random.randint(int(math.pow(10, dificulty)), int(math.pow(10, dificulty+1)))
        ap2 = random.randint(int(math.pow(10, dificulty)), int(math.pow(10, dificulty+1)))
        res = ap1*ap2
        question = f'{res} ÷ {ap2} = ?'
        questionLabel["text"] = question

    labelForAns = Label(root, text = "", font = font2, border = 0)
    labelForAns.pack(pady = 25)

    btnCheck = Button(root, text = 'Ответить', font=font2, bg="#99ff99", border = 0, height=2, width=15, command = lambda: CheckAnswer(entry.get(), ap1, ap2))
    btnCheck.pack(pady = 25)

    btnSkip = Button(root, text = 'Пропустить', font=font2, bg="#cccccc", border = 0, height=2, width=15, command = lambda: lesgo(dificulty, mode))
    btnSkip.pack(pady = 25)

    widgets.append(label)
    widgets.append(questionLabel)
    widgets.append(labelAns)
    widgets.append(entry)
    widgets.append(labelForAns)
    widgets.append(btnCheck)
    widgets.append(btnSkip)

def CheckAnswer(ans, ap1, ap2):
    global widgets, mode, dificulty
    try:
        ans = int(ans)
        answers = [ap1 + ap2, ap1 - ap2, ap1 * ap2, ap1]
        if((mode == 0) and ((ap1 + ap2) == ans)):
            Verno()
            Counter(dificulty)
            
        elif((mode == 1) and ((ap1 - ap2) == ans)):
            Verno()
            Counter(dificulty)
            
        elif((mode == 2) and ((ap1 * ap2) == ans)):
            Verno()
            Counter(dificulty)
            
        elif((mode == 3) and (ap1 == ans)):
            Verno()
            Counter(dificulty)

        else:
            widgets[-3]['text']=f'Не верно!\nОтвет {answers[mode]}'
            widgets[-3]['fg']='#c70000'

            widgets[-2]['text']='Продолжить'
            widgets[-2]['command']=lambda: lesgo(dificulty, mode)

            widgets[-1]['text']='На главную'
            widgets[-1]['command']=lambda: StartWindow()

            widgets[-4]['state']='disabled'
        
    except Exception as e:
        widgets[-3]['text']='Введите число!'
        widgets[-3]['fg']='#c70000'
    #print(widgets)

def Verno():
    global widgets, dificulty, mode
    widgets[-3]['text']='Верно!'
    widgets[-3]['fg']='#00bd52'

    widgets[-2]['text']='Продолжить'
    widgets[-2]['command']=lambda: lesgo(dificulty, mode)

    widgets[-1]['text']='На главную'
    widgets[-1]['command']=lambda: StartWindow()

    widgets[-4]['state']='disabled'

def Counter(dif):
    global easyCount, mediumCount, hardCount, Name
    if dif == 0:
        easyCount += 1
    elif dif == 1:
        mediumCount += 1
    elif dif == 2:
        hardCount += 1

    try:
        sql = "update"
        params = [Name, easyCount, mediumCount, hardCount]
        ans = json.dumps(
            {'sql': sql, 'params': params}
        )
        client.listen(ans)
            
    except Exception as e:
        print(f'ERROR: {str(e)}')

def Profile():
    global widgets, easyCount, mediumCount, hardCount, Name
    for w in widgets:
        w.destroy()

    btnBack = Button(root, text='↶', font=font3, border = 0, command = lambda: StartWindow())
    btnBack.pack(anchor = 'nw')
        
    label = Label(root, text = f"{Name},\nздесь вы можете\nувидеть вашу статистику\nза все время", font = font2, border = 0, height = 4, width = 24)
    label.pack(pady = 50)

    labelEasy = Label(root, text = f"Легкие задачи: {easyCount}", font = font2, border = 0, height = 1, width = 24, fg = '#33ff33')
    labelEasy.pack(pady = 10)

    labelMedium = Label(root, text = f"Средние задачи: {mediumCount}", font = font2, border = 0, height = 1, width = 24, fg = '#ffce52')
    labelMedium.pack(pady = 10)

    labelHard = Label(root, text = f"Сложные задачи: {hardCount}", font = font2, border = 0, height = 1, width = 24, fg = '#ff2e2e')
    labelHard.pack(pady = 10)

    widgets.append(btnBack)
    widgets.append(label)
    widgets.append(labelEasy)
    widgets.append(labelMedium)
    widgets.append(labelHard)

def Main():
    global widgets
    for w in widgets:
        w.destroy()
    widgets = []

    infoLabel = Label(root, text = f"Математический задачник", font = font2, border = 0, height = 1, width = 24)
    infoLabel.pack(pady = 100)
    btnRegister = Button(root, text = 'Зарегистрироваться', font = font2, bg = "#247ad6", fg = '#ffffff', border = 0, height = 2, width=20, command = lambda: Register())
    btnRegister.pack(pady = [100, 30])
    btnJoin = Button(root, text = 'Войти', font = font2, bg="#cccccc", border = 0, height = 2, width = 20, command = lambda: Join())
    btnJoin.pack()

    widgets.append(infoLabel)
    widgets.append(btnRegister)
    widgets.append(btnJoin)

def Register():
    global widgets
    for w in widgets:
        w.destroy()
    widgets = []
        
    btnBack = Button(root, text='↶', font=font3, border = 0, command = lambda: Main())
    btnBack.pack(anchor = 'nw')
    
    registerLabel = Label(root, text = f"Регистрация", font = font2, border = 0, height = 1, width = 24)
    registerLabel.pack(pady = 50)
    
    loginLabel = Label(root, text = f"1. Придумайте логин", font = font2, border = 0, height = 1, width = 24)
    loginLabel.pack(pady = 10)
    
    login = Entry(root, font = font2, border = 0, background = '#cccccc')
    login.pack(pady = 10)
    
    passwordLabel = Label(root, text = f"2. Придумайте пароль", font = font2, border = 0, height = 1, width = 24)
    passwordLabel.pack(pady = 10)
    
    password = Entry(root, font = font2, border = 0, background = '#cccccc')
    password.pack(pady = 10)
    
    passwordTwiceLabel = Label(root, text = f"3. Повторите пароль", font = font2, border = 0, height = 1, width = 24)
    passwordTwiceLabel.pack(pady = 10)
    
    passwordTwice = Entry(root, font = font2, border = 0, background = '#cccccc')
    passwordTwice.pack(pady = 10)

    btnRegister = Button(root, text = 'Регистрация', font = font2, bg = "#247ad6", fg = '#ffffff', border = 0, height = 2, width=20, command = lambda: CheckReg(login.get(), password.get(), passwordTwice.get()))
    btnRegister.pack(pady = 50)
    
    join = Button(root, text = 'Если у вас уже есть аккаунт', font = font2, bg="#cccccc", border = 0, height = 2, width = 26, command = lambda: Join())
    join.pack(pady = 0)

    widgets.append(btnBack)
    widgets.append(registerLabel)
    widgets.append(loginLabel)
    widgets.append(login)
    widgets.append(passwordLabel)
    widgets.append(password)
    widgets.append(passwordTwiceLabel)
    widgets.append(passwordTwice)
    widgets.append(btnRegister)
    widgets.append(join)
    #print(widgets)

def Join():
    global widgets
    for w in widgets:
        w.destroy()
    widgets = []

    btnBack = Button(root, text='↶', font=font3, border = 0, command = lambda: Main())
    btnBack.pack(anchor = 'nw')

    loginLabel = Label(root, text = f"Логин", font = font2, border = 0, height = 1, width = 24)
    loginLabel.pack(pady = 10)

    login = Entry(root, font = font2, border = 0, background = '#cccccc')
    login.pack(pady = 10)

    passwordLabel = Label(root, text = f"Пароль", font = font2, border = 0, height = 1, width = 24)
    passwordLabel.pack(pady = 10)
    
    password = Entry(root, font = font2, border = 0, background = '#cccccc')
    password.pack(pady = 10)

    join = Button(root, text = 'Вход', font = font2, bg="#cccccc", border = 0, height = 2, width = 26, command = lambda: CheckJoin(login.get(), password.get()))
    join.pack(pady = 50)

    widgets.append(btnBack)
    widgets.append(loginLabel)
    widgets.append(login)
    widgets.append(passwordLabel)
    widgets.append(password)
    widgets.append(join)

def CheckReg(login, password, passwordTwice):
    global widgets

    if (login == ''):
        widgets[4]['text']='2. Придумайте пароль'
        widgets[4]['fg']='#000000'
        widgets[5]['background']='#cccccc'
        widgets[6]['text']='3. Повторите пароль'
        widgets[6]['fg']='#000000'
        widgets[7]['background']='#cccccc'
        
        widgets[2]['text']='Введите логин!'
        widgets[2]['fg']='#c70000'
        widgets[3]['background']='#ff6161'
    elif(password == ''):
        widgets[2]['text']='1. Придумайте логин'
        widgets[2]['fg']='#000000'
        widgets[3]['background']='#cccccc'
        widgets[6]['text']='3. Повторите пароль'
        widgets[6]['fg']='#000000'
        widgets[7]['background']='#cccccc'
        
        widgets[4]['text']='Введите пароль!'
        widgets[4]['fg']='#c70000'
        widgets[5]['background']='#ff6161'
    elif(password != passwordTwice):
        widgets[2]['text']='1. Придумайте логин'
        widgets[2]['fg']='#000000'
        widgets[3]['background']='#cccccc'
        widgets[4]['text']='2. Придумайте пароль'
        widgets[4]['fg']='#000000'
        widgets[5]['background']='#cccccc'
        
        widgets[6]['text']='Пароли не совпадают!'
        widgets[6]['fg']='#c70000'
        widgets[7]['background']='#ff6161'
    else:
        widgets[2]['text']='1. Придумайте логин'
        widgets[2]['fg']='#000000'
        widgets[3]['background']='#cccccc'
        widgets[4]['text']='2. Придумайте пароль'
        widgets[4]['fg']='#000000'
        widgets[5]['background']='#cccccc'
        widgets[6]['text']='3. Повторите пароль'
        widgets[6]['fg']='#000000'
        widgets[7]['background']='#cccccc'
        
        if CheckBD('login', login):
            widgets[2]['text']='Логин уже занят!'
            widgets[2]['fg']='#c70000'
            widgets[3]['background']='#ff6161'
        else:
            RegisterServ(login, password)

def CheckJoin(login, password):
    global widgets

    if (login == ''):
        widgets[3]['text']='Пароль'
        widgets[3]['fg']='#000000'
        widgets[4]['background']='#cccccc'
        
        widgets[1]['text']='Введите логин!'
        widgets[1]['fg']='#c70000'
        widgets[2]['background']='#ff6161'
    elif(password == ''):
        widgets[1]['text']='Логин'
        widgets[1]['fg']='#000000'
        widgets[2]['background']='#cccccc'
        
        widgets[3]['text']='Введите пароль!'
        widgets[3]['fg']='#c70000'
        widgets[4]['background']='#ff6161'
    else:
        widgets[1]['text']='Логин'
        widgets[1]['fg']='#000000'
        widgets[2]['background']='#cccccc'
        widgets[3]['text']='Пароль'
        widgets[3]['fg']='#000000'
        widgets[4]['background']='#cccccc'

        if not (CheckBD('login', login)):
            widgets[1]['text']='Логина не существует!'
            widgets[1]['fg']='#c70000'
            widgets[2]['background']='#ff6161'
            
        elif not (CheckBD('loginPassword', [login, password])):
            widgets[3]['text']='Неверный пароль!'
            widgets[3]['fg']='#c70000'
            widgets[4]['background']='#ff6161'
        else:
            JoinServ(login, password)
                

def CheckBD(whatCheck, check):
    try:
        sql = whatCheck
        if sql == 'loginPassword':
            params = check
        else:
            params = [check]
        ans = json.dumps(
            {'sql': sql, 'params': params}
        )
        print(ans)
        client.listen(ans)
        data = json.loads(client.cli.recv(1024).decode('utf-8'))
        if data['answer']:
            #print(f'Server answer: \n\t{data["answer"]}')
            return True
        elif data['error']:
            print(f'Server error: \n\t{data["error"]}')
        else:
            return False
    except Exception as e:
        print(f'ERROR: {str(e)}')

def RegisterServ(login, password):
    try:
        sql = "register"
        params = [login, password, 0, 0, 0]
        ans = json.dumps(
            {'sql': sql, 'params': params}
        )
        client.listen(ans)
        
        JoinServ(login, password)
    except Exception as e:
        print(f'ERROR: {str(e)}')

def JoinServ(login, password):
    global easyCount, mediumCount, hardCount, Name
    try:
        sql = "join"
        params = [login, password]
        ans = json.dumps(
            {'sql': sql, 'params': params}
        )
        client.listen(ans)
        
        data = json.loads(client.cli.recv(1024).decode('utf-8'))
        print(data)
        if data['answer']:
            Name = data['answer'][0][1]
            easyCount = data['answer'][0][3]
            mediumCount = data['answer'][0][4]
            hardCount = data['answer'][0][5]
            StartWindow()
            
        elif data['error']:
            print(f'Server error: \n\t{data["error"]}')
            
    except Exception as e:
        print(f'ERROR: {str(e)}')

f = open('ip.txt', encoding='utf-8')
ip = f.readline()
f.close()

client = Client(ip, 7000)
client.connect()

root = Tk()

WIDTH = 540
HEIGHT = 960

font2 = font.Font(family= "Verdana", size=20, weight="normal", slant="roman")
font3 = font.Font(family= "Verdana", size=30, weight="bold", slant="roman")

widgets = []
easyCount = 0
mediumCount = 0
hardCount = 0
Name = ''
 
root.title("Математический задачник")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)

grafon = Canvas(root, width = WIDTH, height = HEIGHT)
grafon.place(x=0, y =0)

grafon.create_oval(WIDTH-100, HEIGHT-100, WIDTH+100, HEIGHT+100, fill="#41a399", outline = "#41a399")
grafon.create_oval(0-50, HEIGHT-50, 0+50, HEIGHT+50, fill="#5bbdb3", outline = "#5bbdb3")
grafon.create_oval(WIDTH//2-10, HEIGHT-70, WIDTH//2+50, HEIGHT-10, fill="#7dc798", outline = "#7dc798")
grafon.create_oval(WIDTH//2-200, HEIGHT-90, WIDTH//2-170, HEIGHT-60, fill="#a1d6b4", outline = "#a1d6b4")
grafon.create_oval(150, HEIGHT-150, 230, HEIGHT-70, fill="#66cdaa", outline = "#66cdaa")
grafon.create_oval(400, HEIGHT-110, 380, HEIGHT-90, fill="#8dd9bf", outline = "#8dd9bf")

Main()
 
root.mainloop()
