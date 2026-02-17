"""
Test Suite for LeetCode Problems
==================================

Ejecuta: pytest test_leetcode.py -v

Tests completos con casos normales, edge cases, y casos de error.
"""

import pytest
from leetcode_runnable import (
    two_sum,
    is_palindrome,
    reverse_list,
    climb_stairs,
    majority_element,
    intersect,
    single_number,
    move_zeroes,
    roman_to_int,
    binary_search,
    group_anagrams,
    length_of_longest_substring,
    list_to_linked_list,
    linked_list_to_list,
)


# ============================================================================
# TEST 1: TWO SUM
# ============================================================================

class TestTwoSum:
    """Tests para Two Sum."""

    def test_normal_case(self):
        """Caso normal con solución."""
        assert two_sum([2, 7, 11, 15], 9) == [0, 1]

    def test_different_order(self):
        """Solución no está al principio."""
        assert two_sum([3, 2, 4], 6) == [1, 2]

    def test_duplicates(self):
        """Array con duplicados."""
        assert two_sum([3, 3], 6) == [0, 1]

    def test_no_solution(self):
        """No hay solución."""
        assert two_sum([1, 2], 10) is None

    def test_empty_array(self):
        """Array vacío."""
        assert two_sum([], 0) is None

    def test_single_element(self):
        """Solo un elemento."""
        assert two_sum([1], 5) is None

    def test_negative_numbers(self):
        """Números negativos."""
        assert two_sum([-1, -2, -3, -4, -5], -8) == [2, 4]


# ============================================================================
# TEST 2: VALID PALINDROME
# ============================================================================

class TestValidPalindrome:
    """Tests para Valid Palindrome."""

    def test_normal_palindrome(self):
        """Palíndromo normal con puntuación."""
        assert is_palindrome("A man, a plan, a canal: Panama") == True

    def test_not_palindrome(self):
        """No es palíndromo."""
        assert is_palindrome("race a car") == False

    def test_empty_string(self):
        """String vacío."""
        assert is_palindrome("") == True

    def test_single_char(self):
        """Un solo carácter."""
        assert is_palindrome("a") == True

    def test_only_spaces(self):
        """Solo espacios."""
        assert is_palindrome("   ") == True

    def test_only_non_alphanumeric(self):
        """Solo caracteres no alfanuméricos."""
        assert is_palindrome("!!!") == True

    def test_mixed_case(self):
        """Mayúsculas y minúsculas mezcladas."""
        assert is_palindrome("Aa") == True


# ============================================================================
# TEST 3: REVERSE LINKED LIST
# ============================================================================

class TestReverseLinkedList:
    """Tests para Reverse Linked List."""

    def test_normal_list(self):
        """Lista normal."""
        head = list_to_linked_list([1, 2, 3, 4, 5])
        reversed_head = reverse_list(head)
        assert linked_list_to_list(reversed_head) == [5, 4, 3, 2, 1]

    def test_single_node(self):
        """Un solo nodo."""
        head = list_to_linked_list([1])
        reversed_head = reverse_list(head)
        assert linked_list_to_list(reversed_head) == [1]

    def test_empty_list(self):
        """Lista vacía."""
        head = list_to_linked_list([])
        reversed_head = reverse_list(head)
        assert linked_list_to_list(reversed_head) == []

    def test_two_nodes(self):
        """Dos nodos."""
        head = list_to_linked_list([1, 2])
        reversed_head = reverse_list(head)
        assert linked_list_to_list(reversed_head) == [2, 1]


# ============================================================================
# TEST 4: CLIMBING STAIRS
# ============================================================================

class TestClimbingStairs:
    """Tests para Climbing Stairs."""

    def test_base_cases(self):
        """Casos base."""
        assert climb_stairs(1) == 1
        assert climb_stairs(2) == 2

    def test_small_values(self):
        """Valores pequeños."""
        assert climb_stairs(3) == 3
        assert climb_stairs(4) == 5
        assert climb_stairs(5) == 8

    def test_larger_value(self):
        """Valor más grande."""
        assert climb_stairs(10) == 89

    def test_fibonacci_sequence(self):
        """Verifica que sigue Fibonacci."""
        assert climb_stairs(6) == 13
        assert climb_stairs(7) == 21


