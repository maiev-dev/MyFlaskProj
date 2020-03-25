from app import UPLOAD_FOLDER, MAX_FILE_SIZE
from .DB import ins, get, check_username, register, sign, insert_cookie, check_cookie, extended_search
from flask import render_template, redirect, make_response
from app import app
from flask_admin import form
from flask import request
import os
import pymysql
import hashlib
from flask import send_from_directory
import hashlib
from random import randint

con = pymysql.connect('localhost', 'root', 'zxc123qweR', 'test')


@app.route("/", methods=["POST", "GET"])
def index():
    global con
    args = {"method": "GET"}

    if request.method == "POST":
        print(1)
        if bool(request.cookies.get('name')):
            file = request.files["file"]
            if bool(file.filename):
                file_bytes = file.read()
            tags = request.form.get('tags')
            subject = request.form.get('subject')
            date = request.form.get('date')
            args["method"] = "POST"
            args["file_size_error"] = len(file_bytes) > MAX_FILE_SIZE
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
            uploader_nick = request.cookies.get('name')
            ins(con, subject, date, file.filename, uploader_nick, tags)
            return render_template("index.html", args=args)
        else:
            return "<h1>Only registered users allowed</h1>"
    else:
        return render_template("index.html", args=args)


@app.route('/files', methods=["GET", "POST"])
def files():
    global con
    args = {}
    if request.cookies.get('name'):
        args['name'] = request.cookies.get('name')
        args['hash'] = request.cookies.get('hash')
    if request.form.get('subject') and not request.form.get('subject') == "Выберите предмет":
        args['subject'] = request.form.get('subject')
    else:
        args['subject'] = 'all'
    if request.form.get('date'):
        args['date'] = request.form.get('date')
    else:
        args['date'] = 'all'
    conspects = get(con, args)
    args['conspects'] = conspects
    return render_template("table.html", args=args)


@app.route('/register', methods=["GET", "POST"])
def register1():
    args = {}
    if request.method == 'POST':
        args['name'] = request.form.get('nick')
        args['pass'] = request.form.get('pass')
        args['pass_rep'] = request.form.get('pass_rep')
        args['pass_error'] = args['pass'] != args['pass_rep']
        args['name_error'] = check_username(con, args['name'])
        if not args['name_error'] and not args['pass_error']:
            register(con, args)
        return render_template("Register.html", args=args)
    else:
        return render_template('Register.html', args=args)


@app.route('/sign_in', methods=["GET", "POST"])
def sign_in():
    args = {}
    if request.cookies.get('pass'):
        args['method'] = 'GET'
        return render_template("Sign_in.html", args=args)
    if request.method == "POST":
        args['method'] = 'POST'
        args['name'] = request.form.get('nick')
        args['pass'] = request.form.get('pass')
        args['sign_successful'] = sign(con, args)
        if args['sign_successful']:
            password = randint(0, 10000000000000)
            hash_pass = hashlib.md5(str(password).encode())
            args['cookie'] = hash_pass.hexdigest()
            session = make_response(render_template("Sign_in.html", args=args))
            session.set_cookie('pass', hash_pass.hexdigest(), max_age=60 * 60 * 24 * 365 * 2)
            session.set_cookie('name', args['name'], max_age=60 * 60 * 24 * 365 * 2)
            insert_cookie(con, args)
            return session
        return render_template("Sign_in.html", args=args)
    else:
        return render_template("Sign_in.html", args=args)


@app.route('/download/<filename>')
def download(filename):
    print(1)
    return send_from_directory('D:/Desktop/FlaskProg/app/static/files', filename)


@app.route('/log_out', methods=["GET", "POST"])
def log_out():
    ans = make_response(redirect('/sign_in'))
    ans.set_cookie('pass', '0', max_age=0)
    ans.set_cookie('name', '0', max_age=0)
    return ans


@app.route("/extended_search", methods=["POST", "GET"])
def search():
    args = {}
    if request.method == 'POST':
        args['method'] = 'POST'
        args['subject'] = request.form.get('subject')
        args['date'] = request.form.get('date')
        args['uploader_nick'] = request.form.get('uploader_name')
        args['tags'] = request.form.get('tags').split(',')
        for i in range(len(args['tags'])):
            args['tags'][i].replace(' ', '')

        print(args)
        args['conspects'] = extended_search(con, args)
        return render_template('ExtSearch.html', args=args)
    if request.method == 'GET':
        args['method'] = 'GET'
        return render_template('ExtSearch.html', args=args)