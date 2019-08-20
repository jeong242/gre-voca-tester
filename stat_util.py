import json
import json

# more_wrong increase the probability of asking a word.
more_wrong = 2

"""
	Typical use pattern:
	stat = Stat()

	# Do some stuffs...
	if right_answer:
		stat.right_answer(word)	
	else:
		stat.wrong_answer(word)
	...

	stat.save()

"""

class Stat:
	def __init__(self, load_fname="stat.json"):
		with open(load_fname, "r") as f:
			self.stat_dict = json.load(f)
		self._update()

	def _update(self, fname="voca.json"):
		with open(fname, "r") as f:
			voca_dict = json.load(f)
		
		n_voca = len(voca_dict)
		n_stat = len(self.stat_dict)
		# Check if update is required.
		# The difference is only determined by the lengths.
		voca_keys = list(voca_dict.keys())
		while n_stat < n_voca:
			new_key = voca_keys[n_stat]
			self.stat_dict[new_key] = [0,0]	
			n_stat += 1

	def get_prob(self, word):
		n_right, n_wrong = self.stat_dict[word]
		prob = (n_wrong + more_wrong) / (n_right + n_wrong + 2)
		return prob
	
	def right_answer(self, word):
		self.stat_dict[word][0] += 1

	def wrong_answer(self, word):
		self.stat_dict[word][1] += 1

	def save(self, fname = "stat.json"):
		stat = self.stat_dict
		with open(fname, "w") as f:
			json.dump(stat, f)

# Call once.
# Create a dictionary, where dict = {word: (# correct answer, # wrong answer)}.
def init_stat(src_fname="voca.json", dst_fname="stat.json"):
	# Open voca json file.
	with open(src_fname, "r") as f:
		stat = json.load(f)
	# Set all the values to 0.
	for w in stat:
		stat[w] = (0,0)
	# Store stat as json.
	with open(dst_fname, "w") as f:
		json.dump(stat, f)
