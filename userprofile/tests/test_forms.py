from django.test import SimpleTestCase
from userprofile.forms import LectureForm

class TestForms(SimpleTestCase):

    def test_lecture_form_valid(self):

        form = LectureForm(data={
            'title': 'Hello',
            'content': 'content',
        })

        self.assertTrue(form.is_valid())

    
    def test_lecture_form_no_data(self):
        form = LectureForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),2)

