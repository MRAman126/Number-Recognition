from mnist import MNIST
from svmutil import *

mndata = MNIST('./mnist-set')

print ('Reading data...')
images_train, labels_train = mndata.load_training()

images_train = images_train[:10000]
labels_train = labels_train[:10000]


print 'Normalizing data...'
for i in xrange(0, len(images_train)):
	images_train[i] = [x / 255.0 for x in images_train[i]]

print 'Creating model...'
param = svm_parameter('-t 2 -c 64.0 -g 0.03125 -q -b 1')
prob_train = svm_problem(labels_train, images_train)
m = svm_train(prob_train, param)
print 'Saving model to mnist_probability.model...'
svm_save_model('mnist_probability.model', m);
print 'Model created!'

