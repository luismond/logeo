'''LOGEO GET FQ CITIES. Get top fq cities for 1 & 2 word queries'''
import time
start = time.time()
from gensim import corpora
import pandas as pd
from LogeoFuncs import get_query_id, ids_fs_to_bow, get_query_fq 
path = 'ling_assets/'
fname = 'The_top-5000_Spanish_Twitter'
print(time.time()-start)
def get_top_fq_cities(query,n,n_of_cities):
    df = pd.read_csv(path+'datasets/'+fname+'_dataset5.csv')
    print('bow from freqs')
    id_fs = ids_fs_to_bow(df)
    df['bow'] = id_fs
    print(time.time()-start)
    #TOKENS, DICT######
    print('Tokens, dict')
    dict_ = corpora.Dictionary.load(path+'line_assets/'+fname+'.dict')
    print(time.time()-start)
    query_id = get_query_id(query,dict_)
    if query_id != 'query not in dict':
        print('query found')
        df['query_fq'] = df['bow'].apply(lambda x: get_query_fq(x,query_id))
        df = df.dropna()
        df['query_fq'] = df['query_fq'].astype(int)
        print(time.time()-start)
        df['fq_%'] = df['query_fq']/df['freq_sum']
        df = df.sort_values(by=['fq_%'], ascending=False)
        df = df.drop(columns=['lines','freqs','freq_sum','bow'])
        df = df.iloc[:n_of_cities]
        print(time.time()-start)
        #WRITES THE RESULTING CITIES
        with open('templates/query_maps/top_fq_cities'+n+'.html','w',encoding='utf-8') as tw:
            dft = df.iloc[:10]
            top_labels = dft['city_ascii'].tolist()
            top_countries = dft['Country'].tolist()
            fqs = dft['fq_%'].tolist()
            tops = list(zip(top_countries,top_labels,fqs))
            tops_h = []
            for t in tops:
                t0 = """<a class="query0" href="/country?query=%query&metric=frequency&n=200">%query</a>""".replace('%query',str(t[0]))
                ts = t0+", "+str(t[1])+": "+str(round(t[2]*100,4))+'%'
                ts = """<li>%ts</li>""".replace('%ts',ts)
                tops_h.append(ts)
            html = """<div class="top_cities"><h4>Cities with higher % of mentions of %word</h4><ul>%cities</ul></div>"""
            html = html.replace('%cities',''.join(tops_h))
            html = html.replace('%word',u''.join(query))
            tw.write(html)
        df['ids'] = df['ids'].apply(lambda x: ','.join(x))
        df.to_csv('templates/query_maps/sim_cities'+n+'.csv')
        print('query generated sim cities csv')
        print(df.columns.values)
        print(time.time()-start)
    else:
        print('query not found')