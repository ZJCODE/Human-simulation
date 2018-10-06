import matplotlib.pyplot as plt
import numpy as np
import utils


class human:
	
	def __init__(self,identity,physic_dims=2,opinion_dims=5): # born 
		self.physic_dims = physic_dims
		self.opinion_dims = opinion_dims
		self.identity = identity # who you are
		self.age = 0 # what is time ? 
		self.opinion = np.random.random(opinion_dims) # how you think
		self.opinion_trace = [self.opinion]
		self.location = np.random.random(physic_dims) # where you are
		self.location_trace = [self.location]
		self.view_threshold = 0.8
		self.human_meet_set = {} # people who you meet
		self.human_opinion_match_set = {} # people who you agree with their opinion
		self.human_meet_set_obj = {} # people who you meet
		self.human_opinion_match_set_obj = {} # people who you agree with their opinion
		self.forget_level = 0.1
		self.ability_level = 1
		self.walk_direction = np.random.random(physic_dims) # where you go
		self.pre_walk_direction = None
		self.pre_location = None

		
	def add_age(self):
		self.age += 1 # add one for each loop
		
	def walk(self,walk_random_level = 0,walk_influence_level = 0.01):
		self.pre_walk_direction = self.walk_direction
		self.pre_location = self.location
		self.walk_direction = self.pre_walk_direction + walk_random_level * np.random.random(self.physic_dims)
		for someone,weight in self.human_opinion_match_set_obj.items():
			 self.walk_direction += weight * walk_influence_level * someone.pre_walk_direction 
		self.walk_direction = self.walk_direction / np.linalg.norm(self.walk_direction)
		self.location += self.walk_direction

	def location_match(self,someone):
		distance = np.linalg.norm(self.location - someone.location)
		if distance < self.view_threshold:
			print('{} meet {}'.format(self.identity,someone.identity))
			if someone.identity not in self.human_meet_set.keys():
				self.human_meet_set.update({someone.identity:1})
				self.human_meet_set_obj.update({someone:1})
			else:
				self.human_meet_set[someone.identity] += 1
				self.human_meet_set_obj[someone] += 1
			return 1
		else:
			return 0
			
	def _generate_opinion(self,opinion_random_level):
		opinion_distribution = self.opinion / np.sum(self.opinion) + opinion_random_level * np.random.random(self.opinion_dims)
		opinion_distribution_with_random = opinion_distribution / np.sum(opinion_distribution)
		sentence = utils.sampling(opinion_distribution_with_random)
		return sentence # return opinion index
		
	def _generate_response(self,sentence,opinion_agree_level):
		# receive opinion index
		opinon_sort = list(np.argsort(self.opinion))
		match_level = opinon_sort.index(sentence) + 1
		match_level = match_level / self.opinion_dims
		if match_level > opinion_agree_level:
			response = 'yes , you are right !'
		else:
			response = 'no , i don\'t agree with you !'
		return response,match_level

	def _talk_to(self,someone,opinion_random_level,opinion_agree_level):
		sentence = self._generate_opinion(opinion_random_level)
		print('{} say : opinion {}'.format(self.identity,sentence))
		response,_ = someone._generate_response(sentence,opinion_agree_level)
		print('{} response : {}'.format(someone.identity,response))
		return response
		
	def _opinion_influence(self,someone,opinion_influence_level):
		self.opinion = self.opinion + opinion_influence_level * someone.opinion
		self.opinion = self.opinion / np.sum(self.opinion) 
		someone.opinion = someone.opinion + opinion_influence_level * self.opinion
		someone.opinion = someone.opinion / np.sum(someone.opinion)
		
	def opinion_match(self,someone,opinion_random_level,opinion_agree_level,opinion_influence_level):
		result = self._talk_to(someone,opinion_random_level,opinion_agree_level)
		if result == 'yes , you are right !' :
			print('{} \'s opinion matches {}'.format(self.identity,someone.identity))
			if someone.identity not in self.human_opinion_match_set.keys():
				self.human_opinion_match_set.update({someone.identity:1})
				self.human_opinion_match_set_obj.update({someone:1})
			else:
				self.human_opinion_match_set[someone.identity] += 1
				self.human_opinion_match_set_obj[someone] += 1
			return 1
		else:
			return 0
			
		
	def match(self,someone,opinion_random_level=0,opinion_agree_level=0.5,opinion_influence_level=0.01): 
		# opinion_random_level 0 to 1 | can use some random generator to generate opinion_random_level
		if self.location_match(someone):
			if self.opinion_match(someone,opinion_random_level,opinion_agree_level,opinion_influence_level):
				self._opinion_influence(someone,opinion_influence_level)
			else:
				pass
		else:
			pass
	

if __name__ == '__main__':

	h1 = human('u1',physic_dims=2,opinion_dims=3)
	h2 = human('u2',physic_dims=2,opinion_dims=3)
	for i in range(100):
		h1.walk()
		h2.walk()
		print('\nposition\n')
		print(h1.location)
		print(h2.location)
		print(h1.opinion)
		print(h2.opinion)
		print('\ntry match\n')
		h1.match(h2) 
		print('\nmatch result \n')
		print(h1.human_meet_set)
		print(h1.human_opinion_match_set)
		print('-'*40)
		#plt.plot([[h1.pre_location[0],h1.location[1],h1.location])
	#plt.show()
	plt.plot([[1,2],[4,6]])
	plt.show()