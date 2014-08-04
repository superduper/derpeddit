import sure
from konira_django import Spec
from posts.models import Post
from django.contrib.auth.models import User

describe "post meta configuration", Spec:

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

        # OwnerB, will create posts and vote
        ownerB = User(
            first_name="OwnB", 
            last_name="SSmith", 
            email="ownB@ssmith",
            username="ownerB"
        )
        ownerB.save()

        post_by_ownerB = Post(
            owner=ownerB, 
            title="Post by owner B", 
            text="foo bar",
            link="http://google.com"
        )
        post_by_ownerB.save()

        # bind our objects to spec instance
        self.ownerA = ownerA
        self.ownerB = ownerB
        self.postB = post_by_ownerB
    
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
        postA = Post(
            owner=self.ownerA, 
            title="Post by OwnerA", 
            text="foo bar",
            link="http://google.com"
        )
        postA.save()
        self.userA = userA
        self.userB = userB
        self.postA = postA

    after each: 
        self.userA.delete()
        self.userB.delete()
        self.postA.delete()

    it "orders posts by score in descending order":
        self.postA.submit_vote(self.userA, positive=True).should.be.ok
        first, last = Post.objects.all()
        first.pk.should.be.equal(self.postA.pk)
        last.pk.should.be.equal(self.postB.pk)
        # swap votes
        self.postA.submit_vote(self.userA, negative=True).should.be.ok
        self.postA.submit_vote(self.userB, negative=True).should.be.ok
        first, last = Post.objects.all()
        first.pk.should.be.equal(self.postB.pk)
        last.pk.should.be.equal(self.postA.pk)

