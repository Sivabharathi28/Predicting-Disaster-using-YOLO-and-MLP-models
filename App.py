from flask import Flask, render_template, request, session, flash

import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aaa'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/AdminLogin')
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route('/OfficerLogin')
def OfficerLogin():
    return render_template('OfficerLogin.html')


@app.route('/UserLogin')
def UserLogin():
    return render_template('UserLogin.html')


@app.route('/NewUser')
def NewUser():
    return render_template('NewUser.html')


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb',  charset='utf8')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb ")
            data = cur.fetchall()
            flash("you are successfully Login")
            return render_template('AdminHome.html', data=data)

        else:
            flash("UserName or Password Incorrect!")
            return render_template('AdminLogin.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb',charset='utf8')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb  ")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/NewOfficer")
def NewOfficer():
    return render_template('NewOfficer.html')


@app.route("/newofficer", methods=['GET', 'POST'])
def newofficer():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        depart = "National Disaster Management Authority"
        username = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb',charset='utf8')
        cursor = conn.cursor()
        cursor.execute(
            "insert into officertb values('','" + name + "','" + mobile + "','" + email + "','" + address + "','" + depart + "','" + username + "','" + password + "')")
        conn.commit()
        conn.close()
        flash("Record Saved!")

    return render_template('NewOfficer.html')


@app.route("/AOfficerInfo")
def AOfficerInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb',charset='utf8')
    cur = conn.cursor()
    cur.execute("SELECT * FROM officertb ")
    data = cur.fetchall()
    return render_template('AOfficerInfo.html', data=data)


@app.route("/AComplaintInfo")
def AComplaintInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb',charset='utf8')
    cur = conn.cursor()
    cur.execute("SELECT * FROM complainttb  ")
    data = cur.fetchall()
    return render_template('AComplaintInfo.html', data=data)


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        username = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb',charset='utf8')
        cursor = conn.cursor()
        cursor.execute(
            "insert into regtb values('','" + name + "','" + mobile + "','" + email + "','" + address + "','" + username + "','" + password + "')")
        conn.commit()
        conn.close()
        flash("Record Saved!")

    return render_template('UserLogin.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb',charset='utf8')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and password='" + password + "'")
        data = cursor.fetchone()
        if data is None:
            flash('Username or Password is wrong')
            return render_template('UserLogin.html', data=data)

        else:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb',charset='utf8')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + username + "' and password='" + password + "'")
            data = cur.fetchall()
            flash("you are successfully logged in")
            return render_template('UserHome.html', data=data)


@app.route("/NewComplaint")
def NewComplaint():
    return render_template('NewComplaint.html', uname=session['uname'])

