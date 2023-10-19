with open(r"database/user.txt", "r+") as user_table:
    user_info = "1" + "\t" + "yolo111" + "\t" + "123" + "\t" + "23"
    user_table.write(user_info)
    # info = line.rstrip().split("\t")
    # print(info)


# 用户信息实体类
class User(object):
    def __init__(self, *args):
        self.__id = None
        self.__name = None
        self.__password = None
        self.__age = None

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if value:
            self.__id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if value:
            self.__name = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        if value:
            self.__password = value

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        if value:
            self.__age = value

# 模拟数据库查询
class UserService:
    users = []

    def __init__(self):
        for line in open(r"database/user.txt", "r+"):
            # user_info = "yolo111" + "\t" + "123" + "\n"
            # user_table.write(user_info)
            if line is not None or line == "":
                user_info = line.rstrip().split("\t")
                user = User()
                user.id = user_info[0]
                user.name = user_info[1]
                user.password = user_info[2]
                user.age = user_info[3]
                UserService.users.append(user)

    @classmethod
    def query_user_by_name(self, username):
        for user in self.users:
            if username == user['username']:
                return user

    @classmethod
    def query_user_by_id(self, user_id):
        for user in self.users:
            if user_id == user['id']:
                return user


user_service = UserService()
print(UserService.users[0].id)

