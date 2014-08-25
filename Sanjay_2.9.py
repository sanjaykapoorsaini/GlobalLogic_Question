import csv 
import operator

#----------------------------------------------------------------------
def get_desired_data(hours):
    """ Read a csv file and returns the desired format of the data,  
        Maximize the number of presenters and divide into three sessions on basis of minimum cost.    
    """  
    
    reader = csv.DictReader(open('data_file.csv'), delimiter=',') 
    results = []    
    
    sortedlist = sorted(reader, key=lambda x: int(x['Cost benefit for presenter'].replace('$', '')))  # sort the data as per cost   
    sortedlist = sorted(sortedlist, key=operator.itemgetter('No. of Hours for Presentation'))         # Sort the data as per persenter's hours
    results = [i for i in sortedlist if int(i['No. of Hours for Presentation']) <= hours / 2 ]          
    presenters = []
    total_hour = 0
    for result in results:        
        hour = int(result['No. of Hours for Presentation'])   
        if total_hour == hours:
            break     
        if (total_hour + hour) <= hours:            
            total_hour += hour
            presenters.append(result)       # list of all presenters with total hours equal to hours entered   
        else:            
            presenters = sorted(presenters, key=lambda x: int(x['Cost benefit for presenter'].replace('$', '')), reverse=True)# sorting on bases of cost
            # add the presenter in list whose cost is minimum as per its occurrence 
            index = 0
            for presenter in presenters:
                index += 1  
                presenter_time = int(presenter['No. of Hours for Presentation']) 
                presenter_cost = int(presenter['Cost benefit for presenter'].replace('$', ''))
                if presenter_cost > int(result['Cost benefit for presenter'].replace('$', '')) and total_hour + hour - presenter_time <= hours:
                     presenters.pop(index - 1)
                     presenters.append(result)
                     total_hour = total_hour + hour - presenter_time    
        
    if len(presenters) < 3:
        print ('**** Not enough presenters.')   
        return
       
    get_sessions_info(presenters, hours)

def get_sessions_info(presenters, hours):     
    """ get all the sessions details and name of presenters as per sessions"""           
    sessions = []
    presenter_list = []
    final_presenter_list = []
    session_hours = 0
    index = 0    
    last_presenter = presenters.pop()    

    for presenter in presenters:       
        hour = int(presenter['No. of Hours for Presentation'])
        presenter_list.append(presenter['Presenter Name']) 
        session_hours += hour 
        if not (session_hours + hour < hours / 2 or session_hours + hour == 1) :                          
            sessions.insert(index, session_hours)                               #Insert sum of hours as per session
            final_presenter_list.append(presenter_list)                         #Final list of presenters as per session    
            session_hours = 0
            index += 1            
            presenter_list = []        
             
    if index == 1:                                                              # handle case when on one session is formed 
        sessions.insert(index, session_hours)  
        final_presenter_list.append(presenter_list)
        session_hours = 0                    
        presenter_list = []        
    
    # add the last element hours and presenter in third session 
    sessions.insert(2, session_hours + int(last_presenter['No. of Hours for Presentation']))
    presenter_list.append(last_presenter['Presenter Name'])
    final_presenter_list.append(presenter_list)    
        
    print ('Sessions: ' + str(sessions))    
    print ('Name of Presenters (A/o to Sessions) : ' + str(final_presenter_list))      
    
#----------------------------------------------------------------------
def main():
    """First method called, it takes the input Hours"""
    
    hours = raw_input('Please Enter The Conference Hours : ')    
    if hours.isdigit():        
        get_desired_data(int(hours))
    else:
        print ('**** Please Enter an Integer')
        main()

main()
