from flask import Flask, redirect, request, send_file
from flask_cors import CORS
from DataBase.querys import querys
from Users.courses import add_activity, delete_activity, add_new_course, read_activity, read_course,sp_course,add_person_roll,add_student_roll,r_person_roll,r_student_roll,d_p_roll,d_s_roll
from Users.users import del_abs,verif,set_year,Update_abscence,get_abscence
from MessagePdf.messagepdf import set_message,read_message,delete_message,set_pdf,read_arr_pdf,weekly_messages
from DataBase.database import DataBase
from Settings.settings import xml
from Menu.menu import set_menu,read_menu
import os


from asgiref.wsgi import WsgiToAsgi
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve

app = Flask('app')
cors = CORS(app)
app.secret_key = "Asusgo-proyect"
settings = xml()#Read setings on xml
database = DataBase(settings)#Create de database connection
users=[]#save the loged users

#Test route
@app.route('/api', methods=['GET'])
def index():
    return {'msj':'conected'}

#Verif route
@app.route('/api/login', methods=['POST'])
def verification():
    #try:
        context = verif(request.get_json(),database)
        user = context['element']
        vect = []
        for i in user[0]:
            vect.append(i)
        vect.append(context['type'])
        users.append(vect)
        code = users.index(vect)
        return {"id":str(code)}
    #except:
    #    return {'msj':'error'}

@app.route('/api/getuser', methods=['POST'])
def get_user():
    try:
        user = users[int(request.json['id'])]
        if users[int(request.json['id'])] != '':
            context = {}
            context['type']=user[5]
            if context['type']== True:
                context['id']=user[0]
                context['name']=user[1]
                context['email']=user[2]
                context['c_abscence']=user[3]
                context['year']=user[4]
            else:
                context['id']=user[0]
                context['name']=user[1]
                context['email']=user[2]
                context['p_type']=user[3]
                context['c_abscence']=user[4]
            users[int(request.json['id'])] = ''
            return context
        else:
            return {'msj':'invalid id'}
    except:
        return {'msj':'invalid id'}

#User route
@app.route('/api/user/set_year', methods=['POST'])
def setyear():
    try:
        context = set_year(request.get_json(),database)
        return context
    except:
        return{'msj':'error'}

#Message read
@app.route('/api/message/read', methods=['POST'])
def read_week_message():
    #try:
    rq=request.get_json()
    context = read_message(rq,database)
    return context
    #except:
    #    return {'msj':'error'}

#Message week read
@app.route('/api/message_week/read', methods=['POST'])
def readmessage():
    #try:
    rq=request.get_json()
    context = read_message(rq,database)
    response = weekly_messages(context['element'])
    return {'element':response}
    #except:
    #    return {'msj':'error'}

#Message write
@app.route('/api/message/write', methods=['POST'])
def writemessage():
    try:
        rq=request.get_json()
        context = set_message(rq ,database)
        return context
    except:
        return{'msj':'error'}

#Message delete
@app.route('/api/message/delete', methods=['POST'])
def deletemessage():
    try:
        rq=request.get_json()
        context = delete_message(rq ,database)
        return context
    except:
        return{'msj':'error'}

#PDF insert
@app.route('/api/pdf/data_insert', methods=['POST'])
def datainsertpdf():
    #try:
        rq = request.get_json()
        context=set_pdf(rq,database)
        return context
    #except:
    #    return {'msj':'error'}

@app.route('/api/pdf/insert/<id>', methods=['POST'])
def insertpdf(id):
    rq=request.files['a']
    folderdirectory = './MessagePdf/pdf_storage/'
    rq.save(os.path.join(folderdirectory,str(id)+'.pdf'))
    return {'msj':'saved'}

@app.route('/api/pdf/delete', methods=['POST'])
def deletetpdf():
    rq=request.get_json()
    rq['function']='D_PDF_S'
    database.datainsert(querys(rq))
    return {'msj':'deleted'}

#PDF arr read
@app.route('/api/pdf/arrread', methods=['POST'])
def arrreadpdf():
    #try:
        rq= request.get_json()
        context = read_arr_pdf(rq,database)
        return context
    #except:
    #    return {'msj':'error'}

#PDF one read
@app.route('/api/message/pdf/oneread', methods=['POST'])
def onereadpdf():
    #try:
    rq=request.get_json()
    return send_file(path_or_file='./MessagePdf/pdf_storage/'+rq['id']+'.pdf',download_name='form.pdf')
    '''except:
        pass'''

