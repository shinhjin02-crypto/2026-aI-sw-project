app = Flask (__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/login', methods = ['POST'])
def login() :
    