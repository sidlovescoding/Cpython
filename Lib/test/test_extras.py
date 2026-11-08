"""Tests for the extras module."""

import contextlib
import io
import sys
import unittest
from unittest import mock

import extras


class UniqueTests(unittest.TestCase):
    def test_keeps_first_of_each_in_order(self):
        self.assertEqual(extras.unique([3, 1, 3, 2, 1]), [3, 1, 2])

    def test_empty(self):
        self.assertEqual(extras.unique([]), [])

    def test_any_iterable(self):
        self.assertEqual(extras.unique(iter('abca')), ['a', 'b', 'c'])

    def test_key(self):
        self.assertEqual(extras.unique(['a', 'A', 'b'], key=str.lower),
                         ['a', 'b'])

    def test_unhashable_items(self):
        self.assertEqual(extras.unique([[1], [2], [1]]), [[1], [2]])

    def test_mixed_hashable_and_unhashable(self):
        self.assertEqual(extras.unique([1, [1], 1, [1]]), [1, [1]])

    def test_unhashable_key_result(self):
        self.assertEqual(extras.unique([1, 2, 3], key=lambda x: [x % 2]),
                         [1, 2])

    def test_hash_error_from_item_is_not_hidden(self):
        class Bad:
            def __hash__(self):
                raise ZeroDivisionError
        with self.assertRaises(ZeroDivisionError):
            extras.unique([Bad()])


class FirstTests(unittest.TestCase):
    def test_first_item(self):
        self.assertEqual(extras.first([5, 6]), 5)

    def test_falsy_first_item_is_returned(self):
        self.assertEqual(extras.first([0, 1], default=9), 0)

    def test_empty_gives_default(self):
        self.assertIsNone(extras.first([]))
        self.assertEqual(extras.first([], 'none'), 'none')

    def test_where(self):
        self.assertEqual(extras.first([1, 2, 3, 4], where=lambda n: n > 2), 3)

    def test_where_no_match_gives_default(self):
        self.assertEqual(extras.first([1], 'none', where=lambda n: n > 2),
                         'none')

    def test_stops_early(self):
        items = iter([1, 2, 3])
        extras.first(items)
        self.assertEqual(next(items), 2)


class GroupByTests(unittest.TestCase):
    def test_groups_items_that_are_apart(self):
        words = ['apple', 'bean', 'avocado', 'beet', 'cherry']
        self.assertEqual(extras.group_by(words, key=lambda w: w[0]),
                         {'a': ['apple', 'avocado'], 'b': ['bean', 'beet'],
                          'c': ['cherry']})

    def test_group_order_is_first_appearance(self):
        groups = extras.group_by([3, 1, 2, 4, 5], key=lambda n: n % 2)
        self.assertEqual(list(groups), [1, 0])
        self.assertEqual(groups, {1: [3, 1, 5], 0: [2, 4]})

    def test_key_is_positional_or_keyword(self):
        self.assertEqual(extras.group_by([1, 2], str),
                         {'1': [1], '2': [2]})
        self.assertEqual(extras.group_by([1, 2], key=str),
                         {'1': [1], '2': [2]})

    def test_empty(self):
        self.assertEqual(extras.group_by([], key=len), {})

    def test_accepts_any_iterable(self):
        self.assertEqual(extras.group_by((n for n in range(4)), key=bool),
                         {False: [0], True: [1, 2, 3]})

    def test_equal_keys_share_a_group(self):
        self.assertEqual(extras.group_by([1, 1.0, True], key=lambda x: x),
                         {1: [1, 1.0, True]})

    def test_unhashable_key_raises(self):
        with self.assertRaises(TypeError):
            extras.group_by([1], key=lambda x: [x])

    def test_key_error_propagates(self):
        def key(item):
            raise ValueError('bad item')
        with self.assertRaisesRegex(ValueError, 'bad item'):
            extras.group_by([1], key=key)

    def test_key_is_required(self):
        with self.assertRaises(TypeError):
            extras.group_by([1])


