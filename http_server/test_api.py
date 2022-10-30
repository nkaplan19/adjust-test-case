from flask import Flask
import socket
import time

app = Flask(__name__)

# Root function which return timestamp and hostname info
@app.route('/', methods=['GET'])
def infoAPI():
    host_name = socket.gethostname()
    time_stamp = time.time()
    return {"timestamp": time_stamp, "hostname": host_name} 

# Function created for healhcheck which return status
@app.route('/api/healtcheck', methods=['GET'])
def healthAPI():    
    return {"status": "OK"} 

# Main function 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)