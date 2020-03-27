from py2neo import Graph, Node, Relationship, authenticate
from passlib.hash import bcrypt
from datetime import datetime, date
import uuid

authenticate("localhost:7474","neo4j","lpmss1998")
graph = Graph("http://localhost:7474/db/data/")


def timestamp():
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    delta = now - epoch
    return delta.total_seconds()

def date():
    return datetime.now().strftime('%Y-%m-%d')


class User():
    def __init__(self, username, firstname, lastname, profession, country):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.profession = profession
        self.country = country

    def find(self):
        user = graph.find_one('User', 'username', self.username)
        return user

    def register(self, password):
        if not self.find():
            user = Node('User', username=self.username, password=bcrypt.encrypt(password), firstname=self.firstname, lastname=self.lastname, profession=self.profession, country=self.country)
            graph.create(user)
            return True
        else:
            return False

    def verify_password(self, password):
        user = self.find()
        if user:
            return bcrypt.verify(password, user['password'])
        else:
            return False

    def add_post(self, title, tags, text, destination):
        user = self.find()
        post = Node(
            'Post',
            id=str(uuid.uuid4()),
            title=title,
            image=destination,
            text=text,
            timestamp=timestamp(),
            now=datetime.now(),
            date=date()
        )
        rel = Relationship(user, 'PUBLISHED', post)
        graph.create(rel)

        tags = [x.strip() for x in tags.lower().split(',')]
        for tag in set(tags):
            t = graph.merge_one('Tag', 'name', tag)
            rel = Relationship(t, 'TAGGED', post)
            graph.create(rel)

    def like_post(self, post_id):
        user = self.find()
        post = graph.find_one('Post', 'id', post_id)
        graph.create_unique(Relationship(user, 'LIKED', post))

    def comment_post(self, text, post_id):
        user = self.find()
        post = graph.find_one('Post', 'id', post_id)
        comment = Node(
            'Comment',
            id=str(uuid.uuid4()),
            text=text,
            date=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        )

        rel1 = Relationship(post, 'GOT', comment)
        rel2 = Relationship(user, 'COMMENTED', comment)
        graph.create_unique(rel1)
        graph.create_unique(rel2)

    def get_article(self, post_id):
        query = '''
        MATCH (user:User)-[:PUBLISHED]->(post:Post)<-[:TAGGED]-(tag:Tag) 
        WHERE post.id ={post_id}
        RETURN user.username AS username, post, COLLECT(tag.name) AS tags
        '''

        return graph.cypher.execute(query, username=self.username, post_id=post_id)

    def get_recent_posts(self, n):
        query = '''
        MATCH (user:User)-[:PUBLISHED]->(post:Post)<-[:TAGGED]-(tag:Tag)
        WHERE user.username = {username}
        RETURN post, COLLECT(tag.name) AS tags
        ORDER BY post.timestamp DESC LIMIT {n}
        '''

        return graph.cypher.execute(query, username=self.username, n=n)

    def get_similar_users(self, n):
        # Find three users who are most similar to the logged-in user
        # based on tags they've both blogged about.
        query = '''
        MATCH (you:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
              (they:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
        WHERE you.username = {username} AND you <> they
        WITH they, COLLECT(DISTINCT tag.name) AS tags
        ORDER BY SIZE(tags) DESC LIMIT {n}
        RETURN they.username AS similar_user, tags
        '''

        return graph.cypher.execute(query, username=self.username, n=n)

    def get_commonality_of_user(self, user):
        # Find how many of the logged-in user's posts the other user
        # has liked and which tags they've both blogged about.
        query1 = '''
        MATCH (user1:User)-[:PUBLISHED]->(post:Post)<-[:LIKED]-(user2:User)
        WHERE user1.username = {username1} AND user2.username = {username2}
        RETURN COUNT(post) AS likes
        '''
        likes = graph.cypher.execute_one(query1, username1=self.username, username2=user.username)
        likes = 0 if not likes else likes

        query2 = '''
        MATCH (user1:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
        (user2:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag)
        WHERE user1.username = {username1} AND user2.username = {username2}
        RETURN COLLECT(DISTINCT tag.name) AS tags
        '''
        tags = graph.cypher.execute(query2, username1=self.username, username2=user.username)[0]['tags']


        return {'likes':likes, 'tags':tags}

def get_all_posts(n):
    query = '''
    MATCH (user:User)-[:PUBLISHED]->(post:Post)<-[:TAGGED]-(tag:Tag)
    RETURN user.username AS username, post, COLLECT(tag.name) AS tags
    ORDER BY post.timestamp DESC LIMIT {n}
    '''

    return graph.cypher.execute(query, n=n)

def get_comment(user, post_id):

    query = '''
    MATCH (user:User)-[:COMMENTED]->(comment:Comment)<-[:GOT]-(post:Post) 
    WHERE post.id ={post_id}
    RETURN user.username AS username, post, comment, COUNT(comment) AS count
    '''

    return graph.cypher.execute(query, username=user.username, post_id=post_id)

def count_comment(post_id):

    query = '''
        MATCH (comment:Comment)<-[:GOT]-(post:Post) 
        WHERE post.id ={post_id}
        RETURN COUNT(comment) AS count
        '''

    return graph.cypher.execute(query, post_id=post_id)