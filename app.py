from flask import Flask,request,render_template,jsonify,session
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

app = Flask(
    __name__,
    static_folder='static',
    static_url_path='/'
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index', methods=['POST'])
def index():
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    message_text = request.form['message']
    image = request.files['image'] # 使用 request.files 取得上傳的文件
     # 設置郵件內容
    message = MIMEMultipart()
    message['Subject'] = '玻璃訂製規格評估報價__'+ name
    #message['From'] = 'rueishian.chen@gmail.com'
    message['From'] = email
    message['To'] = 'rueishian.chen@gmail.com'

    # 添加文字內容
    text = MIMEText(f"Name: {name}\nPhone: {phone}\nEmail: {email}\nmessage:{message_text}")
    message.attach(text)

    # 添加圖片內容
    img = MIMEImage(image.read(), name=image.filename)
    message.attach(img)

    # 連線至SMTP伺服器並發送郵件
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
       try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()
            smtp.login('rueishian.chen@gmail.com', 'nmxmbawswwkfhwkk') # 登入寄件者gmail
            smtp.sendmail('rueishian.chen@gmail.com', 'rueishian.chen@gmail.com', message.as_string())
            myResult="規格上傳成功,我們將儘快與您聯繫,謝謝~"
            print(myResult)
            return render_template('index.html', myResult = myResult)
       except Exception as e:
            print("Error message: ", e)
            myResult="規格上傳失敗,麻煩重新操作一次,謝謝~"
            return render_template('index.html', myResult = myResult)
        