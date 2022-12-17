from django.db import models
from ckeditor.fields import RichTextField
from category.models import Category,SubCategory
from django.utils.safestring import mark_safe
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count
import math
# Create your models here.

class Product(models.Model):
    product_name=models.CharField(max_length=200)
    slug=models.SlugField(max_length=200)
    description=RichTextField(blank=True)
    price=models.IntegerField()
    image=models.ImageField(upload_to='photos/products')
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_date', )

    def admin_photo(self):
        if self.image:
            return mark_safe('<img src="{}" width="100" />'.format(self.image.url))
        else:
            return mark_safe('<img src="{}" width="100" />'.format("/media/photos/thumbnail/empty.png"))
    admin_photo.short_description="Image"
    admin_photo.allow_tags=True



    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.subcategory.slug,self.id])

    def get_url2(self):
        return reverse('store',args=[self.category.slug,self.subcategory.slug])

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
            whole = math.floor(avg)
            frac = avg - whole
            if (frac >= 0.5):
                all = whole + 0.5
                return  all
            else:
                return whole

        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count



############### variation #######################

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


class Variation(models.Model):

    VARIATION_CATEGORY = (
        ('color', 'color'),
        ('size', 'size'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=VARIATION_CATEGORY)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject




# class ProductGallery(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='product/images/gallery/')
#
#     def __str__(self):
#         return self.product.product_name
#
#     class Meta:
#         verbose_name = 'productgallery'
#         verbose_name_plural = 'product gallery'