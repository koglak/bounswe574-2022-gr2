from django.test import SimpleTestCase
from userprofile.forms import ProfileForm
from django.core.files.uploadedfile import SimpleUploadedFile

class TestForms(SimpleTestCase):

    def test_profile_form_valid(self):

        form = ProfileForm(data={
            'bio': 'Hello',
            'img': SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
        })

        self.assertTrue(form.is_valid())

    
