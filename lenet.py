"""
LeNet Architecture

HINTS for layers:

    Convolutional layers:

    tf.nn.conv2d
    tf.nn.max_pool

    For preparing the convolutional layer output for the
    fully connected layers.

    tf.contrib.flatten
"""
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.contrib.layers import flatten


EPOCHS = 10
BATCH_SIZE = 50


# LeNet architecture:
# INPUT -> CONV -> ACT -> POOL -> CONV -> ACT -> POOL -> FLATTEN -> FC -> ACT -> FC
#
# Don't worry about anything else in the file too much, all you have to do is
# create the LeNet and return the result of the last fully connected layer.
def LeNet(x):
    # Reshape from 2D to 4D. This prepares the data for
    # convolutional and pooling layers.
    x = tf.reshape(x, (-1, 28, 28, 1))
    # Pad 0s to 32x32. Centers the digit further.
    # Add 2 rows/columns on each side for height and width dimensions.
    x = tf.pad(x, [[0, 0], [2, 2], [2, 2], [0, 0]], mode="CONSTANT")
    # TODO: Define the LeNet architecture.
    # Return the result of the last fully connected layer.

    #Convolution layer 1. The output shape should be 28x28x6.
    conv1_filter_w = tf.Variable(tf.truncated_normal([5,5,1,6]))
    conv1_filter_b = tf.Variable(tf.zeros(6))
    conv1 = tf.nn.conv2d(x, conv1_filter_w, strides=[1, 1, 1, 1], padding='VALID') + conv1_filter_b
    # Activation 1. Your choice of activation function.
    conv1 = tf.nn.relu(conv1)
    # Pooling layer 1. The output shape should be 14x14x6.
    conv1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='VALID')
    # Convolution layer 2. The output shape should be 10x10x16.
    conv2_filter_w = tf.Variable(tf.truncated_normal([5,5,6,16]))
    conv2_filter_b = tf.Variable(tf.zeros(16))
    conv2 = tf.nn.conv2d(conv1, conv2_filter_w, strides=[1, 1, 1, 1], padding='VALID') + conv2_filter_b
    # Activation 2. Your choice of activation function.
    conv2 = tf.nn.relu(conv2)
    # Pooling layer 2. The output shape should be 5x5x16.
    conv2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='VALID')
    # Flatten layer. Flatten the output shape of the final pooling layer
    # such that it's 1D instead of 3D. The easiest way to do is by using
    # tf.contrib.layers.flatten, which is already imported for you.
    flatten_conv2 = flatten(conv2)
    # Fully connected layer 1. This should have 120 outputs.
    # 5 * 5 * 16 flatten is 400
    fc1_input = flatten_conv2
    fc1_w = tf.Variable(tf.truncated_normal([400, 120]))
    fc1_b = tf.Variable(tf.zeros(120))
    fc1_output = tf.matmul(fc1_input, fc1_w) + fc1_b
    # Activation 3. Your choice of activation function.
    fc1_output = tf.nn.relu(fc1_output)
    # Fully connected layer 2. This should have 10 outputs.
    fc2_w = tf.Variable(tf.truncated_normal([120, 10]))
    fc2_b = tf.Variable(tf.zeros(10))
    fc2_output = tf.matmul(fc1_output, fc2_w) + fc2_b
    return fc2_output

# MNIST consists of 28x28x1, grayscale images
x = tf.placeholder(tf.float32, (None, 784))
# Classify over 10 digits 0-9
y = tf.placeholder(tf.float32, (None, 10))
fc2 = LeNet(x)

loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(fc2, y))
opt = tf.train.AdamOptimizer()
train_op = opt.minimize(loss_op)
correct_prediction = tf.equal(tf.argmax(fc2, 1), tf.argmax(y, 1))
accuracy_op = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


def eval_data(dataset):
    """
    Given a dataset as input returns the loss and accuracy.
    """
    # If dataset.num_examples is not divisible by BATCH_SIZE
    # the remainder will be discarded.
    # Ex: If BATCH_SIZE is 64 and training set has 55000 examples
    # steps_per_epoch = 55000 // 64 = 859
    # num_examples = 859 * 64 = 54976
    #
    # So in that case we go over 54976 examples instead of 55000.
    steps_per_epoch = dataset.num_examples // BATCH_SIZE
    num_examples = steps_per_epoch * BATCH_SIZE
    total_acc, total_loss = 0, 0
    for step in range(steps_per_epoch):
        batch_x, batch_y = dataset.next_batch(BATCH_SIZE)
        loss, acc = sess.run([loss_op, accuracy_op], feed_dict={x: batch_x, y: batch_y})
        total_acc += (acc * batch_x.shape[0])
        total_loss += (loss * batch_x.shape[0])
    return total_loss/num_examples, total_acc/num_examples


if __name__ == '__main__':
    # Load data
    mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())
        steps_per_epoch = mnist.train.num_examples // BATCH_SIZE
        num_examples = steps_per_epoch * BATCH_SIZE

        # Train model
        for i in range(EPOCHS):
            for step in range(steps_per_epoch):
                batch_x, batch_y = mnist.train.next_batch(BATCH_SIZE)
                loss = sess.run(train_op, feed_dict={x: batch_x, y: batch_y})

            val_loss, val_acc = eval_data(mnist.validation)
            print("EPOCH {} ...".format(i+1))
            print("Validation loss = {:.3f}".format(val_loss))
            print("Validation accuracy = {:.3f}".format(val_acc))
            print()

        # Evaluate on the test data
        test_loss, test_acc = eval_data(mnist.test)
        print("Test loss = {:.3f}".format(test_loss))
        print("Test accuracy = {:.3f}".format(test_acc))
