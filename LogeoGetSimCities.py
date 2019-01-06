'''LOGEO CITY LEVEL. Explore dataset city frequencies
Train a city level similarity engine. Find the top n most similar city-lines to a query'''
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
        
'''
#TEST
query = 'Somos pacífico, estamos unidos Nos une la región La pinta, la raza y el don del sabor Somos pacífico, estamos unidos Nos une la región La pinta, la raza y el don del sabor Ok! si por si acaso usted no conoce En el pacífico hay de todo para que goce Cantadores, colores, buenos sabores Y muchos santos para que adores Es toda una conexión Con un corrillo chocó, valle, cauca Y mis paisanos de nariño Todo este repertorio me produce orgullo Y si somos tantos Porque estamos tan al cucho (en la esquina) Bueno, dejemos ese punto a un lado Hay gente trabajando pero son contados Allá rastrillan, hablan jerguiados Te preguntan si no has janguiado (hanging out) Si estas queda’o Si lo has copiado, lo has vacilado Si dejaste al que está malo o te lo has rumbeado Hay mucha calentura en buenaventura Y si sos chocoano sos arrecho por cultura, ey! Somos pacífico, estamos unidos Nos une la región La pinta, la raza y el don del sabor Somos pacífico, estamos unidos Nos une la región La pinta, la raza y el don del sabor Unidos por siempre, por la sangre, el color Y hasta por la tierra No hay quien se me pierda Con un vínculo familiar que aterra Característico en muchos de nosotros Que nos reconozcan por la mamá Y hasta por los rostros Étnicos, estilos que entre todos se ven La forma de caminar El cabello y hasta por la piel Y dime quién me va a decir que no Escucho hablar de san pacho Mi patrono allá en quibdo, ey! Donde se ven un pico y juran que fue un beso Donde el manjar al desayuno es el plátano con queso Y eso que no te he hablado de buenaventura Donde se baila el currulao, salsa poco pega’o Puerto fiel al pescado Negras grandes con gran tumba’o Donde se baila aguabajo y pasillo En el lado del río (*ritmo folclórico) Con mis prietillos Somos pacífico, estamos unidos Nos une la región La pinta, la raza y el don del sabor Somos pacífico, estamos unidos Nos une la región La pinta, la raza y el don del sabor Es del pacífico, guapi, timbiquí, tumaco El bordo cauca Seguimos aquí con la herencia africana Más fuerte que antes Llevando el legado a todas partes De forma constante Expresándonos a través de lo cultural Música, artes plástica, danza en general Acento golpia’o al hablar El 1, 2,3 al bailar Después de eso seguro hay muchísimo más Este es pacífico colombiano Una raza un sector Lleno de hermanas y hermanos Con nuestra bámbara y con el caché (bendición, buen espíritu) Venga y lo ve usted mismo Pa vé como es, y eh! Piense en lo que se puede perder, y eh! Pura calentura y yenyeré, y eh! Y ahora dígame que cree usted Por qué colombia es más que coca, marihuana y café'
#query = 'Ya chole chango chilango Que chafa chamba te chutas No checa andar de tacuche Y chale con la charola Tan choncho como una chinche Mas chueco que la fayuca Con fusca y con cachiporra Te paso andar de guarura Mejor yo me hecho una chela Y chance enchufo una chava Chambeando de chafirete Me sobra chupe y pachanga Si choco saco chipote La chota no es muy molacha Chiveando a los que machucan Se va en morder su talacha De noche caigo al congal No manches dice la changa Al choro de teporocho Enchifla pasa la pacha Pachuco cholos y chundos Chichinflas y malafachas Aca los chompiras rifan Y bailan tibiri tabara Mejor yo me hecho una chela Y chance enchufo una chava Chambeando de chafirete Me sobra chupe pachanga Mi ñero mata la bata Le encanta la cucaracha Su choya vive de chochos De chemo churro y garnachas Pachuco cholos y chundos Chichinflas y malafachas Aca los chompiras rifan Y bailan tibiri tabara Tranzando de arriba abajo Hay va la chilanga banda Chin chin si me la recuerdan Carcacha y se les retacha Songwriters: Juan Jaime Camacho Lopez'
#query = 'laburo plata boludeces'
query = preprocess(query)
query = query.split(' ')
n = '3'
n_of_cities=10
sorter = 'sim_score'
####
get_sim_cities3(query,n,n_of_cities,sorter)
'''