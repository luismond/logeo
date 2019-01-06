from skip_grams import skipgrams
path = 'ling_assets/'
fname = 'The_top-5000_Spanish_Twitter'
import pandas as pd
import random

def get_cnt_sug(metric):
    df_tfidfs = pd.read_csv(path+'datasets/'+fname+'_cn_df_'+metric+'.csv')
    #df_tfidfs = pd.read_csv(path+'datasets/'+fname+'_cn_df_tfidf.csv')
    df_tfidfs = df_tfidfs.drop(columns=['Unnamed: 0'])
    df_tfidfs.columns=['country','lines']
    df_tfidfs['tokens'] = df_tfidfs['lines'].str.split(',')
    def first_ys(x):
        return x[:100]
    df_tfidfs['tokens'] = df_tfidfs['tokens'].apply(lambda x: first_ys(x))
    #df_tfidfs['tokens'] = df_tfidfs['tokens'].apply(lambda x: random.sample(x,10))
    html = """<a href="//localhost:5000/results?query=%query">%query</a>"""
    def mk_qry(x):
        return [html.replace('%query',y) for y in x]
    df_tfidfs['queries'] = df_tfidfs['tokens'].apply(lambda x: mk_qry(x))
    df_tfidfs['queries'] = df_tfidfs['queries'].apply(lambda x: ', '.join(x))
    df_tfidfs = df_tfidfs.sort_values(by=['country'], ascending=True)
    df_tfidfs = list(zip(df_tfidfs['country'],df_tfidfs['queries']))
    print(df_tfidfs)
    #df_tfidf_html = """<button class="collapsible">%a</button><div class="content">%b</div>""".replace('%a',a)
    #df_tfidf_html = df_tfidf_html.replace('%b',b)
    df_tfidfs = ''.join(['<button class="collapsible">'+a.replace('_',' ')+"</button>"+'<div class="content">'+b
                         +'<br><a href="//localhost:5000/country?query=%query&metric=%metric&n=200"><strong>See more</strong></a></div>'.replace('%query',a) for (a,b) in df_tfidfs])
    df_tfidfs = df_tfidfs.replace('%metric',metric)
    with open('templates/query_maps/country_'+metric+'_list.html', 'w', encoding='utf8') as f:
        f.write(df_tfidfs)

def get_cnt_sug_c(metric,country,n):
    #country = country.title()
    df_tfidfs = pd.read_csv(path+'datasets/'+fname+'_cn_df_'+metric+'.csv')
    #df_tfidfs = pd.read_csv(path+'datasets/'+fname+'_cn_df_tfidf.csv')
    df_tfidfs = df_tfidfs.drop(columns=['Unnamed: 0'])
    df_tfidfs.columns=['country','lines']
    df_tfidfs = df_tfidfs[df_tfidfs['country']==country]
    df_tfidfs['tokens'] = df_tfidfs['lines'].str.split(',')
    def first_ys(x):
        return x[:n]
    df_tfidfs['tokens'] = df_tfidfs['tokens'].apply(lambda x: first_ys(x))
    #df_tfidfs['tokens'] = df_tfidfs['tokens'].apply(lambda x: random.sample(x,10))
    html = """<a href="//localhost:5000/results?query=%query">%query</a>"""
    def mk_qry(x):
        return [html.replace('%query',y) for y in x]
    df_tfidfs['queries'] = df_tfidfs['tokens'].apply(lambda x: mk_qry(x))
    df_tfidfs['queries'] = df_tfidfs['queries'].apply(lambda x: ', '.join(x))
    df_tfidfs = df_tfidfs.sort_values(by=['country'], ascending=True)
    df_tfidfs = list(zip(df_tfidfs['country'],df_tfidfs['queries']))
    print(df_tfidfs)
    #df_tfidf_html = """<button class="collapsible">%a</button><div class="content">%b</div>""".replace('%a',a)
    #df_tfidf_html = df_tfidf_html.replace('%b',b)
    n = str(n)
    title = "Top %metric %n words from".replace('%n',str(n))
    title = title.replace('%metric',metric)
    top500 = """<a href="//localhost:5000/country?query=%query&metric=%metric&n=500">Top 500</a>""".replace('%query',country)
    top500 = top500.replace('%metric',metric)
    top1000 = """<a href="//localhost:5000/country?query=%query&metric=%metric&n=1000">Top 1000</a>""".replace('%query',country)
    top1000 = top1000.replace('%metric',metric)
    df_tfidfs = ''.join([title+' '+a.replace('_',' ')+'<div class="content1">'+b+"<br>"+top500+"<br>"+top1000+"</div>" for (a,b) in df_tfidfs])
    with open('templates/query_maps/country_'+metric+'_single_country_list.html', 'w', encoding='utf8') as f:
        f.write(df_tfidfs)
