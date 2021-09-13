# numpy provides arrays and useful functions for working with them
import numpy
from scipy.ndimage.measurements import label
# scipy.special for the sigmoid function expit()
import scipy.special
# scipy.ndimage for rotating image arrays
import scipy.ndimage

try:
    # cupy version
    import cupy
    import cupyx.scipy.ndimage
except:
    print("Unable to import cupy!")
    print("Please DON'T use cupy associated objects or functions!")

# used when saving datas
import time
import os

# read self-made pics and show
import imageio
import matplotlib.pyplot


class neuralNetwork:
    """neural network class definition"""

    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        """initialise the neural network"""
        # set number of nodes in each input, hidden, output layer
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes

        #learning rate
        self.lr = learningrate


class numpyNetwork(neuralNetwork):
    """neural network class definition"""

    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        """initialise the neural network - numpy"""
        
        super().__init__(inputnodes, hiddennodes, outputnodes, learningrate)

        # link weight matrices, wih and who
        # weights inside the arrays are w_i_j, where link is from node i to node i to j in the next layer
        # w11 w21
        # w12 w22 etc
        self.wih = numpy.random.normal(
            0.0, pow(self.inodes, -0.5), (self.hnodes, self.inodes))
        self.who = numpy.random.normal(
            0.0, pow(self.hnodes, -0.5), (self.onodes, self.hnodes))

        #activation function is the sigmoid function
        self.activation_function = lambda x: scipy.special.expit(x)

        pass

    def train(self, inputs_list, targets_list):
        """train the neural network"""
        # convert inputs list to 2d array
        inputs = numpy.array(inputs_list, ndmin=2).T
        targets = numpy.array(targets_list, ndmin=2).T

        # calculate signals into hidden layer
        hidden_inputs = numpy.dot(self.wih, inputs)
        # calculate the signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)

        # calcute signals into final output layer
        final_inputs = numpy.dot(self.who, hidden_outputs)
        # calculate signals into final output layer
        final_outputs = self.activation_function(final_inputs)

        # output layer error is the (target - actual)
        output_errors = targets - final_outputs
        # hidden layer error is the output_errors, split by weights, recombined at hidden nodes
        hidden_errors = numpy.dot(self.who.T, output_errors)

        # update the weights for the links between the hidden and output layers
        # S' = S(1 - S)
        # dE / Dw = K * e * o * (1 - o)
        self.who += self.lr * numpy.dot((output_errors * final_outputs * (
            1.0 - final_outputs)), numpy.transpose(hidden_outputs))
        self.wih += self.lr * \
            numpy.dot((hidden_errors * hidden_outputs *
                       (1.0 - hidden_outputs)), numpy.transpose(inputs))

        pass

    def query(self, inputs_list):
        """query the neural network"""
        # convert inputs list to 2d array
        inputs = numpy.array(inputs_list, ndmin=2).T

        # calculate signals into hidden layer
        hidden_inputs = numpy.dot(self.wih, inputs)
        # calculate the signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)

        # calcute signals into final output layer
        final_inputs = numpy.dot(self.who, hidden_outputs)
        # calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)

        return final_outputs


class cupyNetwork(neuralNetwork):
    """neural network class definition - cupy ver"""

    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        """initialise the neural network"""
        super().__init__(inputnodes, hiddennodes, outputnodes, learningrate)

        # link weight matrices, wih and who
        # weights inside the arrays are w_i_j, where link is from node i to node i to j in the next layer
        # w11 w21
        # w12 w22 etc
        self.wih = cupy.random.normal(
            0.0, pow(self.inodes, -0.5), (self.hnodes, self.inodes))
        self.who = cupy.random.normal(
            0.0, pow(self.hnodes, -0.5), (self.onodes, self.hnodes))

        #activation function is the sigmoid function
        self.activation_function = lambda x: 1 / (1 + cupy.exp(x) ** (-1))

    def train(self, inputs_list, targets_list):
        """train the neural network"""
        # convert inputs list to 2d array
        inputs = cupy.array(inputs_list, ndmin=2).T
        targets = cupy.array(targets_list, ndmin=2).T

        # calculate signals into hidden layer
        hidden_inputs = cupy.dot(self.wih, inputs)
        # calculate the signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)

        # calcute signals into final output layer
        final_inputs = cupy.dot(self.who, hidden_outputs)
        # calculate signals into final output layer
        final_outputs = self.activation_function(final_inputs)

        # output layer error is the (target - actual)
        output_errors = targets - final_outputs
        # hidden layer error is the output_errors, split by weights, recombined at hidden nodes
        hidden_errors = cupy.dot(self.who.T, output_errors)

        # update the weights for the links between the hidden and output layers
        # S' = S(1 - S)
        # dE / Dw = K * e * o * (1 - o)
        self.who += self.lr * cupy.dot((output_errors * final_outputs * (
            1.0 - final_outputs)), cupy.transpose(hidden_outputs))
        self.wih += self.lr * \
            cupy.dot((hidden_errors * hidden_outputs *
                      (1.0 - hidden_outputs)), cupy.transpose(inputs))

        pass

    def query(self, inputs_list):
        """query the neural network"""
        # convert inputs list to 2d array
        inputs = cupy.array(inputs_list, ndmin=2).T

        # calculate signals into hidden layer
        hidden_inputs = cupy.dot(self.wih, inputs)
        # calculate the signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)

        # calcute signals into final output layer
        final_inputs = cupy.dot(self.who, hidden_outputs)
        # calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)

        return final_outputs


