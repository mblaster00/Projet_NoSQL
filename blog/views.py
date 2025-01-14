from flask import Flask, render_template, request, flash, redirect, url_for, session
from .models import User, get_all_posts, get_comment, count_comment, get_post_categorie, get_tag_categorie, graph, \
    get_search


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'jfif'}

import os
app = Flask(__name__)
app.secret_key = ""
app_root = os.path.dirname(os.path.abspath(__file__))

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    username = session.get('username')
    return User.get_id(id, username)



@app.route('/page/<int:page_num>', methods=['GET'])
def page(page_num):

    try:
        posts = get_all_posts(50)
        posts_page = posts[(page_num - 1) * 5:page_num * 5]
        length = len(posts)//5 + 1


        list = []
        for row in posts_page:
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

        tag_list = []
        tag_lenght = []
        tag = get_tag_categorie(5)

        for row in tag:
            tag_name = row.tags
            tag_list.append(tag_name)
            tag_post = get_post_categorie(tag_name, 20)
            tag_lenght.append(len(tag_post))


         ################################################################################################

        username = session.get('username')
        node = graph.find_one('User', 'username', username)
        subscribe = node['subscribe']
        user = User(username, node['firstname'], node['lastname'], node['email'])

        similar = user.get_similar_users(3)

        list_filename = []
        list_similar = []
        list_post = []

        for users in similar:
            similar_node = graph.find_one('User', 'username', users.similar_user)
            similar_user = User(users.similar_user, similar_node['firstname'], similar_node['lastname'], similar_node['email'])
            list_similar.append(similar_user)

        for user in list_similar:
            similar_posts = user.get_recent_posts(1)
            list_post.append(similar_posts)

        for row in list_post:
            target = 'images'
            properties = row[0][0]
            similar_file_name = '/'.join([target, properties['image']])
            list_filename.append(similar_file_name)



        return render_template('index.html', posts=posts_page, file_name=list, length=length, current_page=page_num, subscribe=subscribe,
                               recent_posts=recent_posts, recent_file_name=recent_list, tag=tag_list, tag_lenght=tag_lenght,
                               similar_posts=list_post, similar_user=list_similar, similar_file_name=list_filename)

    except UnboundLocalError:
        return render_template('index.html', posts=posts, file_name=list, subscribe=subscribe, tag=tag_list, tag_lenght=tag_lenght,
                               recent_posts=recent_posts, recent_file_name=recent_list)

    except:
        return render_template('index.html')



