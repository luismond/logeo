# -*- coding: utf-8 -*- 'Plot a data frame for a given query'
import folium, time
from gensim import corpora#, models,similarities
from LogeoFuncs import iter_zip, stopwords,get_skipgrams, get_colors,word_cloud_divs,condition1 #sub_skipgrams, get_w2v_sim_scores, get_query_sim_scores, 
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

#query = 'amor'
#n='1'
#colors = '#00ADFF #32BDFF #66CDFF #99DEFF #CCEEFF'.split()

def add_to_map(query,n,m,colors):
    ##########################################################################
    df = pd.read_csv(path+'sim_cities'+n+'.csv')
    df = df.drop(columns=['Unnamed: 0','Unnamed: 0.1'])
    print(time.time()-start)  
    sorter = 'fq_%'
    df = df.fillna(value=0)
    df = df.sort_values(by=[sorter], ascending=False)
    print(time.time()-start)  
    ## CALCULATE RADIUS ###########################################################
    fq_radius = 80000000 #~1mio
    df['radius'] = df['fq_%']*fq_radius
    df['radius'] = df['radius'].apply(lambda x: np.sqrt(x))
    df['radius'] = df['radius']*180
    df['radius'] = df['radius'].apply(lambda x: round(x,2))
    print(time.time()-start)  
    ## CALCULATE COLORS ###########################################################
    #colors = '#00ADFF #32BDFF #66CDFF #99DEFF #CCEEFF'.split()
    df = get_colors(df, colors, 'sim_color') #BLUE
    df['fq_%'] = df['fq_%'].apply(lambda x: round(x*100,5))
    top_labels = list(zip(df['city_ascii'],df['Country'],df['lat'],df['lng'],
                          df['radius'],df['fq_%'],df['sim_color'], df['ids']))
    print(time.time()-start)  
    
    # SKIP AND W2V SIMS FOR WORD CLOUD
    first_letter = query[0]
    
    dict_sims = pd.read_csv('ling_assets/datasets/'+fname+'_skip_w2v_sims_'+first_letter+'_.csv')
    print('dict_sims')
    print(time.time()-start)     
    dict_sim0 = dict_sims[dict_sims['line_id']==dict_.token2id[query]]
    dict_sim0 = dict_sim0.fillna(0)
    
    if dict_sim0.iloc[0,4] == 0:   #Check if there are w2v sims
        skip_sims = dict_sim0['sims_tokens_ids'].tolist()[0]
        skip_sims = skip_sims.split(',')[:40]

        skip_sims_h = [dict_[int(w)] for w in skip_sims][:10]
        skip_sims_links = ' '.join(["""<a href="/results?query=%query">%query</a>""".replace('%query',w) 
        for w in skip_sims_h])
        skip_sims_html = """<h5>Similar in form</h5> <div> %sim_words_links </div> """.replace('%sim_words_links',skip_sims_links)
        similar_words = skip_sims
        sim_htmls = skip_sims_html
        sim_words_html = """<div class="sim_words"><h4>Similar words to %word</h4>%sim_htmls</div>""".replace('%sim_htmls',sim_htmls)
        sim_words_html = sim_words_html.replace('%word',''.join(query))
    
        with open('templates/query_maps/similar_words'+n+'.html', 'w', encoding='utf8') as f:
            f.write(sim_words_html)
        print(time.time()-start)   
    
    if not dict_sim0.iloc[0,4] == 0:   #Check if there are w2v sims
        skip_sims = dict_sim0['sims_tokens_ids'].tolist()[0]
        skip_sims = skip_sims.split(',')[:40]
        skip_sims_h = [dict_[int(w)] for w in skip_sims][:10]
        skip_sims_links = ' '.join(["""<a href="/results?query=%query">%query</a>""".replace('%query',w) 
        for w in skip_sims_h])
        skip_sims_html = """<h5>Similar in form</h5> <div class="sim_links"> %sim_words_links </div> """.replace('%sim_words_links',skip_sims_links)
        #similar_words = skip_sims
        
        w2v_sims = dict_sim0['w2v_sims_tokens_ids'].tolist()[0]
        w2v_sims = w2v_sims.split(',')[:40]
        w2v_sims_h = [dict_[int(w)] for w in w2v_sims][:10]
        w2v_sims_links = ' '.join(["""<a href="/results?query=%query">%query</a>""".replace('%query',w) 
        for w in w2v_sims_h])
        w2v_sims_html = """<h5>Close in meaning and usage</h5> <div class="sim_links"> %sim_words_links </div> """.replace('%sim_words_links',w2v_sims_links)
        similar_words = skip_sims + w2v_sims
                
        sim_htmls = skip_sims_html + w2v_sims_html
        
        
        sim_words_html = """<div class="sim_words%n"><h4>Similar words to %word</h4>%sim_htmls</div>""".replace('%sim_htmls',sim_htmls)
        sim_words_html = sim_words_html.replace('%n',n)
        sim_words_html = sim_words_html.replace('%word',''.join(query))
    
        with open('templates/query_maps/similar_words'+n+'.html', 'w', encoding='utf8') as f:
            f.write(sim_words_html)
        print(time.time()-start)   
    

    for t in top_labels:#######################################################
        popup_title = t[1]+', '+t[0].title()
        query_fq = t[5]
        ids = t[7].split(',')
        dict_sim02 = [dict_[int(w)] for w in similar_words if w in ids] 
        sub_df = pd.DataFrame(dict_sim02)
        sub_df.columns=['line']
        print(time.time()-start)   
        sub_df['font_size'] = list(sorted([(n+7)*2 for n in range(len(sub_df.index))],reverse=True))
        words = sub_df['line'].tolist()
        print(words)
        #html_x = """ <a href="/results?query=%w">%w</a> """
        #words = [html_x.replace('%w',w)+'&nbsp;' for w in words]
        font_sizes = sub_df['font_size'].tolist()
        words_dict = dict(zip(words,font_sizes))
        print(time.time()-start)          
        divs = word_cloud_divs(words_dict,n)
        with open (path+'popup_html.html', 'r', encoding='utf8') as f:
            popup_html = f.read()
        
        popup_html = popup_html.replace('%divs',' '.join(divs))
        popup_html = popup_html.replace('%popup_title', popup_title)
        popup_html = popup_html.replace('%query_fq', str(query_fq)+'%')
        
        folium.Circle(
        popup=folium.Popup(popup_html, max_width=250, sticky=False),
        location=[t[2],t[3]],
        radius=t[4],
        color=t[6],
        fill=True,
        fill_color=t[6],
        ).add_to(m)



