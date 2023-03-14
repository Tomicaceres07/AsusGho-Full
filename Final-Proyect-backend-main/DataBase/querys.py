def querys(d_query):
    #### User ####
    if d_query['function'] =='R_U':#Read User 
        return [f"select * from PERSON where MAIL like '{d_query['email']}';",
            f"select * from STUDENT where MAIL like '{d_query['email']}';"]
    elif d_query['function'] =='W_U':#Write User
        return [f"insert into PERSON(NAME, MAIL, C_ABSCENCE, TYPE) values ('{d_query['name']}','{d_query['email']}',0,'0');",
            f"insert into STUDENT(NAME, MAIL, YEAR, C_ABSCENCE) values ('{d_query['name']}','{d_query['email']}','0',0);"]
    elif d_query['function'] =='U_U':#Update User
        return [f"update STUDENT SET C_ABSCENCE = {d_query['c_abscence']}, `YEAR`='{d_query['year']}' WHERE MAIL like '{d_query['email']}';",
        f"update PERSON set C_ABSCENCE = {d_query['c_abscence']} WHERE MAIL like '{d_query['email']}';"]
    
    #### Storage ####
    elif d_query['function'] =='R_S':#Read Storage
        return f"select ID_ST,TEXT_ST,DATE_ST from STORAGE WHERE TYPE_ST = {d_query['type']};"
    elif d_query['function'] =='W_S':#Write Storage
        return f"insert into STORAGE(DATE_ST, TEXT_ST,TYPE_ST) values ('{d_query['date']}','{d_query['text']}',{d_query['type']});"
    elif d_query['function'] =='D_S':#Delete Storage
        return f"delete from STORAGE where ID_ST = '{d_query['id']}';"

    #### PDF ####
    elif d_query['function'] =='R_PDF_S':#Read all PDF 
        return f"select * from PDF_STORAGE where TYPE_PDF_ST = {d_query['type']};"
    elif d_query['function'] =='R_ONE_PDF_S':#Read one PDF
        return f"select ID_PDF_ST from PDF_STORAGE where TYPE_PDF_ST = {d_query['type']} and NAME_PDF like '{d_query['name']}';"
    elif d_query['function'] =='W_PDF_S':#Write PDF
        return f"insert into PDF_STORAGE(NAME_PDF,TYPE_PDF_ST) values ('{d_query['name']}',{d_query['type']});"
    elif d_query['function'] =='D_PDF_S':#Delete PDF
        return f"delete from PDF_STORAGE where ID_PDF_ST = '{d_query['id']}';"

    #### Abscence ####
    elif d_query['function'] =='R_ABS':#Read ABS
        return f"select * from abs_detail WHERE mail like '{d_query['email']}';"
    elif d_query['function'] =='W_ABS':#Write ABS
        return f"insert into abs_detail(mail,abs,justified,date) values ('{d_query['email']}',{d_query['abs']},{d_query['justified']},'{d_query['date']}');"
    elif d_query['function'] =='D_ABS':#Read ABS
        return f"delete from abs_detail WHERE id like '{d_query['id']}';"

    #### Menu ####
    elif d_query['function'] =='R_MENU_S':#Read Menu
        return f"select max(ID_MENU_ST) from MENU_STORAGE;"
    elif d_query['function'] =='W_MENU_S':#Write Menu
        return f"insert into MENU_STORAGE values();"

    #### Courses ####
    elif d_query['function'] =='W_C':#Write Course
        return f"insert into COURSES(NAME,GRADE,DIVISION) values ('{d_query['name']}',{d_query['grade']},'{d_query['division']}');"
    elif d_query['function'] =='R_C':#Read Course
        return f"select * from COURSES where DIVISION like '{d_query['division']}' and GRADE = {d_query['grade']};"
    elif d_query['function'] == 'R_C_ID':#Read Corurse by ID
        return f"select * from COURSES where ID = {d_query['id_c']};"
    elif d_query['function'] == 'D_C_ID':#Read Corurse by ID
        return f"delete from COURSES where ID = {d_query['id_c']};"

    #### Roll ####
    elif d_query['function'] == 'W_R_S':#Write Roll Student
        return f"insert into ROLL(ID_COURSES,ID_PERSON,ID_STUDENT) values ({d_query['id_c']},NULL,{d_query['id_s']});"
    elif d_query['function'] == 'W_R_P':#Write Roll Person
        return f"insert into ROLL(ID_COURSES,ID_PERSON,ID_STUDENT) values ({d_query['id_c']},{d_query['id_p']},NULL);"
    elif d_query['function'] == 'R_R_S':#Read Roll Student
        return f"select * from ROLL where ID_STUDENT = {d_query['id_s']};"
    elif d_query['function'] == 'R_R_P':#Read Roll Person
        return f"select * from ROLL where ID_Person = {d_query['id_p']};"
    elif d_query['function'] == 'D_P_R':#Delete person Roll
        return f"delete from ROLL where ID_Person = {d_query['id']} and ID_COURSES = {d_query['id_c']};"
    elif d_query['function'] == 'D_S_R':#Delete student Roll
        return f"delete from ROLL where ID_student = {d_query['id']} and ID_COURSES = {d_query['id_c']};"

    #### Activities ####
    elif d_query['function'] == 'W_A':#Write Activities
        return [f"insert into ACTIVITIES(ID_COURSES,TITLE) values({d_query['id_c']},'{d_query['title']}');",
        f"select max(ID) from ACTIVITIES where ID_COURSES = {d_query['id_c']} and TITLE LIKE '{d_query['title']}';"]
    elif d_query['function'] == 'R_A':#Read Activities
        return f"select * from ACTIVITIES WHERE ID_COURSES = {d_query['id_c']};"
    elif d_query['function'] == 'D_A':#Delete Activities
        return f"delete from ACTIVITIES WHERE ID = {d_query['id']}"
    
    #### Search ####
    elif d_query['function'] == 'S_S':
        return f"SELECT * FROM STUDENT WHERE NAME LIKE '%{d_query['name']}%';"
    elif d_query['function'] == 'S_P':
        return f"SELECT * FROM PERSON WHERE NAME LIKE'%{d_query['name']}%';"