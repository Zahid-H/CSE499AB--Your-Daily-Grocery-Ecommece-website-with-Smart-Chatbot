from django.db import models
from PIL import Image
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.urls import reverse


# Create your models here.

class Category(models.Model):
    category_name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=100,unique=True)
    description = RichTextField(blank=True,null=True)
    cat_image=models.ImageField(upload_to='photos/categories',blank=True)
    thumbnail = models.ImageField(upload_to='photos/thumbnail', blank=True)



    class Meta:
        verbose_name='category'
        verbose_name_plural='categories'

    #this method will show photo in admin panel
    def admin_photo(self):
        if self.thumbnail:
            return mark_safe('<img src="{}" width="100" />'.format(self.thumbnail.url))
        else:
            return mark_safe('<img src="{}" width="100" />'.format("/media/photos/thumbnail/empty.png"))
    admin_photo.short_description="Image"
    admin_photo.allow_tags=True


    def save(self, *args, **kwargs):
        if self.thumbnail:
            #self.slug=slugify(self.slug)
            super(Category,self).save(*args, **kwargs)

            img = Image.open(self.thumbnail.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.thumbnail.path)
        else:
            #self.slug = slugify(self.slug)
            super(Category,self).save(*args, **kwargs)


    # def delete(self, *args, **kwargs):
    #     if self.thumbnail:
    #         super().delete(*args, **kwargs)
    #         os.remove(self.thumbnail.path)
    #     else:
    #         super().delete(*args, **kwargs)


    def __str__(self):
        return self.category_name

    def get_url(self):
        return reverse('product_by_category',args=[self.slug])



class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'sub-category'
        verbose_name_plural = 'sub-categories'

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('product_by_subcategory',args=[self.category.slug,self.slug])