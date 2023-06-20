from flask import Flask, request, render_template #, request
import pylsl

host = "localhost"
port = 5002

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    print("test")
    return render_template("dashboard.html")

@app.route("/recorder")
def recorder():
    return render_template("recorder.html")

lsl_data = [0] * 12

@app.route('/log', methods=['POST'])
def log():
    
    data = request.get_json('body')
    
    sensorName = data['name']
    sensorValue = data['value']
    
    print(sensorName, sensorValue)
    if sensorName == 'ACC':
        acc_outlet.push_sample(parse_string(sensorValue))
    elif sensorName == 'GYRO':
        gyro_outlet.push_sample(parse_string(sensorValue))
    elif sensorName == 'MAG':
        mag_outlet.push_sample(parse_string(sensorValue))
    elif sensorName == 'PRESSURE':
        press_outlet.push_sample(parse_string(sensorValue))
    elif sensorName == 'TEMP':
       press_outlet.push_sample(parse_string(sensorValue))
    
    #print(empatyarray)
    return ''

# Create a new stream for each of the sensors
acc_stream_info = pylsl.StreamInfo('OpenEarable-ACC', 'EEG', 4, 100, pylsl.cf_double64, 'openErableID')
gyro_stream_info = pylsl.StreamInfo('OpenEarable-GYRO', 'EEG', 4, 100, pylsl.cf_double64, 'openErableID')
mag_stream_info = pylsl.StreamInfo('OpenEarable-MAG', 'EEG', 4, 100, pylsl.cf_double64, 'openErableID')
press_stream_info = pylsl.StreamInfo('OpenEarable-PRESSURE', 'EEG', 2, 100, pylsl.cf_double64, 'openErableID')
temp_stream_info = pylsl.StreamInfo('OpenEarable-TEMP', 'EEG', 2, 100, pylsl.cf_double64, 'openErableID')

# now label the stream's channels
acc_channels = ['AccX', 'AccY', 'AccZ', 'Timestamp']
gyro_channels = ['GyroX', 'GyroY', 'GyroZ', 'Timestamp']
mag_channels = ['MagX', 'MagY', 'MagZ', 'Timestamp']
press_channels = ['Pressure', 'Timestamp']
temp_channels = ['Temperature', 'Timestamp']

# Add labels as the stream's info
for c in acc_channels:
    acc_stream_info.desc().append_child_value("channels", c)
for c in gyro_channels:
    gyro_stream_info.desc().append_child_value("channels", c)
for c in mag_channels:
    mag_stream_info.desc().append_child_value("channels", c)
for c in press_channels:
    press_stream_info.desc().append_child_value("channels", c)
for c in temp_channels:
    temp_stream_info.desc().append_child_value("channels", c)

# create an outlet for each stream_info
acc_outlet = pylsl.StreamOutlet(acc_stream_info)
gyro_outlet = pylsl.StreamOutlet(gyro_stream_info)
mag_outlet = pylsl.StreamOutlet(mag_stream_info)
press_outlet = pylsl.StreamOutlet(press_stream_info)
temp_outlet = pylsl.StreamOutlet(temp_stream_info)

# Create a function for parsing the string and returning an array 
# (e.g. "x: 10, y: 20, z: 30, timestamp: 6" -> [10, 20, 30, 6]}
def parse_string(string):
    values = string.split(', ')
    array = []
    for value in values:
        parts = value.split(': ')
        if len(parts) == 2:
            try:
                array.append(float(parts[1]))
            except ValueError:
                pass
    return array

if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)
