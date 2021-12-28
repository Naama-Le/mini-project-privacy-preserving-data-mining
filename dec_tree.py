import random
import math
from node import Node
from collections import Counter


class Dec_Tree:

    def __init__(self,server):
        self.__united_db = server.get_united_db() #TODO add 
        self.__attrs = list(self.__united_db.get_attributes()) # TODO add.  get array of attrs, for each attr: {attrName: attrValues}
        categories = list(self.__united_db.get_categories()) # TODO add. get array of categories, for each cat: {catName: catValues}
        self.node =  self._id3_recv(self.__united_db[1], self.__attrs, categories, 0, None)

    def _id3_recv(self, data, attrs, x_ids, feature_ids, node):
        """ID3 algorithm. It is called recursively until some criteria is met.
        Parameters
        __________
        :param x_ids: list, list containing the samples ID's
        :param feature_ids: list, List containing the feature ID's
        :param node: object, An instance of the class Nodes
        __________
        :returns: An instance of the class Node containing all the information of the nodes in the Decision Tree
        """
        if not node:
            node = Node()  # initialize nodes
        # sorted labels by instance id
        all_categories = {}
        all_categories = [(all_categories | kmer_value[1]) for kmer_value in data.values()] #merge all kmers categories

        # if all objects have the same category (pure node), return node with this category
        if len(all_categories) == 1:
            node.value = all_categories.keys()[0]
            return node
        # if there are not more attrs to compute, return node with the most probable attr
        if len(attrs) == 0:
            node.value = all_categories.most_common(1).keys()[0]
            return node
        # else...
        # TODO continue from here 25.12 https://towardsdatascience.com/id3-decision-tree-classifier-from-scratch-in-python-b38ef145fd90
        # choose the feature that maximizes the information gain
        best_attr, best_attr_id = self.find_most_informative_attr(data, attrs)
        node.value = best_attr
        node.childs = []
        # value of the chosen feature for each instance
        feature_values = list(set([self.X[x][best_attr_id] for x in x_ids]))
        # loop through all the values
        for value in feature_values:
            child = Node()
            child.value = value  # add a branch from the node to each feature value in our feature
            node.childs.append(child)  # append new child node to current node
            child_x_ids = [x for x in x_ids if self.X[x][best_attr_id] == value]
            if not child_x_ids:
                child.next = max(set(labels_in_features), key=labels_in_features.count)
                print('')
            else:
                if feature_ids and best_attr_id in feature_ids:
                    to_remove = feature_ids.index(best_attr_id)
                    feature_ids.pop(to_remove)
                # recursively call the algorithm
                child.next = self._id3_recv(child_x_ids, feature_ids, child.next)
        return node
   
    def get_united_db(self):
        return self.__united_db

    def get_attr_index(self, attr):
        #  TODO : find a way to know the attr position in the k-mer.
        return

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

    def find_most_informative_attr(self, data, attrs, depth):
        max_info_gain = -1
        max_info_attr = None
        
        for attr in attrs:  #for each attr in the dataset
            attr_info_gain = self.calc_info_gain(attr, data)
            if max_info_gain < attr_info_gain: #selecting attr name with highest information gain
                max_info_gain = attr_info_gain
                max_info_attr = attr
                
        return max_info_attr


    # def generate_sub_tree(attr, data, categories, depth):
    #     attr_value_count_dict = len(data) #dictionary of the count of unqiue feature value
    #     tree = {} #sub tree or node
        
    #     for feature_value, count in attr_value_count_dict.iteritems():
    #         feature_value_data = train_data[train_data[attr] == feature_value] #dataset with only attr = feature_value
            
    #         assigned_to_node = False #flag for tracking feature_value is pure class or not
    #         for c in class_list: #for each class
    #             class_count = feature_value_data[feature_value_data[label] == c].shape[0] #count of class c

    #             if class_count == count: #count of feature_value = count of class (pure class)
    #                 tree[feature_value] = c #adding node to the tree
    #                 train_data = train_data[train_data[attr] != feature_value] #removing rows with feature_value
    #                 assigned_to_node = True
    #         if not assigned_to_node: #not pure class
    #             tree[feature_value] = "?" #should extend the node, so the branch is marked with ?
                
    #     return tree, train_data

    # def build_tree(self, root, prev_attr_value, data, attrs, categories, depth):
    #     if len(attrs) != 0: #if dataset isn't empty after updating
    #         max_info_attr = self.find_most_informative_attr(attrs, data, depth) #most informative attr
    #         # TODO continue to adjust the functions below by https://medium.com/geekculture/step-by-step-decision-tree-id3-algorithm-from-scratch-in-python-no-fancy-library-4822bbfdd88f
    #         tree, data = self.generate_sub_tree(max_info_attr, data, categories, depth) #getting tree node and updated dataset
    #         next_root = None
            
    #         if prev_attr_value != None: #add to intermediate node of the tree
    #             root[prev_attr_value] = dict()
    #             root[prev_attr_value][max_info_attr] = tree
    #             next_root = root[prev_attr_value][max_info_attr]
    #         else: #add to root of the tree
    #             root[max_info_attr] = tree
    #             next_root = root[max_info_attr]
            
    #         for node, branch in list(next_root.items()): #iterating the tree node
    #             if branch == "?": #if it is expandable
    #                 attr_value_data = data[data[max_info_attr] == node] #using the updated dataset
    #                 self.build_tree(next_root, node, attr_value_data, categories) #recursive call with updated dataset

