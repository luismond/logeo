# -*- coding: utf-8 -*-
'Plot a data frame for a given query'
import time
from gensim import corpora, models,similarities
from LogeoFuncs import tfidf_avg, stopwords, get_skipgrams#, get_w2v_sim_scores, tfidf_sum, get_query_sim_scores, 
import pandas as pd
#from selenium import webdriver
import sys
#import numpy as np
#from skip_grams import skipgrams
sys._enablelegacywindowsfsencoding()
###################### VECTORS ################################################
vec_es = 'ling_assets/vectors/cc.es.300.vec/'+"cc.es.300.vec"#vec_en = path+"cc.en.300.vec"
word2vec_es = models.KeyedVectors.load_word2vec_format(vec_es,limit=500000)#word2vec_en = models.KeyedVectors.load_word2vec_format(vec_en, limit=100000)
path = 'templates/freq_maps/'
fname = 'The_top-5000_Spanish_Twitter'
start = time.time()
###############################################################################
###############################################################################
#token_df.to_csv('ling_assets/datasets/'+fname+'_dict_w2v_sims.csv')
print(time.time()-start)

'''
token_df.columns=['line']
token_df = token_df[token_df['line'].str.len()>1]

print(len(token_df.index))
def no_stop(x):         
    if not x in stopwords and not x.endswith('jaj') and not x.endswith('endo') \
    and not x.endswith('ajaj') and not x.endswith('haha') and not x.endswith('mente') \
    and not x.endswith('ando'):         
        return x         
    else:         
        return False         
token_df['line_ns'] = token_df['line'].apply(lambda x: no_stop(x))         
token_df = token_df[token_df['line_ns']!=False]         
token_df = token_df.drop(columns=['line_ns'])

#def get_chars(x):
#    return [w for w in x]
#token_df['chars'] = token_df['line'].apply(lambda x: get_chars(x))
token_df['skipgrams'] = token_df['line'].apply(lambda x: get_skipgrams(x))
token_df['skipgrams'] = token_df['skipgrams'].str.split(',')
tok_dict_ = corpora.Dictionary(token_df['skipgrams'])
token_df['bow'] = token_df['skipgrams'].apply(lambda x: tok_dict_.doc2bow(x))
tfidf = models.TfidfModel(token_df['bow'])
token_df['tfidf'] = token_df['bow'].apply(lambda x: tfidf[x])
token_df['tfidf_avg'] = token_df['tfidf'].apply(lambda x: tfidf_avg(x))
#token_df = token_df.drop(columns=['tfidf','bow'])
#token_df = token_df.sort_values(by=['tfidf_avg'],ascending=False)
token_df = token_df[token_df['tfidf_avg']<0.45]
token_df = token_df.drop(columns=['bow','tfidf','tfidf_avg'])
token_df['skipgrams'] = token_df['skipgrams'].apply(lambda x: ','.join(x))
token_df.to_csv('ling_assets/'+fname+'token_df2.csv')
'''


token_df = pd.read_csv('ling_assets/datasets/'+fname+'_token_df2.csv')

def get_first(x):
    x = [w for w in x]
    return x[0]

letter = 't'
#letters = 'a b c d e f g h i j k l m n o p q r  s t u v w x y z'
#for letter in letters:
token_df['starts'] = token_df['line'].apply(lambda x: get_first(x))

token_df = token_df[token_df['starts']==letter]

#token_df = token_df.iloc[:1000]
token_df = token_df.drop(columns=['Unnamed: 0'])
token_df['skipgrams'] = token_df['skipgrams'].str.split(',')
#token_dfx=token_df.iloc[:6]
#query = ''.join(query)
print('token dict')
tok_dict_ = corpora.Dictionary(token_df['skipgrams'])
#tok_dict_.save('ling_assets/token_assets/token_'+fname+'.dict')
#tok_dict_ = corpora.Dictionary.load('ling_assets/token_assets/token_'+fname+'.dict')
tok_dict_values = [(tok_dict_[id]) for id in tok_dict_.keys()]
print(time.time()-start)
print('token bow')
token_df['bow'] = token_df['skipgrams'].apply(lambda x: tok_dict_.doc2bow(x))


tfidf = models.TfidfModel(token_df['bow'])
#tfidf.save('ling_assets/token_'+fname+'_model.tfidf')
#tfidf = models.TfidfModel.load('ling_assets/token_'+fname+'_model.tfidf')
#print(time.time()-start)
token_df['tfidf'] = token_df['bow'].apply(lambda x: tfidf[x])
lsi = models.LsiModel(token_df['tfidf'])
#lsi.save('ling_assets/token_'+fname+'_model.lsi')
#lsi = models.LsiModel.load('ling_assets/token_'+fname+'_model.lsi')
print(time.time()-start)
tok_index = similarities.MatrixSimilarity(lsi[token_df['bow']]) 
#tok_index.save('ling_assets/token_'+fname+'_similarity.index')
#tok_index = similarities.MatrixSimilarity.load('ling_assets/token_'+fname+'_similarity.index')

