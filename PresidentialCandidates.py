from influenceexplorer import InfluenceExplorer
import numpy as np
import matplotlib.pyplot as plt

api_key = '81ae602f16f34cbc9fe2643c7691f3d3'

ie = InfluenceExplorer(api_key)
person = {}
# set variables for bar chart values and labels
all_recipient_bars=[]
all_recipient_names=[]
all_recipient_colors=[]
    
def add_bar_elements(value, name, color):
    all_recipient_bars.append(value)
    all_recipient_names.append(name)
    all_recipient_colors.append(color)

# enter a candidate
while person != '0':
    person = raw_input('Candidate: ')
    cand_id = {}
    cand = ie.entities.search(person)

    # if more than one choice, print a list of choices and prompt for input
    if len(cand) > 1:
        cand_list = []
        for result in cand:
            cand_list.append([
                result['name'],
                result['seat'],
                result['state'],
                result['id']
                ])
        for name in cand_list:
            print cand_list.index(name), "\t", name[0], name[1], name[2]
        choice = int(raw_input('Choose a person: '))
        cand_id = cand_list[choice][3]
        print "Top contributors for", cand_list[choice][0]

    # if just one candidate, grab their id and proceed
    else:
        cand_id = cand[0]['id']
        print "Top contributors for", cand[0]['name']

    # for each contributor to the candidate, print their total amount contributed,
    # plus a list of other top recipients of employee and direct contributions  
    for contrib in ie.pol.contributors(cand_id, cycle='2012', limit=5):
        print contrib['name'], "."*(30-len(contrib['name'])), contrib['total_amount'] #total contributed to candidate
        
        # insert a blank line
        add_bar_elements(0, ' ', 'b')
              
        # insert a 0-height bar labeled as the contributor
        add_bar_elements(0, contrib['name'].upper(), 'b')
        
        # list top recipients for each contributor...
        try:
            for recipient in ie.org.recipients(contrib['id'], cycle='2012'):
                print "\t", recipient['name'], recipient['employee_amount'], "(employees:", recipient['employee_count'], ")", recipient['direct_amount'], "(direct)"
                recipient_total = float(recipient['employee_amount']) + float(recipient['direct_amount'])
                if recipient['id'] == cand_id:  #add highlighting if recipient is selected candidate
                    add_bar_elements(recipient_total, recipient['name'], 'r')
                else:
                    add_bar_elements(recipient_total, recipient['name'], 'b')
                    
        # unless there are no other recipients.
        except:
            print "\t(no other recipient data available)"
            add_bar_elements(float(contrib['total_amount']), ie.entities.metadata(cand_id)['name'], 'r')

    # flip everything around so everything is in descending order in the horizontal chart                
    all_recipient_bars.reverse()
    all_recipient_names.reverse()
    all_recipient_colors.reverse()
    
    # make the pretty pictures   
    ind = np.arange(len(all_recipient_bars))
    width = 0.8
    plt.barh(ind, all_recipient_bars, color=all_recipient_colors)
    plt.yticks(ind+width/2, all_recipient_names, fontsize=9)
    
    plt.show()