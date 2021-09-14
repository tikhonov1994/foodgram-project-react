from django.http.response import HttpResponse
from django.utils import timezone
import django_filters
from reportlab.pdfbase import pdfmetrics  # for cyrillic
from reportlab.pdfbase.ttfonts import TTFont  # for cyrillic
from reportlab.pdfgen import canvas
from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import (GenericViewSet, ModelViewSet, ReadOnlyModelViewSet,
                                     mixins)

from .models import (Tags, Ingredients, Recipes, RecipeIngredient, Favorite, ShoppingCart)
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer, RecipeInShoppingCart
from .filters import RecipeFilter
from .paginators import PageNumberPaginatorModified
from users.permissions import CurrentUserOrAdmin, GetPost


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    filter_backends = [filters.SearchFilter]


class RecipeViewSet(ModelViewSet):
    queryset = Recipes.objects.all().order_by('-id')
    permission_classes = [GetPost, CurrentUserOrAdmin]
    pagination_class = PageNumberPaginatorModified
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(detail=True,
            methods=['get', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipes, pk=pk)
        user = request.user
        if request.method == 'GET':
            if not user.is_favorited.filter(recipe=recipe).exists():
                Favorite.objects.create(user=user, recipe=recipe)
                serializer = RecipeSerializer(
                    recipe, context={'request': request})
                return Response(data=serializer.data,
                                status=status.HTTP_201_CREATED)
            data = {
                'errors': 'Этот рецепт уже есть в избранном'
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_favorited.filter(recipe=recipe).exists():
            data = {
                'errors': 'Этого рецепта не было в вашем избранном'
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            methods=['get', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipes, pk=pk)
        user = request.user
        if request.method == 'GET':
            if not user.is_in_shopping_cart.filter(recipe=recipe).exists():
                ShoppingCart.objects.create(user=user, recipe=recipe)
                serializer = RecipeInShoppingCart(
                    recipe, context={'request': request})
                return Response(data=serializer.data,
                                status=status.HTTP_201_CREATED)
            data = {
                'errors': 'Этот рецепт уже есть в списке покупок'
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_in_shopping_cart.filter(recipe=recipe).exists():
            data = {
                'errors': 'Этого рецепта не было в вашем списке покупок'
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        ShoppingCart.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart = user.is_in_shopping_cart.all()
        shopping_list = {}
        for item in shopping_cart:
            recipe = item.recipe
            ingredients = RecipeIngredient.objects.filter(recipe=recipe)
            for ingredient in ingredients:
                name = ingredient.ingredient.name
                measurement_unit = ingredient.ingredient.measurement_unit
                amount = ingredient.amount
                if name not in shopping_list:
                    shopping_list[name] = {
                        'measurement_unit': measurement_unit,
                        'amount': amount
                    }
                else:
                    shopping_list[name]['amount'] += amount
        file_name = 'СПИСОК ПОКУПОК'
        doc_title = 'СПИСОК ПОКУПОК ДЛЯ РЕЦЕПТОВ'
        title = 'СПИСОК ПОКУПОК'
        sub_title = f'{timezone.now().date()}'
        response = HttpResponse(content_type='application/pdf')
        content_disposition = f'attachment; filename="{file_name}.pdf"'
        response['Content-Disposition'] = content_disposition
        pdf = canvas.Canvas(response)
        pdf.setTitle(doc_title)
        pdfmetrics.registerFont(TTFont('Dej', 'DejaVuSans.ttf'))
        pdf.setFont('Dej', 24)
        pdf.drawCentredString(300, 770, title)
        pdf.setFont('Dej', 16)
        pdf.drawCentredString(290, 720, sub_title)
        pdf.line(30, 710, 565, 710)
        height = 670
        for name, data in shopping_list.items():
            pdf.drawString(
                50,
                height,
                f"{name} - {data['amount']} {data['measurement_unit']}"
            )
            height -= 25
        pdf.showPage()
        pdf.save()
        return response
