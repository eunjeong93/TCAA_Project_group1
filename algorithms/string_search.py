"""
string_search.py — TCAA Notes Search Engine
Implements Naive, Rabin-Karp, and KMP string-search algorithms from scratch.
All three return (list_of_match_start_indices, elapsed_ms).
No use of str.find(), str.index(), `in`, or re.search() inside any algorithm.
"""

import time
from typing import List, Tuple, Dict, Any

# ── Constants ──────────────────────────────────────────────────────────────────
RABIN_KARP_BASE  = 256            # number of characters in the input alphabet
RABIN_KARP_PRIME = 1_000_000_007  # large prime reduces hash collisions


# ── 1. Naive Search ────────────────────────────────────────────────────────────

def naive_search(text: str, pattern: str) -> Tuple[List[int], float]:
    """
    Naive (brute-force) substring search.

    Slides the pattern over the text one character at a time and compares
    every character of the pattern against the text window.

    Time complexity: O(n * m) worst case, where n = len(text), m = len(pattern).
    Space complexity: O(1) auxiliary.

    Args:
        text:    The document text to search within.
        pattern: The query string to find.

    Returns:
        A tuple of (match_indices, elapsed_ms) where match_indices is a list
        of start positions (0-based) of every occurrence found, and elapsed_ms
        is wall-clock time in milliseconds measured with time.perf_counter().
    """
    if not pattern or len(pattern) > len(text):
        return [], 0.0

    text    = text.lower()
    pattern = pattern.lower()

    n = len(text)
    m = len(pattern)
    matches: List[int] = []

    t_start = time.perf_counter()

    for i in range(n - m + 1):
        # Compare pattern against text window starting at i
        match = True
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            matches.append(i)

    elapsed_ms = (time.perf_counter() - t_start) * 1000.0
    return matches, elapsed_ms


# ── 2. Rabin-Karp Search ──────────────────────────────────────────────────────

def rabin_karp_search(text: str, pattern: str) -> Tuple[List[int], float]:
    """
    Rabin-Karp rolling-hash substring search.

    Computes a polynomial hash of the pattern and a rolling hash of each
    text window of the same length.  When hashes match, a character-by-character
    verification step confirms the match and avoids false positives (spurious hits).

    Hash formula: hash(s) = (s[0]*BASE^(m-1) + s[1]*BASE^(m-2) + ... + s[m-1]) % PRIME

    Rolling update (slide window by one to the right):
        new_hash = (BASE * (old_hash - text[i] * h) + text[i+m]) % PRIME
    where h = BASE^(m-1) % PRIME is precomputed once.

    Time complexity: O(n + m) average case; O(n * m) worst case (all hash collisions).
    Space complexity: O(1) auxiliary.

    Args:
        text:    The document text to search within.
        pattern: The query string to find.

    Returns:
        A tuple of (match_indices, elapsed_ms).
    """
    if not pattern or len(pattern) > len(text):
        return [], 0.0

    text    = text.lower()
    pattern = pattern.lower()

    n = len(text)
    m = len(pattern)
    matches: List[int] = []

    t_start = time.perf_counter()

    # Precompute h = BASE^(m-1) % PRIME — the value of the highest-order term
    h = 1
    for _ in range(m - 1):
        h = (h * RABIN_KARP_BASE) % RABIN_KARP_PRIME

    # Compute initial hash of pattern and first text window
    pattern_hash = 0
    window_hash  = 0
    for i in range(m):
        pattern_hash = (RABIN_KARP_BASE * pattern_hash + ord(pattern[i])) % RABIN_KARP_PRIME
        window_hash  = (RABIN_KARP_BASE * window_hash  + ord(text[i]))    % RABIN_KARP_PRIME

    for i in range(n - m + 1):
        if window_hash == pattern_hash:
            # Hash hit — verify character by character to rule out collision
            match = True
            for j in range(m):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                matches.append(i)

        # Roll the hash forward (don't compute for the last window)
        if i < n - m:
            # Remove leftmost character, add new rightmost character
            window_hash = (
                RABIN_KARP_BASE * (window_hash - ord(text[i]) * h) + ord(text[i + m])
            ) % RABIN_KARP_PRIME

            # Python's % can return negative values when the operand is negative,
            # so ensure the hash stays positive
            if window_hash < 0:
                window_hash += RABIN_KARP_PRIME

    elapsed_ms = (time.perf_counter() - t_start) * 1000.0
    return matches, elapsed_ms


