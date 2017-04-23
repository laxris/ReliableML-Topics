import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


objects = ('Support vector machine', 'Neural network', 'Data set', 'Objective function', 'Markov random field',
           'Feature space', 'Generative model', 'Linear matrix inequality', 'Gaussian mixture model',
           'Principal component analysis',
           'Hidden Markov model', 'Conditional random field', 'Graphical model', 'Maximum likelihood estimation',
           'Clustering algorithm', 'Nearest neighbors', 'Genetic algorithm', 'Latent Dirichlet allocation',
           'Gaussian process', 'Markov chain Monte Carlo')




x_pos = np.arange(len(objects))
performance = [2843.345, 2611.812, 2535.371, 1564.559, 1331.183, 1240.299, 1164.988, 1160.347, 1127.093, 1108.188,
               1045.296, 888.876, 647.043, 646.373, 631.9550, 535.544, 502.833, 499.561, 482.44, 425.27]

width = 1/1.5
plt.bar(x_pos, performance, width, color=['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black',
                                          'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey'])
plt.xticks(x_pos + 0.25, objects, rotation='vertical')
plt.ylabel('Score')
plt.tight_layout()

plt.savefig('bar.eps')