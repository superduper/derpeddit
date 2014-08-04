from django.db import models

class Post(models.Model):
    owner = models.ForeignKey("auth.User")
    title = models.CharField(max_length=100)
    score = models.IntegerField(default=0)
    link = models.URLField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score', '-created']

    def _get_or_create_vote(self, user):
        # Get or create a vote instance
        filters = dict(owner=user, post=self)
        return Vote.objects.get_or_create(**filters)

    def _incr_score(self):
        """Increase total score
        """
        self.score += 1

    def _decr_score(self):
        """Decrease total score
        """
        self.score -= 1

    def submit_vote(self, voter, positive=None, negative=None):
        """Submits vote for post
        @type    voter: User
        @type positive: bool or None
        @type negative: bool or None
        """
        vote, created = self._get_or_create_vote(voter)
        vote_has_been_updated = vote.set_score(self, positive, negative)
        if vote_has_been_updated:
            self.save()
            vote.save()
        return vote_has_been_updated

class Comment(models.Model):
    owner = models.ForeignKey("auth.User", related_name="comments")
    post = models.ForeignKey(Post, related_name="comments")
    text = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created', ]

class Vote(models.Model):
    owner = models.ForeignKey("auth.User", related_name="votes")
    post = models.ForeignKey(Post, related_name="votes")
    score = models.SmallIntegerField(default=0)

    class Meta:
        unique_together = ('owner', 'post')

    def set_score(self, post, positive=None, negative=None):
        """
        @type post: Post
        @type positive: bool or None
        @type negative: bool or None
        """
        self.validate_vote_params(positive, negative)
        setup_positive = (positive and not self.is_positive())
        setup_negative = (negative and not self.is_negative())
        has_been_updated = setup_negative or setup_positive
        if setup_positive:
            post._incr_score()
            self.set_positive()
        elif setup_negative:
            post._decr_score()
            self.set_negative()

        return has_been_updated

    def set_positive(self):
        self.score = 1

    def set_negative(self):
        self.score = -1

    def is_positive(self):
        return self.score == 1

    def is_negative(self):
        return self.score == -1

    @staticmethod
    def validate_vote_params(positive, negative):
        """
        Helper method for validating input params
        """
        invalid_param = (
            positive is None and negative is None,
            positive is not None and negative is not None
        )
        if any(invalid_param):
           raise ValueError("Vote should be either positive or negative")


import signals