from django.db import models
import uuid
from datetime import date
# Create your models here.


class Auto(models.Model):
    """
    Модель представляющая машину (название, цена, изображение)
    """
    name = models.CharField(max_length=200, help_text="Enter a car name")
    price = models.IntegerField(help_text="Enter a car price")
    image = models.ImageField(upload_to='autos')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]


class Order(models.Model):
    """
    Модель представляющая заказ (название машины и дата)
    """
    # Foreign Key используется, потому что заказу соответствует одна машина,
    # а у одной машины может быть много заказов
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auto = models.ForeignKey('Auto', on_delete=models.CASCADE)
    date = models.DateField(default=date.today)

    def __str___(self):
        return '{0} ({1})'.format(self.id,self.auto.name)


