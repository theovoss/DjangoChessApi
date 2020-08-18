from django.test import SimpleTestCase

from DjangoChessApi.Chess.templatetags.get_item import get_item
from DjangoChessApi.Chess.templatetags.index import index
from DjangoChessApi.Chess.templatetags.times import times
from DjangoChessApi.Chess.templatetags.times_reverse import times_reverse


class TemplateTagTest(SimpleTestCase):
    def test_get_item(self):
        actual = get_item({'title': 'Hey There!'}, 'title')
        self.assertEqual(actual, 'Hey There!')

    def test_index(self):
        a = ['a', 'b', 'c', 'd']
        self.assertEqual(index(a, 2), 'c')

    def test_index_outside_range(self):
        a = ['a', 'b', 'c', 'd']
        self.assertIsNone(index(a, 20))

    def test_times(self):
        actual = times(8)
        self.assertEqual(actual, '01234567')

    def test_times_reverse(self):
        actual = times_reverse(8)
        self.assertEqual(actual, '76543210')