import folium
def make_country_map(country):
    m = folium.Map(height=600, width=1150, tiles= 'cartodbpositron')
    df = pd.read_csv(path+'datasets/'+fname+'_dataset5.csv')
    df = df[df['Country']==country]
    top_labels = list(zip(df['city_ascii'],df['lat'],df['lng']))
    for t in top_labels:
        folium.Circle(
        popup=folium.Popup(t[0], max_width=250, sticky=False),
        location=[t[1],t[2]],
        radius=30000,
        color='#00ADFF',
        fill=True,
        fill_color='#00ADFF',
        ).add_to(m)
    m.fit_bounds(m.get_bounds())
    m.save('templates/query_maps/country_map.html')
    #Post-fuckery
    with open('templates/query_maps/country_map.html','r') as f:
        h = f.read()
        h = h.replace("""width: 1000.0px;
        height: 1000.0px;""",'width: 100vw;height:100%;')
        h = h.replace("""    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css"/>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css"/>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css"/>""",'')
        h = h.replace("""<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>""",'')
        #h = h.replace("""<style>html, body {width: 100%;height: 100%;margin: 0;padding: 0;}</style>
    #<style>#map {position:absolute;top:0;bottom:0;right:0;left:0;}</style>""",
    #"""<style>body { padding: 0;  margin: 0; } </style> <style>html, body, #map {     height: 100%;     width: vw; }</style""" )
        h = h.replace("""  width: 1150.0px;
        height: 600.0px;""","""width: vw;         height: 450px;""")
        h = h.replace("""<head>""","""<head><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />""")
    with open('templates/query_maps/country_map.html','w') as f:
        f.write(h)
     
def get_query_id(query,dict_):
    try:
        return dict_.token2id[''.join(query)]
    except:
        return 'query not in dict'


def iter_zip(df,col1,col2,col3):
    df[col1] = df[col1].str.split(',')
    df[col2] = df[col2].str.split(',')
    col1 = df[col1].tolist() 
    col1 = [[str(y) for y in x] for x in col1]
    col2 = df[col2].tolist()
    col2 = [[str(y) for y in x] for x in col2]
    col1_col2 = list(zip(col1,col2))
    col1_col2 = [list(zip(x[0],x[1])) for x in col1_col2]
    df[col3] = col1_col2
    return df

def ids_fs_to_bow(df):
    df['ids'] = df['ids'].str.split(',')
    df['freqs'] = df['freqs'].str.split(',')
    ids = df['ids'].tolist() 
    #ids = [[int(y) for y in x] for x in ids]
    fs = df['freqs'].tolist()
    #fs = [[int(y) for y in x] for x in fs]
    id_fs = list(zip(ids,fs))
    id_fs = [list(zip(x[0],x[1])) for x in id_fs] 
    return id_fs

def get_query_fq(x,query_id):
    for (a,b) in x:
        if int(a) == query_id:
            return b
        
def get_skipgrams(x):
        x = list(skipgrams(x, 2, 0))+list(skipgrams(x, 1, 0))
        return ','.join(set([''.join(z) for z in x]))
    
def get_colors(df,colors,column_name):
    p = int(len(df.index))
    q = round(p/len(colors))+1
    colors_ = [[c]*q for c in colors]
    colors_ = ','.join([','.join(c) for c in colors_]).split(',')
    colors_ = colors_[:p]
    df[column_name] = colors_
    return df

### S T O P W O R D S ########################################################
with open(path+'stopwords/spanish_stopwords.txt', 'r', encoding='utf8') as f:
    stops_es = f.read()
stops_es = stops_es.split('\n')
with open(path+'stopwords/english_stopwords.txt', 'r', encoding='utf8') as f:
    stops_en = f.read()
stops_en = stops_en.split('\n')
stops = stops_es + stops_en
def strip_punct(line):
    charset = set()
    for ch in line:
        charset.update(ch)
    punct = [ch for ch in list(set(charset)) if not ch.isalpha()]# and not ch.isdigit()]
    #print(punct)
    if ' ' in punct:
        punct.remove(' ')
    for ch in punct:
        line = line.replace(ch, ' ').lower()
        line = line.replace('  ', ' ').lower()
    #if len(line)<1:
    #    line = 'empty'
    return line.lower()
def strip_accents(line):
    line = line.replace('á','a')
    line = line.replace('é','e')
    line = line.replace('í','i')
    line = line.replace('ó','o')
    line = line.replace('ú','u')
    return line
stops_stripped = [strip_accents(s) for s in stops]
stopwords = stops + stops_stripped

def tfidf_avg(line):
    return sum([b for (a,b) in line])/len(line)

def tfidf_sum(line):
    return sum([b for (a,b) in line])


def word_cloud_divs(words_dict,n):
    divs = []
    for k,v in words_dict.items():
        div = """<div class="word_cloud" style="font-size:v%px;color:c%;">k%</div>""".replace('k%',str(k))
        div = div.replace('v%',str(v))
        if n==str(0):
            colors = '#009BE5 #00ADFF #32BDFF #66CDFF'.split()      
            color = ' '.join(random.sample(colors,1))
            div = div.replace('c%',color)
            divs.append(div)
        if n==str(1):
            colors = '#ff0038 #ff4c73 #ff6687 #ff7f9b'.split()      
            color = ' '.join(random.sample(colors,1))
            div = div.replace('c%',color)
            divs.append(div)
    return divs

