"""
LeetCode Problems - Runnable Solutions
========================================

Todos los 12 problemas en código ejecutable con tests.

Ejecuta: python leetcode_runnable.py

Autor: Python Extra Class
"""

from typing import List, Optional


# ============================================================================
# HELPER CLASSES Y FUNCIONES
# ============================================================================

class ListNode:
    """Nodo de lista enlazada simple."""
    def __init__(self, val: int = 0, next: Optional['ListNode'] = None):
        self.val = val
        self.next = next


def list_to_linked_list(arr: List[int]) -> Optional[ListNode]:
    """Convierte lista Python a lista enlazada."""
    if not arr:
        return None
    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head


def linked_list_to_list(head: Optional[ListNode]) -> List[int]:
    """Convierte lista enlazada a lista Python."""
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result


# ============================================================================
# BÁSICO 1: TWO SUM
# ============================================================================

def two_sum(nums: List[int], target: int) -> Optional[List[int]]:
    """
    Encuentra dos números que sumen el target.

    Invariante: seen contiene todos los números vistos hasta ahora con sus índices.

    Complejidad: O(n) tiempo, O(n) espacio

    Args:
        nums: Lista de enteros
        target: Suma objetivo

    Returns:
        Lista con dos índices [i, j] o None si no hay solución
    """
    seen = {}
    for i, n in enumerate(nums):
        need = target - n
        if need in seen:
            return [seen[need], i]
        seen[n] = i
    return None


# ============================================================================
# BÁSICO 2: VALID PALINDROME
# ============================================================================

def is_palindrome(s: str) -> bool:
    """
    Verifica si un string es palíndromo (ignorando mayúsculas y no-alfanuméricos).

    Invariante: i <= j, y todos los caracteres comparados hasta ahora coinciden.

    Complejidad: O(n) tiempo, O(1) espacio

    Args:
        s: String a verificar

    Returns:
        True si es palíndromo, False en caso contrario
    """
    i, j = 0, len(s) - 1
    while i < j:
        while i < j and not s[i].isalnum():
            i += 1
        while i < j and not s[j].isalnum():
            j -= 1
        if s[i].lower() != s[j].lower():
            return False
        i += 1
        j -= 1
    return True


# ============================================================================
# BÁSICO 3: REVERSE LINKED LIST
# ============================================================================

