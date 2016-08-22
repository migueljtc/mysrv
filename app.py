from bottle import route, run, debug, template, request, error,static_file,get,post
import threading
import os

class ServerState():

	def __init__(self):
		self.nr_hits = 0
		self.my_lock = threading.Lock()

	def add_hit(self):
		with self.my_lock:
			self.nr_hits+=1
		return self.nr_hits



@route('/')
def todo_list():   
    return 'Hello World %d' %st.add_hit()

@route('/hello/:name')
def hello_name(name):
    return '<h1>HELLO %s <br/></h1>' %name

@route('/static/:filename')
def serve_static(filename):
    return static_file(filename, root='/uploads')

@get('/upload')
def upload_view():
	return template('upload')

@route('/upload', method='POST')
def do_upload():
	upload = request.files.get('upload')
	name, ext = os.path.splitext(upload.filename)
	save_path = "./uploads"
	if not os.path.exists(save_path):
			os.makedirs(save_path)
	file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
	upload.save(file_path)
	return "File successfully saved to '{0}'.".format(save_path)
    
@error(404)
def error404(error):
    return 'Nothing here, sorry'    

st = ServerState()
run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), server='waitress' )
#run(host="192.168.163.177", reloader=True,debug=True, server='waitress')