@app.route('/', methods=['GET'])
def index():

    try:
        posts = get_all_posts(10)
        posts_page = posts[0:5]
        length = len(posts) // 5 + 1

        list = []
        for row in posts_page:
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

        tag_list = []
        tag_lenght = []
        tag = get_tag_categorie(5)

        for row in tag:
            tag_name = row.tags
            tag_list.append(tag_name)
            tag_post = get_post_categorie(tag_name, 20)
            tag_lenght.append(len(tag_post))


         ################################################################################################

        username = session.get('username')
        node = graph.find_one('User', 'username', username)
        subscribe = node['subscribe']
        user = User(username, node['firstname'], node['lastname'], node['email'])


        similar = user.get_similar_users(3)

        list_filename = []
        list_similar = []
        list_post = []

        for users in similar:
            similar_node = graph.find_one('User', 'username', users.similar_user)
            similar_user = User(users.similar_user, similar_node['firstname'], similar_node['lastname'], similar_node['email'])
            list_similar.append(similar_user)

        for user in list_similar:
            similar_posts = user.get_recent_posts(1)
            list_post.append(similar_posts)

        for row in list_post:
            target = 'images'
            properties = row[0][0]
            similar_file_name = '/'.join([target, properties['image']])
            list_filename.append(similar_file_name)



        return render_template('index.html', posts=posts_page, file_name=list, length=length, current_page=1, subscribe=subscribe,
                               recent_posts=recent_posts, recent_file_name=recent_list, tag=tag_list, tag_lenght=tag_lenght,
                               similar_posts=list_post, similar_user=list_similar, similar_file_name=list_filename)

    except UnboundLocalError:
        return render_template('index.html', posts=posts, file_name=list, subscribe=subscribe, tag=tag_list, tag_lenght=tag_lenght,
                               recent_posts=recent_posts, recent_file_name=recent_list)

    except:
        return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():

    if load_user(id):
        try:
            posts = get_all_posts(10)
            posts_page = posts[0:5]
            length = len(posts) // 5 + 1

            list = []
            for row in posts_page:
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

            tag_list = []
            tag_lenght = []
            tag = get_tag_categorie(5)

            for row in tag:
                tag_name = row.tags
                tag_list.append(tag_name)
                tag_post = get_post_categorie(tag_name, 20)
                tag_lenght.append(len(tag_post))

            ################################################################################################

            username = session.get('username')
            node = graph.find_one('User', 'username', username)
            subscribe = node['subscribe']
            user = User(username, node['firstname'], node['lastname'], node['email'])

            similar = user.get_similar_users(3)

            list_filename = []
            list_similar = []
            list_post = []

            for users in similar:
                similar_node = graph.find_one('User', 'username', users.similar_user)
                similar_user = User(users.similar_user, similar_node['firstname'], similar_node['lastname'],
                                    similar_node['email'])
                list_similar.append(similar_user)

            for user in list_similar:
                similar_posts = user.get_recent_posts(1)
                list_post.append(similar_posts)

            for row in list_post:
                target = 'images'
                properties = row[0][0]
                similar_file_name = '/'.join([target, properties['image']])
                list_filename.append(similar_file_name)



            return render_template('index.html', posts=posts_page, file_name=list, length=length, subscribe=subscribe,
                                   recent_posts=recent_posts, recent_file_name=recent_list, tag=tag_list,
                                   tag_lenght=tag_lenght,
                                   similar_posts=list_post, similar_user=list_similar, similar_file_name=list_filename)

        except UnboundLocalError:
            return render_template('index.html', posts=posts, file_name=list, subscribe=subscribe, tag=tag_list,
                                   tag_lenght=tag_lenght,
                                   recent_posts=recent_posts, recent_file_name=recent_list)

        except:
            return render_template('index.html')




    ##################################################################

    else:
        try:
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                firstname = request.form['firstname']
                lastname = request.form['lastname']
                email = request.form['email']

                user = User(username, firstname, lastname, email)

                if not user.register(password):
                    flash("Ce nom d'utilisateur existe deja dans la base.")
                else:
                    flash('Super votre inscription est bien prise en compte. Vous pouvez maintenant vous connecter')

            return render_template('register.html')

        except:

            flash("L'email et le nom d'utilisateur doivent etre uniques.")
            return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():

    if load_user(id):
        try:
            posts = get_all_posts(10)
            posts_page = posts[0:5]
            length = len(posts) // 5 + 1

            list = []
            for row in posts_page:
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

            tag_list = []
            tag_lenght = []
            tag = get_tag_categorie(5)

            for row in tag:
                tag_name = row.tags
                tag_list.append(tag_name)
                tag_post = get_post_categorie(tag_name, 20)
                tag_lenght.append(len(tag_post))

            ################################################################################################

            username = session.get('username')
            node = graph.find_one('User', 'username', username)
            subscribe = node['subscribe']
            user = User(username, node['firstname'], node['lastname'], node['email'])

            similar = user.get_similar_users(3)

            list_filename = []
            list_similar = []
            list_post = []

            for users in similar:
                similar_node = graph.find_one('User', 'username', users.similar_user)
                similar_user = User(users.similar_user, similar_node['firstname'], similar_node['lastname'],
                                    similar_node['email'])
                list_similar.append(similar_user)

            for user in list_similar:
                similar_posts = user.get_recent_posts(1)
                list_post.append(similar_posts)

            for row in list_post:
                target = 'images'
                properties = row[0][0]
                similar_file_name = '/'.join([target, properties['image']])
                list_filename.append(similar_file_name)



            return render_template('index.html', posts=posts_page, file_name=list, length=length, subscribe=subscribe,
                                   recent_posts=recent_posts, recent_file_name=recent_list, tag=tag_list,
                                   tag_lenght=tag_lenght,
                                   similar_posts=list_post, similar_user=list_similar, similar_file_name=list_filename)

        except UnboundLocalError:
            return render_template('index.html', posts=posts, file_name=list, subscribe=subscribe, tag=tag_list,
                                   tag_lenght=tag_lenght,
                                   recent_posts=recent_posts, recent_file_name=recent_list)

        except:
            return render_template('index.html')


    ###########################################################################################


    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        node = graph.find_one('User', 'username', username)

        try:
            user = User(username, node['firstname'], node['lastname'], node['email'])

            if not user.verify_password(password):
                flash('Vos identifiants semblent incorrects.')
            else:
                session['username'] = user.username
                return redirect(url_for('index'))

        except TypeError:
            flash("Identifiants non enregistrés. Veuillez verifier vos identifants encore.")

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

    if load_user(id):

        try:
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
                    user = User(node['username'], node['firstname'], node['lastname'], node['email'])

                    if file and allowed_file(file.filename):
                        file_name = file.filename
                        destination = '/'.join([target, file_name])
                        file.save(destination)

                        user.add_post(title, tags, text, file_name)
                        return redirect(url_for('index'))

            return render_template('poster.html')

        except:
            return render_template('login.html')

    else:
        return render_template('login.html')



