from PyQt5 import uic

fin = open('Yuzuki_Yukari.ui','r',encoding='utf-8')

fout = open('Yuzuki_YukariUI.py','w',encoding='utf-8')

uic.compileUi(fin, fout)

fin.close()
fout.close()