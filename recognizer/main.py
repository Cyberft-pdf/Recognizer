import tensorflow as tf
import cv2
import numpy as np
import datetime

model_gender = tf.keras.models.load_model("model2.h5")  
model_age =tf.keras.models.load_model("model3.h5")


cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


while True:
    ret, frame = cap.read()  

    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        face = frame[y:y+h, x:x+w]
        face = cv2.resize(face, (200, 200))
        face = face / 255.0
        face = np.expand_dims(face, axis=0)



        predictions_gender = model_gender.predict(face)
        predictions_age = model_age.predict(face)

        gender_label = np.argmax(predictions_gender, axis=0 )[0]


        #díky tomuto to funguje 
        female_probability = predictions_gender[0][0]
        old_probability = predictions_age[0][0]

        if female_probability > 0.5:
            gender = "Female"
            with open("poznamky.txt", "a") as file:
                file.write(f"It was a female({str(female_probability)}) and ")

        else:
            gender = "Male"
            with open("poznamky.txt", "a") as file:
                file.write(f"It was a male and ")            

        if old_probability > 0.5:
            age = "Young"
            current_datetime = datetime.datetime.now()
            with open("poznamky.txt", "a") as file:
                file.write(f"its young | date:{current_datetime}\n")            
        else:
            age = "Old"
            current_datetime = datetime.datetime.now()
            with open("poznamky.txt", "a") as file:
                file.write(f"its old | date:{current_datetime}\n")                




        cv2.putText(frame, f'Gender: {gender}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.putText(frame, f"Age: {age}", (x, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow('Live Detekce a Rozpoznávání Pohlaví', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

