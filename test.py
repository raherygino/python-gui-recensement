def is_palindrome(s:str):
    s = s.lower().strip(" ")
    for i in range(len(s)):
        if s[i] != s[-(i+1)]:
            return False
    return True

print(is_palindrome("un homme planifie un canal panama"))