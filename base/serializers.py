from rest_framework.serializers import ModelSerializer
from .models import *

class UserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"

class PostSerializer(ModelSerializer):
    owner = UserSerializer()
    class Meta:
        model = Post
        fields = "__all__"

class RecommendationSerializer(ModelSerializer):
    post_ptr = PostSerializer()
    class Meta:
        model = Recommendation
        fields = "__all__"

class SocialEventSerializer(ModelSerializer):
    post_ptr = PostSerializer()
    class Meta:
        model = SocialEvent
        fields = "__all__"

class ClubEventSerializer(ModelSerializer):
    post_ptr = PostSerializer()
    class Meta:
        model = ClubEvent
        fields = "__all__"

class InternshipSerializer(ModelSerializer):
    post_ptr = PostSerializer()
    class Meta:
        model = Internship
        fields = "__all__"

class TransportSerializer(ModelSerializer):
    post_ptr = PostSerializer()
    class Meta:
        model = Transport
        fields = "__all__"

class AccommodationSerializer(ModelSerializer):
    post_ptr = PostSerializer()
    class Meta:
        model = Accommodation
        fields = "__all__"


