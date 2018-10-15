from flask import Flask
app = Flask('hive', static_folder='site', static_url_path='')


@app.route('/')
def show_main():
    return app.send_static_file('index.html')


@app.route('/<variable>')
def show_html(variable):
    return app.send_static_file('{}/index.html'.format(variable))

# run the application with debug mode
if __name__ == "__main__":
    app.run(debug=True)