# ── 3. KMP Search ─────────────────────────────────────────────────────────────

def compute_lps(pattern: str) -> List[int]:
    """
    Compute the Longest Proper Prefix which is also Suffix (LPS) array for KMP.

    lps[i] is the length of the longest proper prefix of pattern[0..i] that is
    also a suffix of pattern[0..i].  This lets KMP avoid re-examining characters
    that were already matched.

    Time complexity: O(m) where m = len(pattern).
    Space complexity: O(m).

    Args:
        pattern: The search pattern (already lowercased by the caller).

    Returns:
        The LPS array of the same length as pattern.
    """
    m   = len(pattern)
    lps = [0] * m

    length = 0   # length of the previous longest prefix-suffix
    i      = 1   # lps[0] is always 0, start from index 1

    while i < m:
        if pattern[i] == pattern[length]:
            # Characters match — extend the current prefix-suffix
            length += 1
            lps[i]  = length
            i += 1
        else:
            if length != 0:
                # Fall back: try a shorter prefix-suffix using the LPS itself
                # (do NOT increment i here — re-examine position i with new length)
                length = lps[length - 1]
            else:
                # No prefix-suffix of any length matches; lps[i] stays 0
                lps[i] = 0
                i += 1

    return lps


def kmp_search(text: str, pattern: str) -> Tuple[List[int], float]:
    """
    Knuth-Morris-Pratt (KMP) substring search.

    Uses the precomputed LPS array to skip unnecessary comparisons.
    When a mismatch occurs after some matches, the LPS array tells us
    the longest prefix of the pattern that still matches the current
    text suffix, so we restart from there instead of the beginning.

    Time complexity: O(n + m) — O(m) to build LPS, O(n) to scan text.
    Space complexity: O(m) for the LPS array.

    Args:
        text:    The document text to search within.
        pattern: The query string to find.

    Returns:
        A tuple of (match_indices, elapsed_ms).
    """
    if not pattern or len(pattern) > len(text):
        return [], 0.0

    text    = text.lower()
    pattern = pattern.lower()

    n = len(text)
    m = len(pattern)
    matches: List[int] = []

    t_start = time.perf_counter()

    lps = compute_lps(pattern)

    i = 0  # index into text
    j = 0  # index into pattern

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1

        if j == m:
            # Full pattern matched; record start index
            matches.append(i - j)
            # Use LPS to find the next potential match position
            j = lps[j - 1]
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                # Skip ahead using LPS — j falls back, i stays
                j = lps[j - 1]
            else:
                # No partial match at all; advance in text
                i += 1

    elapsed_ms = (time.perf_counter() - t_start) * 1000.0
    return matches, elapsed_ms


# ── 4. Compare All ────────────────────────────────────────────────────────────

def compare_all(text: str, pattern: str) -> Dict[str, Any]:
    """
    Run all three search algorithms on the same (text, pattern) pair.

    Returns a dict keyed by algorithm name, each value containing:
        - "matches"  : list of start indices (ints)
        - "time_ms"  : elapsed time in milliseconds (float)
        - "count"    : number of matches found (int)

    Args:
        text:    The document text to search within.
        pattern: The query string to find.

    Returns:
        {
            "Naive":      {"matches": [...], "time_ms": float, "count": int},
            "Rabin-Karp": {"matches": [...], "time_ms": float, "count": int},
            "KMP":        {"matches": [...], "time_ms": float, "count": int},
        }
    """
    naive_matches, naive_ms = naive_search(text, pattern)
    rk_matches,    rk_ms    = rabin_karp_search(text, pattern)
    kmp_matches,   kmp_ms   = kmp_search(text, pattern)

    return {
        "Naive": {
            "matches": naive_matches,
            "time_ms": naive_ms,
            "count":   len(naive_matches),
        },
        "Rabin-Karp": {
            "matches": rk_matches,
            "time_ms": rk_ms,
            "count":   len(rk_matches),
        },
        "KMP": {
            "matches": kmp_matches,
            "time_ms": kmp_ms,
            "count":   len(kmp_matches),
        },
    }


