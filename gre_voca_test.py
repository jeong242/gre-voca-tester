import json
from copy import deepcopy
import random
from datetime import datetime
from stat_util import Stat

random.seed(datetime.now())

filename = "voca.json"

with open(filename, "r") as f:
	data = json.load(f)

# Save the original one, since we will delete keys.
dict = deepcopy(data)
words = list(dict.keys())

# Number of total words
n_total_words = 0

# Keep track of number of correct answers.
n_correct = 0

# Keep track of incorrect answers.
incorrects = []

# Init Stat.
stat = Stat()

# While dict is non-empty...
while dict:
	# Pick a random word from words list.
	choice = random.randint(0,len(words)-1)
	word = words[choice]
	
	# Probability of asking word.
	prob = stat.get_prob(word)

	ask = False
	if random.uniform(0,1) < prob:
		ask = True

	if ask:
		# Ask a question, and wait for answer.
		answer = input("%s ~ " % word)

		# Process the answer.
		if answer in dict[word]:
			print("%s O" % answer)
			n_correct += 1
			stat.right_answer(word)
		elif answer == "X":
			print("%s X" % answer)
			incorrects.append(word)
			stat.wrong_answer(word)
		else:
			# Check if the answer is typo/not.
			# If so, consider it as a correct answer.
			# If not, it's wrong.
			isTypo = input("%s... typo? (y) or (n) " % answer)

			if isTypo == "n":
				print("%s X" % answer)
				incorrects.append(word)
				stat.wrong_answer(word)
			else:
				print("%s O" % answer)
				n_correct += 1
				stat.right_answer(word)

		n_total_words += 1

		# Print other words.
		print(dict[word])
		print("\n\n")

	# Remove.
	del dict[word]
	words.remove(word)

stat.save()

print("\nScore : %d / %d\n" %(n_correct,n_total_words))
print("Incorrect words : ")
for w in incorrects:
	print(w)
print("\n")
