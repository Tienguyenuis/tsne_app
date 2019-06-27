import numpy as np
import pandas as pd
import csv
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA # Principal Component Analysis module
from sklearn.manifold import TSNE # TSNE module
from reformatting import find_labels, sort_format_data, sort_format_labels, delete_duplicates, multi_label_nodes, add_nodes_embedding

def tsne_visualize(datafile, labelfile, num_iter):
    
    try:
        sort_format_data(datafile)
        sort_format_labels(labelfile)
    except:
        print('Failed to sort and format')
    else:
        add_nodes_embedding(datafile, labelfile)


    path_datafile = 'embeddingfiles/formattedfiles/formatted_' + datafile + '.csv'
    path_labelfile = 'labelfiles/formattedfiles/formatted_' + labelfile

    missing_nodes, length = find_labels(path_datafile, path_labelfile)
    labels_data = pd.read_csv(path_labelfile, sep=',', error_bad_lines=False)
    target = labels_data.iloc[0:length,1]

    target = target.drop(missing_nodes)


    data = pd.read_csv(path_datafile, error_bad_lines=False)
    data.head()
    data = data.fillna(value=0)

    X = data.values

    label_list = delete_duplicates(target)

    tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=int(num_iter))
    tsne_results = tsne.fit_transform(X)

    plt.figure(figsize = (16,11))   

    scatter = plt.scatter(tsne_results[:,0],tsne_results[:,1],  c = target, 
                cmap=plt.cm.get_cmap("jet", max(label_list)), edgecolor = "None", alpha=0.35)

    plt.colorbar(ticks=range(max(label_list)))
    plt.clim(0.5, max(label_list))

    plt.title(datafile + str(num_iter))
    plt.savefig('tsne_images/' + datafile + str(num_iter) + '.png')


#tsne_visualize('deepwalk-PubMed-edgelist.txt.embeddings', 'PubMed-labels.csv', 1000)

