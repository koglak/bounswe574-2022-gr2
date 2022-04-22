from django.test import SimpleTestCase
from django.urls import reverse, resolve
from userprofile.views import user_profile,course_detail,course_enroll

class TestUrls(SimpleTestCase):

    # testing simple url 
    def test_user_profile_url_is_resolved(self):
        # reverse() finds the url of view function
        url = reverse('user_profile')
        # checks if they are equal
        self.assertEquals(resolve(url).func, user_profile)

    # testing <str:title> format url
    def test_course_detail_url_is_resolved(self):
        url = reverse('course_detail', args=['some-slug'])
        self.assertEquals(resolve(url).func, course_detail)

    # testing <int:pk> format url
    def test_course_enroll_url_is_resolved(self):
        url = reverse('course_enroll',args=[5])
        self.assertEquals(resolve(url).func, course_enroll)