import random
import math


class Dec_Tree:

    def __init__(self,server):
        self.__united_db = server.get_united_db() #TODO add 
        self.__attrs = list(self.__united_db.get_attributes()) # TODO add.  get array of attrs, for each attr: {attrName: attrValues}
        categories = list(self.__united_db.get_categories()) # TODO add. get array of categories, for each cat: {catName: catValues}
        self.__tree = {};
        self.__tree_dict = self.build_tree(self.__tree, None, self.__attrs,  self.__united_db[1], categories, 0)

    def get_tree_dict(self):
        return self.__tree_dict

    def get_united_db(self):
        return self.__united_db

    def get_attr_index(self, attr):
        return self.__attrs.index(attr)

    # iterate through the current data and calc E_TA for attr, by all Ta_i and Ta_ic_j
    # attr = {attrName: attrValues}
    def calc_info_gain(self, attr, data):
        Ta = {};
        Tac = {};
        attr_index = self.get_attr_index(attr) #get the position of the attr value in the k-mer order
        for key, value in data.items():
            a = key.split()[attr_index]
            Ta[a] += value[0]
            for key_c, value_c in value[1].items():
                Tac[a][key_c] += value_c
       
        return self.calc_E_TA(self, attr, Ta, Tac)

    # calc E_TA without dividing by T as we'll compare these values to find the best attr A among all
    # A is the set of possible attr values for A attr
    # Ta is an array holds Ta values for each a
    # Tac is a 2D-aaray holds Tac values for each a and category value c
    def calc_E_TA(self, A, Ta, Tac):
        E_TA = (-sum(sum(abs(Tac[attr][cat])*abs(math.log2(Tac[attr][cat])) for cat in Tac) for attr in A))
        + (sum(abs(Ta[attr])*math.log2(abs(Ta[attr])) for attr in A))
        return E_TA  

    def find_most_informative_attr(self, attrs, data, depth):
        max_info_gain = -1
        max_info_attr = None
        
        for attr in attrs:  #for each attr in the dataset
            attr_info_gain = self.calc_info_gain(attr, data)
            if max_info_gain < attr_info_gain: #selecting attr name with highest information gain
                max_info_gain = attr_info_gain
                max_info_attr = attr
                
        return max_info_attr


    def build_tree(self, root, prev_attr_value, data, attrs, categories, depth):
        if len(attrs) != 0: #if dataset isn't empty after updating
            max_info_attr = self.find_most_informative_attr(attrs, data, depth) #most informative attr
            # TODO continue to adjust the functions below by https://medium.com/geekculture/step-by-step-decision-tree-id3-algorithm-from-scratch-in-python-no-fancy-library-4822bbfdd88f
            tree, data = generate_sub_tree(max_info_attr, data, categories) #getting tree node and updated dataset
            next_root = None
            
            if prev_attr_value != None: #add to intermediate node of the tree
                root[prev_attr_value] = dict()
                root[prev_attr_value][max_info_attr] = tree
                next_root = root[prev_attr_value][max_info_attr]
            else: #add to root of the tree
                root[max_info_attr] = tree
                next_root = root[max_info_attr]
            
            for node, branch in list(next_root.items()): #iterating the tree node
                if branch == "?": #if it is expandable
                    attr_value_data = data[data[max_info_attr] == node] #using the updated dataset
                    self.build_tree(next_root, node, attr_value_data, categories) #recursive call with updated dataset

