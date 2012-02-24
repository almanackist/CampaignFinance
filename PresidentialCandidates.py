from influenceexplorer import InfluenceExplorer
import numpy as np
import matplotlib.pyplot as plt

api_key = '81ae602f16f34cbc9fe2643c7691f3d3'

ie = InfluenceExplorer(api_key)
person = {}

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

    # just one possible candidate
    else:
        cand_id = cand[0]['id']
        print "Top contributors for", cand[0]['name']

    # set variables for bar chart values and labels
    all_recipient_bars=[]
    all_recipient_names=[]

    # for each contributor to the candidate,
    # print their total amount contributed,
    # plus a list of other top recipients of 
    # employee and direct contributions  
    for contrib in ie.pol.contributors(cand_id, cycle='2012'):
        print contrib['name'], "."*(30-len(contrib['name'])), contrib['total_amount']
        
        local_recipient_bars=[]
        local_recipient_names=[]
        
        try:
            for recipient in ie.org.recipients(contrib['id'], cycle='2012'):
                print "\t", recipient['name'], recipient['employee_amount'], "(employees:", recipient['employee_count'], ")", recipient['direct_amount'], "(direct)"
                recipient_total = float(recipient['employee_amount']) + float(recipient['direct_amount'])
                local_recipient_bars.append(recipient_total)
                local_recipient_names.append(contrib['name']+":"+recipient['name'])
                    
        except:
            print "\t(no other recipient data available)"
            local_recipient_bars.append(float(contrib['total_amount']))
            local_recipient_names.append(contrib['name'])
        
        all_recipient_bars.append(local_recipient_bars)
        all_recipient_names.append(local_recipient_names)
        
    print all_recipient_bars
    print all_recipient_names
    
    last_max_ind = 0
    index = 0
    
    for sub_plot in all_recipient_bars:
        ind = np.arange(len(sub_plot))
        width = 0.8
        new_ind = [(last_max_ind + i) for i in ind]
        plt.barh(new_ind, sub_plot)
        plt.yticks(new_ind, all_recipient_names[index])
        print sub_plot
        print all_recipient_names[index]
        last_max_ind = new_ind[-1] + 2
        index += 1
    
    plt.show()