@app.route('/like_post/<post_id>')
def like_post(post_id):
    username = session.get('username')
    node = graph.find_one('User', 'username', username)
    user = User(username, node['firstname'], node['lastname'], node['email'])

    user.like_post(post_id)

    return redirect(request.referrer)


@app.route('/comment_post/<post_id>', methods=['GET', 'POST'])
def comment_post(post_id):
    username = session.get('username')
    node = graph.find_one('User', 'username', username)
    user = User(username, node['firstname'], node['lastname'], node['email'])

    if request.method == 'POST':
        text = request.form['comment']
        user.comment_post(text, post_id)

    return redirect(request.referrer)



@app.route('/article/<post_id>')
def article(post_id):

    if load_user(id):

        username = session.get('username')
        node = graph.find_one('User', 'username', username)
        user = User(username, node['firstname'], node['lastname'], node['email'])

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
                                similar_node['email'])
            similar_posts = similar_user.get_recent_posts(2)

        try:
            return render_template('article.html', article=article,
                                   file_name=file_name, similar_posts=similar_posts, similar_user=similar_user.username,
                                   comment=comment, count=count)
        except UnboundLocalError:
            return render_template('article.html', article=article,
                                   file_name=file_name, comment=comment, count=count)


    else:
        return render_template('login.html')


@app.route('/categorie/<tag>', methods=['GET'])
def categorie(tag):

    if load_user(id):

        try:
            username = session.get('username')
            node = graph.find_one('User', 'username', username)
            user = User(username, node['firstname'], node['lastname'], node['email'])

            similar = user.get_similar_users(3)

            list_filename = []
            for users in similar:
                similar_node = graph.find_one('User', 'username', users.similar_user)
                similar_user = User(users.similar_user, similar_node['firstname'], similar_node['lastname'],
                                    similar_node['email'])
                similar_posts = similar_user.get_recent_posts(2)
                for row in similar_posts:
                    target = 'images'
                    properties = row.post
                    similar_file_name = '/'.join([target, properties['image']])
                    list_filename.append(similar_file_name)


            posts = get_post_categorie(tag, 5)

            tag_filename = []
            for row in posts:
                target = 'images'
                properties = row.post
                tag_file_name = '/'.join([target, properties['image']])
                tag_filename.append(tag_file_name)


            return render_template('categories.html', tag=tag, user=user, post=posts,
                                   similar_posts=similar_posts, similar_user=similar_user.username,
                                   similar_file_name=list_filename, tag_filename=tag_filename)


        except UnboundLocalError:

            return render_template('categories.html', tag=tag, user=user, post=posts, tag_filename=tag_filename)

        except:

            return render_template('categories.html')


    else:
        return render_template('login.html')





@app.route('/results', methods=['GET', 'POST'])
def search():

    if load_user(id):
        if request.method == 'POST':
            search = request.form['search']
            try:
                # search by tag or post
                posts = get_search(search, 5)
                if not posts:
                    flash('No results found!')
                    return render_template('search.html')

                else:
                    list = []
                    for row in posts:
                        target = 'images'
                        properties = row.post
                        file_name = '/'.join([target, properties['image']])
                        list.append(file_name)
                    return render_template('search.html', posts=posts, file_name=list)

            except:
                return redirect('/')


    else:
        return render_template('login.html')



@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():

    if request.method == 'POST':
        username = session.get('username')
        node = graph.find_one('User', 'username', username)
        if node['subscribe']:
            node['subscribe'] = False
            node.push()
        else:
            node['subscribe'] = True
            node.push()

    return redirect(request.referrer)
