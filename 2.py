#!/usr/bin/env python3

from collections import Counter

# Task 2
def my_counter(word: str):
	if not isinstance(word, str):
		raise TypeError("Argument is not a str.")
	
	word = word.lower()
	count = dict(Counter(word))
	count = {char: c for char, c in count.items() if c > 1}
	return len(count)
	


if __name__ == "__main__":
	print(my_counter('aBcbA'))
	# {'a': 2, 'b': 2}
	print(my_counter("RabarbArka"))
	# {'r': 3, 'a': 4, 'b': 2}