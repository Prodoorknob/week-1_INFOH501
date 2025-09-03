

# add code below ...
def palindrome(text: str) -> bool:
    """
    Return True if `text` is a palindrome for case-insensitive and alphanumeric strings.
    Examples: "racecar", "A man, a plan, a canal: Panama!"
    """
    filtered = [char.lower() for char in text if char.isalnum()] #isalnum() checkes whether character is alphanumeric value
    return filtered == filtered[::-1]

def parentheses(in_value: str) -> bool:
    """
    Return True if parentheses/brackets/braces in `in_value` are balanced.
    Checks (), [], {} and ignores all other characters.
    """
    pairs = {')': '(', ']': '[', '}': '{'}
    openers = set(pairs.values())
    check = []
    for char in in_value:
        if char in openers:
            check.append(char)
        elif char in pairs:
            if not check or check[-1] != pairs[char]:
                return False
            check.pop()
    return len(check) == 0
