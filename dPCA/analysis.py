# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/03_Analysis.ipynb.

# %% auto 0
__all__ = ['ACM_analysis', 'PACM_analysis', 'Analysis']

# %% ../nbs/03_Analysis.ipynb 2
import pandas as pd
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from .lag import *
from .corrmat import *
from .TEP import *

# %% ../nbs/03_Analysis.ipynb 4
def ACM_analysis(X: pd.DataFrame, # Raw data to perform analysis on
                lag: int # Number of lags to investigate
                )-> dict: # Dict with eigenvalues
    
    res_dict = {}
    
    for i in range(lag+1):
        eigenValues, eigenVectors = np.linalg.eig(ACM(X,i))
        idx_abs = abs(eigenValues).argsort()[::-1]
        eigenValues = abs(eigenValues)[idx_abs]
        eigenVectors = np.real(eigenVectors)[idx_abs]
        res_dict['EigenValues',i] = eigenValues
        res_dict['EigenVectors',i] = eigenVectors
    return res_dict


# %% ../nbs/03_Analysis.ipynb 5
def PACM_analysis(X: pd.DataFrame, # Raw data to perform analysis on
                lag: int # Number of lags to investigate
                )-> dict: # Dict with eigenvalues
    res_dict = {}
    for i in range(lag+1):
        eigenValues, eigenVectors = np.linalg.eig(PACM(X,i))
        idx_abs = abs(eigenValues).argsort()[::-1]
        eigenValues = abs(eigenValues)[idx_abs]
        eigenVectors = np.real(eigenVectors)[idx_abs]
        res_dict['EigenValues', i] = eigenValues
        res_dict['EigenVectors', i] = eigenVectors
    return res_dict

# %% ../nbs/03_Analysis.ipynb 6
class Analysis:
    def __init__(self, X, lag):
        self.X = X
        self.lag = lag
        self.imposter = imposter_matrix(X)
        self.PACM = PACM_analysis(X, lag)
        self.PACM_imposter = PACM_analysis(self.imposter,lag)
        self.ACM = ACM_analysis(X, lag)
        self.ACM_imposter = ACM_analysis(self.imposter, lag)
    
    def show_plots(self):
        
        fig, axs = plt.subplots(1,2, figsize = (10,5))
        
        for i in range(self.lag+1):
            axs[0].scatter(i, self.ACM['EigenValues',i][0], c = 'blue')
            axs[0].scatter(i, self.ACM_imposter['EigenValues',i][0], c = 'red', marker = 'x')
            axs[0].set_title('Autocorrelation Matrix Eigenvalues', fontweight = 'bold')
            axs[0].set_xlabel('Lag')
            axs[0].set_ylabel('Largest Absolute Eigenvalue')
            axs[0].legend(['Data','Imposter'])
            
            axs[1].scatter(i, self.PACM['EigenValues',i][0], c = 'blue')
            axs[1].scatter(i, self.PACM_imposter['EigenValues',i][0], c = 'red', marker = 'x')
            axs[1].set_title('Partial Autocorrelation Matrix Eigenvalues', fontweight = 'bold')
            axs[1].set_xlabel('Lag')
            axs[1].set_ylabel('Largest Absolute Eigenvalue')
            axs[1].legend(['Data','Imposter'])

        
