import networkx as nx
import random
import pandas as pd
from sklearn.metrics import precision_recall_curve, auc
import datetime as dt
import operator

print(f"Start Time: {str(dt.datetime.now().time())}")
random.seed(50)
# graph = nx.dorogovtsev_goltsev_mendes_graph(7)
graph = nx.read_graphml("./twigsEgoGraph.graphml")
graph = graph.to_undirected()
#Get the edges and split into G_training and G_test
for k in [5, 10, 15, 20]:
    #k = 60
    edgesFull = list(graph.edges())
    testEdges = random.sample(edgesFull, k) #Take 15% of edges away
    trainingEdges = list(set(edgesFull) - set(testEdges))

    #Need to add random edges

    G_training = graph.copy()
    G_training.remove_edges_from(testEdges)
    G_testing = graph.copy()
    G_testing.remove_edges_from(trainingEdges)

    pred1 = nx.adamic_adar_index(G_training)
    print("Done prediction 1")
    pred2 = nx.resource_allocation_index(G_training)
    print("Done prediction 2")
    pred3 = nx.jaccard_coefficient(G_training)
    print("Done prediction 3")
    pred4 = nx.preferential_attachment(G_training)
    print("Done prediction 4")
    # pred5 = nx.common_neighbor_centrality(G_training)
    # print("Done prediction 5")

    listOfPredictions = [pred1, pred2, pred3, pred4]
    predictionNames = ["adamic_adar_index", "resource_allocation_index", "jaccard_coefficient", "preferential_attachment", "common_neighbor_centrality"]
    countPred = 0
    for linkPred in listOfPredictions:
        print(f" The predictor being used now is : {predictionNames[countPred]}")

        # need to sort the list of tuples based on the last value
        sortedPred = sorted(linkPred, key=operator.itemgetter(2), reverse=True)
        # topPredictionsLinks = [(k, v) for k,v,n in sortedPred]
        predictions = sortedPred[0:k]
        #print(predictions[k - 1])

        # First y_true, y_pred

        y_true = list()
        y_pred = list()
        thresholds = list()

        for a, b, c in predictions:
            if (a, b) in set(testEdges) or (b, a) in set(testEdges):
                y_true.append(1)
                y_pred.append(c)
                #print("There's a positive")
            else:
                y_true.append(0)
                y_pred.append(c)
            thresholds.append(c)

        # Calculate the precision and recall at each threshold
        Recall = list()
        Precision = list()
        for index in range(1, len(predictions) + 1):
            values = predictions[0:index]
            topPredictionsLinks = [(k, v) for k, v, n in values]
            # topPredictionsLinksReversed = [(v, k) for k,v,n in values]
            # topPredictionsLinks.extend(topPredictionsLinksReversed)

            TP = len([k for k in y_true[0:index] if k == 1])
            FP = len([k for k in y_true[0:index] if k == 0])

            FN = len(list(set(testEdges).difference(set(topPredictionsLinks))))

            Recall.append((TP) / ((TP) + (FN)))
            Precision.append((TP) / ((TP) + (FP)))
        print(f"The array lengths are thresholds {len(thresholds)}, recall {len(Recall)}, precision {len(Precision)}")
        df = pd.DataFrame({"Thresholds": thresholds, "Recall": Recall, "Precision": Precision})
        df = df.T
        print(df)

        aupr_score = auc(Recall, Precision)
        print(f"The aupr_score for {predictionNames[countPred]} Threshold K = {k} is {aupr_score}")
        countPred += 1

print(f"End Time: {str(dt.datetime.now().time())}")




