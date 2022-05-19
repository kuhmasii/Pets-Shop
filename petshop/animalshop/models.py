from django.db import models
from django.http import Http404


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    about = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return f'{self.name}--- created on ---{self.updated}'

    def get_prod(self, id):
        try:
            queryset = self.category_prod.get(id=id)
        except self.DoesNotExist:
            raise Http404
        return queryset

    def get_products(self):
        query = self.category_prod.all()
        return query


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category_prod')
    name = models.CharField(max_length=100, blank=False,
                            null=False, db_index=True)
    slug = models.SlugField(max_length=200, blank=False,
                            null=False, db_index=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    _image = models.ImageField(upload_to='prod_images/%Y/%m/%d', blank=True)
    in_stock = models.BooleanField(default=True)
    shipping = models.BooleanField(default=False)
    _discount = models.DecimalField(max_digits=10, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self) -> str:
        return self.name

    @property
    def discount(self) -> str:
        return self._discount

    @property
    def image(self) -> str:
        try:
            url = self._image.url
        except:
            url = ''
        return url
