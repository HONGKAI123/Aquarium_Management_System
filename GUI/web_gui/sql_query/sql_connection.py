from mysql.connector import connect

class connector():
    def __init__(self, username: str = '', password: str = ''):
        self.host = 'localhost'
        self.database = 'aquarium'
        self.user = 'root'
        self.password = 'lucifer'
        if (username is not None) and (password is not None):
            self.user = username
            self.password = password
        print(self.user,'\t',self.password)

    def connect(self):
        self.connection = connect(host = self.host,
                                  user = self.user,
                                  password = self.password,
                                  database = self.database)
        self.cursor = connect.cursor()

    def disconnect(self):
        self.cursor.close()
        self.connection.disconnect()
