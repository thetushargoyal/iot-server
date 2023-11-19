#111!/usr/bin/env python
# -*- coding: utf-8 -*

#sudo apt-get install python3-flask
#pip3 install opencv-python

from flask import Flask, Response, jsonify
import cv2
from sense_hat import SenseHat

# sense = SenseHat() 
# sense.clear()
# while True:
#     sense.show_message('IOT LAB')

app = Flask(__name__)

def gen():
    """Video streaming generator function."""
    vs = cv2.VideoCapture(0)
    frame_skip = 1  # Send every 5th frame
    count = 0
    while True:
        _, frame = vs.read()

        if count % frame_skip == 0:
            # Resize the frame to a specific size if needed
            resized_frame = cv2.resize(frame, (640, 480))

            # Apply JPEG compression with a quality parameter (adjust as needed)
            _, jpeg = cv2.imencode('.jpg', resized_frame, (cv2.IMWRITE_JPEG_QUALITY, 50))

            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            

        count += 1

    vs.release()
    cv2.destroyAllWindows()

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_data')
def get_data():
    sense = SenseHat()
    sense.clear()
    humidity = sense.get_humidity()
    temperature = sense.get_temperature()
    pressure = sense.get_pressure()
    response = jsonify({"humidity": humidity,
                        "temperature": temperature,
                        "pressure": pressure})
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port =5001, debug=True, threaded=True)