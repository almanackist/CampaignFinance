from influenceexplorer import InfluenceExplorer
from transparencydata import TransparencyData
import numpy as np
import matplotlib.pyplot as plt

api_key = '81ae602f16f34cbc9fe2643c7691f3d3'

ie = InfluenceExplorer(api_key)
td = TransparencyData(api_key)

city_name = ""

while city_name != "0":

    city_name = raw_input("Enter a city: ")
    state_name = raw_input("Enter a state abbreviation: ")
    
    bTotal = []
    oTotal = []
    sTotal = []
    hTotal = []
    
    for i in td.earmarks(city=city_name, state=state_name):
        print i['fiscal_year'], 
        print "Budget:", i['budget_amount'], 
        print "\tOmni:", i['omni_amount'], 
        print "\tSenate", i['senate_amount'], 
        print "\tHouse:", i['house_amount'], 
        print "\n\t", 
        print i['members'], 
        print "\n\t", 
        print i['description'], 
        print "\n\t", 
        print i['bill_section']
        bTotal.append(float(i['budget_amount']))
        oTotal.append(float(i['omni_amount']))
        sTotal.append(float(i['senate_amount']))
        hTotal.append(float(i['house_amount']))
    
    print "Budget total: ", sum(bTotal)
    print "Omni total: ", sum(oTotal)
    print "Senate total: ", sum(sTotal)
    print "House total: ", sum(hTotal)
    
    vals = (sum(bTotal), sum(oTotal), sum(sTotal), sum(hTotal))
    print vals
    print "Overall total: ", sum(vals)
    
    ind = np.arange(len(vals))
    print "ind: ", ind
    width = 1
    plt.barh(ind, vals, width)
    plt.title('Earmarks for '+city_name+" "+state_name)
    plt.yticks(ind+width/2., ('Budget', 'Omni', 'Senate', 'House') )
    plt.show()
