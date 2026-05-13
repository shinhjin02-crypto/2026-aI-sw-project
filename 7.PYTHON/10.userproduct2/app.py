@app.route('/')
def hone():
    return send_from_directory("statkc", "index.html")

@app.route('/user')
def user():
    return send_from_directory("statkc", "")

if __name__ == '__main__':