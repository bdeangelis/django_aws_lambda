# cookbook/schema.py
import graphene
from graphene_django import DjangoObjectType
from ingredients.models import Ingredient

from ingredients.models import Category, Ingredient

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "ingredients")

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")


class Query(graphene.ObjectType):
    all_ingredients = graphene.List(IngredientType)
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))

    def resolve_all_ingredients(root, info):
        # We can easily optimize query count in the resolve method
        return Ingredient.objects.select_related("category").all()

    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return None


class CreateIngredient(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()

    ok = graphene.Boolean()
    name = graphene.String()
    ingredient = graphene.Field(lambda: Ingredient)

    def mutate(root, info, id, name):
        ingredient = Ingredient(id=id, name=name)
        ok = True

        return CreateIngredient(ingredient=ingredient, ok=ok)


class Ingredient(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()


class MyMutations(graphene.ObjectType):
    create_ingredient = CreateIngredient.Field()


schema = graphene.Schema(query=Query, mutation=MyMutations)