def make_html_map(query0,query1):##########################################################  
    m = folium.Map(height=600, width=1150, tiles= 'cartodbpositron')  # #CartoDB dark_matter
    #m = folium.Map(height=950, width=2000, tiles= 'cartodbpositron')  # #CartoDB dark_matter
    
    print(time.time()-start)
    colors0 = '#00ADFF #32BDFF #66CDFF #99DEFF #CCEEFF'.split() #blue
    colors1 = '#ff0038 #ff4c73 #ff6687 #ff7f9b #ff99af #ffb2c3'.split() #pink
    #colors1 = '#ff4800 #ff5a19 #ff6c32 #ff7e4c #ff9166'.split() #yellow

    
    add_to_map(query0, '0', m, colors0)
    if not query1 == 'None':
        add_to_map(query1, str(1),m,colors1)
    ####################################################################################
    
    legend_html = """<div class="queries">
        <span class="query0"><a class="query0" href="/results?query=%query0">%query0</a></span> 
        <span class="query1"><a class="query1"href="/results?query=%query1">%query1</a></span>
        </div>"""
        
    #legend_html = """<div style="position:fixed;text-align:center; color:#656565;top:420px; left: 1320px; width:550px; height: 90px; z-index:9999; font-size:66px; font-family:Georgia;"> El español de México y E.E.U.U en Twitter</div><div class="queries" style="position:fixed;top:550px; text-align:center; left: 10px; width:550px; height: 90px; z-index:9999; font-size:100px; color:#000000; font-family:Georgia;">
    #    <span class="query0" style="border-bottom:6px solid #00ADFF">%query0</span><br>
    #    <span class="query1" style="border-bottom:6px solid #ff0038; padding-top:20px;">%query1</span><br>
    #    <div style="color:#656565;font-size:16px;position:fixed;top:860px;text-align:left;font-familiy:Georgia"><p>u/serioredditor</p><p>Source: https://www.datos.gov.co/Ciencia-Tecnolog-a-e-Innovaci-n/Las-5000-palabras-m-s-frecuentes-en-Twitter-en-Esp/wvij-k76z</p></div></div>"""
    legend_html = legend_html.replace('%query0', ''.join(query0))
    if not query1 == 'None':
        legend_html = legend_html.replace('%query1', ''.join(query1))
    if query1 == 'None':
        legend_html = legend_html.replace('%query1', '')
    with open('templates/query_maps/query.html', 'w', encoding='utf8') as f:
        f.write(legend_html)
     
    #m.get_root().html.add_child(folium.Element(legend_html))
    
    m.fit_bounds(m.get_bounds())
    #m.fit_bounds([[14.424750,-117.128778], [32.464044,-86.559757]])#MEXICO
    #m.fit_bounds([[46.607941,-68.325869], [13.480448,-115.766056]])#MEX,US
    #legend_html = '''      <!--<div style="position:fixed;text-align:center; color:#7f7f7f;top:350px; left: 1260px; width:550px; height: 90px; z-index:9999; font-size:66px; font-family:Georgia;"> El español de México en Twitter</div>--></br>  <div style="position:fixed;top:370px; text-align:center; left: 10px; width:550px; height: 90px; z-index:9999; font-size:90px; color:#000000; font-family:Georgia;"><i>%query</i></div>  <div style="position:fixed;text-align:center;top:505px; left: 10px; width:550px; height: 90px; z-index:9999; font-size:36px; color:#494949; font-family:Georgia;"> Menciones: %fq_sum</div><br>  <!-- <div style="position:fixed;text-align:left;top:460px; left: 20px; width:550px; height: 90px; z-index:9999; font-size:26px; color:#3a3a3a; font-family:Georgia;"> Menciones: %fq_sum<br> Ciudades donde se menciona: %#cities</div><br>--> <div style="position:fixed;text-align:left;top:935px; left: 20px; width:1200px; height: 90px; z-index:9999; font-size:14px; color:#3a3a3a; font-family:Georgia;">Fuente: https://www.datos.gov.co/Ciencia-Tecnolog-a-e-Innovaci-n/Las-5000-palabras-m-s-frecuentes-en-Twitter-en-Esp/wvij-k76z</div><br> <div style="position:fixed;top:535px; left: 1px; width:300px; height: 90px; z-index:9999; font-size:18px; color:#0a0000;"> <img src= "%freq_chart" height="415" width="740"></div>  <!-- <div style="position: fixed;top:770px; left: 25px; width: 700px; height: 90px; z-index:9999; font-size:19px; color:#0a0000; font-family:Georgia;"> Más menciones: %max_city, %max_fq<br> Menos menciones: %min_city, %min_fq</div> --> <!--<div style="position:fixed;text-align:center;top:550px; left:1260px; width:550px; height: 90px; z-index:9999; font-size:18px; color:#8c8c8c; font-family:Georgia;"> <p>u/serioredditor</p></div>-->'''
    #top_label_len = str(int(len(top_labels)))
    #m.save('templates/query_maps/'+top_label_len+'_'+''.join(query)+'_sim_cns_map.html')
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
        

