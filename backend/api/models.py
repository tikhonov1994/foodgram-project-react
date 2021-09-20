from django.db import models
from django.db.models import constraints

from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=256,
                            unique=True)
    color = models.CharField(verbose_name=(u'Color'), max_length=7,
                             help_text=(u'HEX color, as #RRGGBB'), unique=True)
    slug = models.SlugField(verbose_name='slug', max_length=64, unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('slug',)

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=64)
    measurement_unit = models.CharField(verbose_name='Единица измерения',
                                        max_length=32)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        related_name='ingredients_recipes',
    )
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               verbose_name='Автор',
                               related_name='author_recipes')
    tags = models.ManyToManyField(Tag, verbose_name='Тэги',
                                  related_name='tags_recipes')
    image = models.ImageField(verbose_name='Изображение',
                              upload_to='recipes/')
    name = models.CharField(verbose_name='Название', max_length=200)
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (в минутах)'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Subscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='subscription_on')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='subscriber')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'author'],
            name='subscription_unique'
        )]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='amounts')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='amounts')
    amount = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['recipe', 'ingredient'],
            name='recipe_ingredient_unique'
        )]


class ShoppingCart(models.Model):
    user = models.ForeignKey(CustomUser, related_name='purchases',
                             on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name='customers',
                               on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['recipe', 'user'],
                                               name='recipe_unique')]


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, related_name='favorite_subscriber',
                             on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name='favorite_recipe',
                               on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['recipe', 'user'],
                                               name='favorite_recipe_unique')]
