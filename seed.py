from models import User, Post, db
from app import app


with app.app_context():
    db.drop_all()
    db.create_all()

    u1 = User(first_name="Mason", last_name="Bybee")
    u2 = User(first_name="Chloe", last_name="Getso")
    u3 = User(first_name="Kaleb", last_name="Creason")
    u4 = User(first_name="Tanner", last_name="Barnes")

    p1 = Post(
        title="First Post!",
        content="Hi, this is the first post on the website!",
        user_id=1,
    )
    p2 = Post(
        title="Favorite animal", content="My favorite animal is an otter", user_id=1
    )
    p3 = Post(title="Below Deck", content="Kate is my favorite!!!!!", user_id=2)
    p4 = Post(
        title="Nail Polish",
        content="Ugh, nail polish is soooooo expensive!!",
        user_id=2,
    )
    p5 = Post(
        title="League of Legends",
        content="my teams are always running it down mid",
        user_id=3,
    )
    p6 = Post(
        title="MMORPG",
        content="hey anyone want to play an MMORPG that i will only play for 2 days max",
        user_id=3,
    )
    p7 = Post(
        title="Destiny 2",
        content="Did you guys see the Destiny 2 gun crafting glitch?!?!?",
        user_id=4,
    )
    p8 = Post(
        title="Street fighter",
        content="doing street fighter 1v1s ill beat anyone because i spend all day looking at exactly how many frames each attack takes!",
        user_id=4,
    )

    db.session.add_all([u1, u2, u3, u4])
    db.session.commit()

    db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8])
    db.session.commit()
