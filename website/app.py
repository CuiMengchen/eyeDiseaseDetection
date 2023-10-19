import os.path

import torch
from werkzeug.utils import secure_filename

from flask import Flask, request, flash, render_template, redirect, url_for, session
from flask_login import UserMixin, LoginManager, login_required, logout_user, login_user, current_user
from check_form import is_null, check_session

app = Flask(__name__)
app.secret_key = 'Lebrj'
# Model
model = torch.hub.load('../', 'custom', './best_eye.pt', source='local')

# 1、实例化登录管理对象
login_manager = LoginManager()

# 参数配置
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Access denied.'

login_manager.init_app(app)  # 初始化应用


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
    idx = 0
    for line in open(r"database/user.txt", "r+"):
        # user_info = "yolo111" + "\t" + "123" + "\n"
        # user_table.write(user_info)
        if len(line.strip()) != 0 or line == "":
            if line.rstrip != "":
                user_info = line.rstrip().split("\t")
                user = User()
                user.id = user_info[0]
                user.name = user_info[1]
                user.password = user_info[2]
                user.age = user_info[3]
                users.append(user)
                idx += 1

    @classmethod
    def query_user_by_name(self, username):
        for user in self.users:
            if username == user.name:
                return user
        return None

    @classmethod
    def query_user_by_id(self, user_id):
        for user in self.users:
            if user_id == user.id:
                return user
        return None

    @classmethod
    def query_user_by_name_password(self, username, password):
        for user in self.users:
            if username == user.name and password == user.password:
                return user
        return None


user_service = UserService()


