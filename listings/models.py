from django.db import models
from django.forms import ModelForm, DecimalField, IntegerField, ImageField
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.owner_user.id, filename)


# Create your models here.
class Listing(models.Model):
    title_text    = models.CharField(max_length=60)
    desc_text     = models.TextField(max_length=5000)
    money_price   = models.DecimalField(max_digits=19, decimal_places=2)
    int_inventory = models.PositiveIntegerField()
    owner_user    = models.ForeignKey(User, on_delete=models.CASCADE)
    image         = models.ImageField(upload_to=user_directory_path, height_field=None, width_field=None, max_length=None, null=True)


class ListingModelForm(ModelForm):
    money_price = DecimalField(validators=[MinValueValidator(0.01)], label="Price per unit")
    int_inventory = IntegerField(validators=[MinValueValidator(1)], label="Units on hand")
    image = ImageField(required=False, label="Image (optional)")
    class Meta:
        model = Listing
        fields = ['title_text', 'desc_text', 'money_price', 'int_inventory', 'image']
        labels = {
            'title_text': 'Title',
            'desc_text': 'Description',
            'money_price': 'Price per unit',
            'int_inventory': 'Units on hand',
            'image': 'Image (optional)'
        }