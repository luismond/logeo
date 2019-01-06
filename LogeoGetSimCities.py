'''Train a similarity engine. Find the top n most similar city to a query'''
import time
start = time.time()
from gensim import corpora,models,similarities
import pandas as pd
from LogeoFuncs import get_query_id, ids_fs_to_bow, get_query_fq,preprocess #, tokens_f, preprocess, strip_accents, get_sim_cns, get_query_sim_scores, get_top_w2v,bow_from_freqs, , stopwords, get_top_tfidf, get_top_bow
path = 'ling_assets/sim_assets/'
fname = 'The_top-5000_Spanish_Twitter'
print(time.time()-start)


def get_sim_cities(query,n,n_of_cities,sorter):
    df = pd.read_csv('ling_assets/datasets/The_top-5000_Spanish_Twitter_dataset5.csv')
    #df1 = df[df['Country']=='Mexico']#df2 = df[df['Country']=='USA']#dfs = [df1,df2]#df = pd.concat(dfs)
    #BOW FROM FREQS####    #print('bow from freqs')    #id_fs = ids_fs_to_bow(df)    #df['bow'] = id_fs    #print(time.time()-start)
    #TOKENS, DICT######
    print('Tokens, dict')
    df['tokens'] = df['lines'].str.split(',')
    #dict_ = corpora.Dictionary(df['tokens'])
    #dict_.save(path+fname+'.dict')
    dict_ = corpora.Dictionary.load(path+fname+'.dict')
    df['bow'] = df['tokens'].apply(lambda x: dict_.doc2bow(x))
    #TFIDF############ 
    #tfidf = models.TfidfModel(df['bow']) 
    #tfidf.save(path+fname+'_model.tfidf') 
    #tfidf = models.TfidfModel.load(path+fname+'_model.tfidf') 
    #df['tfidf'] = df['bow'].apply(lambda x: tfidf[x]) 
    #LSI ####################################################################### 
    #lsi = models.LsiModel(df['tfidf'],num_topics=200)
    #lsi.save(path+fname+'_model.lsi')
    lsi = models.LsiModel.load(path+fname+'_model.lsi')
    print('Then we create an LSI similarity model.') 
    #index = similarities.MatrixSimilarity(lsi[df['tfidf']]) 
    #index.save(path+fname+'_similarity.index') 
    index = similarities.MatrixSimilarity.load(path+fname+'_similarity.index')
    print('similarity model loaded') 
    query_bow = dict_.doc2bow(query)
    print(query_bow)
    query_lsi = lsi[query_bow] 
    sim_scores = index[query_lsi]
    df['sim_score'] = sim_scores
    df = df.dropna()
    print(time.time()-start)
    df = df.sort_values(by=[sorter], ascending=False)
    df = df.drop(columns=['lines','freqs','freq_sum','bow'])
    df = df.iloc[:n_of_cities]
    print(time.time()-start)
    #WRITES THE RESULTING CITIES
    with open('templates/query_maps/top_fq_cities'+n+'.html','w',encoding='utf-8') as tw:
        dft = df.iloc[:10]
        top_labels = dft['city_ascii'].tolist()
        top_countries = dft['Country'].tolist()
        values = dft[sorter].tolist()
        tops = list(zip(top_countries,top_labels,values))
        tops_h = []
        for t in tops:
            print(t)
            t0 = """<a class="query0" href="//localhost:5000/country?query=%query&metric=bow&n=200">%query</a>""".replace('%query',str(t[0]))
            ts = t0+", "+str(t[1])+": "+ str(round(t[2],4))
            ts = """<li>%ts</li>""".replace('%ts',ts)
            tops_h.append(ts)
        html = """<div class="top_cities"><h4>The text entered is similar to the vocabulary of the following cities:<br></h4>
        <p class="city_sim_score">City : Similarity Score</p><ul>%cities</ul></div>"""
        html = html.replace('%cities',''.join(tops_h))
        tw.write(html)
    ###############################################################################
    df.to_csv('templates/query_maps/sim_cities'+n+'.csv')
    print('query generated sim cities csv')
    print(time.time()-start)
        
