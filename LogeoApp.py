from flask import Flask, render_template, flash, request, Markup
from wtforms import Form, TextField, validators

from LogeoGetTopFreqCities import get_top_fq_cities
from LogeoFreqCitiesMap import make_html_map

from LogeoGetTopSimCities import get_sim_cities
from LogeoSimCitiesMap import make_sim_map
from LogeoFuncs import preprocess,get_query_id,make_country_map,get_top_words_from_country

from gensim import corpora

path = 'ling_assets/'
fname = 'The_top-5000_Spanish_Twitter'
# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
class ReusableForm(Form):
    name = TextField('word:', validators=[validators.required()])
@app.route("/", methods=['GET', 'POST'])
def home():
    form = ReusableForm(request.form)
    dict_ = corpora.Dictionary.load(path+'sim_assets/'+fname+'.dict')
    print (form.errors)
    if request.method == 'POST':
        name=request.form['name']
        if form.validate():
            query = name
            query = preprocess(query)
            query = query.split(' ')
            if len(query)==1:
                query0 = query[0]
                query_id = get_query_id(query0,dict_)
                if query_id == 'query not in dict':
                    flash('Word not in dictionary. Please try again')
                if query_id != 'query not in dict':
                    query1 = 'None'
                    get_top_fq_cities(query0,'0',100)
                    make_html_map(query0,query1)
                    with open('templates/query_maps/top_fq_cities0.html','r',encoding='utf8') as top_labels0:
                        top_labels0 = top_labels0.read()
                        top_labels0 = Markup(top_labels0)
                    with open('templates/query_maps/similar_words0.html','r',encoding='utf8') as sim_words0:
                        sim_words0 = sim_words0.read()
                        sim_words0 = Markup(sim_words0) + top_labels0
                        flash(sim_words0)
            if len(query)==2:
                query0 = query[0]
                query_id0 = get_query_id(query0,dict_)
                query1 = query[1]
                query_id1 = get_query_id(query1,dict_)
                if query_id0 == 'query not in dict':
                    flash('Word not in dictionary. Please try again')
                if query_id1 == 'query not in dict':
                    flash('Word not in dictionary. Please try again')
                if query_id0 != 'query not in dict' and query_id1 != 'query not in dict':
                    get_top_fq_cities(query0,'0',50)
                    get_top_fq_cities(query1,'1',50)
                    make_html_map(query0,query1)    
                    with open('templates/query_maps/top_fq_cities0.html','r',encoding='utf8') as top_labels0:
                        top_labels0 = top_labels0.read()
                        top_labels0 = Markup(top_labels0)
                    with open('templates/query_maps/similar_words0.html','r',encoding='utf8') as sim_words0:
                        sim_words0 = sim_words0.read()
                        results0 = Markup(sim_words0) + top_labels0
                    with open('templates/query_maps/top_fq_cities1.html','r',encoding='utf8') as top_labels1:
                        top_labels1 = top_labels1.read()
                        top_labels1 = Markup(top_labels1)
                    with open('templates/query_maps/similar_words1.html','r',encoding='utf8') as sim_words1:
                        sim_words1 = sim_words1.read()
                        results1 = Markup(sim_words1) + top_labels1
                        results = results0+results1
                        flash(results) 
            if len(query)>2:
                get_sim_cities(query,'3',5,'sim_score')
                make_sim_map(query)
                with open('templates/query_maps/top_fq_cities3.html','r',encoding='utf8') as top_labels0:
                    top_labels0 = top_labels0.read()
                    top_labels0 = Markup(top_labels0)
                    flash(top_labels0)
        else:
            flash('Please, enter one or two words')
    return render_template('logeo_home.html', form=form)

@app.route("/results", methods=['GET', 'POST'])
def query_example():
    form = ReusableForm(request.form)
    dict_ = corpora.Dictionary.load(path+'sim_assets/'+fname+'.dict')
    query = request.args.get('query') 
    query = preprocess(query)
    query = query.split(' ')
    if len(query)==1:
        query0 = query[0]
        query_id = get_query_id(query0,dict_)
        if query_id == 'query not in dict':
            flash('Word not in dictionary. Please try again')
        if query_id != 'query not in dict':
            query1 = 'None'
            get_top_fq_cities(query0,'0',100)
            make_html_map(query0,query1)
            with open('templates/query_maps/top_fq_cities0.html','r',encoding='utf8') as top_labels0:
                top_labels0 = top_labels0.read()
                top_labels0 = Markup(top_labels0)
            with open('templates/query_maps/similar_words0.html','r',encoding='utf8') as sim_words0:
                sim_words0 = sim_words0.read()
                sim_words0 = Markup(sim_words0) + top_labels0
                flash(sim_words0)
    return render_template('logeo_home.html', form=form)

@app.route("/country", methods = ['GET','POST'])
def get_country_map():
    form = ReusableForm(request.form)
    query = request.args.get('query')
    n = request.args.get('n')
    n = int(n)
    metric = request.args.get('metric')
    make_country_map(query)
    get_top_words_from_country(metric,query,n)
    if metric == 'frequency':
        page = 'logeo_country_frequency.html'
        return render_template(page, form=form)
    if metric == 'tfidf':
        page = 'logeo_country_tfidf.html'
        return render_template(page, form=form)
    

    
if __name__ == "__main__":
	app.run(host='0.0.0.0')