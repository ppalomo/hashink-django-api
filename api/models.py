from django.db import models

# region Signer


class Signer(models.Model):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=245, blank=False)
    address = models.CharField(
        max_length=50, null=True, blank=True, unique=True)
    price = models.FloatField(blank=False, default=0)
    response_time = models.IntegerField(blank=False, default=0)
    avatar = models.ImageField(
        upload_to='avatars', blank=True, default="avatars/default.jpg")
    autograph = models.ImageField(
        upload_to='autographs', blank=True, default="autographs/default.jpg")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    @property
    def price_eth(self):
        return self.price / 1e18

    class Meta:
        verbose_name = "signer"
        verbose_name_plural = "signers"
        ordering = ['-created_at']

    def __str__(self):
        return "{} - {}".format(self.id, self.full_name)

# endregion

# region GroupSig


class GroupSig(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    price = models.FloatField(blank=False, default=0)
    response_time = models.IntegerField(blank=False, default=0)
    avatar = models.ImageField(
        upload_to='avatars', blank=True, default="avatars/default.jpg")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    signers = models.ManyToManyField(
        Signer, related_name='groups', blank=True, through='GroupSig_Signer')

    @property
    def price_eth(self):
        return self.price / 1e18

    class Meta:
        verbose_name = "groupsig"
        verbose_name_plural = "groupsigs"
        ordering = ['-created_at']

    def __str__(self):
        return "{} - {}".format(self.id, self.name)

# endregion

# region GroupSig_Signer


class GroupSig_Signer(models.Model):
    groupsig = models.ForeignKey(GroupSig, models.CASCADE)
    signer = models.ForeignKey(Signer, models.CASCADE)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "groupsig signer"
        verbose_name_plural = "groupsig signers"
        ordering = ['-created_at']

    def __str__(self):
        return "{} - {}".format(self.groupsig.name, self.signer.full_name)

# endregion

# region Request


class Request(models.Model):
    requester_address = models.CharField(max_length=50, null=True, blank=True)
    groupsig = models.ForeignKey(
        GroupSig, null=True, blank=True, on_delete=models.RESTRICT)
    signer = models.ForeignKey(
        Signer, null=True, blank=True, on_delete=models.RESTRICT)
    price = models.FloatField(blank=False, default=0)
    response_time = models.IntegerField(blank=False, default=0)
    state = models.IntegerField(blank=False, null=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    signers = models.ManyToManyField(
        Signer, related_name='requests', blank=True, through='Request_Signer')

    @property
    def name(self):
        return self.signer.full_name if self.groupsig is None else self.groupsig.name

    class Meta:
        verbose_name = "request"
        verbose_name_plural = "requests"
        ordering = ['-created_at']

    def __str__(self):
        return "{} - {} - {}".format(self.id, self.signer.full_name if self.groupsig is None else self.groupsig.name, self.requester_address)

# endregion

# region Request_Signer


class Request_Signer(models.Model):
    request = models.ForeignKey(Request, models.CASCADE)
    signer = models.ForeignKey(Signer, models.CASCADE)
    signed_at = models.DateTimeField(null=True)

    @property
    def is_signed(self):
        return True if self.signed_at is not None else False

    def __str__(self):
        return "{} - {}".format(self.request.id, self.signer.full_name)

# endregion

# region Category


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    parent_category = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    signers = models.ManyToManyField(
        Signer, blank=True, related_name='categories')
    groupsigs = models.ManyToManyField(
        GroupSig, blank=True, related_name='categories')

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ['id']

    def __str__(self):
        return "{} - {} ({})".format(self.id, self.name, self.parent_category)


# endregion