class trainedNetwork(neuralNetwork):
    """trained network"""

    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate, wih, who):
        """
        Initialize the network
        Besides inodes, hnodes, onodes, lr, wih and who is needed, which 
            must be saved with numpy.savetxt and read by numpy.loadtxt
        Remember to match your nodes with saved w-matrix, don't make 
            mistakes or it may raise error. We don't like it, right?
        Have FUN! :)
                                                        Author: Lu Ruiqi
                                                               2021/9/10
        """
        super().__init__(inputnodes, hiddennodes, outputnodes, learningrate)

        self.wih = wih
        self.who = who
        
        self.activation_function = lambda x: scipy.special.expit(x)

    def query(self, inputs_list):
        """query the neural network"""
        # convert inputs list to 2d array
        inputs = numpy.array(inputs_list, ndmin=2).T

        # calculate signals into hidden layer
        hidden_inputs = numpy.dot(self.wih, inputs)
        # calculate the signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)

        # calcute signals into final output layer
        final_inputs = numpy.dot(self.who, hidden_outputs)
        # calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)

        return final_outputs



def train_numpy(n, training_data_list, onodes=10, epochs=5):
    """
    train the network with data

    n = train_numpy(n, training_data_list, onodes=10, epochs=5)
    
    Args:
        n                 : network to be trained
        training_data_list: pre-processed data list
        onodes            : output nodes, default 10
        epochs            : how many times U wanna train the net, default 5

    Return:
        n                 : network trained
    """

    # train the neural network
    print("Training...")

    for e in range(epochs):
        print("Epoch:", e)
        # go through all records in the training data set
        for record in training_data_list:
            # split the tecord by the ',' commas
            all_values = record.split(',')
            # scale and shift the inputs
            inputs = (numpy.asfarray(all_values[1:]) / 255 * 0.99) + 0.01
            # create the target output values (all 0.01, except the desired lavel which is 0.99)
            targets = numpy.zeros(onodes) + 0.01
            # all_values[0] is the target lavel for this record
            targets[int(all_values[0])] = 0.99
            n.train(inputs, targets)

            # create rotated variations
            # rotated anticlockwise by x degrees
            inputs_plusx_img = scipy.ndimage.interpolation.rotate(
                inputs.reshape(28, 28), 10, cval=0.01, order=1, reshape=False)
            n.train(inputs_plusx_img.reshape(784), targets)
            # rotated clockwise by x degrees
            inputs_minusx_img = scipy.ndimage.interpolation.rotate(
                inputs.reshape(28, 28), -10, cval=0.01, order=1, reshape=False)
            n.train(inputs_minusx_img.reshape(784), targets)

    return n


def train_cupy(n, training_data_list, onodes=10, epochs=5):
    """
    train the neural network - cupy ver

    n = train_cupy(n, training_data_list, onodes=10, epochs=5)
    
    Args:
        n                 : network to be trained
        training_data_list: pre-processed data list
        onodes            : output nodes, default 10
        epochs            : how many times U wanna train the net, default 5

    Return:
        n                 : network trained
    """

    print("Training...")

    # epochs is the number of times the training data set is used for training
    epochs = 5

    for e in range(epochs):
        print("Epoch:", e)
        # go through all records in the training data set
        for record in training_data_list:
            # split the tecord by the ',' commas
            all_values = record.split(',')
            temp = list(map(eval, all_values[1:]))
            # scale and shift the inputs
            inputs = (cupy.asarray(temp) / 255 * 0.99) + 0.01
            # create the target output values (all 0.01, except the desired lavel which is 0.99)
            targets = cupy.zeros(onodes) + 0.01
            # all_values[0] is the target lavel for this record
            targets[int(all_values[0])] = 0.99
            n.train(inputs, targets)

            # create rotated variations
            # rotated anticlockwise by x degrees
            inputs_plusx_img = cupyx.scipy.ndimage.interpolation.rotate(
                inputs.reshape(28, 28), 10, cval=0.01, order=1, reshape=False)
            n.train(inputs_plusx_img.reshape(784), targets)
            # rotated clockwise by x degrees
            inputs_minusx_img = cupyx.scipy.ndimage.interpolation.rotate(
                inputs.reshape(28, 28), -10, cval=0.01, order=1, reshape=False)
            n.train(inputs_minusx_img.reshape(784), targets)

    return n


def load_datasets(filepath):
    """
    load the mnist data CSV file into a list

    data_list = load_datasets(filepath)

    Arg:
        filepath: the path of a csv file which contains img data

    Return:
        data_list: the data got from the file
    """

    data_file = open(filepath, 'r')
    data_list = data_file.readlines()
    data_file.close()

    return data_list


