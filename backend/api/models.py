from django.db import models
from django.db.models import fields
from users.models import CustomUser


class Tags(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=256, unique=True)
    color = models.CharField(verbose_name=(u'Color'), max_length=7,
                         help_text=(u'HEX color, as #RRGGBB'), unique=True)
    slug = models.SlugField(verbose_name='slug', max_length=64, unique=True)
    
    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('slug',)

    def __str__(self) -> str:
        return self.name


class Ingredients(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=64, blank=False)
    measurement_unit = models.CharField(verbose_name='Единица измерения', max_length=32, blank=False)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class Recipes(models.Model):
    ingredients = models.ManyToManyField(Ingredients, verbose_name='Ингредиенты', related_name='ingredients_recipes', blank=False)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Автор', related_name='author_recipes', blank=False)
    tags = models.ManyToManyField(Tags, verbose_name='Тэги', related_name='tags_recipes', blank=False)
    image = models.ImageField(verbose_name='Изображение', upload_to='recipes/', blank=False)
    name = models.CharField(verbose_name='Название', max_length=200, blank=False)
    text = models.TextField(verbose_name='Описание', blank=False)
    cooking_time = models.PositiveIntegerField(verbose_name='Время приготовления (в минутах)', blank=False)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Subscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscription_on')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscriber')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['recipe', 'ingredient'], name='recipe_ingredient_unique')]


class ShoppingCart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['recipe', 'user'], name='recipe_unique')]


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['recipe', 'user'], name='favorite_recipe_unique')]