class DeepGetTests(unittest.TestCase):
    data = {'user': {'name': 'Sid', 'pets': ['Rex', 'Tom']}, 'empty': None}

    def test_nested(self):
        self.assertEqual(extras.deep_get(self.data, 'user', 'name'), 'Sid')

    def test_list_index(self):
        self.assertEqual(extras.deep_get(self.data, 'user', 'pets', 1), 'Tom')

    def test_no_keys_returns_data(self):
        self.assertIs(extras.deep_get(self.data), self.data)

    def test_missing_gives_default(self):
        self.assertIsNone(extras.deep_get(self.data, 'nope'))
        self.assertEqual(extras.deep_get(self.data, 'user', 'age', default=0),
                         0)

    def test_index_out_of_range(self):
        self.assertEqual(
            extras.deep_get(self.data, 'user', 'pets', 9, default='x'), 'x')

    def test_going_past_a_plain_value(self):
        self.assertEqual(
            extras.deep_get(self.data, 'empty', 'more', default='x'), 'x')
        self.assertEqual(
            extras.deep_get(self.data, 'user', 'pets', 'a', default='x'), 'x')

    def test_none_value_is_not_replaced_by_default(self):
        self.assertIsNone(extras.deep_get(self.data, 'empty', default='x'))


class HumanSizeTests(unittest.TestCase):
    def test_bytes(self):
        self.assertEqual(extras.human_size(0), '0 B')
        self.assertEqual(extras.human_size(1), '1 B')
        self.assertEqual(extras.human_size(999), '999 B')

    def test_decimal_units(self):
        self.assertEqual(extras.human_size(1000), '1.0 KB')
        self.assertEqual(extras.human_size(1_536_000), '1.5 MB')
        self.assertEqual(extras.human_size(2 * 10**9), '2.0 GB')
        self.assertEqual(extras.human_size(3 * 10**12), '3.0 TB')
        self.assertEqual(extras.human_size(4 * 10**15), '4.0 PB')

    def test_largest_unit_is_kept(self):
        self.assertEqual(extras.human_size(5 * 10**18), '5000.0 PB')

    def test_binary_units(self):
        self.assertEqual(extras.human_size(1023, binary=True), '1023 B')
        self.assertEqual(extras.human_size(1024, binary=True), '1.0 KiB')
        self.assertEqual(extras.human_size(1536 * 1024, binary=True),
                         '1.5 MiB')

    def test_rounding_moves_up_a_unit(self):
        self.assertEqual(extras.human_size(999_999), '1.0 MB')
        self.assertEqual(extras.human_size(1024**2 - 1, binary=True),
                         '1.0 MiB')

    def test_negative(self):
        self.assertEqual(extras.human_size(-1500), '-1.5 KB')
        self.assertEqual(extras.human_size(-5), '-5 B')

    def test_not_a_number(self):
        with self.assertRaises(TypeError):
            extras.human_size('10')


class SlugifyTests(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(extras.slugify('Hello World!'), 'hello-world')

    def test_runs_collapse(self):
        self.assertEqual(extras.slugify('  a -- b__c  '), 'a-b-c')

    def test_accents_are_removed(self):
        self.assertEqual(extras.slugify('Café Crème'), 'cafe-creme')

    def test_digits_kept(self):
        self.assertEqual(extras.slugify('Python 3.14'), 'python-3-14')

    def test_nothing_usable(self):
        self.assertEqual(extras.slugify(''), '')
        self.assertEqual(extras.slugify('!!!'), '')
        self.assertEqual(extras.slugify('日本語'), '')


class TimerTests(unittest.TestCase):
    def run_timer(self, *args, **kwargs):
        output = io.StringIO()
        with (mock.patch('time.perf_counter', side_effect=[10.0, 11.5]),
              contextlib.redirect_stdout(output)):
            with extras.timer(*args, **kwargs) as t:
                pass
        return t, output.getvalue()

    def test_prints_elapsed(self):
        t, output = self.run_timer()
        self.assertEqual(t.elapsed, 1.5)
        self.assertEqual(output, 'Elapsed: 1.500 seconds\n')

    def test_label(self):
        _, output = self.run_timer('Loading')
        self.assertEqual(output, 'Loading: 1.500 seconds\n')

    def test_show_false_prints_nothing(self):
        t, output = self.run_timer(show=False)
        self.assertEqual(t.elapsed, 1.5)
        self.assertEqual(output, '')

    def test_elapsed_is_none_until_finished(self):
        with extras.timer(show=False) as t:
            self.assertIsNone(t.elapsed)
        self.assertGreaterEqual(t.elapsed, 0)

    def test_exception_is_not_swallowed(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            with self.assertRaises(ZeroDivisionError):
                with extras.timer('Broken'):
                    1 / 0
        self.assertIn('Broken:', output.getvalue())


class ModuleTests(unittest.TestCase):
    def test_listed_as_standard_library(self):
        self.assertIn('extras', sys.stdlib_module_names)


if __name__ == '__main__':
    unittest.main()
