from django.test import TestCase

from .text_preprocessing import preprocess_text, convert_words_to_numbers
from .greedy_string_tiling import greedy_string_tiling


class PreprocessingTestCase(TestCase):
    def test_numbers_to_words(self):
        text = "123"
        result = preprocess_text(text, lemmatize=False, numbers_to_words=True)
        expected = (
            ["one", "hundred", "and", "twentythree"],
            "one hundred and twentythree",
        )
        self.assertEqual(result, expected)

    def test_strip_spaces(self):
        text = "  test   test  "
        result = preprocess_text(text, lemmatize=False)
        expected = (["test", "test"], "test test")
        self.assertEqual(result, expected)


class W2NTestCase(TestCase):
    def test_default_lang(self):
        text = "one two three"
        result = convert_words_to_numbers(text)
        expected = "1 2 3"

        self.assertEqual(result, expected)

    def test_spanish_lang(self):
        text = "uno dos tres"
        result = convert_words_to_numbers(text, language="es")
        expected = "1 2 3"

        self.assertEqual(result, expected)

    def test_unsupported_lang(self):
        text = "jeden dva tri"
        result = convert_words_to_numbers(text, language="sk")
        expected = "jeden dva tri"

        self.assertEqual(result, expected)


class GSTTestCase(TestCase):
    def test_single_full_match(self):
        text_a = "hello"
        text_b = "how delightful, hello there"

        expected = ([{"fromA": 0, "fromB": 16, "toA": 5, "toB": 21}], 5)
        result = greedy_string_tiling(text_a, text_b, len(text_a))

        self.assertEqual(result, expected)

    def test_single_partial_match(self):
        text_a = "hello"
        text_b = "we are in helsinki now"
        match_len = 3

        expected = ([{"fromA": 0, "toA": 3, "fromB": 10, "toB": 13}], 3)
        result = greedy_string_tiling(text_a, text_b, match_len)

        self.assertEqual(result, expected)

    def test_no_match(self):
        text_a = "hello"
        text_b = "go away, you nuisance"

        expected = ([], 0)
        result = greedy_string_tiling(text_a, text_b, len(text_a))

        self.assertEqual(result, expected)

    def test_gst_normal(self):
        text_a = (
            "dnes je pekne miesa sinym vlaknitym materialom. Pouziva sa na vy slovo"
        )
        text_b = "dnes je pekne miesa asdasdasd sinym vlaknitym materialom. asdasdadasd Pouziva sa na vy nieco ine"

        expected = (
            [
                {"fromA": 0, "toA": 20, "fromB": 0, "toB": 20},
                {"fromA": 20, "toA": 48, "fromB": 30, "toB": 58},
                {"fromA": 48, "toA": 65, "fromB": 70, "toB": 87},
            ],
            65,
        )
        result = greedy_string_tiling(text_a, text_b, 4)

        self.assertEqual(result, expected)

    def test_gst_short(self):
        text_a = (
            "dnes je pekne miesa sinym vlaknitym materialom. Pouziva sa na vy slovo"
        )
        text_b = "dnes"

        expected = ([], 0)
        result = greedy_string_tiling(text_a, text_b, 5)

        self.assertEqual(result, expected)
