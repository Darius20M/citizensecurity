from rest_flex_fields import FlexFieldsModelSerializer
from security.models import ApplicationModel
from security.serializers import UserSerializer


class ApplicationSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = ApplicationModel
        fields = (
            'id',
            'name',
            'code',
            'user',
            'about',
            'key',
            'secret',
            'is_staff',
            'is_enabled',
            'created',
            'created_by',
            'modified',
            'modified_by',
        )
        read_only_fields = ('id', 'created', 'modified',)
        expandable_fields = {
            'user': (UserSerializer, {'many': False, 'read_only': True}),
            'created_by': (UserSerializer, {'many': False, 'read_only': True}),
            'modified_by': (UserSerializer, {'many': False, 'read_only': True})
        }

    def update(self, instance, validated_data):
        instance.modified_by = self.context["request"].user
        return super().update(instance, validated_data)
    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)