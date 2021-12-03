from rest_framework import serializers
from .models import *
from .utils import get_user_analytics


class FaqCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FaqCategory
        exclude = []


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        exclude = []


class FeedbackMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackMessage
        exclude = []


class UserDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    cards = serializers.SerializerMethodField()
    guarantors = serializers.SerializerMethodField()
    analytics = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()
    wallet = serializers.DictField(source='get_wallet', read_only=True)

    def get_analytics(self, obj):
        return get_user_analytics(obj)

    def get_first_name(self, obj):
        return obj.first_name()

    def get_last_name(self, obj):
        return obj.last_name()

    def get_email(self, obj):
        return obj.email()

    def get_group(self, obj):
        if Group.objects.filter(user__email=obj.user.email).exists():
            return [{'id': group.id, 'name': group.name} for group in Group.objects.filter(user__email=obj.user.email)]
        return None

    def get_guarantors(self, obj):
        guarantors = [guarantor.guarantor for guarantor in Guarantor.objects.filter(user=obj).distinct()
                      if guarantor.guarantor != obj]
        return UserDetailSerializer(guarantors, many=True).data

    def get_cards(self, obj):
        return UserCard.objects.filter(user=obj).values('id', 'bank', 'card_type', 'bin', 'last4', 'exp_month',
                                                        'exp_year', 'default') or None

    class Meta:
        model = Profile
        exclude = ['bvn', 'user']


class GuarantorSerializer(serializers.ModelSerializer):
    # guarantor = serializers.SerializerMethodField()
    # guarantor = UserDetailSerializer()

    # def get_guarantor(self, obj):
    #     return UserDetailSerializer(obj.guarantor).data

    class Meta:
        model = Guarantor
        exclude = ['id', 'user']


class WalletSerializer(serializers.ModelSerializer):
    user_detail = serializers.SerializerMethodField()

    def get_user_detail(self, obj):
        user = dict()
        user['first_name'] = obj.user.first_name()
        user['last_name'] = obj.user.last_name()
        user['email'] = obj.user.email()
        return user

    class Meta:
        model = Wallet
        exclude = ['user']


class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    def get_permissions(self, obj):
        if obj.permissions:
            perm = [perms.name for perms in obj.permissions.all()]
            return perm
        return None

    class Meta:
        model = Group
        exclude = []


