# -*- coding: utf-8 -*- 'Plot a data frame for a given query'
import folium, time
from gensim import corpora#, models,similarities
from LogeoFuncs import iter_zip, preprocess, stopwords,get_skipgrams, get_colors,word_cloud_divs,condition1 #sub_skipgrams, get_w2v_sim_scores, get_query_sim_scores, 
import pandas as pd
import numpy as np
#import sys
#sys._enablelegacywindowsfsencoding()
#from selenium import webdriver
path = 'templates/query_maps/'
fname = 'The_top-5000_Spanish_Twitter'
start = time.time()
dict_ = corpora.Dictionary.load('ling_assets/line_assets/'+fname+'.dict')
###############################################################################
'''
#test
query = 'banamex oxxo amlo'
#query = 'laburo plata boludeces'
query = preprocess(query)
query = query.split(' ')
n='3'
colors = '#00ADFF #32BDFF #66CDFF #99DEFF #CCEEFF'.split()
'''
def make_sim_map(query):##########################################################
    m = folium.Map(height=600, width=1150, tiles= 'cartodbpositron')  # #CartoDB dark_matter
    #m = folium.Map(height=950, width=2000, tiles= 'cartodbpositron')  # #CartoDB dark_matter
    print(time.time()-start)
    colors = '#00ADFF #32BDFF #66CDFF #99DEFF #CCEEFF'.split() #blue
    #colors1 = '#ff0038 #ff4c73 #ff6687 #ff7f9b #ff99af #ffb2c3'.split() #pink
    #colors1 = '#ff4800 #ff5a19 #ff6c32 #ff7e4c #ff9166'.split() #yellow
        ##########################################################################
    df = pd.read_csv(path+'sim_cities3.csv')
    df = df.drop(columns=['Unnamed: 0','Unnamed: 0.1'])
    print(time.time()-start)  
    sorter = 'sim_score'
    df = df.fillna(value=0)
    df = df.sort_values(by=[sorter], ascending=False)
    print(time.time()-start)  
    ## CALCULATE RADIUS ###########################################################
    fq_radius = 800000 #~1mio
    df['radius'] = df[sorter]*fq_radius
    df['radius'] = df['radius'].apply(lambda x: np.sqrt(x))
    df['radius'] = df['radius']*180
    df['radius'] = df['radius'].apply(lambda x: round(x,2))
    print(time.time()-start)  
    ## CALCULATE COLORS ###########################################################
    #colors = '#00ADFF #32BDFF #66CDFF #99DEFF #CCEEFF'.split()
    df = get_colors(df, colors, 'sim_color') #BLUE
    df[sorter] = df[sorter].apply(lambda x: round(x*100,5))
    top_labels = list(zip(df['city_ascii'],df['Country'],df['lat'],df['lng'],
                          df['radius'],df[sorter],df['sim_color'], df['ids']))
    print(time.time()-start)  
    for t in top_labels:#######################################################
        folium.Circle(
        popup = t[0],
        #popup=folium.Popup(popup_html, max_width=250, sticky=False),
        location=[t[2],t[3]],
        radius=t[4],
        color=t[6],
        fill=True,
        fill_color=t[6],
        ).add_to(m)
    ####################################################################################
    legend_html = """<div class="query3">%query</div>"""
    legend_html = legend_html.replace('%query', ' '.join(query[:50])+'...')
    with open('templates/query_maps/query.html', 'w', encoding='utf8') as f:
        f.write(legend_html)
    m.fit_bounds(m.get_bounds())
    #m.fit_bounds([[14.424750,-117.128778], [32.464044,-86.559757]])#MEXICO
    #m.fit_bounds([[46.607941,-68.325869], [13.480448,-115.766056]])#MEX,US
    #legend_html = '''      <!--<div style="position:fixed;text-align:center; color:#7f7f7f;top:350px; left: 1260px; width:550px; height: 90px; z-index:9999; font-size:66px; font-family:Georgia;"> El espaÃ±ol de MÃ©xico en Twitter</div>--></br>  <div style="position:fixed;top:370px; text-align:center; left: 10px; width:550px; height: 90px; z-index:9999; font-size:90px; color:#000000; font-family:Georgia;"><i>%query</i></div>  <div style="position:fixed;text-align:center;top:505px; left: 10px; width:550px; height: 90px; z-index:9999; font-size:36px; color:#494949; font-family:Georgia;"> Menciones: %fq_sum</div><br>  <!-- <div style="position:fixed;text-align:left;top:460px; left: 20px; width:550px; height: 90px; z-index:9999; font-size:26px; color:#3a3a3a; font-family:Georgia;"> Menciones: %fq_sum<br> Ciudades donde se menciona: %#cities</div><br>--> <div style="position:fixed;text-align:left;top:935px; left: 20px; width:1200px; height: 90px; z-index:9999; font-size:14px; color:#3a3a3a; font-family:Georgia;">Fuente: https://www.datos.gov.co/Ciencia-Tecnolog-a-e-Innovaci-n/Las-5000-palabras-m-s-frecuentes-en-Twitter-en-Esp/wvij-k76z</div><br> <div style="position:fixed;top:535px; left: 1px; width:300px; height: 90px; z-index:9999; font-size:18px; color:#0a0000;"> <img src= "%freq_chart" height="415" width="740"></div>  <!-- <div style="position: fixed;top:770px; left: 25px; width: 700px; height: 90px; z-index:9999; font-size:19px; color:#0a0000; font-family:Georgia;"> MÃ¡s menciones: %max_city, %max_fq<br> Menos menciones: %min_city, %min_fq</div> --> <!--<div style="position:fixed;text-align:center;top:550px; left:1260px; width:550px; height: 90px; z-index:9999; font-size:18px; color:#8c8c8c; font-family:Georgia;"> <p>u/serioredditor</p></div>-->'''
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
    
    #make_html_map3(query)
