from DataBase.querys import *
from datetime import *
import pandas

def set_message(request,database):
    '''ss'''
    try:
        request['function']='W_S'
        dr_r = database.datainsert(querys(request))
        return {'msj':dr_r}
    except:
        return {'msj':'error'}

def read_message(request,database):
    #try:
        request['function']='R_S'
        dr_r = database.datasearch(querys(request))
        messages=[]
        advisors=[]
        actual = []
        n = datetime.now().strftime('%d-%m-%Y')
        for i in dr_r:
            messages.append({'text':i[1],'date':i[2],'id':i[0]})
        for e in range(len(messages)):
            date=messages[e]['date']
            date =date.split(sep='/')
            date=date[::-1]
            messages[e]['date']=date[0]+'/'+date[1]+'/'+date[2]
        orded=sorted(messages, key=lambda order: order['date'])
        for e in range(len(orded)):
            date=orded[e]['date']
            date =date.split(sep='/')
            date=date[::-1]
            orded[e]['date']=date[0]+'/'+date[1]+'/'+date[2]
        for x in orded:
            if x['date'][6]+x['date'][7]+x['date'][8]+x['date'][9] > n[6]+n[7]+n[8]+n[9]:
                actual.append(x)
            elif x['date'][6]+x['date'][7]+x['date'][8]+x['date'][9] == n[6]+n[7]+n[8]+n[9]:
                if x['date'][3]+x['date'][4] > n[3]+n[4]:
                    actual.append(x)
                elif x['date'][3]+x['date'][4] == n[3]+n[4]:
                    if x['date'][0]+x['date'][1] > n[0]+n[1]:
                        actual.append(x)
                    elif x['date'][0]+x['date'][1] == n[0]+n[1]:
                        actual.append(x)
        if len(actual) <= 5:
            return {'element':actual}
        else:
            for e in range(5):
                advisors.append(actual[e])
        return {'element':advisors}
    #except:
    #    return {'msj':'error'}

def delete_message(request,database):
    try:
        request['function']='D_S'
        dr_r = database.datainsert(querys(request))
        return {'element':dr_r}
    except:
        return {'msj':'error'}

def set_pdf(request,database):
    request['id']=0
    request['function']='R_ONE_PDF_S'
    db_r = database.datasearch(querys(request))
    if db_r == ():
        request['function']='W_PDF_S'
        database.datainsert(querys(request))
        request['function']='R_ONE_PDF_S'
        db_r = database.datasearch(querys(request))
        return {'id':db_r}
    else:
        return {'msj':'pdf already exist'}

def read_arr_pdf(request,database):
    request['function']='R_PDF_S'
    db_r = database.datasearch(querys(request))
    context=[]
    if db_r != ():
        for i in db_r:
            aux={'id':str(i[0]),'name':i[1],'type':i[2]}
            context.append(aux)
    return {'element':context}

def weekly_messages(messages):
    d = datetime.strptime(datetime.now().strftime('%d-%m-%Y'), '%d-%m-%Y')
    l  = []
    week_days = []
    response = []
    for x in range(0,7):
        d = d + timedelta(days=1)
        l.append(d)
    for e in l:
        date = e.strftime('%d-%m-%Y')
        week_days.append(date[0]+date[1]+'/'+date[3]+date[4]+'/'+date[6]+date[7]+date[8]+date[9])
        response.append({'name':pandas.Timestamp(date[6]+date[7]+date[8]+date[9]+'-'+date[3]+date[4]+'-'+date[0]+date[1]).day_name(),'date':date[0]+date[1]+'/'+date[3]+date[4]+'/'+date[6]+date[7]+date[8]+date[9],'messages':[]})
    for m in messages:
        if m['date'] in week_days:
            for e in response:
                if m['date'] == e['date']:
                    e['messages'].append(m)
    return response