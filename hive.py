from flask import Flask
from github_webhook import Webhook
import git


app = Flask('hive', static_folder='site', static_url_path='')
webhook = Webhook(app)

# git_dir = 'hive_mind'  # a github repository folder
git_dir = 'test2'  # a github repository folder
g = git.cmd.Git(git_dir)


@app.route('/')
def show_main():
    return app.send_static_file('index.html')


@app.route('/<variable>/')
def show_html(variable):
    return app.send_static_file('{}/index.html'.format(variable))


# Github: Pull
@app.route('/pull/')
def git_pull():
    msg = g.pull()
    return msg


# Webhooks: Define a handler for the 'push' event
@webhook.hook()
def on_push(data):
    print("Got push with: {0}".format(data))


# run the application with debug mode
if __name__ == "__main__":
    # app.run(debug=True, host='0.0.0.0', port=80)
    app.run(debug=True)