'''
query = 'playa'
query_ = get_skipgrams(query)
query_ = query_.split(',')
query_bow = tok_dict_.doc2bow(query_)#query_tfidf = tfidf[query_bow]
print('query bow')
print(query_bow)
query_lsi = lsi[query_bow] 
# convert the query to lsi space
sim_scores = tok_index[query_lsi]
token_df['sim_score'] = sim_scores
token_df = token_df.sort_values(by=['sim_score'],ascending=False)
token_dfx = token_df.iloc[:100]
'''

#print(time.time()-start)
###############################################################################
top_sims = []
def get_top_sims(query,token_df):
    #query = 'playa'
    query_ = get_skipgrams(query)
    query_ = query_.split(',')
    query_bow = tok_dict_.doc2bow(query_)#query_tfidf = tfidf[query_bow]
    query_lsi = lsi[query_bow] # convert the query to lsi space
    sim_scores = tok_index[query_lsi]
    token_df['sim_score'] = sim_scores
    sim_lines = list(zip(token_df['sim_score'],token_df['line']))
    sim_lines = list(sorted(sim_lines,reverse=True))[:10]
    top_sims.append(sim_lines)
    print(time.time()-start)
queries = token_df['line'].tolist()
#queries = queries[:100]
for q in queries:
    get_top_sims(q,token_df)

token_df['sims'] = top_sims
token_df = token_df.drop(columns=['skipgrams','bow','tfidf','sim_score'])

def get_a(x):
    return ','.join([str(a) for (a,b) in x])

def get_b(x):
    return ','.join([str(b) for (a,b) in x])

token_df['sims_scores'] = token_df['sims'].apply(lambda x: get_a(x))
token_df['sims_tokens'] = token_df['sims'].apply(lambda x: get_b(x))
token_df = token_df.drop(columns=['sims'])
token_dfx = token_df.iloc[:20]

#x = pd.read_csv('ling_assets/datasets/'+fname+'_dict_w2v_sims.csv')
#### TOKEN LING ASSETS #########################################################
dict_ = corpora.Dictionary.load('ling_assets/line_assets/'+fname+'.dict')

def get_query_sims(query,n):
    print(time.time()-start)
    try:
        x = word2vec_es.most_similar(positive=query,topn=n)
        x = list(sorted([(b,a.lower()) for (a,b) in x if a in token_df['line'].tolist()
        and b>0.45],reverse=True))[:10]
        #x = [(a.lower(),b) for (a,b) in x if a in token_df['line'].tolist()]
        #x = list(sorted([(b,a) for (a,b) in x],reverse=True))[:30]
        return x
        
    except:
        return None  

token_df['w2v_sims'] = token_df['line'].apply(lambda x: get_query_sims(x,300))


def get_a(x):
    if not x==[]:
        try:
            return ','.join([str(a) for (a,b) in x])
        except:
            return None
            

def get_b(x):
    if not x==[]:
        try:
            return ','.join([str(b) for (a,b) in x])
        except:
            return None


token_df['w2v_sims_scores'] = token_df['w2v_sims'].apply(lambda x: get_a(x))

token_df['w2v_sims_tokens'] = token_df['w2v_sims'].apply(lambda x: get_b(x))
token_df = token_df.drop(columns=['w2v_sims'])
token_dfx = token_df.iloc[:20]
#token_df.to_csv('ling_assets/datasets/'+fname+'_dict_sims.csv')


#token_df = pd.read_csv('ling_assets/datasets/'+fname+'_dict_sims.csv')
#token_df = pd.read_csv('ling_assets/datasets/'+fname+'_dict_w2v_sims.csv')
#token_df['w2v_sims_a'] = token_df['w2v_sims_a'].str.split()
def get_tok_ids(x):
    try:
        return ','.join([str(dict_.token2id[y]) for y in x.split(',')])
    except:
        return None
token_df['sims_tokens_ids'] = token_df['sims_tokens'].apply(get_tok_ids)

token_df['w2v_sims_tokens_ids'] = token_df['w2v_sims_tokens'].apply(get_tok_ids)

token_df['line_id'] = token_df['line'].apply(lambda x: dict_.token2id[x])
#token_df = token_df.drop(columns=['Unnamed: 0', 'top_sims_tokens', 'line'])

def round_(x):
    try:
        return [round(float(y),3) for y in x.split(',')]
    except:
        return None
token_df['sims_scores'] = token_df['sims_scores'].apply(lambda x: round_(x))
token_df['w2v_sims_scores'] = token_df['w2v_sims_scores'].apply(lambda x: round_(x))

def k(x):
    try:
        return ','.join([str(y) for y in x])
    except:
        return None

token_df['sims_scores'] = token_df['sims_scores'].apply(lambda x: k(x))
token_df['w2v_sims_scores'] = token_df['w2v_sims_scores'].apply(lambda x: k(x))
token_df = token_df.drop(columns=['sims_tokens','w2v_sims_tokens','line','starts'])

new_order = [4,2,0,3,1]
token_df = token_df[token_df.columns[new_order]]
token_dfx = token_df.iloc[:20]


token_df.to_csv('ling_assets/datasets/'+fname+'_skip_w2v_sims_'+letter+'_.csv')
print(time.time()-start)