@app.route("/newcomplaint", methods=['GET', 'POST'])
def newcomplaint():
    if request.method == 'POST':
        import cv2
        uname = session['uname']
        depart = "National Disaster Management Authority"
        info = request.form['info']

        import random
        file = request.files['file']
        fnew = random.randint(1111, 9999)
        savename = str(fnew) + ".png"
        file.save("static/upload/" + savename)
        org = "static/upload/" + savename

        from ultralytics import YOLO
        import cv2

        # image = cv2.imread(import_file_path)
        image = cv2.imread(org)
        model = YOLO('runs/detect/flood/weights/best.pt')

        class_labels = ['flood', 'level 0', 'level 1', 'level 10', 'level 11', 'level 2', 'level 3', 'level 4', 'level 5', 'level 6', 'level 7', 'level 8', 'level 9']

        # Perform object detection
        results = model(image, conf=0.6)

        confidences = results[0].boxes.conf  # Confidence scores
        class_indices = results[0].boxes.cls  # Class indices

        if len(confidences) > 0:
            max_confidence_index = confidences.argmax().item()  # Get index of highest confidence
            predicted_class_index = int(class_indices[max_confidence_index].item())  # Get correct class index

            # Ensure index is within bounds
            if 0 <= predicted_class_index < len(class_labels):
                predicted_class = class_labels[predicted_class_index]  # Map index to label
            else:
                predicted_class = "Unknown Class"

            confidence_score = confidences[max_confidence_index].item()  # Get highest confidence score

            print(f"Predicted Class: {predicted_class}")
            print(f"Confidence Score: {confidence_score:.4f}")  # Display with 4 decimal places
        else:
            predicted_class = "No Detections"
            confidence_score = 0.0
            print("No objects detected.")

        annotated_frame = results[0].plot()
        outi = "static/Out/out.jpg"
        cv2.imwrite("static/Out/out.jpg", annotated_frame)

        if predicted_class == "level 0":

            flash("Normal")
            cv2.imshow("Output", annotated_frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return render_template('NewComplaint.html', uname=session['uname'])
        else:
            cv2.imshow("Output", annotated_frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb',charset='utf8')
            cursor = conn.cursor()
            cursor.execute("SELECT  *  FROM regtb where  username='" + uname + "'")
            data = cursor.fetchone()

            if data:
                mobile = data[2]

            else:
                return 'Incorrect username / password !'

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb',charset='utf8')
            cursor = conn.cursor()
            cursor.execute(
                "insert into complainttb values('','" + uname + "','" + mobile + "','" + depart + "','" + info + "','" + savename + "','','waiting','','','" +
                predicted_class + "')")
            conn.commit()
            conn.close()

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb',charset='utf8')
            cur = conn.cursor()
            cur.execute("SELECT * FROM complainttb where username='" + uname + "'  ")
            data = cur.fetchall()
            flash('Complaint Post Successfully!')
            return render_template('UComplaintInfo.html', data=data)






@app.route("/UComplaintInfo")
def UComplaintInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb',charset='utf8')
    cur = conn.cursor()
    cur.execute("SELECT * FROM complainttb where username='" + session['uname'] + "' and Status='waiting' ")
    data = cur.fetchall()
    return render_template('UComplaintInfo.html', data=data)


@app.route("/UActionInfo")
def UActionInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb',charset='utf8')
    cur = conn.cursor()
    cur.execute("SELECT * FROM complainttb where username='" + session['uname'] + "' and Status !='waiting' ")
    data = cur.fetchall()
    return render_template('UActionInfo.html', data=data)


@app.route("/officerlogin", methods=['GET', 'POST'])
def officerlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['oname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb',charset='utf8')
        cursor = conn.cursor()
        cursor.execute("SELECT * from officertb where username='" + username + "' and password='" + password + "'")
        data = cursor.fetchone()
        if data is None:
            flash('Username or Password is wrong')
            return render_template('OfficerLogin.html', data=data)

        else:
            session['depart'] = data[5]
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb',charset='utf8')
            cur = conn.cursor()
            cur.execute("SELECT * FROM officertb where username='" + username + "' and password='" + password + "'")
            data = cur.fetchall()
            flash("you are successfully logged in")
            return render_template('OfficerHome.html', data=data)


@app.route("/OfficerHome")
def OfficerHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb',charset='utf8')
    cur = conn.cursor()
    cur.execute("SELECT * FROM officertb where username='" + session['oname'] + "' ")
    data = cur.fetchall()
    return render_template('OActionInfo.html', data=data)


@app.route("/OActionInfo")
def OActionInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb',charset='utf8')
    cur = conn.cursor()
    cur.execute("SELECT * FROM complainttb where Department='" + session['depart'] + "' and Status ='completed' ")
    data = cur.fetchall()
    return render_template('OActionInfo.html', data=data)


@app.route("/OComplaintInfo")
def OComplaintInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb',charset='utf8')
    cur = conn.cursor()
    cur.execute("SELECT * FROM complainttb where Department='" + session['depart'] + "' and Status !='completed' ")
    data = cur.fetchall()
    return render_template('OComplaintInfo.html', data=data)


@app.route("/action")
def action():
    id = request.args.get('id')
    session["cid"] = id

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb',charset='utf8')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM complainttb where  id='" + id + "'")
    data = cursor.fetchone()

    if data:
        mobile = data[2]

    else:
        return 'Incorrect username / password !'

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb',charset='utf8')
    cur = conn.cursor()
    cur.execute("SELECT * FROM complainttb where id='" + id + "' ")
    data = cur.fetchall()
    return render_template('Action.html', data=data)


@app.route("/actioninfo", methods=['GET', 'POST'])
def actioninfo():
    if request.method == 'POST':
        act = request.form['act']
        ainfo = request.form['ainfo']
        oname = session['oname']

        import random
        file = request.files['file']
        fnew = random.randint(1111, 9999)
        savename = str(fnew) + ".png"
        file.save("static/upload/" + savename)

        id = session["cid"]

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb',charset='utf8')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM complainttb where  id='" + id + "'")
        data = cursor.fetchone()

        if data:
            mobile = data[2]
        else:
            return 'Incorrect username / password !'
        msg = "Your Complaint Action Info" + ainfo
        sendmsg(mobile, msg)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb',charset='utf8')
        cursor = conn.cursor()
        cursor.execute(
            "update   complainttb set Action='" + ainfo + "',Status='" + act + "' , OfficerName='" + oname + "',Cimage='"+savename+"' where id='" + id + "'")
        conn.commit()
        conn.close()

        flash("Action Info Update successfully")

        return render_template('OActionInfo.html')



def sendmsg(targetno,message):
    import requests
    requests.post(
        "http://sms.creativepoint.in/api/push.json?apikey=6555c521622c1&route=transsms&sender=FSSMSS&mobileno=" + targetno + "&text=Dear customer your msg is " + message + "  Sent By FSMSG FSSMSS")


@app.route("/EarthQuakePrediction")
def EarthQuakePrediction():
    return render_template('EarthQuakePrediction.html', uname=session['uname'])

import pickle
import numpy as np
@app.route("/imupload", methods=['GET', 'POST'])
def imupload():
    if request.method == 'POST':
        t1 = request.form['t1']
        t2 = request.form['t2']
        t3 = request.form['t3']
        t4 = request.form['t4']


        t1 = float(t1)
        t2 = float(t2)
        t3 = float(t3)
        t4 = float(t4)


        filename = 'runs/detect/flood/weights/earthquakeprediction.pkl'
        classifier = pickle.load(open(filename, 'rb'))

        data = np.array(
            [[t1, t2, t3, t4]])
        my_prediction = classifier.predict(data)
        print(my_prediction[0])
        Answer = ''

        if my_prediction == 'Earthquake':
            Answer = 'Earthquake'
        elif  my_prediction == 'Explosion':
            Answer = 'Explosion'

        elif my_prediction == 'Nuclear Explosion':
            Answer = 'Nuclear Explosion'

        #sendmsg(session['mob'],"Prediction Result : "+my_prediction[0])
        return render_template('EarthQuakePrediction.html', res=my_prediction[0],t1=t1,t2=t2,t3=t3,t4=t4)


@app.route("/Predict")
def Predict():
    import cv2
    from ultralytics import YOLO
    model = YOLO('runs/detect/flood/weights/best.pt')
    cap = cv2.VideoCapture(0)
    dd1 = 0

    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:
            # Run YOLOv8 inference on the frame
            results = model(frame, conf=0.7)
            for result in results:
                if result.boxes:
                    box = result.boxes[0]
                    class_id = int(box.cls)
                    object_name = model.names[class_id]
                    print(object_name)

                    if object_name != 'level 0':
                        dd1 += 1
                        print(dd1)

                    if dd1 == 100:
                        dd1 = 0
                        import winsound

                        filename = 'alert.wav'
                        winsound.PlaySound(filename, winsound.SND_FILENAME)

                        annotated_frame = results[0].plot()

                        cv2.imwrite("alert.jpg", annotated_frame)



                        sendmail('akshayabharathi2804@gmail.com')
                        sendmsg("8098106766", "Prediction Name:" + object_name)

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Display the annotated frame
            cv2.imshow("YOLOv11 Inference", annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()
def sendmail(mail):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "projectmailm@gmail.com"
    toaddr = mail

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Alert"

    # string to store the body of the mail
    body = " Solar Panel Fault Detection"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "alert.jpg"
    attachment = open("alert.jpg", "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "tdyr kebi hnyr yzyh")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
