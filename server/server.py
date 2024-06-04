from socket import *
import sqlite3 as sql
import json

class Server:
    def __init__(self, ip, port, base_name):
        print(f'Server IP: {ip}\nServer Port: {port}\n')
        self.data_name = base_name
        self.ser = socket(AF_INET, SOCK_STREAM)
        self.ser.bind(
            (ip, port)
        )
        self.ser.listen(3)

    def sender(self, user, text):
        user.send(text.encode('utf-8'))

    def start_server(self):
        while True:
            user, addr = self.ser.accept()
            print(f'Client connected:\n\tIP: {addr[0]}\n\tPORT: {addr[1]}')
            self.listen(user)

    def listen(self, user):
        self.sender(user, 'YOU ARE CONNECTED!')
        is_work = True

        while is_work:
            try:
                data = user.recv(1024)
                self.sender(user, 'GETTED')
            except Exception as e:
                data = ''
                is_work = False

            if len(data) > 0:
                msg = data.decode('utf-8')
                
                if msg == 'disconnect':
                    self.sender(user, 'YOU ARE DISCONNECTED')
                    print('Client disconnected!')
                    user.close()
                    is_work = False
                else:
                    con = sql.connect(self.data_name)
                    cur = con.cursor()
                        
                    dataJson = json.loads(msg)
                    if dataJson['sql'] == 'register':
                        print(f'Регистрирую')
                        try:
                            answer = [x for x in cur.execute("insert into users (login, password, easyCount, mediumCount, hardCount) values (?, ?, ?, ?, ?)", (dataJson['params'][0], dataJson['params'][1], dataJson['params'][2], dataJson['params'][3], dataJson['params'][4]))]
                            error = ''
                        except Exception as e:
                            error = str(e)
                            answer = ''
                    elif dataJson['sql'] == 'login':
                        print(f'Проверяю наличие логина')
                        try:
                            answer = [x for x in cur.execute("select * from users where login = ?", (dataJson['params'][0],))]
                            error = ''
                        except Exception as e:
                            error = str(e)
                            answer = ''
                    elif dataJson['sql'] == 'loginPassword':
                        print(f'Проверяю правильность пароля')
                        try:
                            answer = [x for x in cur.execute("select * from users where login = ? and password = ?", (dataJson['params'][0], dataJson['params'][1]))]
                            error = ''
                        except Exception as e:
                            error = str(e)
                            answer = 'Неверный пароль'
                    elif dataJson['sql'] == 'join':
                        print(f'Произвожу вход в аккаунт')
                        try:
                            answer = [x for x in cur.execute("select * from users where login = ? and password = ?", (dataJson['params'][0], dataJson['params'][1]))]
                            error = ''
                        except Exception as e:
                            error = str(e)
                            answer = ''
                    elif dataJson['sql'] == 'update':
                        print(f'Обновляю данные')
                        try:
                            answer = [x for x in cur.execute("update users set easyCount = ?, mediumCount = ?, hardCount = ? where login = ?", (dataJson['params'][1], dataJson['params'][2], dataJson['params'][3], dataJson['params'][0]))]
                            error = ''
                        except Exception as e:
                            error = str(e)
                            answer = ''
                    else:
                        try:
                            answer = [x for x in cur.execute(msg)]
                            error = ''
                        except Exception as e:
                            error = str(e)
                            answer = ''

                    con.commit()
                    cur.close()
                    con.close()

                    ans = json.dumps(
                        {'answer': answer, 'error': error}
                    )
                    self.sender(user, ans)
                data = b''
                msg = ''
            else:
                print('Client disconnected!')
                is_work = False

f = open('ip.txt', encoding='utf-8')
ip = f.readline()
f.close()

Server(ip, 7000, 'data.db').start_server()
