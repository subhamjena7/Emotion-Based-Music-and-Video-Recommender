import time
import secret
import requests

import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array

from flask import Flask,render_template,request,Response, url_for, redirect
from spotify import Spotify

app = Flask(__name__)
spotify = Spotify()
camera = cv2.VideoCapture(0)

face_classifier = cv2.CascadeClassifier('frontalface.xml')
classifier = load_model('fer.h5')

emotion_labels = ['Angry', 'Fear', 'Happy', 'Neutral', 'Sad']


def generate_frames():
    camera = cv2.VideoCapture(0) 
    while True:
        success, _ = camera.read()
        if not success:
            break
        else:
            capture_duration = 5
            start_time = time.time()
            while(int(time.time() - start_time) < capture_duration):
                _, frame = camera.read()
                frame = cv2.flip(frame,1)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

                for (x,y,w,h) in faces:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
                    roi_gray = gray[y:y+h,x:x+w]
                    roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)

                    if np.sum([roi_gray]) != 0:
                        roi = roi_gray.astype('float')/255.0
                        roi = img_to_array(roi)
                        roi = np.expand_dims(roi,axis=0)
                        prediction = classifier.predict(roi)[0]
                        global label
                        label = emotion_labels[prediction.argmax()]
                        label_position = (x,y)
                        cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                        print(label)
                        
                _, buffer = cv2.imencode('.jpg',frame)
                frame = buffer.tobytes()
                cv2.waitKey(0)
                yield(b'--frame\r\n'
                      b'Content-Type: image/jpeg\r\n\r\n'+ frame + 
                      b'\r\n\r\n')


@app.route('/')
def home():
    if not spotify.is_authenticated():
        return redirect(spotify.get_oauth2_url())
    
    if spotify.is_token_expired():
        auth_code: None = request.args.get("code")
        if auth_code:
            spotify.get_or_refresh_access_token("GET", auth_code)
        else:
            spotify.get_or_refresh_access_token("refresh")
            
    return render_template('main.html')


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype = 'multipart/x-mixed-replace; boundary=frame')


######### Code for displaying Videos or Music #########
@app.route('/result',methods = ["POST", "GET"])
def playlistmanager():
        option = request.form['btnradio']
        print("option is "+ option)
        
        try:
            label
        except NameError:
            return Response("Emotion was not detected properly")
        else:
            # _input = []
            _input = label
            print(_input)
            
            ###playlist selection###
            if _input == 'Happy':
                if option == "video":
                    playlist_id = secret.happy
                else:
                    playlist_id = secret.mhappy

            elif _input == 'Sad':
                if option == "video":
                    playlist_id = secret.sad
                else:
                    playlist_id = secret.msad
                    
            elif _input == 'Neutral':
                if option == "video":
                    playlist_id = secret.neutral
                else:
                    playlist_id = secret.mneutral
                    
            elif _input == 'Angry':
                if option == "video":
                    playlist_id = secret.angry
                else:
                    playlist_id = secret.mangry

                    
            elif _input == 'Fear':
                if option == "video":
                    playlist_id = secret.fear
                else:            
                    playlist_id = secret.mfear
                    
            else:
                return Response("Enter valid keyword")
            

        if option == "video":
            ######### Youtube Code ###########                        
            search_url = 'https://www.googleapis.com/youtube/v3/playlistItems'
            search_params = {
                'key': secret.youtube_key,
                'playlistId': playlist_id,
                'part': 'contentDetails',
                'maxResults': 10,
            }
                                        
            r = requests.get(search_url, params=search_params)
            results = r.json()['items']
            video_ids = []
            for result in results:
                video_ids.append(result['contentDetails']['videoId'])
            return render_template('results.html', input=_input, video_ids=video_ids)
        else:
            ########## Spotify Code ##########
            music_ids = spotify.get_playlist(playlist_id)
            return render_template('music.html', input=_input, music_ids=music_ids)
            
                                                                                 
if __name__ == '__main__':
    app.run(debug=True)