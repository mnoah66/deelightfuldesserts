from django.db import models
from django.contrib.auth.models import User

from django.core.files import File

from PIL import Image
from io import BytesIO

def compress(image):
    im = Image.open(image)
    loadedImage = im.load()
    # create a BytesIO object
    im_io = BytesIO() 
    # save image to BytesIO object
    #im = im.resize([500,500])
    im = loadedImage.convert("RGB")
    im = im.save(im_io,'JPEG', quality=30) 
    # create a django-friendly Files object
    new_image = File(im_io, name=image.name)
    return new_image

class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name


class Photo(models.Model):
    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'
    
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=False, blank=False)
    description = models.TextField()

    def __str__(self):
        return self.description
    
    def save(self, *args, **kwargs):
        if self.image:
            if self.image.size > (300 * 1024):
                # call the compress function
                try:
                    new_image = compress(self.image)
                except:
                    new_image = self.image
                # set self.image to new_image
                self.image = new_image
        super().save(*args, **kwargs)
