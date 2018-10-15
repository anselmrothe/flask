from github_webhook import Webhook
from flask import Flask

app = Flask('hive', static_folder='site', static_url_path='')
webhook = Webhook(app)


@app.route('/')
def show_main():
    return app.send_static_file('index.html')


@app.route('/<variable>/')
def show_html(variable):
    return app.send_static_file('{}/index.html'.format(variable))


# Define a handler for the 'push' event
@webhook.hook()
def on_push(data):
    print("Got push with: {0}".format(data))

# run the application with debug mode
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
