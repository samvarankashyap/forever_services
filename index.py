from flask import Flask
from flask import render_template
from flask import Flask, request, send_from_directory
app = Flask(__name__,static_url_path='/static')
from subprocess import Popen, PIPE

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/')
def index():
    return 'Index Page'

@app.route('/list_forever_services')
def list_forever_services():
    cmd = get_command("list")
    output = run_command(cmd)
    return output

@app.route('/start_service', methods=['POST'])
def start_service():
    service_name =  request.form['service_name'];
    script_name =  request.form['script_name'];
    cmd = get_command("start")
    output = run_command(cmd, script_name)
    return output

@app.route('/stop_service', methods=['POST'])
def stop_service():
    service_name =  request.form['service_name'];
    cmd = get_command("stop")
    cmd.append(service_name)
    output = run_command(cmd) 
    return output

def run_command(command, script_name = None):
    if script_name == None:
        p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    else:
        command.append(str("./service_scripts/"+script_name))
        p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    rc = p.returncode
    return output
   

def get_command(type_of_command):
    command_list = {
        "list": ["forever", "list"],
        "stop": ["forever", "stop"],
        "start": ["forever", "start", "-c","python"]
    }
    return command_list[type_of_command]


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
