from flask import Flask, redirect, request
from flask_httpauth import HTTPBasicAuth
from github_webhook import Webhook
import git
import subprocess


# git_dir = 'hive_mind'  # a github repository folder
git_dir = 'test2'  # a github repository folder
g = git.cmd.Git(git_dir)

html_folder = git_dir + '/site'
app = Flask('hive', static_folder=html_folder, static_url_path='')
webhook = Webhook(app)
auth = HTTPBasicAuth()

users = {
    "simple": "pw1",  # has access to main page
    "advanced": "level2"  # has access to sub pages
}


@app.route('/')
@auth.login_required
def show_main():
    return app.send_static_file('index.html')


@app.route('/<variable>/')
@auth.login_required
def show_html(variable):
    if auth.username() == 'advanced':
        return app.send_static_file('{}/index.html'.format(variable))
    else:
        msg = 'No access for user: ' + auth.username()
        login_trigger_url = 'http://login:xxx@' + request.host
        login_link = '<a href="{}">Login as a different user</a>'.format(
            login_trigger_url + '/' + variable)
        return msg + '<br><br>' + login_link


# Password: Check
@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


# Password: Change user
@app.route('/login/')
def login():
    login_trigger_url = 'http://login:xxx@' + request.host
    return redirect(login_trigger_url)


# Github: Pull
@app.route('/pull/')
def git_pull():
    msg = g.pull()
    return msg


# Mkdocs: Build
@app.route('/build/')
def mkdocs_build():
    p = subprocess.Popen('cd ' + git_dir + '; mkdocs build',
                         shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    msg = '[Mkdocs] ' + p.stdout.read()
    return msg


# Webhooks: Define a handler for the 'push' event
@webhook.hook()
def on_push(data):
    print("Got push with: {0}".format(data))


# run the application with debug mode
if __name__ == "__main__":
    # app.run(debug=True, host='0.0.0.0', port=80)
    app.run(debug=True)
