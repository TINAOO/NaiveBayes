from collections import defaultdict
import numpy as np

def file_reader(file_path, label):
    list_of_lines = []
    list_of_labels = []

    for line in open(file_path):
        line = line.strip()
        if line=="":
            continue
        list_of_lines.append(line)
        list_of_labels.append(label)


    return (list_of_lines, list_of_labels)


def data_reader(source_directory):
    

    positive_file = source_directory+"Positive.txt"
    (positive_list_of_lines, positive_list_of_labels)=file_reader(file_path=positive_file, label=1)

    negative_file = source_directory+"Negative.txt"
    (negative_list_of_lines, negative_list_of_labels)=file_reader(file_path=negative_file, label=-1)

    neutral_file = source_directory+"Neutral.txt"
    (neutral_list_of_lines, neutral_list_of_labels)=file_reader(file_path=neutral_file, label=0)

    list_of_all_lines = positive_list_of_lines + negative_list_of_lines + neutral_list_of_lines
    list_of_all_labels = np.array(positive_list_of_labels + negative_list_of_labels + neutral_list_of_labels)


    return list_of_all_lines, list_of_all_labels


def evaluate_predictions(test_set,test_labels,trained_classifier):
    correct_predictions = 0
    predictions_list = []
    prediction = -1
    for dataset,label in zip(test_set, test_labels):
        probabilities = trained_classifier.predict(dataset)
        if probabilities[0] >= probabilities[1] and probabilities[0] >= probabilities[-1]:
            prediction = 0
        elif  probabilities[1] >= probabilities[0] and probabilities[1] >= probabilities[-1]:
            prediction = 1
        else:
            prediction=-1
        if prediction == label:
            correct_predictions += 1
            predictions_list.append("+")
        else:
            predictions_list.append("-")
    
    print("Total Sentences correctly: ", len(test_labels))
    print("Predicted correctly: ", correct_predictions)
    print("Accuracy: {}%".format(round(correct_predictions/len(test_labels)*100,5)))

    return predictions_list, round(correct_predictions/len(test_labels)*100)


class NaiveBayesClassifier(object):
    def __init__(self, n_gram=1, printing=False):
        self.prior = defaultdict(int)
        self.logprior = {}
        self.train_data = defaultdict(list)
        self.loglikelihoods = defaultdict(defaultdict)
        self.V = []
        self.n = n_gram

    

    def compute_vocabulary(self, training_sentences):
        vocabulary = set()

        for sentence in training_sentences:
            for word in sentence.split(" "):
                vocabulary.add(word.lower())

        return vocabulary

    def count_word_in_classes(self):
        counts = {}
        for c in list(self.train_data.keys()):
            sentences = self.train_data[c]
            counts[c] = defaultdict(int)
            for sent in sentences:
                words = sent.split(" ")
                for word in words:
                    counts[c][word] += 1

        return counts

    def train(self, training_sentences, training_labels):
        # Get number of sentences in the training set
        N_sentences = len(training_sentences)

        # Get vocabulary used in training set
        self.V = self.compute_vocabulary(training_sentences)

        # Create thre complete training data by combining the training labels with the training sentences
        for x, y in zip(training_sentences, training_labels):
            self.train_data[y].append(x)

        # Get set of all classes
        all_classes = set(training_labels)

        # Compute a dictionary with all word counts for each class
        self.word_count = self.count_word_in_classes()


        
        
        #add code
        #compute the log likelihood and priors from traing data
                #compute the log likelihood and priors from traing data
        #-----------------------#
        #You need to find the log probabiltiy each label and save them in self.logprior, 
        #so that self.logprior[-1] will store the value of the log probablity of Negative Sentitment.#

        #You need to find the log probabiltiy of a word being in a class c and save them in self.loglikelihoods, 
        #so that self.loglikelihoods[-1]["bad"] will store the value of the log probablity of seeing the word "bad" 
        #in sentence with Negative Sentitment.#

        #Debugging Tips: print the variable self.logprior and 
        #check if it is storing the the expected log probablity values for that class.#
        #-----------------------#
        for c in all_classes:
            total = sum(training_labels == c)
            Num = float(total) # change the total number to float for further calcualtion
            self.logprior[c] = np.log(Num/N_sentences) # calculate logprior
            #total wrods in one class
            total_words = 0
            for vocabulary in self.V:
                total_words = total_words + self.word_count[c][vocabulary]
            #use total words to calculate loglikelihoods
            for vocabulary in self.V:
                number = self.word_count[c][vocabulary]
                self.loglikelihoods[c][vocabulary] = np.log((number+1)/(total_words+1*len(self.V)))

        

    def predict(self, test_sentence):
        label_probability = {
            0: 0,
            1: 0,
            -1:0,
        }
        words = test_sentence.split(" ")

       
        #add code
        # return a dictionary of log probablity for each class for a given test sentence: 
        # i,e, {0: -39.39854137691295, 1: -41.07638511893377, -1: -42.93948478571315}

        for c in self.train_data.keys():
            label_probability[c] = self.logprior[c]
            for vocabulary in words:
                if vocabulary in self.V:
                    label_probability[c] =label_probability[c]+ self.loglikelihoods[c][vocabulary]
        return label_probability



if __name__ == '__main__':
    train_folder = "data-sentiment/train/"
    test_folder = "data-sentiment/test/"

    training_sentences, training_labels = data_reader(train_folder)
    test_sentences, test_labels = data_reader(test_folder)

    NBclassifier = NaiveBayesClassifier(n_gram=1)
    NBclassifier.train(training_sentences,training_labels)


    results, acc = evaluate_predictions(test_sentences, test_labels, NBclassifier)



