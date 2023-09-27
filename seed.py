from models import User, Post, Tag, PostTag, db
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
    t1 = Tag(name="Fun")
    t2 = Tag(name="Even More")
    t3 = Tag(name="Bloop")
    t4 = Tag(name="Zope")

    pt1 = PostTag(post_id=1, tag_id=1)
    pt2 = PostTag(post_id=2, tag_id=2)
    pt3 = PostTag(post_id=3, tag_id=3)
    pt4 = PostTag(post_id=4, tag_id=4)
    pt5 = PostTag(post_id=5, tag_id=1)
    pt6 = PostTag(post_id=6, tag_id=2)
    pt7 = PostTag(post_id=7, tag_id=3)
    pt8 = PostTag(post_id=8, tag_id=4)
    pt9 = PostTag(post_id=1, tag_id=2)
    pt10 = PostTag(post_id=2, tag_id=3)
    pt11 = PostTag(post_id=3, tag_id=4)
    pt12 = PostTag(post_id=4, tag_id=1)
    pt13 = PostTag(post_id=5, tag_id=2)
    pt14 = PostTag(post_id=6, tag_id=3)
    pt15 = PostTag(post_id=7, tag_id=4)
    pt16 = PostTag(post_id=8, tag_id=1)

    db.session.add_all([u1, u2, u3, u4])
    db.session.commit()

    db.session.add_all([t1, t2, t3, t4])
    db.session.commit()

    db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8])
    db.session.commit()

    db.session.add_all(
        [
            pt1,
            pt2,
            pt3,
            pt4,
            pt5,
            pt6,
            pt7,
            pt8,
            pt9,
            pt10,
            pt11,
            pt12,
            pt13,
            pt14,
            pt15,
            pt16,
        ]
    )
    db.session.commit()
