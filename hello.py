from flask import Flask
app = Flask('hello', static_url_path='/static')


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/fun')
def the_name_is_arbitrary():
    return 'Hello, Fun!'


@app.route('/<variable>')
def the_name_is_arbitrary_but_unique(variable):
    return 'Your variable is: ' + variable


@app.route('/x')
def arbitrary():
    return app.send_static_file('hello.html')

# run the application with debug mode
if __name__ == "__main__":
    app.run(debug=True)
