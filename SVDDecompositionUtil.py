# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 18:56:37 2014

@author: chris
"""
from PIL import Image
import matplotlib.pyplot as plt
import pyparsing
import sys
import getopt
import numpy
import scipy.misc

class SVDDecompositionUtil(object):
    
    def __init__(self):
        # string path to the image that we need to load into memory
        self.pathToTargetImage = None
        # display name of image
        self.displayName = None
        # original color imported image
        self.importedImageAsArray = None
        # imported image converted to grayscale
        self.importedImageGrayScale = None
        # image as a matrix
        self.imageMatrix = None
        #
        # SVD components
        #
        # U
        self.leftOrthogonalVector = None
        # V
        self.rightOrthogonalVector = None
        # S
        self.singularValues = None

    """
        This is a command-line method for inputing a non default image. 
        The default is the "Lena" image processing gold standard image
        
    """    
    def main(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'i:h', ['image=', 'help'])
        except getopt.GetoptError:
            sys.exit(2)
        # get all the parameters to run a test with SVD decomposition
        for o, a in opts:
            if o in ("-h", "--help"):
                self.usage();
                sys.exit(0)
            elif o in ("-i", "--image"):
                # set the fully qualified path to the image
                self.pathToTargetImage = a
                self.displayName = self.pathToTargetImage.split(".")[0].split("\\")[-1] 
                # loading the target image
                self.loadTargetImage()
            else:
                sys.exit(2)
        # loading the default target Lena image from scipy
        if(None==self.pathToTargetImage):
            self.loadDefaultTargetImage()
            self.displayName = "Lena"
        # SVD factorization of the image
        self.decomposeTargetImage()
        # plotting target image
        self.plotImage()

    def usage(self):
        print "<SVDDecompositionUtil.py> [options]\n\n"
        print "Options:\n\n"
        print "(-i or --image=) the fully qualified string path to the image."
        print "                 OPTIONAL: a default is set from SciPy.\n\n"
        
        print "(-h or --help) print this usage dialog."
                
    """
        This method loads a target image from file in grayscale.
    """        
    def loadTargetImage(self):
        if(None == self.pathToTargetImage):
            return
        # convert image to grayscale
        self.importedImageGrayScale = Image.open(self.pathToTargetImage).convert('LA') 
        print "The image, located at: %s, is loaded as a numerical array for processing." % (self.pathToTargetImage)

    """
        This method loads the built-in "Lena" image in grayscale.
    """        
    def loadDefaultTargetImage(self):
        self.importedImageAsArray = scipy.misc.lena()
        # convert image to grayscale
        self.importedImageGrayScale = self.importedImageAsArray 
        print "The image, located at: %s, is loaded as a numerical array for processing." % (self.pathToTargetImage)

    
    """ 
        This method reshapes the data loaded from the input image into a 2-D numpy array, 
        and decomposes the image into a SVD factorization: [U,S,V]
    """    
    def decomposeTargetImage(self):
        if(None!=self.pathToTargetImage):
            # reshaping  grayscale image to massage into the SVD method
            self.imageMatrix = numpy.array(list(self.importedImageGrayScale.getdata(band=0)), float)
            self.imageMatrix.shape = (self.importedImageGrayScale.size[1], self.importedImageGrayScale.size[0])
            self.imageMatrix = numpy.matrix(self.imageMatrix)
        else:
            # using the default scipy lena image
            self.imageMatrix = numpy.array(self.importedImageGrayScale)
        [self.leftOrthogonalVector, self.singularValues, self.rightOrthogonalVector] = numpy.linalg.svd(self.imageMatrix, full_matrices=True)
        print "The loaded image has been factorized with %d singular values." % (len(self.singularValues))

    """
        This method test plots successive reconstructions of "Lena" up to the fully reconstructed image.
    """
    def plotImage(self):
        plt.figure(1)
        plt.subplot(231)
        plt.imshow(self.importedImageGrayScale, cmap='gray')
        plt.title("Original %s Grayscale" % (self.displayName))
        plt.subplot(232)        
        plt.imshow(self.reconstructTargetImage(int(0.05*len(self.singularValues))), cmap='gray')
        plt.title("%s Keeping 5 Percent Singular Values" % (self.displayName))        
        plt.subplot(233)
        plt.imshow(self.reconstructTargetImage(int(0.10*len(self.singularValues))), cmap='gray')
        plt.title("%s Keeping 10 Percent Values" % (self.displayName))
        plt.subplot(234)
        plt.imshow(self.reconstructTargetImage(int(0.25*len(self.singularValues))), cmap='gray')
        plt.title("%s Keeping 25 Percent Values" % (self.displayName))
        plt.subplot(235)
        plt.imshow(self.reconstructTargetImage(int(0.50*len(self.singularValues))), cmap='gray')
        plt.title("%s Keeping 50 Singular Values" % (self.displayName))        
        plt.subplot(236)
        plt.imshow(self.reconstructTargetImage(len(self.singularValues)), cmap='gray')
        plt.title("%s Fully Reconstructed" % (self.displayName))
        plt.show()

    """
        This method reconstructs the data represented by the SVD decomposition [U,S,V] by
        only keeping the number of singular values (highest order) indicated. 
        
        Note: A full reconstruction of the image can be achieved with this method.
        
        @param: numSingularValuesKept (int) the number of higher order singular values that is retained
        
        @return: reconstructedImageGrayScale (numpy matrix) The partially or fully reconstructed image.
        
    """
    def reconstructTargetImage(self, numSingularValuesKept):
        reconstructedImageGrayScale = numpy.matrix(self.leftOrthogonalVector[:, :numSingularValuesKept]) * numpy.diag(self.singularValues[:numSingularValuesKept]) * numpy.matrix(self.rightOrthogonalVector[:numSingularValuesKept, :])
        return reconstructedImageGrayScale    
    
if __name__ =='__main__':
    sutil = SVDDecompositionUtil()
    sutil.main()