def test_network(n, test_data_list):
    """
    test the neural network

    scorecard = test(n, test_data_list)
    
    Args:
        n             : trained network
        test_data_list: pre-processed data list

    Return:
        scorecard     : list object, 0 for wrong and 1 for right
    """

    print("Testing...")

    # scorecard for how well the network performs, initially empty
    scorecard = []

    # go through all the records in the test data set
    for record in test_data_list:
        # split the record by the ',' commas
        all_values = record.split(',')
        # correct answer is first value
        correct_label = int(all_values[0])
        # scale and shift the inputs
        inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
        # query the network
        outputs = n.query(inputs)
        # the index of the highest value corresponds to the label
        label = numpy.argmax(outputs)
        # append correct or incorrect to list
        if (label == correct_label):
            # network's answer matches correct answer, add 1 to scorecard
            scorecard.append(1)
        else:
            # network's answer doesn't match correct answer, add 0 to scorecard
            scorecard.append(0)

    return scorecard

def calculate_performance(scorecard):
    """
    calculate the performance score, the fraction of correct answers

    performance = calculate_performance(scorecard)

    Arg:
        scorecard  : list object, 0 for wrong and 1 for right

    Return:
        performance: float object, right / (right + wrong)
    """
    
    scorecard_array = numpy.asarray(scorecard)
    performance = scorecard_array.sum() / scorecard_array.size

    return performance


def save_w_matrix(wih, who, epochs=5, hnodes=400, path='saved_data/', iscupy=False):
    """
    save weights matrix of trained network

    save_w_matrix(wih, who, epochs=5, hnodes=400, path='saved_data/', iscupy=False)

    Args:
        wih   : weights between input layer and hidden layer
        who   : weights between hidden layer and output layer
        epochs: times U trained the net, default 5
        hnodes: hidden nodes, default 400 ('cause I always use 400)
        path  : path U wanna save the datas, default 'saved_data/'
        iscupy: whether the weights are from cupy network
    """
    
    print("Saving Data...")

    t = time.asctime(time.localtime(time.time()))
    t = t.replace(':', '_')

    filepath = path + t + "/"
    try:
        os.mkdir(filepath)
    except:
        pass
    filename_wih = f"hn{hnodes}_wih_epoch_{epochs}.csv"
    filename_who = f"hn{hnodes}_who_epoch_{epochs}.csv"

    if iscupy:
        wih = cupy.asnumpy(wih)
        who = cupy.asnumpy(who)

    numpy.savetxt(filepath + filename_wih, wih)
    numpy.savetxt(filepath + filename_who, who)
    print("Saving Succeeded!")

def read_w_matrix(filepath, hnodes=400, epochs=5):
    """
    read weights matrix of trained network

    wih, who = read_w_matrix(filepath, hnodes=400, epochs=5)
    
    Args:
        filepath: path U saved the datas
        hnodes:   hidden nodes, default 400
        epochs:   times U trained the net, default 5

    Returns:
        wih
        who
    """
    
    filename_wih = filepath + f"hn{hnodes}_wih_epoch_{epochs}.csv"
    filename_who = filepath + f"hn{hnodes}_who_epoch_{epochs}.csv"
    wih = numpy.loadtxt(filename_wih)
    who = numpy.loadtxt(filename_who)

    return wih, who


def img2data(filename, show=False):
    """
    turn 28*28 hand-written num img to data which can be used by the net

    img_data = img2data(filename, show=False)
    
    Arg:
        filename: *Please name the file like "1.png", "6.png"
        show    : show img with matplotlib.pyplot.imshow, default False

    Return:
        img_data: converted data, including label in position 0
    """

    print("loading", filename, "...")
    # use the filename to set the correct label
    label = int(filename[-5: -4])
    # load image data from png files into an array
    img_array = imageio.imread(filename, as_gray=True)
    # reshape from 28×28 to list of 784 values, invert values
    img_data = 255.0 - img_array.reshape(784)
    # then scale data to range from 0.01 to 1.0
    img_data = (img_data / 255.0 * 0.99) + 0.01

    # append label and image data to test data set
    img_data = numpy.append(label, img_data)

    if show:
        matplotlib.pyplot.figure()
        matplotlib.pyplot.imshow(255 - img_array, cmap='Greys', interpolation='None')
        matplotlib.pyplot.title(f"{label}")

    return img_data

def testsingle(n, img_data, show=False):
    """
    test a single pic

    result = testsingle(n, img_data)

    Args:
        n       : network
        img_data: converted img data with label
        show    : show img with matplotlib.pyplot.imshow, default False

    Return:
        result: True for right and False for wrong
    """

    true_label = img_data[0]
    inputs = img_data[1:]
    outputs = n.query(inputs)
    # the index of the highest value corresponds to the label
    label = numpy.argmax(outputs)

    if show:
        matplotlib.pyplot.figure()
        matplotlib.pyplot.imshow(inputs.reshape(28, 28), cmap='Greys', interpolation='None')
        matplotlib.pyplot.title(
            "True     : {:.00f}\nPredicted: {:.00f}".format(true_label, label))
    else:
        print("True     : {:.00f}".format(true_label))
        print("Predicted: {:.00f}".format(label))

    return label == true_label
