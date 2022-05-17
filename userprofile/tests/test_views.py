from datetime import datetime
from django.shortcuts import redirect
from django.test import TestCase, Client
from django.urls import reverse
from userprofile.models import Lecture,Course,Rating,Profile
import json
from django.contrib.auth.models import User
from django.utils import timezone

from userprofile.views import user_profile
from django.core.files.uploadedfile import SimpleUploadedFile


class TestViews(TestCase):

    def setUp(self):
        self.client=Client()
        #create user
        self.user = User.objects.create_user('testuser', 'testuser@mail.com','123456')
        self.user2 = User.objects.create_user('testuser2', 'testuser2@mail.com','123456')

        # create Profile model object
        Profile.objects.create(
            user = self.user,
            bio= "Hello"
        )

        # create Course model object
        course=Course.objects.create(
            user=self.user,
            title='Course Title',
            description='Course Description',
            published_date= timezone.now(),
            img = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
        )
        course.enrolled_users.add(self.user2)
        course.save()

        self.delete_course = reverse('delete_course', args=[course.title])
  

    # testing user_profile view
    def test_user_profile_GET(self):
        self.client.login(username='testuser', password='123456')
        response=self.client.get(reverse('user_profile'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'userprofile/profile.html')

    # testing delete_course view
    def test_delete_course_GET(self):
        self.client.login(username='testuser', password='123456')
        response=self.client.get(self.delete_course)
        self.assertRedirects(response, '/myspace/profile', target_status_code=301)

    # testing course_new view
    def test_course_new_GET(self):
        response = self.client.post(reverse('course_new'), {
            'user' : self.user,
            'title' : 'Course Test',
            'description' : 'Test Description',
            'published_date': timezone.now(),
            'img': SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
        })

        self.assertEquals(response.status_code, 302)

    