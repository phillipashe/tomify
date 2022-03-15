from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from PIL import Image as Img
import io 

# for writing to picture
from django.core.files import File


# Create your models here.
class Profile(models.Model):
    #name = models.CharField(max_length = 50)
    picture = models.ImageField(upload_to = 'pictures')
    is_tom = models.BooleanField(default=False) 
    output = None
    img = None

    # function resizes picture so the largest dimension is 680px
    def save(self, *args, **kwargs):
        img = self.img
        output = self.output
        img.save(output, format='JPEG', quality=90)
        output.seek(0)
        self.picture= InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.picture.name.split('.')[0], 'image/jpeg', '100', None)
        super(Profile, self).save(*args, **kwargs) 

    def resize(self, *args, **kwargs):
        if self.picture:
            img = Img.open(io.BytesIO(self.picture.read()))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            #img.thumbnail((self.picture.width/1.5,self.picture.height/1.5), Img.ANTIALIAS)
            if self.picture.height < self.picture.width:
                new_width = 680
                img.thumbnail((new_width, new_width * self.picture.height / self.picture.width), Img.ANTIALIAS)
            else:
                new_height = 680
                img.thumbnail((new_height * self.picture.width / self.picture.height, new_height), Img.ANTIALIAS)
            self.output = io.BytesIO()
            self.img = img

    class Meta:
        db_table = "profile"
