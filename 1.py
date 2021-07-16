#!/usr/bin/env python3

# Task 1
def my_upper(word: str):
	if not isinstance(word, str):
		raise TypeError("Argument is not a str.")

	word1, word2 = [], []

	for i, char in enumerate(word):
			word1.append(char.upper() if i % 2 else char.lower())
			word2.append(char.lower() if i % 2 else char.upper())

	return [''.join(word1), ''.join(word2)]

if __name__ == '__main__':
	print(my_upper('abcdef'))
	# ['aBcDeF', 'AbCdEf']
	

