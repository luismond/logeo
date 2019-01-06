'''
LOGEO, Country level
'''
import time
from gensim import models,corpora,similarities
import pandas as pd
from LogeoFuncs import stopwords #preprocess, , get_top_bow
import folium, random

#from TextProcFuncs import sub_skipgrams, stopwords, no_dups, drop_substrings, get_word2vec_embeddings, viz, print_, ngrams_, get_chars, remove_stops, strip_punct, tfidf_sum
#from TextProcFuncs import sub_skipgrams, no_dups, drop_substrings, get_word2vec_embeddings, viz, print_, ngrams_, get_chars, remove_stops, strip_punct, tfidf_sum

start = time.time()
path = 'ling_assets/'

###################### VECTORS ################################################
#vec_es = path+"cc.es.300.vec"
#vec_en = path+"cc.en.300.vec"
#word2vec_es = models.KeyedVectors.load_word2vec_format(vec_es, limit=100000)
#word2vec_en = models.KeyedVectors.load_word2vec_format(vec_en, limit=100000)
#print(time.time()-start)

###############################################################################

df = pd.read_csv(path+'/datasets/The_top-5000_Spanish_Twitter_dataset2.csv')

df['freqs'] = df['freqs'].str.split(',')

def sub_fl(x):
    return ','.join([str(round(float(y)/250)) for y in x])#Big compression
df['freqs'] = df['freqs'].apply(lambda x: sub_fl(x))
#df['tokens'] = df['lines'].str.split(',')
dfx = df.iloc[:1]


#Analyze country level ###################################################
countries = df['Country'].tolist()
print('We analyze a dataset with the 5000 most frequent words \n in 292 Spanish speaking cities of 19 countries')
from collections import Counter
cnt = Counter()
for word in countries:
     cnt[word] += 1
print('Countries and number of cities per country in the dataset:')
cnt = cnt.most_common()
print(cnt)

print('Cities in the dataset')

for x in list(zip(df['Country'],df['city_ascii'])):
    print (x[0]+', '+x[1].title())

def get_cn_df(cn):
    dfcn = df[df['Country']==cn]
    dfcn_ = ','.join(dfcn['lines'].tolist())
    freqs = ','.join(dfcn['freqs'].tolist())
    #dfcn_ = dfcn['lines'].tolist()
    #dfcn_ = [x for x in dfcn_]
    #dfcn_f = [x for x in freqs]
    #dfcn_ = dict({cn:dfcn_})
    dfcn_ = cn,dfcn_,freqs
    return dfcn_

cn_dicts = [get_cn_df(cn) for cn in set(countries)]

cn_df = pd.DataFrame(cn_dicts)
#cn_dfx = cn_df.iloc[:1]

cn_df.columns = ['Country', 'lines','freqs']
cn_df['tokens'] = cn_df['lines'].str.split(',')
cn_df['freqs'] = cn_df['freqs'].str.split(',')

cn_dict_ = corpora.Dictionary(cn_df['tokens'])
#cn_df['freqs'] = cn_df['freqs'].str.split(' ')
cn_dfx=cn_df.iloc[:1]

#############
print('We multiply the tokens by its frequency, so that the tfidf algo has something to pick')
tokens = cn_df['tokens'].tolist()
freqs = cn_df['freqs'].tolist()

tk_fs = list(zip(tokens,freqs))
tk_fs = [list(zip(x[0],x[1])) for x in tk_fs] 
cn_df['tokens_freqs'] = tk_fs
def tokens_f(x):
    x = [(a+' ',int(b)) for (a,b) in x]
    return ' '.join([(a*b) for (a,b) in x]).split()
cn_df['tokens_exp'] = cn_df['tokens_freqs'].apply(lambda x: tokens_f(x))
cn_df = cn_df.drop(columns=['tokens_freqs'])
#cn_dfx=cn_df.iloc[:1]

#dict_values = [dict_[id] for id in dict_.keys()]
cn_df['bow'] = cn_df['tokens_exp'].apply(lambda x: cn_dict_.doc2bow(x))
cn_tfidf = models.TfidfModel(cn_df['bow'])
cn_df['tfidf'] = cn_df['bow'].apply(lambda x: cn_tfidf[x])

def cn_tx(x):
    return [(b,cn_dict_[a]) for (a,b) in x]
  
#cn_df['tfidf_'] = cn_df['tfidf'].apply(lambda x: cn_tx(x))
cn_df['bow_'] = cn_df['bow'].apply(lambda x: cn_tx(x))

cn_dfx = cn_df.drop(columns=['lines','freqs','tokens','tokens_exp','tfidf']).iloc[:2]
#cn_df['bow_'] = cn_df['bow'].apply(lambda x: cn_tx(x))


cn_dfx_tfidfs = []
for n in range(len(cn_df)):
    cn_dfx = cn_df.iloc[n]
    cn_dfx_sorted = list(sorted(cn_dfx['bow_'],reverse=True))
    cn_dfx_sorted = ','.join([b for (a,b) in cn_dfx_sorted if not b in stopwords and not b.startswith('jaj')])
    #print(cn_dfx_sorted[:5])
    cn_dfx = [cn_dfx['Country'],cn_dfx_sorted]   
    cn_dfx_tfidfs.append(cn_dfx)

print('By implementing a tfidf algorithm, we can quickly see \n the most characteristic words of each country')

for cdt in cn_dfx_tfidfs:
    print(cdt[0],cdt[1][0:20])


cn_df_tfidf = pd.DataFrame(cn_dfx_tfidfs)

cn_df_tfidf.to_csv(path+'datasets/The_top-5000_Spanish_Twitter_cn_df_bow.csv')

print(time.time()-start)