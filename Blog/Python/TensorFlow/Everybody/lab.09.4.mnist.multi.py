import tensorflow as tf
import numpy as np

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)


num_input = 784
nb_classes = 10 # 0 ~ 9 digits
l1 = 784
l2 = 784


X = tf.placeholder(tf.float32, [None, num_input]) # 28 * 28 = 784
Y = tf.placeholder(tf.float32, [None, nb_classes])

W1 = tf.Variable(tf.random_normal([num_input, l1]), name="weight1")
b1 = tf.Variable(tf.random_normal([l1]), name="bias1")
h1 = tf.nn.softmax(tf.matmul(X, W1) + b1)

W2 = tf.Variable(tf.random_normal([l1, l2]), name="weight2")
b2 = tf.Variable(tf.random_normal([l2]), name="bias2")
h2 = tf.nn.softmax(tf.matmul(h1, W2) + b2)

W3 = tf.Variable(tf.random_normal([l2, nb_classes]), name="weight3")
b3 = tf.Variable(tf.random_normal([nb_classes]), name="bias3")
hypothesis = tf.nn.softmax(tf.matmul(h2, W3) + b3)

# Softmax
#hypothesis = tf.nn.softmax(tf.matmul(X, W) + b)
cost = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(hypothesis), axis=1))
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.1).minimize(cost)

# Test model
is_correct = tf.equal(tf.argmax(hypothesis, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))

# training parameters
training_epochs = 20
batch_size = 100

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    for epoch in range(training_epochs):
        avg_cost = 0
        total_batch = int(mnist.train.num_examples / batch_size)

        for i in range(total_batch):
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            c, _ = sess.run([cost, optimizer], feed_dict={X: batch_xs, Y: batch_ys})
            avg_cost += c / total_batch

        print("Epoch: ", epoch + 1, 'cost = ', avg_cost)

    print("Accuracy: ", accuracy.eval(session=sess, feed_dict={X: mnist.test.images, Y: mnist.test.labels}))