def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Invierte una lista enlazada.

    Invariante: prev contiene la lista revertida hasta ahora.

    Complejidad: O(n) tiempo, O(1) espacio

    Args:
        head: Cabeza de la lista enlazada

    Returns:
        Nueva cabeza de la lista invertida
    """
    prev = None
    cur = head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev


# ============================================================================
# BÁSICO 4: CLIMBING STAIRS
# ============================================================================

def climb_stairs(n: int) -> int:
    """
    Cuenta formas de subir n escalones (1 o 2 pasos a la vez).

    Invariante: a y b representan ways[i-2] y ways[i-1].

    Complejidad: O(n) tiempo, O(1) espacio

    Args:
        n: Número de escalones

    Returns:
        Número de formas distintas de subir
    """
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


# ============================================================================
# BÁSICO 5: MAJORITY ELEMENT
# ============================================================================

def majority_element(nums: List[int]) -> Optional[int]:
    """
    Encuentra el elemento que aparece más de n/2 veces (Boyer-Moore).

    Invariante: cand es el candidato mayoritario del subarray procesado.

    Complejidad: O(n) tiempo, O(1) espacio

    Args:
        nums: Lista de enteros (se garantiza que existe elemento mayoritario)

    Returns:
        El elemento mayoritario
    """
    cand = None
    count = 0
    for n in nums:
        if count == 0:
            cand = n
        count += 1 if n == cand else -1
    return cand


# ============================================================================
# BÁSICO 6: INTERSECTION OF TWO ARRAYS II
# ============================================================================

def intersect(nums1: List[int], nums2: List[int]) -> List[int]:
    """
    Encuentra la intersección de dos arrays con conteo de duplicados.

    Invariante: counts refleja cuántas veces cada número está disponible.

    Complejidad: O(n+m) tiempo, O(n) espacio

    Args:
        nums1: Primer array
        nums2: Segundo array

    Returns:
        Array con la intersección
    """
    counts = {}
    for n in nums1:
        counts[n] = counts.get(n, 0) + 1
    out = []
    for n in nums2:
        if counts.get(n, 0) > 0:
            out.append(n)
            counts[n] -= 1
    return out


# ============================================================================
# BÁSICO 7: SINGLE NUMBER
# ============================================================================

def single_number(nums: List[int]) -> int:
    """
    Encuentra el número que aparece una sola vez (XOR).

    Invariante: x ^ a ^ a = x (los pares se cancelan).

    Complejidad: O(n) tiempo, O(1) espacio

    Args:
        nums: Lista donde todos aparecen dos veces excepto uno

    Returns:
        El número único
    """
    x = 0
    for n in nums:
        x ^= n
    return x


# ============================================================================
# BÁSICO 8: MOVE ZEROES
# ============================================================================

def move_zeroes(nums: List[int]) -> None:
    """
    Mueve todos los ceros al final (in-place).

    Invariante: nums[0:k] contiene todos los no-ceros en orden.

    Complejidad: O(n) tiempo, O(1) espacio

    Args:
        nums: Lista a modificar (modifica in-place)
    """
    k = 0
    for n in nums:
        if n != 0:
            nums[k] = n
            k += 1
    for i in range(k, len(nums)):
        nums[i] = 0


# ============================================================================
# BÁSICO 9: ROMAN TO INTEGER
# ============================================================================

def roman_to_int(s: str) -> int:
    """
    Convierte número romano a entero.

    Invariante: Si val[i] < val[i+1], entonces restamos; si no, sumamos.

    Complejidad: O(n) tiempo, O(1) espacio

    Args:
        s: String con número romano

    Returns:
        Valor entero
    """
    val = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    for i in range(len(s)):
        if i + 1 < len(s) and val[s[i]] < val[s[i + 1]]:
            total -= val[s[i]]
        else:
            total += val[s[i]]
    return total


# ============================================================================
# BÁSICO 10: BINARY SEARCH
# ============================================================================

def binary_search(nums: List[int], target: int) -> int:
    """
    Busca un valor en array ordenado.

    Invariante: Si target está en nums, está en nums[lo:hi+1].

    Complejidad: O(log n) tiempo, O(1) espacio

    Args:
        nums: Array ordenado
        target: Valor a buscar

    Returns:
        Índice del valor o -1 si no existe
    """
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


# ============================================================================
# INTERMEDIO 1: GROUP ANAGRAMS
# ============================================================================

def group_anagrams(strs: List[str]) -> List[List[str]]:
    """
    Agrupa palabras que son anagramas.

    Invariante: Anagramas tienen la misma firma (conteo de letras).

    Complejidad: O(n * k) tiempo, O(n * k) espacio (k = longitud promedio)

    Args:
        strs: Lista de strings

    Returns:
        Lista de grupos de anagramas
    """
    groups = {}
    for s in strs:
        count = [0] * 26
        for ch in s:
            count[ord(ch) - ord('a')] += 1
        key = tuple(count)
        groups.setdefault(key, []).append(s)
    return list(groups.values())


# ============================================================================
# INTERMEDIO 2: LONGEST SUBSTRING WITHOUT REPEATING CHARACTERS
# ============================================================================

def length_of_longest_substring(s: str) -> int:
    """
    Longitud máxima de substring sin caracteres repetidos.

    Invariante: s[left:right+1] no tiene caracteres repetidos.

    Complejidad: O(n) tiempo, O(min(n, alfabeto)) espacio

    Args:
        s: String de entrada

    Returns:
        Longitud máxima
    """
    last = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best


# ============================================================================
# TESTS Y EJEMPLOS
# ============================================================================

def run_tests():
    """Ejecuta todos los tests con output visible."""
    print("=" * 70)
    print("LEETCODE RUNNABLE - TESTS")
    print("=" * 70)

    # Test 1: Two Sum
    print("\n[1] Two Sum")
    assert two_sum([2, 7, 11, 15], 9) == [0, 1], "Caso normal"
    assert two_sum([3, 2, 4], 6) == [1, 2], "Orden diferente"
    assert two_sum([3, 3], 6) == [0, 1], "Duplicados"
    assert two_sum([1, 2], 10) is None, "Sin solución"
    print("[OK] Todos los casos pasaron")

    # Test 2: Valid Palindrome
    print("\n[2] Valid Palindrome")
    assert is_palindrome("A man, a plan, a canal: Panama") == True
    assert is_palindrome("race a car") == False
    assert is_palindrome(" ") == True
    assert is_palindrome("a") == True
    print("[OK] Todos los casos pasaron")

    # Test 3: Reverse Linked List
    print("\n[3] Reverse Linked List")
    head = list_to_linked_list([1, 2, 3, 4, 5])
    reversed_head = reverse_list(head)
    assert linked_list_to_list(reversed_head) == [5, 4, 3, 2, 1]

    head = list_to_linked_list([1])
    reversed_head = reverse_list(head)
    assert linked_list_to_list(reversed_head) == [1]

    head = list_to_linked_list([])
    reversed_head = reverse_list(head)
    assert linked_list_to_list(reversed_head) == []
    print("[OK] Todos los casos pasaron")

    # Test 4: Climbing Stairs
    print("\n[4] Climbing Stairs")
    assert climb_stairs(2) == 2
    assert climb_stairs(3) == 3
    assert climb_stairs(4) == 5
    assert climb_stairs(5) == 8
    print("[OK] Todos los casos pasaron")

    # Test 5: Majority Element
    print("\n[5] Majority Element")
    assert majority_element([3, 2, 3]) == 3
    assert majority_element([2, 2, 1, 1, 1, 2, 2]) == 2
    assert majority_element([1]) == 1
    print("[OK] Todos los casos pasaron")

    # Test 6: Intersection of Two Arrays II
    print("\n[6] Intersection of Two Arrays II")
    result = intersect([1, 2, 2, 1], [2, 2])
    assert sorted(result) == [2, 2]

    result = intersect([4, 9, 5], [9, 4, 9, 8, 4])
    assert sorted(result) == [4, 9]

    result = intersect([1, 2], [3, 4])
    assert result == []
    print("[OK] Todos los casos pasaron")

    # Test 7: Single Number
    print("\n[7] Single Number")
    assert single_number([2, 2, 1]) == 1
    assert single_number([4, 1, 2, 1, 2]) == 4
    assert single_number([1]) == 1
    print("[OK] Todos los casos pasaron")

    # Test 8: Move Zeroes
    print("\n[8] Move Zeroes")
    nums = [0, 1, 0, 3, 12]
    move_zeroes(nums)
    assert nums == [1, 3, 12, 0, 0]

    nums = [0]
    move_zeroes(nums)
    assert nums == [0]

    nums = [1, 2, 3]
    move_zeroes(nums)
    assert nums == [1, 2, 3]
    print("[OK] Todos los casos pasaron")

    # Test 9: Roman to Integer
    print("\n[9] Roman to Integer")
    assert roman_to_int("III") == 3
    assert roman_to_int("LVIII") == 58
    assert roman_to_int("MCMXCIV") == 1994
    assert roman_to_int("IV") == 4
    assert roman_to_int("IX") == 9
    print("[OK] Todos los casos pasaron")

    # Test 10: Binary Search
    print("\n[10] Binary Search")
    assert binary_search([-1, 0, 3, 5, 9, 12], 9) == 4
    assert binary_search([-1, 0, 3, 5, 9, 12], 2) == -1
    assert binary_search([5], 5) == 0
    assert binary_search([], 1) == -1
    print("[OK] Todos los casos pasaron")

    # Test 11: Group Anagrams
    print("\n[11] Group Anagrams")
    result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    # Ordenamos para comparar (el orden de grupos no importa)
    result_sorted = [sorted(group) for group in result]
    expected = [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
    expected_sorted = [sorted(group) for group in expected]
    assert sorted([str(x) for x in result_sorted]) == sorted([str(x) for x in expected_sorted])

    result = group_anagrams([""])
    assert result == [[""]]

    result = group_anagrams(["a"])
    assert result == [["a"]]
    print("[OK] Todos los casos pasaron")

    # Test 12: Longest Substring Without Repeating Characters
    print("\n[12] Longest Substring Without Repeating Characters")
    assert length_of_longest_substring("abcabcbb") == 3  # "abc"
    assert length_of_longest_substring("bbbbb") == 1     # "b"
    assert length_of_longest_substring("pwwkew") == 3    # "wke"
    assert length_of_longest_substring("") == 0
    assert length_of_longest_substring(" ") == 1
    print("[OK] Todos los casos pasaron")

    print("\n" + "=" * 70)
    print("[OK] TODOS LOS 12 PROBLEMAS PASARON")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()
