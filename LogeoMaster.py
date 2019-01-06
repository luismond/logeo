#LOGEO MASTER. Make city similarity map with word cloud results.
import time
from LogeoGetSimCities import get_sim_cities
from LogeoMakeCitiesMap import make_html_map
###############################################################################
start = time.time()
path = 'ling_assets/'
fname = 'The_top-5000_Spanish_Twitter'
print(time.time()-start)

###################### VECTORS ################################################
#vec_es = 'vectors/'+"cc.es.300.vec"#vec_en = path+"cc.en.300.vec"
#word2vec_es = models.KeyedVectors.load_word2vec_format(vec_es, limit=100000)#word2vec_en = models.KeyedVectors.load_word2vec_format(vec_en, limit=100000)
#print(time.time()-start)

## QUERY ######################################################################
#query0 = 'amlo'
#query1 = 'lmao'

#queries = [['amlo','lmao'],['amor','odio'],['wey','guey'],['tacos','burritos'],['pedo','peda'],['cheve','chela'],
# ['caray','carajo'],['cheves','chelas'],['mole','pozole'],['tequila','mezcal'],['cheve','chela'],
# ['coca','pepsi'],['pizza','mariscos'],['futbol','beisbol'],['playa','montaña'],
# ['pizza','mariscos'],['amor','sexo'],['paz','guerra'],['frontera','capital'],['chingo','chingos'],['frío','calor'],
# ['paz','guerra'],['juan','pedro'],['chale','chido'],['nadamas','nomás'],['vato','morra']]

#queries = [['ntc','omg'],['nomas','nomás'],['asada','barbacoa'],['televisa','telemundo'],['gorditas','quesadillas'],
#           ['tamales','tortas'],['chivas','pumas'],['rayados','tigres'],['oxxo','starbucks'],['barrio','fraccionamiento'],
#           ['santa','santo'],['acá','aquí'],['belleza','chulada'],['neta','verdad'],['tanto','tantito'],['amonos','vamonos'], 
#           ['mexico','méxico'],['apoco','nimodo'],['telmex','pemex'],['ándale','órale'],['dios','vida'],['preparatoria','bachillerato'],

       
#queries = [['chipotle','dominos'],['pinche','inche'],['weba','hueva'],
#           ['guacamole','aguacate'],['mames','manches'],['marihuana','marijuana'],['problema','problemo'],['san','santa'],['san','santa'],['santo','santa']

#queries = [['jorge','luis'],['derecha','izquierda'],['lópez','gómez'],['gonzález','pérez'],['hernández','garcía']]

#queries = [['nacos','fresas'],['naco','fresa'],['naca','fresa'],['chingón','chingona'],['puto','puta']]
#queries = [['',''],['',''],['',''],['',''],['','']]

#queries = [['soriana','walmart'],['banda','corridos'],['rock','pop']]


for q in queries:
    query0 = q[0]
    query1 = q[1]
    
    #### M A K E R S ##############################################################
    get_sim_cities(query0,str(0),75)
    get_sim_cities(query1,str(1),75)
    
    make_html_map(query0,query1)
