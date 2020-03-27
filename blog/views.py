from flask import Flask, render_template, request, flash, redirect, url_for, session
from .models import User, get_all_posts, get_comment, count_comment, graph

import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'jfif'}

app = Flask(__name__)
app.secret_key = "Vegeta#5"
app_root = os.path.dirname(os.path.abspath(__file__))


@app.route('/', methods=['GET'])
def index():

    try:
        username = session.get('username')
        node = graph.find_one('User', 'username', username)
        user = User(username, node['firstname'], node['lastname'], node['profession'], node['country'])

        similar = user.get_similar_users(3)

        list_filename = []
        for users in similar:
            similar_node = graph.find_one('User', 'username', users.similar_user)
            similar_user = User(users.similar_user, similar_node['firstname'], similar_node['lastname'], similar_node['profession'], similar_node['country'])
            similar_posts = similar_user.get_recent_posts(1)
            for row in similar_posts:
                target = 'images'
                properties = row.post
                similar_file_name = '/'.join([target, properties['image']])
                list_filename.append(similar_file_name)


        posts = get_all_posts(10)

        list = []
        for row in posts:
            target = 'images'
            properties = row.post
            file_name = '/'.join([target, properties['image']])
            list.append(file_name)

        recent_posts = get_all_posts(3)

        recent_list = []
        for row in recent_posts:
            target = 'images'
            properties = row.post
            recent_file_name = '/'.join([target, properties['image']])
            recent_list.append(recent_file_name)



        return render_template('index.html', posts=posts, file_name=list,
                               recent_posts=recent_posts, recent_file_name=recent_list,
                               similar_posts=similar_posts, similar_user=similar_user.username, similar_file_name=list_filename)

    except UnboundLocalError:
        return render_template('index.html', posts=posts, file_name=list,
                               recent_posts=recent_posts, recent_file_name=recent_list)

    except:
        return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        profession = request.form['profession']
        country = request.form['country']

        user = User(username, firstname, lastname, profession, country)

        if not user.register(password):
            flash('Cet utilisateur existe deja dans la base.')
        else:
            flash('Super votre inscription est bien prise en compte. Vous pouvez maintenant vous connecter')

    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        node = graph.find_one('User', 'username', username)
        user = User(username, node['firstname'], node['lastname'], node['profession'], node['country'])

        if not user.verify_password(password):
            flash('Vos identifiants semblent incorrects.')
        else:
            session['username'] = user.username
            return redirect(url_for('index'))

    return render_template('login.html')



@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/post', methods=['GET', 'POST'])
def add_post():

    target = os.path.join(app_root, 'static/images/')
    if not os.path.isdir(target):
        os.mkdir(target)

    if request.method == 'POST' and 'file' in request.files:
        title = request.form['title']
        tags = request.form['tags']
        text = request.form['text']
        file = request.files['file']

        if not title or not tags or not text:
            flash('You must give a title, tags and post a text body.')
        else:
            node = graph.find_one('User', 'username', session['username'])
            user = User(node['username'], node['firstname'], node['lastname'], node['profession'], node['country'])

            if file and allowed_file(file.filename):
                file_name = file.filename
                destination = '/'.join([target, file_name])
                file.save(destination)

                user.add_post(title, tags, text, file_name)
                return redirect(url_for('index'))

    return render_template('poster.html')


@app.route('/like_post/<post_id>')
def like_post(post_id):
    username = session.get('username')
    node = graph.find_one('User', 'username', username)
    user = User(username, node['firstname'], node['lastname'], node['profession'], node['country'])

    user.like_post(post_id)

    return redirect(request.referrer)


@app.route('/comment_post/<post_id>', methods=['GET', 'POST'])
def comment_post(post_id):
    username = session.get('username')
    node = graph.find_one('User', 'username', username)
    user = User(username, node['firstname'], node['lastname'], node['profession'], node['country'])

    if request.method == 'POST':
        text = request.form['comment']
        user.comment_post(text, post_id)

    return redirect(request.referrer)



@app.route('/article/<post_id>')
def article(post_id):

    username = session.get('username')
    node = graph.find_one('User', 'username', username)
    user = User(username, node['firstname'], node['lastname'], node['profession'], node['country'])

    comment = get_comment(user, post_id)
    count = count_comment(post_id)
    for row in count:
        count = row.count

    article = user.get_article(post_id)
    for row in article:
        target = 'images'
        properties = row.post
        file_name = '/'.join([target, properties['image']])

    similar = user.get_similar_users(3)

    for users in similar:
        similar_node = graph.find_one('User', 'username', users.similar_user)
        similar_user = User(users.similar_user, similar_node['firstname'], similar_node['lastname'],
                            similar_node['profession'], similar_node['country'])
        similar_posts = similar_user.get_recent_posts(1)

    try:
        return render_template('article.html', article=article,
                               file_name=file_name, similar_posts=similar_posts, similar_user=similar_user.username,
                               comment=comment, count=count)
    except UnboundLocalError:
        return render_template('article.html', article=article,
                               file_name=file_name, comment=comment, count=count)


@app.route('/categorie/', methods=['GET'])
def categorie():
    return render_template('categories.html')