#query0 = 'amor'
#query1 = 'odio'
#make_html_map(query0,query1)

    '''
    import os
    #Selenium
    delay=5
    fn= 'templates/query_maps/sim_cities_map.html'
    tmpurl='file://{path}/{mapfile}'.format(path=os.getcwd(),mapfile=fn)
    #m.save(fn)
    browser = webdriver.Firefox()
    browser.maximize_window()
    browser.get(tmpurl) 
    time.sleep(delay)#Give the map tiles some time to load
    browser.save_screenshot('templates/query_maps/'+query0+'_'+query1+'_sim_cities_map.png')
    browser.quit()
    '''



  

#####################################################################################    

#disp_query = query.split('_')    #disp_query = disp_query[1]

#top_label = top_labels[0]
#bottom_label = top_labels[-1:][0]
#fq_sum = int(sum(df['query_fq'].tolist()))
#fq_sum = fq_sum*100
#legend_html = legend_html.replace('%fq_sum',str(fq_sum))
#legend_html = legend_html.replace('%min_city', bottom_label[6].title())
#legend_html = legend_html.replace('%min_freq', str(top_label[5]))  
#legend_html = legend_html.replace('%max_city', top_label[6].title())
#legend_html = legend_html.replace('%max_fq', str(int(top_label[5])))
#legend_html = legend_html.replace('%min_fq', str(int(bottom_label[5])))
#legend_html = legend_html.replace('%#cities', str(len(top_labels)))
#top_label_len = str(int(len(top_labels)))
#df_top = df.iloc[:5]
#df_top['query_fq'] = df_top['query_fq'].astype(int)
#legend_html = legend_html.replace('%freq_chart', savename)
 
# SELENIUM ####################################################################
'''
#Selenium #delay=5 #fn= 'templates/simple_maps/'+top_label_len+'_'+''.join(query)+'_sim_cns_map.html' #tmpurl='file://{path}/{mapfile}'.format(path=os.getcwd(),mapfile=fn) #m.save(fn) #browser = webdriver.Firefox() #browser.maximize_window() #browser.minimize_window() #browser.get(tmpurl) #time.sleep(delay) #Give the map tiles some time to load #browser.save_screenshot(top_label_len+'_'+''.join(query)+'_sim_cns_map.png') #browser.save_screenshot(''.join(query)+'_sim_cns_map.png') #browser.quit()
'''
###############################################################################

#from LogeoGifMaker import make_gif
#make_gif()
'''
#df_plot
fig = df_top.plot(x='city_display',
                      y='fq_%', 
                      kind='bar', 
                      rot=14, 
                      legend=False,
                      figsize=(65,35),
                      fontsize=74,
                      colormap='coolwarm',
                      grid=False).get_figure()
savename = top_label_len+'_'+''.join(query)+'_freq_chart.png'
fig.savefig('templates/freq_maps/'+savename,transparent=True)

'''