from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ModelForm

# Create your models here.
User = get_user_model()


class Message(models.Model):
    author = models.ForeignKey(
        User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.TextField(default="main")

    def __str__(self):
        return self.author.username

    async def lastmsgs(room):
        # return Message.objects.order_by('-timestamp').all()[:10]
        return Message.objects.order_by('-timestamp').all().filter(room=room)[:50]
      
      

# class MessageModelForm(ModelForm):
#     author = DecimalField(validators=[MinValueValidator(0.01)])
#     int_inventory = IntegerField(validators=[MinValueValidator(1)])
#     image = ImageField(required=False)