@app.route('/api/search/student', methods=['POST'])
def serch_st():
    rq = request.get_json()
    rq['function']='S_S'
    context = database.datasearch(querys(rq))
    response=[]
    for i in context:
        response.append({'id_s':i[0],'name':i[1],'email':i[2]})
    return {'students':response}

@app.route('/api/search/person', methods=['POST'])
def serch_oerson():
    rq = request.get_json()
    rq['function']='S_P'
    context = database.datasearch(querys(rq))
    response=[]
    for i in context:
        response.append({'id_s':i[0],'name':i[1],'email':i[2]})
    return {'persons':response}

@app.route('/api/abs', methods=['POST'])
def addabs():
    try:
        context = Update_abscence(request.get_json(),database)
        return context
    except:
        return {'msj':'error'}

@app.route('/api/get_abs', methods=['POST'])
def getabs():
    context = get_abscence(request.get_json(),database)
    return {'db':context[0],'abs':context[1]}

@app.route('/api/del_abs', methods=['POST'])
def delabs():
    del_abs(request.get_json(),database)
    return {'msj':'deleted'}

#add menu
@app.route('/api/add_menu',methods=['POST'])
def add_menu():
    set_menu(request.files['file'],database)
    return {'msj':'saved'}

#read last menu
@app.route('/api/menu',methods=['GET'])
def r_menu():
    menu =read_menu(database)
    return {'menu':menu}


#############################################


#read the courses by id
@app.route('/api/id/course',methods=['POST'])
def r_corurse():
    context =sp_course(request.get_json(),database)
    context['activities']=read_activity(request.get_json(),database)
    return context

#read the courses by year and division
@app.route('/api/division_year/course',methods=['POST'])
def dy_corurse():
    context =read_course(request.get_json(),database)
    return context

#add course
@app.route('/api/add/course',methods=['POST'])
def add_corurse():
    context =add_new_course(request.get_json(),database)
    return context
 #add course
@app.route('/api/delete/course',methods=['POST'])
def delete_corurse():
    rq= request.get_json()
    rq['function']='D_C_ID'
    context =database.datainsert(querys(rq))
    return context

##################################################

#add student roll
@app.route('/api/add/student_roll',methods=['POST'])
def add_s_roll():
    context =add_student_roll(request.get_json(),database)
    return context

#add person roll
@app.route('/api/add/person_roll',methods=['POST'])
def add_p_roll():
    context =add_person_roll(request.get_json(),database)
    return context

#read student roll
@app.route('/api/read/student_roll',methods=['POST'])
def read_student_roll():
    context =r_student_roll(request.get_json(),database)
    return context

#read person roll
@app.route('/api/read/person_roll',methods=['POST'])
def read_person_roll():
    context =r_person_roll(request.get_json(),database)
    return context

#delete student roll
@app.route('/api/delete/student_roll',methods=['POST'])
def delete_student_roll():
    rq= request.get_json()
    rq['function']='D_S_R'
    context =database.datainsert(querys(rq))
    return context

#delete person roll
@app.route('/api/delete/person_roll',methods=['POST'])
def delete_person_roll():
    rq= request.get_json()
    rq['function']='D_P_R'
    context =database.datainsert(querys(rq))
    return context

###################################################

#add activity
@app.route('/api/add/activity',methods=['POST'])
def add_p_activity():
    context =add_activity(request.get_json(),database)
    return context

@app.route('/api/add/activity/<id>', methods=['POST'])
def insert_act_pdf(id):
    rq=request.files['a']
    folderdirectory = './MessagePdf/pdf_Activities/'
    rq.save(os.path.join(folderdirectory,str(id)+'.pdf'))
    return {'msj':'saved'}

@app.route('/api/activity/pdf', methods=['POST'])
def read_pdf_activity():
    #try:
    rq=request.get_json()
    return send_file(path_or_file='./MessagePdf/pdf_Activities/'+rq['id']+'.pdf',download_name='form.pdf')

@app.route('/api/delete/activity', methods=['POST'])
def delete_act():
    context =delete_activity(request.get_json(),database)
    return context

if __name__ == "__main__":
    type_s = ''
    if type_s == 'flask':
        app.run(debug=True, port=5000)
    else:
        asgi_app = WsgiToAsgi(app)  
        conf = Config()
        conf._bind=['localhost:5000']
        asyncio.run(serve(asgi_app,conf))