@login_manager.user_loader
def user_loader(user_id: str):
    """
    :param user_id:
    :return:
    """
    if UserService.query_user_by_id(int(user_id)) is not None:
        curr_user = User()
        curr_user.id = user_id
        return curr_user


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('login.html')
    else:
        # print(request.form)
        # print(request.get_json())
        username = request.form['name']
        password = request.form['password']
        age = request.form['age']
        if is_null(username, password, age):
            login_massage = "Please input username, password, age."
            return render_template("login.html", message=login_massage)

        user = UserService.query_user_by_name(username)
        print(user)
        if user is not None:
            login_massage = "User already existed"
            return render_template("login.html", message=login_massage)

        user = User()
        user.id = str(UserService.idx)
        UserService.idx += 1
        user.name = username
        user.password = password
        user.age = age
        # elif is_existed(username, password):
        #     return render_template('index.html', username=username)
        # elif exist_user(username):
        #     login_massage = "温馨提示：密码错误，请输入正确密码"
        #     return render_template('login.html', message=login_massage)
        # else:
        #     login_massage = "温馨提示：不存在该用户，请先注册"
        #     return render_template('login.html', message=login_massage)
        with open(r"database/user.txt", "a") as user_table:
            user_info = str(user.id) + "\t" + user.name + "\t" + user.password + "\t" + user.age + "\r\n"
            user_table.write(user_info)
        session["username"] = username
        session["age"] = age
        user = {
            "name": username,
            "age": age
        }
        # return redirect(url_for('index', user))
        return render_template("index.html", user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user_info = check_session(session)

        if user_info:
            return render_template("index.html", user=user_info)
        else:
            username = request.form['name_login']
            password = request.form['password_login']

            user = UserService.query_user_by_name(username)

            if user:
                user = UserService.query_user_by_name_password(username, password)
                if user:
                    user_info = {
                        "name": user.name,
                        "age": user.age
                    }

                    session["username"] = user.name
                    session["age"] = user.age
                    return render_template("index.html", user=user_info)
                else:
                    login_massage = "Password wrong!"
                    return render_template("login.html", message=login_massage)
            else:
                login_massage = "Please register first!"
                return render_template("login.html", message=login_massage)
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    # 通过Flask-Login的logout_user方法登出用户
    session.pop("username")
    session.pop("age")
    return render_template("index.html")


@app.route('/' or "index")
def index():
    user_info = check_session(session)
    if user_info:
        return render_template("index.html", user=user_info)
    else:
        return render_template('index.html')


@app.route('/detect')
def detect():
    user_info = check_session(session)
    if user_info:
        return render_template("detect.html", user=user_info)
    else:
        return render_template('detect.html')
    
@app.route('/ssdDetect')
def ssdDetect():
    user_info = check_session(session)
    if user_info:
        return render_template("ssdDetect.html", user=user_info)
    else:
        return render_template('ssdDetect.html')


@app.route('/detect/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        save_name = "database/" + secure_filename(f.filename)
        f.save(save_name)

        img_path = save_name

        # Inference
        results = model(img_path)
        
        img_local_path_dir = os.path.join("website_res", "runs", "detect", "exp")

        # file name, file suffix
        file_name = os.path.splitext(secure_filename(f.filename))[0]
        file_name = file_name + ".jpg"

        msg = ""
        if results.xyxy[0][0][5] == 0:
            msg = "n"
        elif results.xyxy[0][0][5] == 1:
            msg = "d"
        elif results.xyxy[0][0][5] == 2:
            msg = "g"
        elif results.xyxy[0][0][5] == 3:
            msg = "c"
        # Results
        results.save(save_dir=img_local_path_dir)  # or .show(), .save(), .crop(), .pandas(), etc.

        img_local_path = os.path.join("website_res", "runs", "detect", "exp", secure_filename(file_name))
        # img_local_path = os.path.join(os.path.dirname(__file__), "website", "runs", "detect", "exp")

        import base64

        with open(img_local_path, 'rb') as img_f:
            img_stream = img_f.read()
            img_stream = base64.b64encode(img_stream).decode()

        with open(save_name, 'rb') as img_o:
            img_stream_o = img_o.read()
            img_stream_o = base64.b64encode(img_stream_o).decode()

        return render_template('detect.html', img_stream=img_stream, img_ori=img_stream_o, msg=msg)

    return render_template('detect.html')

@app.route('/ssdDetect/upload', methods=['GET', 'POST'])

def upload_ssdfile():
    if request.method == 'POST':
        f = request.files['file']
        save_name = "database/" + secure_filename(f.filename)
        f.save(save_name)

        img_path = save_name

        # Inference(ssd)


        from ssd import SSD
        from PIL import Image
        import cv2

        def map_clear(image):
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
            cl1 = clahe.apply(gray)
            out_image = cv2.cvtColor(cl1, cv2.COLOR_GRAY2RGB)
            return out_image

        #img = r"E:\research\SSD\ssd-keras-master\img\cataract_0064.jpg"
        image = cv2.imread(img_path)
        image = map_clear(image)

        image_new = Image.fromarray(image.astype('uint8')).convert('RGB')
        ssd = SSD()
        r_image = ssd.detect_image(image_new)
        #r_image.show()
        r_image.save(r"D:/result2.jpg")
        #image_label = ssd.detect_image(image_new)
        mc = 1
        ### import finished
        #results = model(img_path)

        #img_local_path_dir = os.path.join("website", "runs", "ssdDetect", "exp")

        # file name, file suffix
        #file_name = os.path.splitext(secure_filename(f.filename))[0]
        #file_name = file_name + ".jpg"

        msg = ""
        if r_image == "normal":
            msg = "n"
        elif r_image == "diabetic_retinopathy":
            msg = "d"
        elif r_image == "glaucoma":
            msg = "g"
        elif r_image == "cataract":
            msg = "c"
        # Results
        #results.save(img_local_path_dir)  # or .show(), .save(), .crop(), .pandas(), etc.

        #img_local_path = os.path.join("website", "runs", "detect", "exp", secure_filename(file_name))
        img_local_path = (r"D:/result2.jpg")
        import base64

        with open(img_local_path, 'rb') as img_f:
            img_stream = img_f.read()
            img_stream = base64.b64encode(img_stream).decode()

        with open(save_name, 'rb') as img_o:
            img_stream_o = img_o.read()
            img_stream_o = base64.b64encode(img_stream_o).decode()

        return render_template('ssdDetect.html', img_stream=img_stream, img_ori=img_stream_o, msg=msg)

    return render_template('ssdDetect.html')

@app.route('/glaucoma')
def glaucoma():
    user_info = check_session(session)
    if user_info:
        return render_template("glaucoma.html", user=user_info)
    else:
        return render_template("glaucoma.html")

@app.route('/cataract')
def cataract():
    user_info = check_session(session)
    if user_info:
        return render_template("cataract.html", user=user_info)
    else:
        return render_template("cataract.html")


@app.route('/diabetic')
def diabetic():
    user_info = check_session(session)
    if user_info:
        return render_template("diabetic.html", user=user_info)
    else:
        return render_template("diabetic.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
