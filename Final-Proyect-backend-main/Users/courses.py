from DataBase.querys import querys

def add_student_roll(request,database):
    request['function']='W_R_S'
    context=database.datainsert(querys(request))
    return context

def add_person_roll (request,database):
    request['function']='W_R_P'
    context=database.datainsert(querys(request))
    return context

def r_student_roll (request,database):
    request['function']='R_R_S'
    context=database.datasearch(querys(request))
    response = []
    courses = {}
    for i in context:
        response.append({'id':i[0],'id_course':i[1],'id_person':i[3]})
    for e in response:
        course = sp_course({'id_c':int(e['id_course'])},database)['course']
        if str(course['grade'])+str(course['division']) in courses:
            courses[str(course['grade'])+str(course['division'])].append(course)
        else:
            courses[str(course['grade'])+str(course['division'])]=[course]
    return {'rolls':response,'class':courses}

def r_person_roll (request,database):
    request['function']='R_R_P'
    context=database.datasearch(querys(request))
    response = []
    courses={}
    for i in context:
        response.append({'id':i[0],'id_course':i[1],'id_student':i[2]})
    for e in response:
        course = sp_course({'id_c':int(e['id_course'])},database)['course']
        if str(course['grade'])+str(course['division']) in courses:
            courses[str(course['grade'])+str(course['division'])].append(course)
        else:
            courses[str(course['grade'])+str(course['division'])]=[course]
    return {'rolls':response,'class':courses}

def d_p_roll (request,database):
    request['function']='D_P_R'
    context=database.datainsert(querys(request))
    return context

def d_s_roll (request,database):
    request['function']='D_S_R'
    context=database.datainsert(querys(request))
    return context

def delete_activity(request,database):
    request['function']='D_A'
    context =database.datainsert(querys(request))
    return {'status':context}

def add_activity(request,database):
    request['function']='W_A'
    database.datainsert(querys(request)[0])
    context=database.datasearch(querys(request)[1])
    return {'id':context[0][0]}

def read_activity(request,database):
    request['function']='R_A'
    activities = []
    context=database.datasearch(querys(request))
    for i in context:
        activities.append({'pdf_id':i[0],'title':i[2]})
    return activities

def sp_course(request,database):
    request['function']='R_C_ID'
    context=database.datasearch(querys(request))[0]
    return {'course':{'id':context[0],'name':context[1],'grade':context[2],'division':context[3]}}

def add_new_course(request,database):
    request['function']='W_C'
    context=database.datainsert(querys(request))
    return context

def read_course(request,database):
    request['function']='R_C'
    context=database.datasearch(querys(request))
    response = []
    rolled_id = []
    if 'id_s' in request.keys():
        rolls = r_student_roll(request,database)['rolls'] 
        for r in rolls:
            rolled_id.append(r['id_course'])
    if 'id_p' in request.keys():
        rolls = r_person_roll(request,database)['rolls'] 
        for r in rolls:
            rolled_id.append(r['id_course'])
    for i in context:
        if not i[0] in rolled_id:
            response.append({'id':i[0],'name':i[1]})
    return {'courses':response}
