import pytest
from assignment3 import (
    insert,
    count_words,
    contains,
    height,
    count_from_prefix,
    get_suggestions,
)


# --------------------------------------------------------------------------
# Tests for count_words (PASS cases)
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "words, expected_count",
    [
        # Basic test from docstring
        (["test", "testing", "doc", "docs", "document", "documenting"], 6),
        # Empty trie
        ([], 0),
        # Single word
        (["hello"], 1),
        # Words with common prefixes
        (["app", "apple", "apples", "applet"], 4),
        # All words from example trie
        (["I", "an", "app", "apple", "apples", "applet", "or", "orange", "origin"], 9),
        # Words with overlapping paths
        (["two", "to", "too", "the", "they", "there"], 6),
        # Single character words
        (["a", "b", "c", "i"], 4),
        # Mix of short and long words
        (["a", "at", "ate", "b", "be", "bee", "been"], 7),
        # Duplicate insertions (should still count once)
        (["test", "test", "testing"], 2),
        # Long words
        (["documentation", "documenting", "documented"], 3),
    ],
)
def test_count_words_pass(words, expected_count):
    """Tests that count_words correctly counts words in trie."""
    data = {}
    for word in words:
        insert(data, word)
    assert count_words(data) == expected_count


@pytest.mark.parametrize(
    "words, not_expected",
    [
        # Should not count prefixes that aren't words
        (["testing", "test"], 3),  # Wrong - should be 2
        # Should not return 0 for non-empty trie
        (["hello", "world"], 0),
        # Should not overcount
        (["app", "apple"], 3),  # Wrong - should be 2
    ],
)
def test_count_words_fail(words, not_expected):
    """Tests that count_words does not produce incorrect results."""
    data = {}
    for word in words:
        insert(data, word)
    assert count_words(data) != not_expected


# --------------------------------------------------------------------------
# Tests for contains (PASS cases)
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "words, search_word, expected",
    [
        # Basic tests from docstring
        (["tree", "trie", "try", "trying"], "try", True),
        (["tree", "trie", "try", "trying"], "trying", True),
        (["tree", "trie", "try", "trying"], "the", False),
        # Prefix exists but not as word
        (["testing", "tester"], "test", False),
        # Word exists
        (["test", "testing"], "test", True),
        # Empty string in empty trie
        ([], "", False),
        # Empty string in non-empty trie
        (["hello"], "", False),
        # Single character
        (["a", "an", "and"], "a", True),
        # Word doesn't exist at all
        (["hello", "world"], "goodbye", False),
        # Longer word exists but searching for prefix
        (["document", "documentation"], "doc", False),
        # Complete overlap
        (["app", "apple", "application"], "app", True),
        (["app", "apple", "application"], "apple", True),
        (["app", "apple", "application"], "application", True),
        # Case sensitivity (lowercase only)
        (["hello"], "Hello", False),
        # Word exists multiple times (duplicate insert)
        (["test", "test"], "test", True),
    ],
)
def test_contains_pass(words, search_word, expected):
    """Tests that contains correctly identifies words in trie."""
    data = {}
    for word in words:
        insert(data, word)
    assert contains(data, search_word) == expected


@pytest.mark.parametrize(
    "words, search_word, not_expected",
    [
        # Should not find prefix that isn't marked as word
        (["testing"], "test", True),
        # Should not miss existing word
        (["hello", "world"], "hello", False),
        # Should not find non-existent word
        (["test"], "testing", True),
    ],
)
def test_contains_fail(words, search_word, not_expected):
    """Tests that contains does not produce incorrect results."""
    data = {}
    for word in words:
        insert(data, word)
    assert contains(data, search_word) != not_expected


# --------------------------------------------------------------------------
# Tests for height (PASS cases)
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "words, expected_height",
    [
        # Basic test from docstring
        (["test", "testing", "doc", "docs", "document", "documenting"], 11),
        # Empty trie
        ([], 0),
        # Single character word
        (["a"], 1),
        # Multiple words, same length
        (["cat", "dog", "bat"], 3),
        # Increasing lengths
        (["a", "at", "ate", "ated"], 4),
        # Very long word
        (["supercalifragilisticexpialidocious"], 34),
        # Mix of lengths
        (["i", "am", "the", "best", "coder"], 5),
        # All single character
        (["a", "b", "c", "d", "e"], 1),
        # Two character words
        (["at", "be", "to", "do"], 2),
        # From example trie
        (["I", "an", "app", "apple", "apples", "applet", "or", "orange", "origin"], 6),
        # Words with common long prefix
        (["programming", "programmer", "program"], 11),
    ],
)
def test_height_pass(words, expected_height):
    """Tests that height correctly finds longest word length."""
    data = {}
    for word in words:
        insert(data, word)
    assert height(data) == expected_height


@pytest.mark.parametrize(
    "words, not_expected",
    [
        # Should not return wrong length
        (["test", "testing"], 4),  # Wrong - should be 7
        # Should not return 0 for non-empty trie
        (["hello"], 0),
        # Should not return shortest word
        (["a", "testing"], 1),  # Wrong - should be 7
    ],
)
def test_height_fail(words, not_expected):
    """Tests that height does not produce incorrect results."""
    data = {}
    for word in words:
        insert(data, word)
    assert height(data) != not_expected


