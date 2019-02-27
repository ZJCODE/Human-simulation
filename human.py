import matplotlib.pyplot as plt
import numpy as np
import copy
import time
import utils


class human:

    def __init__(self, identity, physic_dims=2, opinion_dims=5):  # born
        self.physic_dims = physic_dims
        self.opinion_dims = opinion_dims
        self.identity = identity  # who you are
        self.age = 0  # what is time ?
        self.opinion = np.random.normal(0, 1, opinion_dims)  # how you think
        self.opinion_trace = []
        self.location = 10 * np.random.normal(0, 1, physic_dims)  # where you are
        self.location_trace = []
        self.view_threshold = 5
        self.human_meet_set = {}  # people who you meet
        self.human_opinion_match_set = {}  # people who you agree with their opinion
        self.human_meet_set_obj = {}  # people who you meet
        self.human_opinion_match_set_obj = {}  # people who you agree with their opinion
        self.forget_level = 0.1
        self.ability_level = 1
        self.walk_direction = np.random.normal(0, 1, physic_dims)  # where you go
        self.pre_walk_direction = None

    def get_opinion(self):
        return utils.softmax(self.opinion)

    def get_location(self):
        return self.location

    def add_age(self):
        self.age += 1  # add one for each loop

    def walk(self, walk_random_level=0.3, walk_influence_level=0.01):
        self.pre_walk_direction = self.walk_direction
        self.walk_direction = self.pre_walk_direction + walk_random_level * np.random.normal(0, 1, self.physic_dims)
        for someone, weight in self.human_opinion_match_set_obj.items():
            self.walk_direction += weight * walk_influence_level * someone.pre_walk_direction
        self.walk_direction = self.walk_direction / np.linalg.norm(self.walk_direction)
        self.location += self.walk_direction
        self.location_trace.append(copy.deepcopy(self.location))

    def location_match(self, someone):
        distance = np.linalg.norm(self.location - someone.location)
        if distance < self.view_threshold:
            print('{} meet {}'.format(self.identity, someone.identity))
            # update self
            if someone.identity not in self.human_meet_set.keys():
                self.human_meet_set.update({someone.identity: 1})
                self.human_meet_set_obj.update({someone: 1})
            else:
                self.human_meet_set[someone.identity] += 1
                self.human_meet_set_obj[someone] += 1
            # update someone
            if self.identity not in someone.human_meet_set.keys():
                someone.human_meet_set.update({self.identity: 1})
                someone.human_meet_set_obj.update({self: 1})
            else:
                someone.human_meet_set[self.identity] += 1
                someone.human_meet_set_obj[self] += 1

            return 1
        else:
            return 0

    def _generate_opinion(self, opinion_random_level):
        opinion_distribution = self.get_opinion() + \
                               opinion_random_level * np.random.normal(0, 1, self.opinion_dims)
        opinion_distribution_with_random = opinion_distribution / np.sum(opinion_distribution)
        sentence = utils.sampling(opinion_distribution_with_random)
        return sentence  # return opinion index

    def _generate_response(self, sentence, opinion_agree_level):
        # receive opinion index
        opinon_sort = list(np.argsort(self.opinion))
        match_level = opinon_sort.index(sentence) + 1
        match_level = match_level / self.opinion_dims
        if match_level > opinion_agree_level:
            response = 'yes , you are right !'
        else:
            response = 'no , i don\'t agree with you !'
        return response, match_level

    def _talk_to(self, someone, opinion_random_level, opinion_agree_level):
        sentence = self._generate_opinion(opinion_random_level)
        print('{} say : opinion {}'.format(self.identity, sentence))
        response, _ = someone._generate_response(sentence, opinion_agree_level)
        print('{} response : {}'.format(someone.identity, response))
        return response

    def _opinion_influence(self, someone, opinion_influence_level):
        self.opinion = self.opinion + opinion_influence_level * someone.opinion
        someone.opinion = someone.opinion + opinion_influence_level * self.opinion

    def opinion_match(self, someone, opinion_random_level, opinion_agree_level):
        result = self._talk_to(someone, opinion_random_level, opinion_agree_level)
        if result == 'yes , you are right !':
            print('{} \'s opinion matches {}'.format(self.identity, someone.identity))
            # update self
            if someone.identity not in self.human_opinion_match_set.keys():
                self.human_opinion_match_set.update({someone.identity: 1})
                self.human_opinion_match_set_obj.update({someone: 1})
            else:
                self.human_opinion_match_set[someone.identity] += 1
                self.human_opinion_match_set_obj[someone] += 1
            # update someone
            if self.identity not in someone.human_opinion_match_set.keys():
                someone.human_opinion_match_set.update({self.identity: 1})
                someone.human_opinion_match_set_obj.update({self: 1})
            else:
                someone.human_opinion_match_set[self.identity] += 1
                someone.human_opinion_match_set_obj[self] += 1

            return 1
        else:
            return 0

    def match(self, someone, opinion_random_level=0.0, opinion_agree_level=0.5, opinion_influence_level=0.01):
        # opinion_random_level 0 to 1 | can use some random generator to generate opinion_random_level
        if self.location_match(someone):
            if self.opinion_match(someone, opinion_random_level, opinion_agree_level):
                self._opinion_influence(someone, opinion_influence_level)
            else:
                pass
        else:
            pass

    def plot_location_trace(self, color):
        for i in range(1, len(self.location_trace)):
            pre_location = self.location_trace[i - 1]
            location = self.location_trace[i]
            plt.plot([pre_location[0], location[0]], [pre_location[1], location[1]], '{}-'.format(color), alpha=0.3)


if __name__ == '__main__':

    times = 300
    human_num = 30
    humans = []

    for i in range(human_num):  # move this to environment
        humans.append(human('u{}'.format(i), physic_dims=2, opinion_dims=10))

    opinion_original = np.zeros(humans[0].opinion_dims)
    for h in humans:
        opinion_original += h.get_opinion()
    opinion_original = opinion_original / human_num

    t1 = time.time()
    for i in range(times):
        for h in humans:
            h.walk()
        for index_1 in range(human_num - 1):
            for index_2 in range(index_1 + 1, human_num):
                humans[index_1].match(humans[index_2], opinion_random_level=0.2, opinion_agree_level=0.6,
                                      opinion_influence_level=1)
    print('cost : {} seconds'.format(time.time() - t1))

    color_generator = utils.get_color()
    opinion_final = np.zeros(humans[0].opinion_dims)
    print('-' * 80)
    for h in humans:
        t1 = time.time()
        print(h.identity, 'location match', h.human_meet_set)
        print(h.identity, 'opinion match ', h.human_opinion_match_set)
        h.plot_location_trace(next(color_generator))

        plt.plot(h.location_trace[-1][0], h.location_trace[-1][1], '{}.'.format(next(color_generator)),alpha=0.5)
        opinion_final += h.get_opinion()
        print(h.identity, 'location:', h.location)
        print(h.identity, 'opinion: ', h.get_opinion())
        print('cost : {} seconds'.format(time.time() - t1))
        print('-' * 80)
    plt.show()
    opinion_final = opinion_final / human_num
    print('-' * 80)
    print(opinion_original)
    print(opinion_final)
