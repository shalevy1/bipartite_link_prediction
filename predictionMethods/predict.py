from _operator import itemgetter
from collections import defaultdict
from datetime import datetime

import networkx as nx

from helperFunctions.getAdjacents import getAdj2
from predictionMethods.algorithms import adamic_adar, common_neighbors, preferential_attachment, katz_similarity, \
    jaccard


def jc_predict(G):
    start_jc = datetime.now()

    # print('Jaccard prediction starting...')
    dictionary = {}
    out = open('./predictions/jaccard.csv', 'w')
    outN = open('./predictions/jaccard_with_name.csv', 'w')
    hop2s = dict()
    neighbors = dict()
    jaccard_sim = defaultdict(dict)
    left_set = [n for n, d in G.nodes(data=True) if d['bipartite'] == 0]
    right_set = [n for n, d in G.nodes(data=True) if d['bipartite'] == 1]

    out.write('(left_element, right_element)')
    out.write(",")
    out.write('Probability')
    out.write("\n")

    # outN.write('(left_element, right_element)')
    # outN.write(",")
    # outN.write('Probability')
    # outN.write("\n")
    exception_count = 0
    for left_element in left_set:
        hop2s[left_element] = getAdj2(G, list(set(G[left_element])), 1)
        for right_element in right_set:
            neighbors[right_element] = list(set(G[right_element]))
            if not (left_element, right_element) in G.edges:
                try:
                    jaccard_sim[left_element][right_element] = jaccard(hop2s[(left_element)],
                                                                       neighbors[(right_element)])
                    if jaccard_sim[left_element][right_element] > 0:
                        dictionary.update({(left_element, right_element): jaccard_sim[left_element][right_element]})
                except:
                    exception_count += 1
                    print(exception_count)

    for k, v in sorted(dictionary.items(), key=itemgetter(1), reverse=True):
        # print(k[0],v)
        out.write(str((k[0], k[1])))
        out.write(",")
        out.write(str(jaccard_sim[k[0]][k[1]]))
        out.write("\n")

        # outN.write(str((df_nodes[k[0]], df_nodes[k[1]])))
        # outN.write(",")
        # outN.write(str(jaccard_sim[k[0]][k[1]]))
        # outN.write("\n")
    # print('Jaccard prediction finished sucnessfully')
    end_jc = datetime.now()
    # print('Jaccard duration: {}'.format(end_jc - start_jc), "\n")
    return dictionary


def aa_predict(G):
    start_aa = datetime.now()

    # print('Adamic_adar prediction starting...')

    out = open('./predictions/adamic_adar.csv', 'w')
    outN = open('./predictions/adamic_adar_with_name.csv', 'w')
    hop2s = dict()
    neighbors = dict()
    aa_sim = defaultdict(dict)
    sortDic = {}
    left_set = [n for n, d in G.nodes(data=True) if d['bipartite'] == 0]
    right_set = [n for n, d in G.nodes(data=True) if d['bipartite'] == 1]
    # print('left side: ', left_set.__len__())
    dictionary = {}
    out.write('(left_element, right_element)')
    out.write(",")
    out.write('Probability')
    out.write("\n")

    # outN.write('(left_element, right_element)')
    # outN.write(",")
    # outN.write('Probability')
    # outN.write("\n")
    exception_count = 0
    for left_element in left_set:
        hop2s[left_element] = getAdj2(G, list(set(G[left_element])), 1)
        for right_element in right_set:
            neighbors[right_element] = list(set(G[right_element]))
            if not (left_element, right_element) in G.edges:
                try:
                    aa_sim[left_element][right_element] = adamic_adar(hop2s[(left_element)],
                                                                      neighbors[(right_element)], G)
                    if aa_sim[left_element][right_element] > 0:
                        # print(left_element, right_element, aa_sim[left_element][right_element])
                        dictionary.update({(left_element, right_element): aa_sim[left_element][right_element]})
                except:
                    exception_count += 1
                    print(exception_count)


    for k, v in sorted(dictionary.items(), key=itemgetter(1), reverse=True):
        # print(k[0],v)
        out.write(str((k[0], k[1])))
        out.write(",")
        out.write(str(aa_sim[k[0]][k[1]]))
        out.write("\n")

        # outN.write(str((df_nodes[k[0]], df_nodes[k[1]])))
        # outN.write(",")
        # outN.write(str(aa_sim[k[0]][k[1]]))
        # outN.write("\n")
    # print('Adamic-adar prediction finished sucnessfully')
    end_aa = datetime.now()
    # print('Adamic-adar duration: {}'.format(end_aa - start_aa), "\n")
    return dictionary


