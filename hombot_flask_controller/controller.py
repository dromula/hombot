from flask import Flask, render_template, request, jsonify
#from hombot_motor_control.test import set_left

app = Flask(__name__)
#app.run(host= '192.168.178.57')


@app.route('/')
def index():
    return render_template('index.html')

#rendering the HTML page which has the button
@app.route('/json')
def json():
    return render_template('json.html')

#background process happening without any refreshing
@app.route('/motor_left', methods=['POST'])
def background_process_test():
    data = request.json
    power = int(data["power"])
    print("Power: "+ str(power))
    
    return jsonify(data)