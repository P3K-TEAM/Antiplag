from django.test import TestCase

from .text_preprocessing import preprocess_text


class PreprocessingTestCase(TestCase):
    def test_numbers_to_words(self):
        text = "123"
        result = preprocess_text(text, lemmatize=False, numbers_to_words=True)
        expected = (['one', 'hundred', 'and', 'twentythree'], 'one hundred and twentythree')
        self.assertEqual(result, expected)

    def test_strip_spaces(self):
        text = "  test   test  "
        result = preprocess_text(text, lemmatize=False)
        expected = (['test', 'test'], 'test test')
        self.assertEqual(result, expected)
