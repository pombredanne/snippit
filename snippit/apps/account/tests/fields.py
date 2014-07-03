# -*- coding: utf-8 -*-
from django.test import TestCase
from account.models import User
from account.fields import GravatarField
from rest_framework.serializers import ModelSerializer
from snippit.core.mixins import HttpStatusCodeMixin
from django.core.validators import URLValidator


class GravatarFieldTest(HttpStatusCodeMixin, TestCase):
    """
    Tests for the GravatarField field_to_native() behavior
    """

    def test_field_to_native(self):
        """
        GravatarField field_to_native() manuel tests
        """
        user = User.objects.filter().order_by('?')[0]
        field = GravatarField(source='email')
        regex = URLValidator.regex
        self.assertIsNotNone(field.field_to_native(user, 'avatar'))
        self.assertRegexpMatches(field.field_to_native(user, 'avatar'), regex)

    def test_form(self):
        """
        GravatarField field_to_native() form tests
        """
        class GravatarForm(ModelSerializer):
            avatar = GravatarField(source='email')

            class Meta:
                model = User
                fields = ('avatar',)

        regex = URLValidator.regex
        user = User.objects.filter().order_by('?')[0]
        serializer = GravatarForm(instance=user)
        self.assertIn('avatar', serializer.data)
        self.assertIsNotNone(serializer.data['avatar'])
        self.assertRegexpMatches(serializer.data['avatar'], regex)