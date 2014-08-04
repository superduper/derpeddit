import sure
from konira_django import Spec
from posts.models import Vote, Post
from django.contrib.auth.models import User

describe "vote post", Spec:

    before all: 
        # required as we override this helper method here
        self.setup_django_test_environment()
        
        # - 
        # Create test fixture
        # -
        
        # OwnerA, will create posts and vote
        ownerA = User(
            first_name="OwnA", 
            last_name="SSmith", 
            username="ownera",
            email="ownA@ssmith"
        )
        ownerA.save()

        # bind our objects to spec instance
        self.ownerA = ownerA
    
    before each:
        userA = User(first_name="AJ", 
            last_name="ASmith",
            email="aj@smith",
            username="userA"
        )
        userA.save()
        userB = User(
            first_name="AJB",
            last_name="ASmith",
            email="aj@smith",
            username="userB"
        )
        userB.save()
        post = Post(
            owner=self.ownerA, 
            title="Post by OwnerA", 
            text="foo bar",
            link="http://google.com"
        )
        post.save()
        self.userA = userA
        self.userB = userB
        self.post = post

    after each: 
        self.userA.delete()
        self.userB.delete()
        self.post.delete()

    it "post is upvoted by owner by default":
        self.post.score.should.be.equal(1)
        self.post.owner.votes.get().is_positive().should.be.ok

    it "updates post score on positive vote":
        self.post.submit_vote(self.userA, positive=True).should.be.ok
        self.post.score.should.be.equal(2)

    it "updates post score on negative vote":
        self.post.submit_vote(self.userA, negative=True).should.be.ok
        self.post.score.should.be.equal(0)

    it "updates score if vote was changed":
        self.post.submit_vote(self.userA, positive=True).should.be.ok
        self.post.score.should.be.equal(2)
        self.post.submit_vote(self.userA, negative=True).should.be.ok
        self.post.score.should.be.equal(1)

    it "doesnt update score if vote was not updated":
        self.post.submit_vote(self.userA, positive=True).should.be.ok
        self.post.submit_vote(self.userA, positive=True).shouldnt.be.ok
        self.post.score.should.be.equal(2)

        self.post.submit_vote(self.userA, negative=True).should.be.ok
        self.post.submit_vote(self.userA, negative=True).shouldnt.be.ok
        self.post.score.should.be.equal(1)

    it "handles multiple votes": 
        self.post.submit_vote(self.userA, positive=True).should.be.ok
        self.post.submit_vote(self.userB, positive=True).should.be.ok
        self.post.score.should.be.equal(3)
        
        self.post.submit_vote(self.userA, negative=True).should.be.ok
        self.post.score.should.be.equal(2)
        self.post.submit_vote(self.userB, negative=True).should.be.ok
        self.post.score.should.be.equal(1)
    
        
