# Shabnam Nazmi.
# Graduate research assistant at electrical and computer engineering department,
# North Carolina A&T State University, Greensboro, NC.
# snazmi@aggies.ncat.edu.
#
# ------------------------------------------------------------------------------
from scipy import sparse
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse.csgraph import connected_components

from hfps_clustering import density_based
from classifier import Classifier
from config import *


def calculate_similarity(label_matrix, measure=0):
    if measure == 0:  # cosine similarity
        label_matrix_sparse = sparse.csr_matrix(np.array(label_matrix).transpose())
        return cosine_similarity(label_matrix_sparse)
    elif measure == 1:  # Hamming distance-based similarity
        similarity = np.zeros([NO_LABELS, NO_LABELS])
        for i in range(NO_LABELS):
            first_label = [label[i] for label in label_matrix]
            for j in range(i + 1, NO_LABELS):
                second_label = [label[j] for label in label_matrix]
                similarity[i, j] = np.sum(
                    np.array([1 for (l1, l2) in zip(first_label, second_label) if l1 == l2])) \
                    / len(label_matrix)
                similarity[j, i] = similarity[i, j]
        return similarity
    else:  # co-occurrence-based similarity
        similarity = np.zeros([NO_LABELS, NO_LABELS])
        for i in range(NO_LABELS):
            for j in range(NO_LABELS):
                first_label = [label[i] for label in label_matrix]
                second_label = [label[j] for label in label_matrix]
                similarity[i, j] = np.dot(first_label, second_label) / np.linalg.norm(second_label, 1)


class GraphPart:
    def __init__(self):
        self.classifiers = []
        self.label_clusters = []
        self.label_similarity = None
        self.predicted_labels = []
        self.label_matrix = []

    def build_graph(self, matching_classifiers):
        self.label_clusters = []
        self.label_matrix = []
        self.classifiers = matching_classifiers
        if any([classifier.prediction.__len__() > 1 for classifier in self.classifiers]):
            self.predicted_labels = sorted(list(set().union(*[classifier.prediction for classifier in self.classifiers])))

            def label_vector(classifier):
                return [max(classifier.label_based[label] / classifier.match_count, INIT_FITNESS)
                        if label in classifier.prediction else 0 for label in self.predicted_labels]

            for classifier in matching_classifiers:
                if classifier.match_count > 0:
                    for idx in range(classifier.numerosity):
                        self.label_matrix.append(label_vector(classifier))
            self.label_similarity = calculate_similarity(self.label_matrix)
        else:
            return

    def refine_prediction(self, it, target):
        self.label_clusters = []
        self.label_similarity = np.where(self.label_similarity > 0.7, self.label_similarity, 0)
        n_connected, label_connected = connected_components(self.label_similarity)
        if n_connected > 1:
            for c in range(n_connected):
                temp = [self.predicted_labels[node] for node in range(self.predicted_labels.__len__())
                        if label_connected[node] == c]
                self.label_clusters.append(set(temp))
        else:
            label_clusters_unmerged, self.label_clusters = density_based(K, self.label_matrix, 1 - self.label_similarity,
                                                                         self.predicted_labels)

        new_classifiers = [self.breakdown_labelset(classifier, it, target) for classifier in self.classifiers if
                           classifier.prediction.__len__() > L_MIN]
        return new_classifiers

    def breakdown_labelset(self, classifier, it, target):
        prediction = set(classifier.label_based.keys())
        new_classifiers = []
        label_subsets = [prediction.intersection(cluster) for cluster in self.label_clusters if
                         prediction.intersection(cluster).__len__() > 0]

        if label_subsets.__len__() > 1:
            classifier.update_numerosity(-1)
            for cluster in label_subsets:
                new_classifier = Classifier()
                new_classifier.classifier_copy(classifier, it)
                new_classifier.prediction = cluster
                new_classifier.label_based = {k: 1 if k in cluster.intersection(target) else 0 for k in cluster}
                new_classifier.match_count = 1
                new_classifier.parent_prediction.append(prediction)
                new_classifier.set_fitness(INIT_FITNESS)
                new_classifiers.append(new_classifier)
        return new_classifiers
