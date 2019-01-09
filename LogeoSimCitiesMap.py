# 'Plot a data frame for a given query'
import folium, time
from gensim import corpora
from LogeoFuncs import get_colors
import pandas as pd
import numpy as np

path = 'templates/query_maps/'
fname = 'The_top-5000_Spanish_Twitter'
start = time.time()
dict_ = corpora.Dictionary.load('ling_assets/line_assets/'+fname+'.dict')


def make_sim_map(query):
    m = folium.Map(height=600, width=1150, tiles= 'cartodbpositron')  

    print(time.time()-start)
    colors = '#00ADFF #32BDFF #66CDFF #99DEFF #CCEEFF'.split() #blue
    df = pd.read_csv(path+'sim_cities3.csv')
    df = df.drop(columns=['Unnamed: 0','Unnamed: 0.1'])
    print(time.time()-start)  
    sorter = 'sim_score'
    df = df.fillna(value=0)
    df = df.sort_values(by=[sorter], ascending=False)
    print(time.time()-start)  
    ## CALCULATE RADIUS ##
    fq_radius = 700000 #~1mio
    df['radius'] = df[sorter]*fq_radius
    df['radius'] = df['radius'].apply(lambda x: np.sqrt(x))
    df['radius'] = df['radius']*180
    df['radius'] = df['radius'].apply(lambda x: round(x,2))
    print(time.time()-start)  
    ## CALCULATE COLORS ####
    df = get_colors(df, colors, 'sim_color') #BLUE
    df[sorter] = df[sorter].apply(lambda x: round(x*100,5))
    top_labels = list(zip(df['city_ascii'],df['Country'],df['lat'],df['lng'],
                          df['radius'],df[sorter],df['sim_color'], df['ids']))
    print(time.time()-start)  
    for t in top_labels:
        folium.Circle(
        popup = t[0],
        location=[t[2],t[3]],
        radius=t[4],
        color=t[6],
        fill=True,
        fill_color=t[6],
        ).add_to(m)

    legend_html = """<div class="query3">%query</div>"""
    legend_html = legend_html.replace('%query', ' '.join(query[:50])+'...')
    with open('templates/query_maps/query.html', 'w', encoding='utf8') as f:
        f.write(legend_html)
    m.fit_bounds(m.get_bounds())

    m.save('templates/query_maps/sim_cities_map.html')
    #Post-fuckery
    with open('templates/query_maps/sim_cities_map.html','r') as f:
        h = f.read()
        h = h.replace("""width: 1000.0px;
        height: 1000.0px;""",'width: 100vw;height:100%;')
        h = h.replace("""    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css"/>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css"/>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css"/>""",'')
        h = h.replace("""<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>""",'')
        h = h.replace("""<style>html, body {width: 100%;height: 100%;margin: 0;padding: 0;}</style>
    <style>#map {position:absolute;top:0;bottom:0;right:0;left:0;}</style>""",
    """<style>body { padding: 0;  margin: 0; } </style> <style>html, body, #map {     height: 100%;     width: vw; }</style""" )
        h = h.replace("""        width: 1150.0px;
        height: 600.0px;
        left: 0.0%;
        top: 0.0%;
        }
    </style>""","""width: vw;
        height: 500px;
        left: 0.0%;
        top: 0.0%;
        }
    </style>""")
        h = h.replace("""<head>""","""<head><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />""")
    print(time.time()-start)
    with open('templates/query_maps/sim_cities_map.html','w') as f:
        f.write(h)
    
