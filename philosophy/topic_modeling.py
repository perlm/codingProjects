# -*- coding: utf-8 -*-

import glob, sys, string
import numpy as np 
from text_search import *
from sklearn import feature_extraction, decomposition

# try some topic modeling! examples:
# https://de.dariah.eu/tatom/topic_model_python.html
# http://scikit-learn.org/stable/auto_examples/applications/topics_extraction_with_nmf_lda.html#sphx-glr-auto-examples-applications-topics-extraction-with-nmf-lda-py

def print_top_words(model, feature_names, n_top_words):
	for topic_idx, topic in enumerate(model.components_):
		print("Topic #%d:" % topic_idx)
		print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))

def topic_modeling_prep(filenames, n_features):
	vectorizer = feature_extraction.text.CountVectorizer(input='filename', max_df=0.95, min_df=2, max_features=n_features, stop_words='english')
	tf_matrix = vectorizer.fit_transform(filenames).toarray()
	return vectorizer, tf_matrix

def calc_lda(tf_matrix, n_topics=10,max_iter=20):
	lda = decomposition.LatentDirichletAllocation(n_topics=n_topics, max_iter=max_iter,
                                learning_method='online',
                                learning_offset=50.)
	doctopic = lda.fit_transform(tf_matrix)
	return doctopic, lda

def assign_topic(text_names,doctopic,num_topics):
	doctopic_grouped = np.zeros((text_names.shape[0], num_topics))
	for i, name in enumerate(text_names):
		doctopic_grouped[i, :] = np.mean(doctopic[text_names == name, :], axis=0)
	doc_topic_assign = np.argmax(doctopic_grouped, axis=1)
	return doc_topic_assign


def summarize_results(doc_topic_assign, lda, vectorizer, filenames):
	summary = read_summary()
	bookids = [f[5:-4] for f in filenames]

	# for each topic, print out words and documents.
	feature_names = vectorizer.get_feature_names()
	n_top_words = 5
	for topic_idx, topic in enumerate(lda.components_):
                print "Topic #%d:" % topic_idx,
                print(" ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))

		# which docs are placed in this topic?
		ids = np.where(doc_topic_assign==topic_idx)[0].tolist()
		print("\n".join([summary[(bookids[i],'title')] + " by " + summary[(bookids[i],'author')]  for i in ids]))
		print("\n")


def main():

	# constants
	num_topics = 10
	num_features = 1000

	# read input files
	filenames = glob.glob("data/[0-9]*.txt")
	text_names = np.asarray(filenames)

	# create model
	vectorizer, tf_matrix = topic_modeling_prep(filenames,num_features)
	doctopic, lda = calc_lda(tf_matrix,num_topics)
	doc_topic_assign = assign_topic(text_names,doctopic,num_topics)

	# describe results
	summarize_results(doc_topic_assign, lda, vectorizer,filenames)

	#print_top_words(lda, vectorizer.get_feature_names(), 5)


if __name__ == "__main__":
	main()	
