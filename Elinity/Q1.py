
##Problem Statement:
from flask import Flask, request, jsonify
from peewee import *
app = Flask(__name__)
# Database Setup (SQLite)
db = SqliteDatabase('marketplace.db')
class BaseModel(Model):
    class Meta:
        database = db

#defining user model 
class User(BaseModel):
    username = CharField(unique=True)
#defining Image containing below attributes (We have assumned but it can be vary dependsupon the need and use cases)
class ImagePost(BaseModel):
    title = CharField()
    author = ForeignKeyField(User, backref='images', on_delete='CASCADE')
    description = TextField()
    price = FloatField()
    sole_buyer = BooleanField()
    labels = TextField()  # Comma-separated
    likes = IntegerField(default=0)
    avg_rating = FloatField(default=0.0)
    ratings_count = IntegerField(default=0)

class Like(BaseModel):
    user = ForeignKeyField(User, backref='likes', on_delete='CASCADE')
    image = ForeignKeyField(ImagePost, backref='liked_by', on_delete='CASCADE')

class Rating(BaseModel):
    user = ForeignKeyField(User, backref='ratings', on_delete='CASCADE')
    image = ForeignKeyField(ImagePost, backref='rated_by', on_delete='CASCADE')
    stars = IntegerField()

# Initialize Database
db.connect()
db.drop_tables([User, ImagePost, Like, Rating])
db.create_tables([User, ImagePost, Like, Rating])
print("Database reset successful.")

# Create User
@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    user, created = User.get_or_create(username=data['username'])
    return jsonify({'message': 'User created', 'id': user.id})

# Create Image Post
@app.route('/post_image', methods=['POST'])
def post_image():
    data = request.json
    user = User.get(User.id == data['author_id'])
    image = ImagePost.create(
        title=data['title'],
        author=user,
        description=data['description'],
        price=data['price'],
        sole_buyer=data['sole_buyer'],
        labels=data['labels']
    )
    return jsonify({'message': 'Image posted', 'id': image.id})

# Get Marketplace Feed
@app.route('/feed', methods=['GET'])
def feed():
    images = ImagePost.select().order_by(-ImagePost.likes, ImagePost.price)
    return jsonify([image.__data__ for image in images])

# Search Images
@app.route('/search', methods=['GET'])
def search():
    label = request.args.get('label')
    author = request.args.get('author')
    query = ImagePost.select()
    if label:
        query = query.where(ImagePost.labels.contains(label))
    if author:
        query = query.join(User).where(User.username == author)
    return jsonify([image.__data__ for image in query])

# Like an Image
@app.route('/like/<int:image_id>/<int:user_id>', methods=['POST'])
def like(image_id, user_id):
    user = User.get_by_id(user_id)
    image = ImagePost.get_by_id(image_id)
    _, created = Like.get_or_create(user=user, image=image)
    if created:
        image.likes += 1
        image.save()
    return jsonify({'message': 'Image liked'})

# Rate an Image
@app.route('/rate/<int:image_id>/<int:user_id>', methods=['POST'])
def rate(image_id, user_id):
    stars = request.json.get('stars')
    if stars not in range(1, 6):
        return jsonify({'error': 'Rating must be 1-5'}), 400
    user = User.get_by_id(user_id)
    image = ImagePost.get_by_id(image_id)
    Rating.create(user=user, image=image, stars=stars)
    avg = Rating.select(fn.AVG(Rating.stars)).where(Rating.image == image).scalar()
    image.avg_rating = avg
    image.save()
    return jsonify({'message': 'Image rated'})

# Filter Images
@app.route('/filter', methods=['GET'])
def filter_images():
    min_price = request.args.get('min_price', type=float, default=0)
    max_price = request.args.get('max_price', type=float, default=99999)
    min_rating = request.args.get('min_rating', type=float, default=0)
    sole_buyer = request.args.get('sole_buyer', type=bool, default=None)

    query = ImagePost.select().where(
        (ImagePost.price >= min_price) & (ImagePost.price <= max_price) & (ImagePost.avg_rating >= min_rating)
    )
    if sole_buyer is not None:
        query = query.where(ImagePost.sole_buyer == sole_buyer)
    
    return jsonify([image.__data__ for image in query])

if __name__ == '__main__':
    app.run(debug=True)


##Note:  Please Use curl.txt to run curl command on postman for Api testing