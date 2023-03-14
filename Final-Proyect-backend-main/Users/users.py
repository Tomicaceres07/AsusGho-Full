import datetime
from DataBase.querys import querys

#Verificate
def verif(user,database):
        #get information of user
    context =user

    #Verificate the mail direction
    if ('@liceopaz.edu.ar' in context['email']) == True:#Personal

        context['function']='R_U'
        db_r = database.datasearch(querys(context)[0])

        if db_r != ():
            return {'element':db_r,'type':False}
        else:
            context['function']='W_U'
            db_r =database.datainsert(querys(context)[0])
            context['function']='R_U'
            db_r = database.datasearch(querys(context)[0])
            return {'element':db_r,'type':False}

    elif ('@alumnos.liceopaz.edu.ar' in context['email'])== True:#Students
        context['function']='R_U'
        db_r = database.datasearch(querys(context)[1])

        if db_r != ():
            return {'element':db_r,'type':True}
        else:
            context['function']='W_U'
            database.datainsert(querys(context)[1])
            context['function']='R_U'
            db_r = database.datasearch(querys(context)[1])
            return {'element':db_r,'type':True}
    else:    
        return {'msj':'mail not valid'}


def set_year(user,database):
    user['function']='R_U'
    data=database.datasearch(querys(user)[1])
    if data != ():
        user['c_abscence']=database.datasearch(querys(user)[1])[0][3]
        user['function']='U_U'
        context=database.datainsert(querys(user)[0])
        return context
    else:
        return {'msj':'data error'}

def del_abs(user,database):
    try:
        abs =get_abscence(user,database)[1]
        context ={}
        #Verificate the mail direction
        if ('@liceopaz.edu.ar' in user['email']) == True:#Person
            context['deatil']=database.datainsert(querys({'function':'D_ABS','id':user['id']}))

            user['function']='R_U'
            context['c_abscence']=database.datasearch(querys(user)[0])[0][4]
            user['c_abscence']=abs-context['c_abscence']

            user['function']='U_U'
            context=database.datainsert(querys(user)[1])
            return context

        elif ('@alumnos.liceopaz.edu.ar' in user['email'])== True:#Students
            context['deatil']=database.datainsert(querys({'function':'D_ABS','id':user['id']}))

            user['function']='R_U'
            context['c_abscence']=database.datasearch(querys(user)[1])[0][3]
            user['year']=database.datasearch(querys(user)[1])[0][4]
            user['c_abscence']=abs-context['c_abscence']

            user['function']='U_U'
            context=database.datainsert(querys(user)[0])
            return context
    except:
        return {'msj':'error'}

def Update_abscence(user,database):
    try:
        context ={}
        #Verificate the mail direction
        if ('@liceopaz.edu.ar' in user['email']) == True:#Person
            date = datetime.datetime.today().strftime('%Y-%m-%d')
            context['deatil']=database.datainsert(querys({'function':'W_ABS','email':user['email'],'abs':user['c_abscence'],'justified':user['justified'],'date':date}))

            user['function']='R_U'
            context['c_abscence']=database.datasearch(querys(user)[0])[0][4]
            user['c_abscence']=user['c_abscence']+context['c_abscence']

            user['function']='U_U'
            context=database.datainsert(querys(user)[1])
            return context

        elif ('@alumnos.liceopaz.edu.ar' in user['email'])== True:#Students
            date = datetime.datetime.today().strftime('%Y-%m-%d')
            context['deatil']=database.datainsert(querys({'function':'W_ABS','email':user['email'],'abs':user['c_abscence'],'justified':user['justified'],'date':date}))

            user['function']='R_U'
            context['c_abscence']=database.datasearch(querys(user)[1])[0][3]
            user['year']=database.datasearch(querys(user)[1])[0][4]
            user['c_abscence']=user['c_abscence']+context['c_abscence']

            user['function']='U_U'
            context=database.datainsert(querys(user)[0])
            return context
    except:
        return {'msj':'error'}

def get_abscence(user,database):
    response = []
    abscence = 0
    user['function']='R_ABS'
    context=database.datasearch(querys(user))
    for i in range(len(context)):
        dict={}
        aux = context[i]      
        dict['id']=aux[0]
        dict['c_abscence']=aux[2]
        abscence = abscence + aux[2]
        dict['justified']=aux[3]
        dict['date']=aux[4]
        response.append(dict)
    user['function']='R_U'
    return [response,abscence]