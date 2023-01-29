"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import (
    Recipe,
    Tag
)

class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""
    class Meta:
        model = Tag
        fields = ["name", "id"]
        read_only_fields = ["id"]

class RecipeSerializer(serializers.ModelSerializer):
    """Serialzer for recipes."""
    tags = TagSerializer(many=True, required=False)
    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "time_minutes",
            "price",
            "link",
            "tags"
        ]
        read_only_fields = [ "id" ]

    # This method gets/creates the given tags and assign it to the recipe.
    # It is added to avoid code duplication
    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags as needed."""
        auth_user = self.context["request"].user
        for tag in tags:
            if "user" not in tag:
                tag["user"] = auth_user
            tag_obj, created = Tag.objects.get_or_create(
                **tag
            )
            recipe.tags.add(tag_obj)

    # Overriding create method to check wether the tags are already created.
    def create(self, validated_data):
        """Create a recipe."""
        tags = validated_data.pop("tags", [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)

        return recipe

    def update(self, instance, validated_data):
        """Update recipe."""
        tags = validated_data.pop("tags", None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for Recipe detail view."""
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + [ "description" ]
