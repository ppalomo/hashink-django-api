from django.db import models


class Signer(models.Model):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=245, blank=False)
    address = models.CharField(max_length=50, null=True, blank=True)
    price = models.FloatField(blank=False, default=0)
    response_time = models.IntegerField(blank=False, default=0)
    avatar = models.ImageField(
        upload_to='avatars', blank=True, default="avatars/default.jpg")
    autograph = models.ImageField(
        upload_to='autographs', blank=True, default="autographs/default.jpg")
    active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now=True)

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
        return self.full_name
        # return "{}, {}".format(self.last_name, self.first_name)
