from DataBase.querys import *
import os
from pandas import *

def set_menu(file,database):
    '''Save new menu with if of BD'''
    database.datainsert(querys({'function':'W_MENU_S'}))
    db_r = database.datasearch(querys({'function':'R_MENU_S'}))[0][0]
    file.save(os.path.join('./Menu/Menu_storage',str(db_r)+'.xlsx'))
    return {'msj':'saved menu'}

def get_menu(path,name):
    '''Read the excel file with ID'''
    xls = ExcelFile(path+'/'+str(name)+'.xlsx')
    df = xls.parse(xls.sheet_names[0])
    menu= df.to_dict()
    return menu

def read_menu(database):
    '''Look ID for the last menu file'''
    db_r = database.datasearch(querys({'function':'R_MENU_S'}))
    menu = get_menu('./Menu/Menu_storage',db_r[0][0])
    return {'menu':menu}