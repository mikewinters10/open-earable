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

@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    print(data)
    return ''

# create a new stream
stream_info = pylsl.StreamInfo('OpenEarable-LSL', 'EEG', 11, 100, pylsl.cf_double64, 'openErableID')

# now create the stream's channels
channels = ['AccX', 'AccY', 'AccZ', 'GyroX', 'GyroY', 'GyroZ', 'MagX', 'MagY', 'MagZ', 'Temperature', 'Pressure']

# Add channels as the stream's channels
for c in channels:
    stream_info.desc().append_child_value("channels", c)

# next make an outlet
outlet = pylsl.StreamOutlet(stream_info)

if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)
