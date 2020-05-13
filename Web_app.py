from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from time import time
from RGB_controller import RGB
from threading import Thread
import sys

app = Flask(__name__)

rgb_leds = []

@app.route('/')
def goHome():
    return render_template('go_home.html')

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/rgb-lights")
def rgbController():
    try:
        return render_template('rgblights.html', leds=rgb_leds)
    except:
        return render_template('rgblights.html', leds=rgb_leds)
        
    """
    try:
        with open("config/RGBs.txt", 'r') as rgbs:
            leds = rgbs.readlines()
        return render_template('rgblights.html', leds=leds)
    except:
        rgb_file = open("config/RGBs.txt", 'w')
        rgb_file.close()
        return render_template('rgblights.html', leds=leds)
    """

@app.route("/rgb-lights/add", methods=['POST','GET'])
def rgbAdd():
    if request.method == 'POST':
        try:
            rpin = int(request.form['redpin'])
            gpin = int(request.form['greenpin'])
            bpin = int(request.form['bluepin'])
            rgb_led = RGB(rpin, gpin, bpin) 
            thread = Thread(name='startLed',target=rgb_led.startLed)
            thread.start()
            rgb_leds.append(rgb_led)
            return redirect("/rgb-lights")
        except:
            return ("<p>ERROR: The pin numbers you tried to submit are not valid.</p><a href='/rgb-lights'>Press here to go to the previous page.</a>")
    else:
        return redirect("/rgb-lights")        

@app.route("/rgb-lights/turn/<int:id>", methods=['GET'])
def turnOnOff(id):
    if request.method == 'GET':
        for led in rgb_leds:
            if led.getId == id:
                led.changeState()
        return redirect('/rgb-lights')
    else:
        return redirect('/rgb-lights')

@app.route("/rgb-lights/modify/<int:id>", methods=['GET','POST'])
def modifyLed(id):
    if request.method == 'GET':
        for led_index in range(len(rgb_leds)):
            if rgb_leds[led_index].getId == id:
                return render_template('modify_rgb.html', led_number=led_index+1, led=rgb_leds[led_index])
    else:
        return render_template('modify_rgb.html')

@app.route("/rgb-lights/modify/delete/<int:id>", methods=['GET'])
def deleteLed(id):
    if request.method == 'GET':
        for led_index in range(len(rgb_leds)):
            if rgb_leds[led_index].getId == id:
                rgb_leds[led_index].deleteRGB()
                rgb_leds.pop(led_index)
                threads.pop(led_index)
                return redirect('/rgb-lights')
    else:
        return redirect('/rgb-lights')

@app.route("/rgb-lights/modify/update/<int:id>", methods=['POST'])
def updateLed(id):
    if request.method == 'POST':
        #try:
        for led in rgb_leds:
            if led.getId == id:
                mode = request.form['mode']
                timing = float(request.form['light_duration'])
                rval = float(request.form['redval'])*100/255
                gval = float(request.form['greenval'])*100/255
                bval = float(request.form['blueval'])*100/255
                if timing > 0:
                    if 0<=rval<=255 and 0<=gval<=255 and 0<=bval<=255:
                        if mode == 'rainbow':
                            rval = 100
                            gval = 0
                            bval = 0
                        led.setColour(rval,gval,bval)
                        led.setDelay(timing)
                        led.setMode(mode)
                        return redirect('/rgb-lights')
                    else:
                        return  "<p>ERROR: The value for RGB were out of the range allowed.</p><a href='/rgb-lights'>Press here to go to the previous page.</a>"
                else:
                    return "<p>ERROR: Value for time you submited was under 0.</p><a href='/rgb-lights'>Press here to go to the previous page.</a>"
                return redirect('/rgb-lights')
        #except:
        #    error = sys.exc_info()
        #    return "<p>ERROR: {}.</p><a href='/rgb-lights'>Press here to go to the previous page.</a>".format(error)
    else:
        return redirect('/rgb-lights')

if __name__ == '__main__':
    app.run(debug=True)