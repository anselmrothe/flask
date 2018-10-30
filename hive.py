from flask import Flask, redirect, request
from flask_httpauth import HTTPBasicAuth
from github_webhook import Webhook
import subprocess
import json
import git
import os


git_dir = os.getcwd()  # a github repository folder
g = git.cmd.Git(git_dir)

html_folder = git_dir + '/site'  # html files from mkdocs
app = Flask('hive', static_folder=html_folder, static_url_path='')
webhook = Webhook(app)
auth = HTTPBasicAuth()

users = json.load(open("users.txt"))
# users = {
#     "simple": 'xxxx',  # has access to main page
#     "advanced": 'xxxx'  # has access to sub pages
# }


def advanced_user_only():
    if auth.username() == 'advanced':
        return 'access granted'
    else:
        msg = 'No access for user: ' + auth.username()
        login_trigger_url = 'http://login:xxx@' + request.host
        login_link = '<a href="{}">Login as a different user</a>'.format(
            login_trigger_url)
        return msg + '<br><br>' + login_link


# Website: Main Page
@app.route('/')
@auth.login_required
def show_main():
    return app.send_static_file('index.html')


# Website: Sub Page
@app.route('/<variable>/')
@auth.login_required
def show_html(variable):
    check = advanced_user_only()
    if check == 'access granted':
        return app.send_static_file('{}/index.html'.format(variable))
    else:
        return check


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
    check = advanced_user_only()
    if check == 'access granted':
        cmd = 'cd ' + git_dir + '; mkdocs build'
        proc = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc_out, proc_err = proc.communicate()
        out = proc_out.replace('\n', '<br>')
        err = proc_err.replace('\n', '<br>')
        msg = '[Mkdocs] <br>' + err + out
        return msg
    else:
        return check


# Webhooks: Define a handler for the 'push' event
@webhook.hook()
def on_push(data):
    print("Got push with: {0}".format(data))


# run the application with debug mode
if __name__ == "__main__":
    # app.run(debug=True, host='0.0.0.0', port=80)
    app.run(debug=True)