# ── Self-tests ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    PASS = "\033[92mPASS\033[0m"
    FAIL = "\033[91mFAIL\033[0m"
    all_passed = True

    def check(label: str, got, expected):
        global all_passed
        ok = got == expected
        if not ok:
            all_passed = False
        status = PASS if ok else FAIL
        print(f"  [{status}] {label}")
        if not ok:
            print(f"         expected: {expected}")
            print(f"         got:      {got}")

    def run_all(text, pattern):
        """Return (naive_indices, rk_indices, kmp_indices)."""
        ni, _ = naive_search(text, pattern)
        ri, _ = rabin_karp_search(text, pattern)
        ki, _ = kmp_search(text, pattern)
        return ni, ri, ki

    print("\n=== string_search.py self-tests ===\n")

    # ── Test 1: agreement on "ababd" in "ababcabcabababd" ─────────────────────
    # Expected: single match at index 10
    print("Test 1 — 'ababd' in 'ababcabcabababd'")
    text1, pat1 = "ababcabcabababd", "ababd"
    n1, r1, k1 = run_all(text1, pat1)
    check("Naive result",      n1, [10])
    check("Rabin-Karp result", r1, [10])
    check("KMP result",        k1, [10])
    check("All three agree",   n1 == r1 == k1, True)

    # ── Test 2: multiple matches ───────────────────────────────────────────────
    print("\nTest 2 — multiple matches ('ab' in 'ababab')")
    text2, pat2 = "ababab", "ab"
    n2, r2, k2 = run_all(text2, pat2)
    check("Naive result",      n2, [0, 2, 4])
    check("Rabin-Karp result", r2, [0, 2, 4])
    check("KMP result",        k2, [0, 2, 4])
    check("All three agree",   n2 == r2 == k2, True)

    # ── Test 3: empty pattern ──────────────────────────────────────────────────
    print("\nTest 3 — empty pattern")
    n3, t3 = naive_search("hello world", "")
    check("Naive empty pattern → []",     n3, [])
    check("Naive empty pattern → 0.0 ms", t3, 0.0)
    r3, _  = rabin_karp_search("hello world", "")
    check("RK empty pattern → []",        r3, [])
    k3, _  = kmp_search("hello world", "")
    check("KMP empty pattern → []",       k3, [])

    # ── Test 4: pattern longer than text ──────────────────────────────────────
    print("\nTest 4 — pattern longer than text")
    n4, _ = naive_search("hi", "hello world")
    r4, _ = rabin_karp_search("hi", "hello world")
    k4, _ = kmp_search("hi", "hello world")
    check("Naive → []", n4, [])
    check("RK → []",    r4, [])
    check("KMP → []",   k4, [])

    # ── Test 5: pattern not found ──────────────────────────────────────────────
    print("\nTest 5 — pattern not in text")
    n5, r5, k5 = run_all("abcdef", "xyz")
    check("Naive → []", n5, [])
    check("RK → []",    r5, [])
    check("KMP → []",   k5, [])

    # ── Test 6: match at the very start ───────────────────────────────────────
    print("\nTest 6 — match at start")
    n6, r6, k6 = run_all("helloworld", "hello")
    check("Naive → [0]", n6, [0])
    check("RK → [0]",    r6, [0])
    check("KMP → [0]",   k6, [0])

    # ── Test 7: match at the very end ─────────────────────────────────────────
    print("\nTest 7 — match at end")
    n7, r7, k7 = run_all("helloworld", "world")
    check("Naive → [5]", n7, [5])
    check("RK → [5]",    r7, [5])
    check("KMP → [5]",   k7, [5])

    # ── Test 8: case-insensitive ───────────────────────────────────────────────
    print("\nTest 8 — case-insensitive search")
    n8, r8, k8 = run_all("Hello World HELLO", "hello")
    check("Naive → [0, 12]", n8, [0, 12])
    check("RK → [0, 12]",    r8, [0, 12])
    check("KMP → [0, 12]",   k8, [0, 12])

    # ── Test 9: compare_all returns consistent dict ────────────────────────────
    print("\nTest 9 — compare_all dict structure & agreement")
    result = compare_all("ababcabcabababd", "ababd")
    check("All counts agree",
          result["Naive"]["count"] == result["Rabin-Karp"]["count"] == result["KMP"]["count"],
          True)
    check("All indices agree",
          result["Naive"]["matches"] == result["Rabin-Karp"]["matches"] == result["KMP"]["matches"],
          True)

    print("\n" + ("=" * 42))
    if all_passed:
        print("\033[92m All tests passed!\033[0m")
    else:
        print("\033[91m Some tests FAILED — check implementation.\033[0m")
        sys.exit(1)
