from django.contrib import admin
from products.models import Product, PBI, Task,User
# Register your models here.


admin.site.register(Product)
admin.site.register(PBI)
admin.site.register(Task)
admin.site.register(User)
