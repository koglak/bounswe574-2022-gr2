from django.test import TestCase
from userprofile.models import Profile, Course, Lecture, Rating
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone


class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'testuser@mail.com','123456')

        self.profile= Profile.objects.create(
            user = self.user,
            bio= "Hello"
        )

        self.course=Course.objects.create(
            user=self.user,
            title='Course Title',
            description='Course Description',
            published_date= timezone.now(),
            img = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
        )
        self.course.enrolled_users.add(self.user)
        self.course.save()

    def test_profile_model(self):
        self.assertEquals(self.profile.bio, 'Hello')

    def test_course_model(self):
        self.assertEquals(self.course.title, 'Course Title' )