#!/usr/bin/python3

# this script computes individual-record recall

import sys
import statistics

if len(sys.argv) > 1:
    input_citation_file = sys.argv[1]
else:
    input_citation_file = "pmid_citations.txt"


input_file = "pmid_annotations_gene2pubmed.txt"
output_file = input_citation_file + "_" + "bc2gn_annotation_recall.txt"
input_target_annotation_file = "pmid_annotations_bc2.txt"

f_in = open(input_file, "r")

# read existing annotations


print("Reading annotations...")
annotations_pmid = {}
counter_annotations=0
for line in f_in:
    line = line[:-1]
    data = line.split("\t")
    pmid = data[0]
    if pmid != "":
        annotations_pmid[pmid] = data[1]
        counter_annotations += len(annotations_pmid[pmid].split("|"))

print("Annotations read: " + str(counter_annotations))


print("Reading BC2GN annotations...")

f_in = open(input_target_annotation_file, "r")

counter_annotations = 0
pmids_bc2 = {}

for line in f_in:
    line = line[:-1]
    data = line.split("\t")
    pmid = data[0]
    if pmid != "":
        annotations_pmid[pmid] = data[1]
        pmids_bc2[pmid] = 1
        counter_annotations += len(annotations_pmid[pmid].split("|"))

print("Annotations read: " + str(counter_annotations))
print("PMIDs concerned: " + str(len(pmids_bc2.keys())))

citation_counter_all = {}
citation_counter_annotations = {}
counter = 0

# read available citation data
print("Reading citation data...")
shared_annotations = {}
not_shared_annotations = {}
f_in = open(input_citation_file)

for line in f_in:
#for i in range(1,1000000):
    #line = f_in.readline()
    data = line[:-1].split("\t")
    counter+=1
    if counter / 10000000 == int(counter / 10000000):
        print("Read " + str(counter) + " citations")
    if len(data) > 1:
        pmid1 = data[0]
        pmid2 = data[1]
        if pmid1 in annotations_pmid.keys() or pmid2 in annotations_pmid.keys():
            if pmid1 in citation_counter_all.keys():
                citation_counter_all[pmid1] += 1
            else:
                citation_counter_all[pmid1] = 1
            if pmid2 in citation_counter_all.keys():
                citation_counter_all[pmid2] += 1
            else:
                citation_counter_all[pmid2] = 1
            # check if first PMID is annotated
            if pmid1 in annotations_pmid.keys():
                # check if second PMID is annotated
                if pmid2 in annotations_pmid.keys():
                    if pmid1 in citation_counter_annotations.keys():
                        citation_counter_annotations[pmid1] += 1
                    else:
                        citation_counter_annotations[pmid1] = 1
                    if pmid2 in citation_counter_annotations.keys():
                        citation_counter_annotations[pmid2] += 1
                    else:
                        citation_counter_annotations[pmid2] = 1
                    annotations1 = annotations_pmid[pmid1].split("|")
                    annotations2 = annotations_pmid[pmid2].split("|")    
                    # count annotations that the second PMID shared with the first 
                    for annotation in annotations2:
                        if annotation in annotations1:
                            if pmid1 in shared_annotations.keys():
                                if annotation not in shared_annotations[pmid1]:
                                    shared_annotations[pmid1].append(annotation)
                            else:
                                shared_annotations[pmid1] = [annotation]
                        else:
                            if pmid1 in not_shared_annotations.keys():
                                if annotation not in not_shared_annotations[pmid1]:
                                    not_shared_annotations[pmid1].append(annotation)
                            else:
                                not_shared_annotations[pmid1] = [annotation]
                    # same as before but reverse
                    for annotation in annotations1:
                        if annotation in annotations2:
                            if pmid2 in shared_annotations.keys():
                                if annotation not in shared_annotations[pmid2]:
                                    shared_annotations[pmid2].append(annotation)
                            else:
                                shared_annotations[pmid2] = [annotation]
                        else:
                            if pmid2 in not_shared_annotations.keys():
                                if annotation not in not_shared_annotations[pmid2]:
                                    not_shared_annotations[pmid2].append(annotation)
                            else:
                                not_shared_annotations[pmid2] = [annotation]

    
# compute recall for each PMID based on the previous counts

print("Writing output file " + output_file + "...")

f_out = open(output_file, "w")
f_out.write("PMID\tShared annotations\tTotal\tRecall\tPrecision\tConnections with annotations\tTotal connections\n")
total_recall = 0
recall_sum = 0
precision_sum = 0
total_sum = 0
list_count_annotations = []
list_count_connections = []
for pmid in pmids_bc2.keys():
    total = len(annotations_pmid[pmid].split("|"))
    if pmid in shared_annotations.keys():
        shared = len(shared_annotations[pmid])
    else:
        shared = 0
    if pmid in not_shared_annotations.keys():
        not_shared = len(not_shared_annotations[pmid])
    else:
        not_shared = 0

    if pmid in citation_counter_annotations.keys():
        count_annotations = citation_counter_annotations[pmid]
    else:
        count_annotations = 0
    if pmid in citation_counter_all.keys():
        count_all = citation_counter_all[pmid]
    else:
        count_all = 0
    if total > 0:
        recall = shared / total
        if shared + not_shared > 0:
            precision = shared / (shared + not_shared)
        else:
            precision = 0
        f_out.write(str(pmid) + "\t" + str(shared) + "\t" + str(total) + "\t" + str(recall) + "\t" + str(precision) + "\t" + str(count_annotations) + "\t" + str(count_all) + "\n")
        if recall == 1:
            total_recall += 1
        precision_sum += precision
        recall_sum += shared
        total_sum += total
        list_count_annotations.append(count_annotations)
        list_count_connections.append(count_all)

percentage_total_recall = 100 * total_recall / len(pmids_bc2)

print("Articles with 100% recall: " + str(total_recall) + "/" + str(len(pmids_bc2)) + "(" + "{0:.2f}".format(100 * total_recall / len(pmids_bc2)) + "%)")
print("Annotations recalled in total: " + str(recall_sum) + "/" + str(total_sum) + "(" + "{0:.2f}".format(100 * recall_sum / total_sum) + "%)")
print("Annotation precision in total: " + str(precision_sum) + "/" + str(total_sum) + "(" + "{0:.2f}".format(100 * precision_sum / total_sum) + "%)")
print("Median number of annotated neighbors: " + str(statistics.median(list_count_annotations)))
print("Median number of neighbors: " + str(statistics.median(list_count_connections)))
