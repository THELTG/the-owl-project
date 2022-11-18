# flask web server
from flask import Flask, render_template, Response, send_from_directory

# computer vision 
import cv2

# # raspberry pi GPIO pins
# import RPi.GPIO as GPIO

# telegram bot handling
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

# file system manipulation
import os 
import shutil

# utilities
import threading
from datetime import datetime
from time import sleep

# create global objects
app = Flask(__name__)
camera = cv2.VideoCapture(0)

# IF it shows a Failed to select stream 0 err
# please ensure that only one camera is connected
# and that the cable is secure

# initialise start time
start_time = datetime.now()

# initialise GPIO pins
buzzer = 17
green_led = 27
red_led = 22

# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# GPIO.setup(red_led,GPIO.OUT, initial=GPIO.LOW)
# GPIO.setup(green_led,GPIO.OUT, initial=GPIO.HIGH) # always turned on when script starts
# GPIO.setup(buzzer,GPIO.OUT, initial=GPIO.LOW)

# buzzer_pwm = GPIO.PWM(buzzer, 440) 


# def buzzer_sound():
#     buzzer_pwm.start(50)
#     for i in range(3):
#         buzzer_pwm.ChangeFrequency(2000)
#         sleep(0.5)
#         buzzer_pwm.ChangeFrequency(3560)
#         sleep(0.5)
#     buzzer_pwm.stop()

# def motion_detected():
#     GPIO.output(red_led,GPIO.HIGH)
#     buzzer_sound()
#     GPIO.output(red_led,GPIO.LOW)

# live stream footage
def generate_frames():
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT,1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
    while True:
        sleep(0.1)
        success, frame = camera.read()
        if not success:
            print("capture error")
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')   

# opencv motion detection function
def motion_detection():
    redundant , firstImg = camera.read() 
    previousProcessed = cv2.GaussianBlur(cv2.cvtColor(firstImg,cv2.COLOR_BGR2GRAY),(21, 21), 0)
    ctr = len(os.listdir("./images/")) % 300 # can never go more than 300 images
    cooldown = 100
    while True:
        sleep(0.1)
        success, frame = camera.read()  
        if not success:
            break
        else:
            processedImg = cv2.GaussianBlur(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY),(21, 21), 0)
            delta = cv2.absdiff(previousProcessed,processedImg)
            ret, thresh = cv2.threshold(delta,30,255,cv2.THRESH_BINARY)
            cnt, hier = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            for contours in cnt:
                if cv2.contourArea(contours) < 1000:
                    continue 
                (x,y,w,h) = cv2.boundingRect(contours)
                cv2.rectangle(img=frame, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 0), thickness=2)
                cv2.putText(frame,datetime.now().strftime("%d/%m/%y %H:%M:%S"),(00, 35),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                if ctr >= 300:
                    ctr = 0
                if cooldown == 100:
                    cv2.imwrite(f'./images/{ctr}.png',frame)
                    # motion_detected()
                    ctr += 1
                    cooldown = 0
                else:
                    cooldown += 1
            previousProcessed = processedImg

# web server routing and hosting
@app.route('/',methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/assets/<path:path>")
def assets(path):
    return send_from_directory("assets",path)

    # monkey error handling
@app.errorhandler(404)
def errors(error):
    return render_template("/error.html",error=error)

# api token here
updater = Updater("TOKEN REDACTED FOR PRIVACY PLEASE TAKE NOTE",use_context=True)

# define functions here
def start(update: Update, context: CallbackContext):
    update.message.reply_text('''
Hello! Welcome to project owl!
Here are the commands:

/start - Display this message
/latest - Show the last picture taken
/extractall - Send all images in an archive
/beep - Beep the alarm
/uptime - Shows the amount of time project owl has been running

This project was made by Koh Kai En
Python Programming for IoT Singapore Poly
''')

def latest(update: Update, context: CallbackContext):
    try:        
        image = [int(i.split(".")[0]) for i in os.listdir("./images/")]
        path = f"./images/{max(image)}.png"
        update.message.reply_photo(photo=open(path,'rb'))
    except:
        update.message.reply_text("There are no images!")

def extract(update: Update, context: CallbackContext):
    try:
        shutil.make_archive("Archive",'zip','./images')
        update.message.reply_document(document=open("Archive.zip",'rb'))
    except:
        update.message.reply_text("Extraction Failed!")

def beep(update: Update, context: CallbackContext):
    try:
        # buzzer_sound()
        update.message.reply_text("Alarm beeped")
    except:
        update.message.reply_text("Alarm failed!")

def uptime(update: Update, context: CallbackContext):
    try:
        update.message.reply_text(f"{str(datetime.now() - start_time).split('.')[0]}")
    except:
        update.message.reply_text("Failed to calculate uptime")

def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(f"Sorry '{update.message.text}' is not a valid command")

def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(f"Sorry I can't recognize you , you said '{update.message.text}'")

# define dispatchers and handlers here
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('latest', latest))
updater.dispatcher.add_handler(CommandHandler('extractall', extract))
updater.dispatcher.add_handler(CommandHandler('beep', beep))
updater.dispatcher.add_handler(CommandHandler('uptime', uptime))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

if __name__ == "__main__":

    # define threading objs
    bot = threading.Thread(target=updater.start_polling)
    webserver = threading.Thread(target=app.run,args=("0.0.0.0",8081,))
    motiondetection = threading.Thread(target=motion_detection)

    # start all services
    bot.start()
    webserver.start()
    motiondetection.start()

    print('all services has started')


