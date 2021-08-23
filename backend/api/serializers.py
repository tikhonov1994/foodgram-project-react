 
import base64
import imghdr
import uuid

from django.db import models
from django.db.models import fields
from rest_framework import serializers

from .models import Tags, Ingredients, Recipes


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        required=True,
        allow_empty_file=False,
        use_url=True,
    )

    class Meta:
        model = Recipes
        fields = '__all__'


class RecipeInShoppingCart(serializers.ModelSerializer):
    image = serializers.ImageField(
        required=True,
        allow_empty_file=False,
        use_url=True,
    )

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')