# ============================================================================
# TEST 5: MAJORITY ELEMENT
# ============================================================================

class TestMajorityElement:
    """Tests para Majority Element."""

    def test_simple_case(self):
        """Caso simple."""
        assert majority_element([3, 2, 3]) == 3

    def test_longer_array(self):
        """Array más largo."""
        assert majority_element([2, 2, 1, 1, 1, 2, 2]) == 2

    def test_single_element(self):
        """Un solo elemento."""
        assert majority_element([1]) == 1

    def test_all_same(self):
        """Todos iguales."""
        assert majority_element([5, 5, 5, 5]) == 5

    def test_majority_at_end(self):
        """Mayoría al final."""
        assert majority_element([1, 2, 3, 3, 3, 3, 3]) == 3


# ============================================================================
# TEST 6: INTERSECTION OF TWO ARRAYS II
# ============================================================================

class TestIntersection:
    """Tests para Intersection of Two Arrays II."""

    def test_normal_case(self):
        """Caso normal."""
        result = intersect([1, 2, 2, 1], [2, 2])
        assert sorted(result) == [2, 2]

    def test_different_sizes(self):
        """Arrays de diferente tamaño."""
        result = intersect([4, 9, 5], [9, 4, 9, 8, 4])
        assert sorted(result) == [4, 9]

    def test_no_intersection(self):
        """Sin intersección."""
        result = intersect([1, 2], [3, 4])
        assert result == []

    def test_empty_arrays(self):
        """Arrays vacíos."""
        assert intersect([], []) == []
        assert intersect([1], []) == []
        assert intersect([], [1]) == []

    def test_all_same(self):
        """Todos los elementos son iguales."""
        result = intersect([1, 1, 1], [1, 1])
        assert sorted(result) == [1, 1]


# ============================================================================
# TEST 7: SINGLE NUMBER
# ============================================================================

class TestSingleNumber:
    """Tests para Single Number."""

    def test_simple_case(self):
        """Caso simple."""
        assert single_number([2, 2, 1]) == 1

    def test_longer_array(self):
        """Array más largo."""
        assert single_number([4, 1, 2, 1, 2]) == 4

    def test_single_element(self):
        """Un solo elemento."""
        assert single_number([1]) == 1

    def test_negative_numbers(self):
        """Números negativos."""
        assert single_number([-1, -1, -2]) == -2


# ============================================================================
# TEST 8: MOVE ZEROES
# ============================================================================

class TestMoveZeroes:
    """Tests para Move Zeroes."""

    def test_normal_case(self):
        """Caso normal."""
        nums = [0, 1, 0, 3, 12]
        move_zeroes(nums)
        assert nums == [1, 3, 12, 0, 0]

    def test_single_zero(self):
        """Un solo cero."""
        nums = [0]
        move_zeroes(nums)
        assert nums == [0]

    def test_no_zeroes(self):
        """Sin ceros."""
        nums = [1, 2, 3]
        move_zeroes(nums)
        assert nums == [1, 2, 3]

    def test_all_zeroes(self):
        """Todos ceros."""
        nums = [0, 0, 0]
        move_zeroes(nums)
        assert nums == [0, 0, 0]

    def test_zeroes_at_end(self):
        """Ceros ya al final."""
        nums = [1, 2, 0, 0]
        move_zeroes(nums)
        assert nums == [1, 2, 0, 0]


# ============================================================================
# TEST 9: ROMAN TO INTEGER
# ============================================================================

class TestRomanToInt:
    """Tests para Roman to Integer."""

    def test_simple_cases(self):
        """Casos simples."""
        assert roman_to_int("III") == 3
        assert roman_to_int("IV") == 4
        assert roman_to_int("IX") == 9

    def test_normal_cases(self):
        """Casos normales."""
        assert roman_to_int("LVIII") == 58
        assert roman_to_int("MCMXCIV") == 1994

    def test_single_characters(self):
        """Caracteres individuales."""
        assert roman_to_int("I") == 1
        assert roman_to_int("V") == 5
        assert roman_to_int("X") == 10
        assert roman_to_int("L") == 50
        assert roman_to_int("C") == 100
        assert roman_to_int("D") == 500
        assert roman_to_int("M") == 1000

    def test_subtractive_cases(self):
        """Casos con resta."""
        assert roman_to_int("CM") == 900
        assert roman_to_int("CD") == 400
        assert roman_to_int("XC") == 90
        assert roman_to_int("XL") == 40


