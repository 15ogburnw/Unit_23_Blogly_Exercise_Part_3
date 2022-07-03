from models import db, User, Post, Tag, PostTag
from app import app

db.drop_all()
db.create_all()

User.query.delete()
Post.query.delete()
Tag.query.delete()
PostTag.query.delete()

alan = User(first_name='Alan', last_name='Alda',
            image_url='https://t4.ftcdn.net/jpg/02/19/63/31/360_F_219633151_BW6TD8D1EA9OqZu4JgdmeJGg4JBaiAHj.jpg')
joel = User(first_name='Joel', last_name='Burton',
            image_url='https://image.shutterstock.com/mosaic_250/698308/567772042/stock-photo-headshot-of-successful-smiling-cheerful-african-american-businessman-executive-stylish-company-567772042.jpg')
jane = User(first_name='Jane', last_name='Smith',
            image_url='https://jaysoriano.com/wp-content/uploads/2018/04/P8110606-Edit.jpg')


db.session.add_all([alan, joel, jane])
db.session.commit()

post1 = Post(title="Joel's First Post",
             content='Hello my name is Joel, and I am posting for the first time!', user_id=2)
post2 = Post(title="My Favorite Ice Cream Flavors", content="""
Joel here again! My top 3 flavors of ice cream are:

1. Chocolate
2. Pistachio
3. Mint Chocolate Chip

""", user_id=2)
post3 = Post(title="What a Great Day!",
             content='Today I went on a hike, and the weather was beautiful! My dog had a great time running up and down the trail.', user_id=3)

db.session.add_all([post1, post2, post3])
db.session.commit()


fun = Tag(name='Fun')
nature = Tag(name='Nature')
hiking = Tag(name='Hiking')
yummy = Tag(name='Yummy')

post2.tags.append(yummy)
post3.tags.append(fun)
post3.tags.append(nature)
post3.tags.append(hiking)

db.session.commit()
