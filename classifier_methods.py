# Shabnam Nazmi.
# Graduate research assistant at electrical and computer engineering department,
# North Carolina A&T State University, Greensboro, NC.
# snazmi@aggies.ncat.edu.
#
# ------------------------------------------------------------------------------
from config import *


class ClassifierMethods:
    def __init__(self, dtypes):
        self.dtypes = dtypes

    def get_deletion_vote(self, classifier, ave_fitness):
        if classifier.fitness >= ave_fitness * DELTA * classifier.numerosity or classifier.match_count < THETA_DEL:
            classifier.deletion_vote = classifier.ave_matchset_size * classifier.numerosity
        else:
            classifier.deletion_vote = classifier.ave_matchset_size * classifier.numerosity ** 2 * ave_fitness / \
                                       classifier.fitness
        return classifier.deletion_vote

    def is_equal(self, classifier1, classifier2):
        if classifier1.prediction == classifier2.prediction and \
                len(classifier1.specified_atts) == len(classifier2.specified_atts):
            if sorted(classifier1.specified_atts) == sorted(classifier2.specified_atts):
                for idx in range(classifier1.specified_atts.__len__()):
                    if classifier1.condition[idx] == classifier2.condition[idx]:
                        pass
                    else:
                        return False
                return True
        return False

    def subsumption(self, classifier1, classifier2):
        if classifier1.prediction == classifier2.prediction:
            if self.is_subsumer(classifier1) and self.is_more_general(classifier1, classifier2):
                return True
        return False

    def is_subsumer(self, classifier1):
        if classifier1.match_count > THETA_SUB:
            acc = sum([acc / classifier1.match_count for acc in classifier1.label_based.values()]) \
                  / float(classifier1.prediction.__len__())
            if acc > ACC_SUB:
                return True
        return False

    def is_more_general(self, classifier1, classifier2):
        cl1_attributes = classifier1.specified_atts
        cl2_attributes = classifier2.specified_atts
        if cl1_attributes.__len__() > cl2_attributes.__len__():
            return False
        for ref in cl1_attributes:
            if ref not in cl2_attributes:
                return False
            if self.dtypes[ref] == 1:
                if classifier1.condition[cl1_attributes.index(ref)][0] < \
                        classifier2.condition[cl2_attributes.index(ref)][0]:
                    return False
                if classifier1.condition[cl1_attributes.index(ref)][1] > \
                        classifier2.condition[cl2_attributes.index(ref)][1]:
                    return False
        return True

    def classifier_print(self, classifier):
        classifier_string = ""
        for ref in range(self.dtypes.__len__()):
            if ref in classifier.specified_atts:
                ind = classifier.specified_atts.index(ref)
                if self.dtypes[ref] == 1:
                    classifier_string += (str("%.4f" % classifier.condition[ind][0]) + ';'
                                          + str("%.4f" % classifier.condition[ind][1]))
                else:
                    classifier_string += str(classifier.condition[ind])
            else:
                classifier_string += "#"
            classifier_string += ","
        classifier_string += str("%.4f" % float(classifier.specified_atts.__len__()/self.dtypes.__len__())) + ","
        prediction_string = ";".join([str(label) for label in classifier.prediction])
        classifier_string += (prediction_string + ",")
        label_precision = ";".join([str(label) + '%' + str(round(pr, 4)) for label, pr in classifier.label_based.items()])
        classifier_string += (label_precision + ",")
        try:
            loss = float(classifier.loss/classifier.match_count)
        except ZeroDivisionError:
            loss = 0.0
        parameter_string = str("%.4f" % classifier.fitness) + "," + \
            str("%.4f" % loss) + "," + \
            str("%d" % classifier.numerosity) + "," + \
            str("%d" % classifier.match_count) + "," + \
            str("%.4f" % classifier.ave_matchset_size) + "," + \
            str("%d" % classifier.init_time) + "," + \
            str("%d" % classifier.ga_time) + "\n"
        classifier_string += parameter_string
        return classifier_string


if __name__ == "__main__":
    print('nothing goes here!')
    # str("%d" % classifier.correct_count) + "," +