# ============================================================================
# TEST 10: BINARY SEARCH
# ============================================================================

class TestBinarySearch:
    """Tests para Binary Search."""

    def test_found_middle(self):
        """Elemento en el medio."""
        assert binary_search([-1, 0, 3, 5, 9, 12], 9) == 4

    def test_not_found(self):
        """Elemento no existe."""
        assert binary_search([-1, 0, 3, 5, 9, 12], 2) == -1

    def test_single_element_found(self):
        """Un elemento, encontrado."""
        assert binary_search([5], 5) == 0

    def test_single_element_not_found(self):
        """Un elemento, no encontrado."""
        assert binary_search([5], 3) == -1

    def test_empty_array(self):
        """Array vacío."""
        assert binary_search([], 1) == -1

    def test_first_element(self):
        """Primer elemento."""
        assert binary_search([1, 2, 3, 4, 5], 1) == 0

    def test_last_element(self):
        """Último elemento."""
        assert binary_search([1, 2, 3, 4, 5], 5) == 4


# ============================================================================
# TEST 11: GROUP ANAGRAMS
# ============================================================================

class TestGroupAnagrams:
    """Tests para Group Anagrams."""

    def test_normal_case(self):
        """Caso normal."""
        result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        # Convertimos a sets para comparar sin importar orden
        result_sets = [set(group) for group in result]
        expected_sets = [{"eat", "tea", "ate"}, {"tan", "nat"}, {"bat"}]
        assert len(result_sets) == len(expected_sets)
        for expected_set in expected_sets:
            assert expected_set in result_sets

    def test_empty_string(self):
        """String vacío."""
        result = group_anagrams([""])
        assert result == [[""]]

    def test_single_string(self):
        """Un solo string."""
        result = group_anagrams(["a"])
        assert result == [["a"]]

    def test_no_anagrams(self):
        """Sin anagramas."""
        result = group_anagrams(["abc", "def", "ghi"])
        assert len(result) == 3

    def test_all_anagrams(self):
        """Todos son anagramas."""
        result = group_anagrams(["abc", "bca", "cab"])
        assert len(result) == 1
        assert set(result[0]) == {"abc", "bca", "cab"}


# ============================================================================
# TEST 12: LONGEST SUBSTRING WITHOUT REPEATING CHARACTERS
# ============================================================================

class TestLongestSubstring:
    """Tests para Longest Substring Without Repeating Characters."""

    def test_normal_cases(self):
        """Casos normales."""
        assert length_of_longest_substring("abcabcbb") == 3  # "abc"
        assert length_of_longest_substring("bbbbb") == 1     # "b"
        assert length_of_longest_substring("pwwkew") == 3    # "wke"

    def test_empty_string(self):
        """String vacío."""
        assert length_of_longest_substring("") == 0

    def test_single_char(self):
        """Un solo carácter."""
        assert length_of_longest_substring("a") == 1
        assert length_of_longest_substring(" ") == 1

    def test_all_unique(self):
        """Todos únicos."""
        assert length_of_longest_substring("abcdef") == 6

    def test_two_chars(self):
        """Dos caracteres."""
        assert length_of_longest_substring("au") == 2

    def test_special_characters(self):
        """Caracteres especiales."""
        assert length_of_longest_substring("a!b@c#") == 6


# ============================================================================
# TEST DE PERFORMANCE
# ============================================================================

class TestPerformance:
    """Tests de performance para verificar escalabilidad."""

    def test_two_sum_large(self):
        """Two sum con array grande."""
        nums = list(range(10000))
        result = two_sum(nums, 19997)
        assert result == [9998, 9999]

    def test_binary_search_large(self):
        """Binary search con array grande."""
        nums = list(range(100000))
        assert binary_search(nums, 50000) == 50000

    def test_group_anagrams_many(self):
        """Group anagrams con muchas palabras."""
        words = ["abc"] * 100 + ["def"] * 100
        result = group_anagrams(words)
        assert len(result) == 2

    def test_longest_substring_long(self):
        """Longest substring con string largo."""
        s = "abcdefghijk" * 100
        assert length_of_longest_substring(s) == 11
