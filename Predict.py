
'''
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

        import torch
        import numpy as np
        # Load the model
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp2/weights/best.pt',
                               force_reload=True)
        # model.conf = 0.2
        # Set webcam input
        cam = cv2.VideoCapture("static/upload/" + savename)
        dd1 = 0
        dd2 = 0
        dd3 = 0
        dd4 = 0
        ret, img = cam.read()
        dd2 += 1

        # Perform object detection

        # print(results)

        try:
            results = model(img)
            # Access the detection results
            class_names = ['flood', 'level 0', 'level 1', 'level 10', 'level 11', 'level 2', 'level 3', 'level 4',
                           'level 5', 'level 6', 'level 7', 'level 8',
                           'level 9']  # List of class names in the order corresponding to the model's output

            # Assuming results contains bounding box coordinates and class indices
            bounding_boxes = results.xyxy[0]  # Assuming the first image in results
            class_indices = bounding_boxes[:, -1].int().tolist()  # Extracting class indices
            # Mapping class indices to class names
            prediction_names = [class_names[idx] for idx in class_indices]
            # Printing prediction names
            print(prediction_names[0])

            if prediction_names[0] == "level 0":
                session["out"] = "Normal"
            else:
                session["out"] = prediction_names[0]



        except:
            pass

        if session['out'] == "Normal":

            flash("Normal")
            cv2.imshow("Output", np.squeeze(results.render()))
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return render_template('NewComplaint.html', uname=session['uname'])
        else:
            cv2.imshow("Output", np.squeeze(results.render()))
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb')
            cursor = conn.cursor()
            cursor.execute("SELECT  *  FROM regtb where  username='" + uname + "'")
            data = cursor.fetchone()

            if data:
                mobile = data[2]

            else:
                return 'Incorrect username / password !'

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb')
            cursor = conn.cursor()
            cursor.execute(
                "insert into complainttb values('','" + uname + "','" + mobile + "','" + depart + "','" + info + "','" + savename + "','','waiting','','','" +
                session["out"] + "')")
            conn.commit()
            conn.close()

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM complainttb where username='" + uname + "'  ")
            data = cur.fetchall()
            flash('Complaint Post Successfully!')
            return render_template('UComplaintInfo.html', data=data)



        # Press 'q' or 'Esc' to quit
        #if (cv2.waitKey(1) & 0xFF == ord("q")) or (cv2.waitKey(1) == 27):
            #break

        # Close the camera
'''



