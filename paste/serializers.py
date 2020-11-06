from rest_framework import serializers

from paste import constants
from paste.models import Snippet


class SnippetSerializer(serializers.ModelSerializer):
    """Snippet model serializer."""

    class Meta:
        model = Snippet
        fields = '__all__'
        read_only_fields = ['owner']

    def create(self, validated_data: dict) -> Snippet:
        """Check that if current user is anonymous they are not trying to
        create a private snippet, then create new instance.
        """
        if (self.context['request'].user.is_anonymous
                and validated_data.get('private', constants.DEFAULT_PRIVATE)):
            raise serializers.ValidationError(
                'anonymous users cannot create private snippets')

        return super().create(validated_data)
