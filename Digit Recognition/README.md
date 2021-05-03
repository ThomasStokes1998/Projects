# MNIST Digit Recongition
Using the well known data set of handwritten digits from MNIST. I built a convolution neural network (CNN) to classify the images. The CNN was done for a Kaggle competition
involving the dataset. The competition can be found here: https://www.kaggle.com/c/digit-recognizer. I decided to enter this competition so that I could teach myself how to
code neural networks using TensorFlow. Before entering this competition, I understood the maths behind neural networks -including the convolution layers- (from my maths degree).
* CNN accuracy: 98.6%

# Pneumonia Classification
On Kaggle there is dataset with thousands of images of X-rays of patients with Pneumonia and healthy lungs. To create an image classifier for this I tried a lot different pre-
trained models in Keras. After trying a lot of different pretrained models and some I made myself, I found that DenseNet121 was the best. DenseNet121 was the only neural network
that sucessfully predicted all the 16 images on the validation dataset. VGG16, Xception and Inception managed to get 15/16 images. 