# --------------------------------------------------------------------------
# Tests for count_from_prefix (PASS cases)
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "words, prefix, expected_count",
    [
        # Basic test from docstring
        (
            [
                "python",
                "pro",
                "professionnal",
                "program",
                "programming",
                "programmer",
                "programmers",
            ],
            "pro",
            5,
        ),
        # No words with prefix
        (["hello", "world"], "test", 0),
        # Prefix is a word itself (shouldn't count itself)
        (["test", "testing", "tester"], "test", 2),
        # All words share prefix
        (
            ["app", "apple", "application", "apply"],
            "app",
            3,
        ),  # Doesn't count "app" itself
        # Single character prefix
        (["apple", "apricot", "application", "banana"], "a", 3),
        # Prefix with no extensions
        (["hello"], "hello", 0),
        # Empty prefix (counts all words except prefix itself)
        (["test", "hello"], "", 2),
        # Prefix doesn't exist at all
        (["hello", "world"], "xyz", 0),
        # Long prefix
        (["programming", "programmer", "program"], "progr", 3),
        # Prefix exists but no words extend it
        (["program"], "program", 0),
        # Multiple branches from prefix
        (["tree", "trie", "try", "trying", "tried"], "tr", 5),
        # Single letter words after prefix
        (["a", "at", "an"], "a", 2),
    ],
)
def test_count_from_prefix_pass(words, prefix, expected_count):
    """Tests that count_from_prefix correctly counts words with given prefix."""
    data = {}
    for word in words:
        insert(data, word)
    assert count_from_prefix(data, prefix) == expected_count


@pytest.mark.parametrize(
    "words, prefix, not_expected",
    [
        # Should not count the prefix itself
        (["test", "testing"], "test", 2),  # Wrong - should be 1
        # Should not return wrong count
        (
            ["app", "apple", "application"],
            "app",
            3,
        ),  # Wrong - should be 2 (not counting "app")
        # Should not count unrelated words
        (["test", "hello"], "test", 1),  # Wrong - should be 0
    ],
)
def test_count_from_prefix_fail(words, prefix, not_expected):
    """Tests that count_from_prefix does not produce incorrect results."""
    data = {}
    for word in words:
        insert(data, word)
    assert count_from_prefix(data, prefix) != not_expected


# --------------------------------------------------------------------------
# Tests for get_suggestions (PASS cases)
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "words, prefix, expected_suggestions",
    [
        # Basic test from docstring
        (
            [
                "python",
                "pro",
                "professionnal",
                "program",
                "programming",
                "programmer",
                "programmers",
            ],
            "progr",
            ["program", "programming", "programmer", "programmers"],
        ),
        # No suggestions
        (["hello", "world"], "test", []),
        # Prefix is a word (doesn't include itself)
        (["test", "testing", "tester"], "test", ["testing", "tester"]),
        # Single suggestion
        (["apple"], "app", ["apple"]),
        # Multiple suggestions
        (
            ["app", "apple", "application", "apply"],
            "app",
            ["apple", "application", "apply"],
        ),
        # Empty prefix (returns all words)
        (["test", "hello", "world"], "", ["test", "hello", "world"]),
        # Prefix doesn't exist
        (["hello", "world"], "xyz", []),
        # All single character extensions
        (["a", "at", "an", "as"], "a", ["at", "an", "as"]),
        # Nested prefixes
        (["tree", "trie", "try", "trying"], "tr", ["tree", "trie", "try", "trying"]),
        # Long words
        (
            ["documentation", "documenting", "documented"],
            "doc",
            ["documentation", "documenting", "documented"],
        ),
    ],
)
def test_get_suggestions_pass(words, prefix, expected_suggestions):
    """Tests that get_suggestions returns correct list of words."""
    data = {}
    for word in words:
        insert(data, word)
    result = get_suggestions(data, prefix)
    # Sort both lists for comparison (order may vary)
    assert sorted(result) == sorted(expected_suggestions)


@pytest.mark.parametrize(
    "words, prefix",
    [
        # Should not include prefix itself
        (["test", "testing"], "test"),
        # Should not include words without prefix
        (["apple", "banana"], "app"),
        # Should not be empty when suggestions exist
        (["testing", "tester"], "test"),
    ],
)
def test_get_suggestions_fail(words, prefix):
    """Tests that get_suggestions produces correct results."""
    data = {}
    for word in words:
        insert(data, word)
    result = get_suggestions(data, prefix)

    # Verify prefix itself is not in results if it's a word
    if contains(data, prefix):
        assert prefix not in result

    # Verify all results start with prefix
    for word in result:
        assert word.startswith(prefix)

    # Verify all results are actual words in trie
    for word in result:
        assert contains(data, word)


# --------------------------------------------------------------------------
# Edge case tests
# --------------------------------------------------------------------------


def test_empty_string_handling():
    """Tests handling of empty strings across all functions."""
    data = {}
    insert(data, "")  # Insert empty string

    # Empty string might be considered as "no word" or count as one word
    # Based on insert logic, empty string returns early, so shouldn't be counted
    assert count_words(data) == 0
    assert height(data) == 0
    assert contains(data, "") == False


def test_single_character_words():
    """Tests all functions with single character words."""
    data = {}
    for char in "abcdefg":
        insert(data, char)

    assert count_words(data) == 7
    assert height(data) == 1
    assert contains(data, "a") == True
    assert contains(data, "h") == False
    assert count_from_prefix(data, "a") == 0
    assert get_suggestions(data, "a") == []


def test_complex_trie():
    """Tests all functions on the complex example from assignment."""
    data = {}
    words = ["I", "an", "app", "apple", "apples", "applet", "or", "orange", "origin"]
    for word in words:
        insert(data, word)

    assert count_words(data) == 9
    assert height(data) == 6  # "apples", "applet", "orange", "origin" are all 6 chars
    assert contains(data, "apple") == True
    assert contains(data, "appl") == False
    assert (
        count_from_prefix(data, "app") == 3
    )  # apple, apples, applet (not "app" itself)
    suggestions = get_suggestions(data, "app")
    assert sorted(suggestions) == sorted(["apple", "apples", "applet"])