def cn_predict(G):
    start_cn = datetime.now()

    # print('Common neighbor prediction starting...')

    out = open('./predictions/common_neighbor.csv', 'w')
    outN = open('./predictions/common_neighbor_with_name.csv', 'w')
    hop2s = dict()
    neighbors = dict()
    cn_sim = defaultdict(dict)
    sortDic = {}

    left_set = [n for n, d in G.nodes(data=True) if d['bipartite'] == 0]
    right_set = [n for n, d in G.nodes(data=True) if d['bipartite'] == 1]

    dictionary = {}
    out.write('(left_element, right_element)')
    out.write(",")
    out.write('Probability')
    out.write("\n")

    # outN.write('(left_element, right_element)')
    # outN.write(",")
    # outN.write('Probability')
    # outN.write("\n")

    for left_element in left_set:
        # print('snp {} -- '.format(len(G[left_element])))
        hop2s[left_element] = getAdj2(G, list(set(G[left_element])), 1)
        # print('snp hop 2 {} -- '.format(len(hop2s[left_element])))
        for right_element in right_set:
            # print('cancer {} -- '.format(len(G[right_element])))
            neighbors[right_element] = list(set(G[right_element]))
            if not (left_element, right_element) in G.edges:
                cn_sim[left_element][right_element] = common_neighbors(hop2s[left_element],
                                                                       neighbors[right_element])

                # if (left_element, right_element) in edge_subset:
                #   print((left_element, right_element), cn_sim[left_element][right_element])
                if cn_sim[left_element][right_element] > 0:
                    dictionary.update({(left_element, right_element): cn_sim[left_element][right_element]})

    for k, v in sorted(dictionary.items(), key=itemgetter(1), reverse=True):
        # print(k[0],v)
        out.write(str((k[0], k[1])))
        out.write(",")
        out.write(str(cn_sim[k[0]][k[1]]))
        out.write("\n")
    #
    #     outN.write(str((df_nodes[k[0]], df_nodes[k[1]])))
    #     outN.write(",")
    #     outN.write(str(cn_sim[k[0]][k[1]]))
    #     outN.write("\n")
    # print('Common neghbor prediction finished sucnessfully')
    end_cn = datetime.now()
    # print('Common neghbor duration: {}'.format(end_cn - start_cn), "\n")
    return dictionary


def pa_predict(G):
    start_pa = datetime.now()
    # print('Preferential_attachment prediction starting...')
    dictionary = {}
    out = open('./predictions/preferential_attachment.csv', 'w')
    outN = open('./predictions/preferential_attachment_with_name.csv', 'w')
    hop2s = dict()
    neighbors_right_element = dict()
    neighbors_left_element = dict()
    pa_sim = defaultdict(dict)
    sortDic = {}
    left_set = [n for n, d in G.nodes(data=True) if d['bipartite'] == 0]
    right_set = [n for n, d in G.nodes(data=True) if d['bipartite'] == 1]

    out.write('(left_element, right_element)')
    out.write(",")
    out.write('Probability')
    out.write("\n")

    # outN.write('(left_element, right_element)')
    # outN.write(",")
    # outN.write('Probability')
    # outN.write("\n")

    for left_element in left_set:
        # hop2s[left_element] = getAdj2(G, list(set(G[left_element])), 1)
        neighbors_left_element[left_element] = list(set(G[left_element]))
        for right_element in right_set:
            neighbors_right_element[right_element] = list(set(G[right_element]))
            if not (left_element, right_element) in G.edges:
                pa_sim[left_element][right_element] = preferential_attachment(
                    neighbors_left_element[(left_element)], neighbors_right_element[(right_element)])
                if pa_sim[left_element][right_element] > 0:
                    dictionary.update({(left_element, right_element): pa_sim[left_element][right_element]})

    for k, v in sorted(dictionary.items(), key=itemgetter(1), reverse=True):
        # print(k[0],v)
        out.write(str((k[0], k[1])))
        out.write(",")
        out.write(str(pa_sim[k[0]][k[1]]))
        out.write("\n")

        # outN.write(str((df_nodes[k[0]], df_nodes[k[1]])))
        # outN.write(",")
        # outN.write(str(pa_sim[k[0]][k[1]]))
        # outN.write("\n")
    # print('Preferential_attachment prediction finished sucnessfully')
    end_pa = datetime.now()
    # print('Common neghbor duration: {}'.format(end_pa - start_pa), "\n")
    return dictionary


def katz_predict(G, df_nodes):
    start_pa = datetime.now()

    # print('Preferential_attachment prediction starting...')

    out = open('./predictions/preferential_attachment.csv', 'w')
    outN = open('./predictions/preferential_attachment_with_name.csv', 'w')
    hop2s = dict()
    neighbors = dict()
    pa_sim = defaultdict(dict)
    sortDic = {}
    left_set = list(set(nx.bipartite.sets(G)[0]))
    right_set = list(set(nx.bipartite.sets(G)[1]))

    out.write('(left_element, right_element)')
    out.write(",")
    out.write('Probability')
    out.write("\n")

    outN.write('(left_element, right_element)')
    outN.write(",")
    outN.write('Probability')
    outN.write("\n")

    for left_element in left_set:
        hop2s[left_element] = getAdj2(G, list(set(G[left_element])), 1)
        for right_element in right_set:
            neighbors[right_element] = list(set(G[right_element]))
            if not (left_element, right_element) in G.edges:
                pa_sim[left_element][right_element] = katz_similarity(int(left_element), int(right_element), G)
                if pa_sim[left_element][right_element] > 0:
                    out.write(str((left_element, right_element)))
                    out.write(",")
                    out.write(str(pa_sim[left_element][right_element]))
                    out.write("\n")

                    outN.write(str((df_nodes[left_element], df_nodes[right_element])))
                    outN.write(",")
                    outN.write(str(pa_sim[left_element][right_element]))
                    outN.write("\n")
    # print('Preferential_attachment prediction finished sucnessfully')
    end_pa = datetime.now()
    # print('Common neghbor duration: {}'.format(end_pa - start_pa), "\n")
