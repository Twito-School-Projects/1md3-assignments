from typing import Dict, List

# just to make my life easier
type Trie = Dict[str, tuple[Trie, bool]]

def insert(data, s: str) -> None:
    if s == "":
        return
    if len(s) == 1:
        if s in data:
            data[s][1] = True
        else:
            data[s] = [{}, True]
    if s[0] in data:
        insert(data[s[0]][0], s[1:])
    else:
        data[s[0]] = [{}, False]
        insert(data[s[0]][0], s[1:])


def count_words(data: Trie) -> int:
    """
    Returns the number of words encoded in data. You may assume
    data is a valid trie.

    >>> data = {}
    >>> insert(data, "test")
    >>> insert(data, "testing")
    >>> insert(data, "doc")
    >>> insert(data, "docs")
    >>> insert(data, "document")
    >>> insert(data, "documenting")

    >>> count_words(data)
    6
    """
    if len(data.keys()) == 0:
        return 0

    count = 0
    for character, [sub_trie, is_word] in data.items():
        if is_word:
            count += 1
        count += count_words(sub_trie)
    return count


def contains(data: Trie, s: str) -> bool:
    """
    Returns True if and only if s is encoded within data. You may
    assume data is a valid trie.

    >>> data = {}
    >>> insert(data, "tree")
    >>> insert(data, "trie")
    >>> insert(data, "try")
    >>> insert(data, "trying")

    >>> contains(data, "try")
    True
    >>> contains(data, "trying")
    True
    >>> contains(data, "the")
    False
    """

    # new solution
    filtered_trie = data
    found = False

    # only runs length of s times
    for i in range(len(s)):
        char = s[i]
        if char not in filtered_trie:
            return False

        elif i == len(s) - 1:
            found = filtered_trie[char][1]
            break
        filtered_trie = filtered_trie[char][0]

    return found

    # bad solution
    # if len(data.keys()) > 0 and s == "":
    #     return True

    # for character, [sub_trie, is_word] in data.items():
    #     if s == "":
    #         return is_word

    #     return (s[0] == character) and contains(sub_trie, s[1:])


def height(data: Trie) -> int:
    """
    Returns the length of longest word encoded in data. You may
    assume that data is a valid trie.

    >>> data = {}
    >>> insert(data, "test")
    >>> insert(data, "testing")
    >>> insert(data, "doc")
    >>> insert(data, "docs")
    >>> insert(data, "document")
    >>> insert(data, "documenting")

    >>> height(data)
    11
    """
    longest = 0

    # nothing in the trie
    if len(data.keys()) == 0:
        return 0

    for character, [sub_trie, is_word] in data.items():
        trie_height = 1 + height(sub_trie)

        if longest < trie_height:
            longest = trie_height
    return longest


def count_from_prefix(data: Trie, prefix: str) -> int:
    """
    Returns the number of words in data which starts with the string
    prefix, but is not equal to prefix. You may assume data is a valid
    trie.

    data = {}
    >>> insert(data, "python")
    >>> insert(data, "pro")
    >>> insert(data, "professionnal")
    >>> insert(data, "program")
    >>> insert(data, "programming")
    >>> insert(data, "programmer")
    >>> insert(data, "programmers")

    >>> count_from_prefix(data, 'pro')
    5
    """
    # if the prefix is nothing
    if len(prefix) == 0:
        return count_words(data)

    # new solution
    filtered_trie = {}
    for i in range(len(prefix)):
        # setup
        char = prefix[i]
        if i == 0:
            if char in data:
                filtered_trie = data[char][0]
            else:
                return 0

        elif i > 0:
            if char in filtered_trie:
                filtered_trie = filtered_trie[char][0]
            else:
                return 0
    return count_words(filtered_trie)

    ##bad version doesnt work
    # if height(data) == 0:
    #     return 0

    # elif len(prefix) >= height(data):
    #     return 0

    # count = 0

    # for character, [sub_trie, is_word] in data.items():
    #     # prefix cannot be the word
    #     if (is_word and prefix == character) or prefix == "":
    #         print("found a word", character)
    #         count += 1

    #         count += count_from_prefix(sub_trie, prefix[1:])

    # return count


data = {}
insert(data, "app")
insert(data, "python")
insert(data, "pro")
insert(data, "professional")
insert(data, "program")
insert(data, "programming")
insert(data, "programmer")
insert(data, "programmer")


def get_suggestions(data: Trie, prefix: str) -> List[str]:
    """
    Returns a list of words which are encoded in data, and starts with
    prefix, but is not equal to prefix. You may assume data is a valid
    trie.

    data = {}
    >>> insert(data, "python")
    >>> insert(data, "pro")
    >>> insert(data, "professionnal")
    >>> insert(data, "program")
    >>> insert(data, "programming")
    >>> insert(data, "programmer")
    >>> insert(data, "programmers")

    >>> get_suggestions(data, "progr")
    ['program', 'programming', 'programmer', 'programmers']
    """
    #not efficient but hopefully it does not matter in this course
    results = construct_words(data, [])
    filtered  = []
    for word in results:
        if word.lower().startswith(prefix) and word.lower() != prefix:
            filtered.append(word)
    return filtered

def construct_words(data: Trie, results, current = "") -> List[str]:
    for character, [sub_trie, is_word] in data.items():
        if is_word:
            results.append(current + character)
        construct_words(sub_trie, results, current + character)
    return results

print(get_suggestions(data, "prog"))