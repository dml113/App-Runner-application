from flask import Flask, request
import time
import socket
from datetime import datetime, timedelta

app = Flask(__name__)

try:
    import requests
except ImportError:
    requests = None  

try:
    import psutil
except ImportError:
    psutil = None

try:
    import humanize
except ImportError:
    humanize = None

unicorn = r"""
                                                    /
                                                  .7
                                       \       , //
                                       |\.--._/|//
                                      /\ ) ) ).'/
                                     /(  \  // /
                                    /(   J`((_/ \
                                   / ) | _\     /
                                  /|)  \  eJ    L
                                 |  \ L \   L   L
                                /  \  J  `. J   L
                                |  )   L   \/   \
                               /  \    J   (\   /
             _....___         |  \      \   \```
      ,.._.-'        '''--...-||\     -. \   \
    .'.=.'                    `         `.\ [ Y
   /   /                                  \]  J
  Y / Y                                    Y   L
  | | |          \                         |   L
  | | |           Y                        A  J
  |   I           |                       /I\ /
  |    \          I             \        ( |]/|
  J     \         /._           /        -tI/ |
   L     )       /   /'-------'J           `'-:.
   J   .'      ,'  ,' ,     \   `'-.__          \
    \ T      ,'  ,'   )\    /|        ';'---7   /
     \|    ,'L  Y...-' / _.' /         \   /   /
      J   Y  |  J    .'-'   /         ,--.(   /
       L  |  J   L -'     .'         /  |    /\
       |  J.  L  J     .-;.-/       |    \ .' /
       J   L`-J   L____,.-'`        |  _.-'   |
        L  J   L  J                  ``  J    |
        J   L  |   L                     J    |
         L  J  L    \                    L    \
         |   L  ) _.'\                    ) _.'\
         L    \('`    \                  ('`    \
          ) _.'\`-....'                   `-....'
         ('`    \
          `-.___/   
"""

@app.route('/healthcheck')
def health():
    return '{"status": "200 OK"}', 200

@app.route('/v1/unicorn')
def cloud():
    return f"<pre>{unicorn}</pre>"

@app.route('/request')
def request_info():
    want = request.args.get('security', '')

    if want == 'time':
        current_time = datetime.now()
        current_time -= timedelta(hours=3)
        current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        return f"Current time is: {current_time_str}"

    elif want == 'myip':
        ip_address = socket.gethostbyname(socket.gethostname())
        return f"My IP address is: {ip_address}"

    elif want == 'cpu':
        if psutil:
            cpu_usage = psutil.cpu_percent(interval=1)
            return f"CPU usage is: {cpu_usage}%"
        else:
            return "what's the reason ?"

    elif want == 'memory':
        if psutil and humanize:
            memory = psutil.virtual_memory()
            memory_used = humanize.naturalsize(memory.used)
            memory_total = humanize.naturalsize(memory.total)
            return f"Memory usage: {memory_used} / {memory_total}"
        else:
            return "what's the reason ?"

    elif want == 'externalip':
        if requests:
            response = requests.get('https://api.ipify.org?format=json')
            external_ip = response.json().get('ip')
            return f"My external IP address is: {external_ip}"
        else:
            return "what's the reason ?"

    else:
        return "Invalid request. Please provide 'want=time', 'want=myip', 'want=cpu', 'want=memory', or 'want=externalip' in the query string."

if __name__ == '__main__':
    app.run(host='0.0.0.0')
