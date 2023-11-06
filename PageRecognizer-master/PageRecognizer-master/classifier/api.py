import os, sys
#print os.path.dirname(os.path.abspath(__file__))
from svmutil import *

m = svm_load_model('%(classifier)s/mnist_probability.model' % {'classifier': os.path.dirname(os.path.abspath(__file__))})
label_order = m.get_labels()
reverse_label_order = [i[0] for i in sorted(enumerate(label_order), key=lambda x:x[1])]

def classify(image):
	t1, t2, probabilities = svm_predict([0], [image], m, '-b 1');
	return [probabilities[0][k] for k in reverse_label_order]