def condition1(x):         
        if not x in stopwords:# and not x.endswith('ando') and not x.endswith('endo') and not x.endswith('mente'):
            return x
        else:
            return False  


def preprocess(line):
    line = strip_punct(line)
    #line = strip_accents(line)
    #line = remove_stops(line)
    return line



'''
def remove_stops(line):
    line = line.split()
    return ','.join([w for w in line if not w in stops and not w.isdigit()]).split(',')# and len(w)>2])
def preprocess(line):
    line = strip_punct(line)
    line = strip_accents(line)
    line = remove_stops(line)
    return line
def get_top_tfidf(x,dict_,stopwords):
    x = [(dict_[a],b) for (a,b) in x if b>=0.005 and not dict_[a] in stopwords]
    x = [(float(b),a) for (a,b) in x]
    x = list(sorted(x,reverse=True))[:10]
    #x = [b for (a,b) in x]
    return x 
def get_top_bow(x,dict_,stopwords):
    x = [(dict_[a],b) for (a,b) in x if b>=10 and not dict_[a] in stopwords]
    x = [(int(b),a) for (a,b) in x]
    x = list(sorted(x,reverse=True))[:10]
    #x = [b for (a,b) in x]
    return x  
def get_top_w2v(x,dict_):
    x = [y for y in x if not y=='None']
    x = [(int(b),dict_[a]) for (a,b) in x]
    x = list(sorted(x,reverse=True))[:10]
    #x = [b for (a,b) in x]
    return x    


def get_query_sims(query,n):
    try:
        query = [query]+[word2vec_es.most_similar(positive=query,topn=n)]
        return query
    except:
        return None  
#For line level
def get_query_sim_scores(query,lines,dict_):
    nlines = []
    for l in lines:
        try:
            l = (float(word2vec_es.similarity(query,dict_[l])),l)
            nlines.append(l)#return l
        except:
            nlines.append((0, l)) #return 'None'  
    nlines = list(sorted(nlines,reverse=True))
    nlines = [str(a)+':'+str(b) for (a,b) in nlines]
    return nlines[:30]
#For token level
def get_w2v_sim_scores(query,x):
    print(query)
    try:
        x = word2vec_es.similarity(query,x)
        return x
    except:
        return None   
def tokens_f(x):
    x = [(a+' ',int(b)) for (a,b) in x]
    return ' '.join([(a*b) for (a,b) in x]).split()
def bow_from_freqs(x,dict_):
    return [(dict_.token2id[a],b) for (a,b) in x]

def get_top_w2v_a(x,dict_):
    x = [y for y in x if not y=='None']
    x = [(b,dict_[a]) for (a,b) in x]
    x = list(sorted(x,reverse=True))[:10]
    x = list(float(a) for (a,b) in x)
    x = ','.join([str(a) for a in x])
    return x    
def get_top_w2v_b(x,dict_):
    x = [y for y in x if not y=='None']
    x = [(b,dict_[a]) for (a,b) in x]
    x = list(sorted(x,reverse=True))[:10]
    x = list(b for (a,b) in x)
    x = ','.join([a for a in x])
    return x 
def sub_skipgrams(x):
    x1 = x[:1]
    x2 = x[:2]
    x3 = x[:3]
    x4 = x[:4]
    x5 = x[:5]
    x6 = x[:6]
    x7 = x[-4:]
    x8 = x[-4:]
    x9 = x[-3:]
    x10 = x[-2:]
    x11 = x[-1:]
    xs = list(set([x,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11]))
    return ','.join(xs)
'''
'''
def get_cnt_sug_(metric):
    df_tfidfs = pd.read_csv(path+'datasets/'+fname+'_cn_df_'+metric+'.csv')
    #df_tfidfs = pd.read_csv(path+'datasets/'+fname+'_cn_df_tfidf.csv')
    df_tfidfs = df_tfidfs.drop(columns=['Unnamed: 0'])
    df_tfidfs.columns=['country','lines']
    df_tfidfs['tokens'] = df_tfidfs['lines'].str.split(',')
    def first_ys(x):
        return x[:75]
    df_tfidfs['tokens'] = df_tfidfs['tokens'].apply(lambda x: first_ys(x))
    df_tfidfs['tokens'] = df_tfidfs['tokens'].apply(lambda x: random.sample(x,10))
    html = """<a href="/results?query=%query">%query</a>"""
    def mk_qry(x):
        return [html.replace('%query',y) for y in x]
    df_tfidfs['queries'] = df_tfidfs['tokens'].apply(lambda x: mk_qry(x))
    df_tfidfs['queries'] = df_tfidfs['queries'].apply(lambda x: ', '.join(x))
    df_tfidfs = df_tfidfs.sort_values(by=['country'], ascending=True)
    df_tfidfs = list(zip(df_tfidfs['country'],df_tfidfs['queries']))
    print(df_tfidfs)
    df_tfidfs = "<ul>"+''.join(["<li>"+"<strong>"+a+"</strong>"+": "+b+"</li>" for (a,b) in df_tfidfs])+"</ul>"
    with open('templates/query_maps/country_'+metric+'_list.html', 'w', encoding='utf8') as f:
        f.write(df_tfidfs)
'''
