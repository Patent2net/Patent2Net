# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 08:50:16 2014

@author: dreymond
"""
IPCRCodes = {'A':'HUMAN NECESSITIES', 'B':'PERFORMING OPERATIONS; TRANSPORTING', 'C':'CHEMISTRY; METALLURGY',
'D':'TEXTILES; PAPER', 'E':'FIXED CONSTRUCTIONS', 'F':'MECHANICAL ENGINEERING; LIGHTING; HEATING; WEAPONS; BLASTING',
'G':' PHYSICS', 'H':'ELECTRICITY'}
Status = [u'A', u'B', u'C', u'U', u'Y', u'Z', u'M', u'P', u'S', u'L', u'R', u'T', u'W', u'E', u'F', u'G', u'H', u'I', u'N', u'X']
#    A – First publication level
#    B – Second publication level
#    C – Third publication level
#Group 2 – Use for utility model documents having a numbering series other than the documents of Group 1:
#    U – First publication level
#    Y – Second publication level
#    Z – Third publication level
#Group 3 – Use for special series of patent documents as specified below:
#    M – Medicament patent documents (e.g., documents previously published by FR)
#    P – Plant patent documents (e.g., published by US)
#    S – Design patent documents (e.g., published by US)
#Group 4 – Use for special types of patent documents or documents derived from/relating to patent applications and not covered by Groups 1 to 3, above, as specified below:
#    L – Documents, not covered by the letter code W, relating to patent documents and containing bibliographic information and only the text of an abstract and/or claim(s) and, where appropriate, a drawing
#    R – Separately published search reports
#    T – Publication, for information or other purposes, of the translation of the whole or part of a patent document already published by another office or organization
#    W – Documents relating to utility model documents falling in Group 2 and containing bibliographic information and only the text of an abstract and/or claim(s) and, where appropriate, a drawing
#Group 5 – Use for series of patent documents not covered by Groups 1 to 4, above:
#    E – First publication level
#    F – Second publication level
#    G – Third publication level
#Group 6 – Use for series of patent documents or documents derived from/relating to patent applications and not covered by Groups 1 to 5, above, according to the special requirements of each industrial property office:
#    H
#    I
#Group 7 – Other (see paragraph 2, above):
#    N – Non-patent literature documents
#    X ]

import re
import datetime

def isMaj(car):
    if car.lower() != car:
        return True
    else:
        return False

def ReturnBoolean(string):
    if string.count('True')>0 or string.count('true')>0:
        return True # to gather contents
    else:
        return False

def CleanPatent(dico):
        
    if isinstance(dico, dict):
        res = dict()
        lstCle=dico.keys()
        for cle in lstCle:
            if isinstance(dico[cle], list):
                if len(dico[cle])==1:
                    if isinstance(dico[cle][0], list):
                        if len(dico[cle][0]) >1:
                            res[cle] = CleanPatent(dico[cle][0])
                        else:
                            res[cle] = unicode(CleanPatent(dico[cle][0][0]))
                    else:
                        res[cle] = unicode(CleanPatent(dico[cle][0]))
                elif len(dico[cle])>1:
                    tempo = []
                    for content in dico[cle]:
                        if CleanPatent(content) not in tempo:    
                            tempo.append(CleanPatent(content))  
                    res[cle] = tempo #print "hum"
                else:
                    res[cle] = u''
            elif dico[cle] =='N/A':
                res[cle] = u''
            elif isinstance(dico[cle], dict):
                res[cle] = CleanPatent(dico[cle])
            else: 
                res[cle] = CleanPatent(dico[cle])
        return res
    elif isinstance(dico, list):
        if len(dico) == 1:
            return CleanPatent(dico[0])
        else:
            res = []
            for ent in dico:
                temp =  CleanPatent(ent)
                
                if temp is not None and len(temp) >0 :
                    res.append(temp)
            return res
    elif isinstance(dico, str) or isinstance(dico, unicode):
        return dico
       
def getStatus2(noeud, listeBrevet):
    for Brev in listeBrevet:
        if Brev['label'] == noeud:
            return Brev['kind']
    return ''

def getClassif(noeud, listeBrevet):
    for Brev in listeBrevet:
        if Brev['label'] == noeud:
            return Brev['IPCR11']
    return ''

def getCitations(noeud, listeBrevet):
    for Brev in listeBrevet:
        if Brev['label'] == noeud:
            if Brev.has_key('citations'):
                return Brev['citations']
            else:
                return 0
    return 0

def getFamilyLenght(noeud, listeBrevet):
    for Brev in listeBrevet:
        if Brev['label'] == noeud:
            if Brev.has_key('family lenght'):
                return Brev['family lenght']
            else:
                return 0
    return 0
    
def getPrior(noeud, listeBrevet):
    for Brev in listeBrevet:
        if Brev['label'] == noeud:
            return Brev['prior']
    return ''

def getActiveIndicator(noeud, listeBrevet):
    for Brev in listeBrevet:
        if Brev['label'] == noeud:
            return Brev['priority-active-indicator']
    return 0

def getRepresentative(noeud, listeBrevet):
    for Brev in listeBrevet:
        if Brev['label'] == noeud:
            return Brev['representative']
    return 0

def UnNest(liste):
#    assert isinstance(liste, list)
    if liste is not None:
        if isinstance(liste, list):
            if len(liste)>1:
                temp = []
                for cont in liste:
                    if isinstance(cont, list) and cont is not None:
                        tempo = []
    
                        for contenu in cont:
                            if contenu is not None:
                                if contenu != '' and contenu != u'':
                                    Tpr = UnNest(contenu)
                                    if Tpr != u'':
                                        tempo.append(Tpr)
                        if len(tempo)>0:
                            temp.extend(tempo)
                    elif cont is not None:
                        if cont !='' and cont !=u'':
                            temp.append(cont)
                    else:
                        pass
                return temp
            elif len(liste) == 1:
                if isinstance(liste[0], list):
                    return UnNest(liste[0])
                elif len(liste[0])>0:
                    return liste[0]
                else:
                    return u''
            else:
                return u''
                    
        else:
            return liste
    else:
        return u''
        
def Decoupe(dico):
    """will return a list of dictionnary patents monovaluated as long as the product of multivalued entries"""
    Res = dict()
    remp  = dict()
    lstCle = dico.keys()
    dico = CleanPatent(dico)
    for cle in lstCle:
        if isinstance(dico[cle], list):
            temp = [CleanPatent(k) for k in dico[cle] if k != 'N/A' and k != None and k!='']
            if len(temp) ==1:
                if isinstance(temp[0], list) and len(temp[0])>1:
                    remp[cle] = UnNest(temp[0])
                else:
                    pass
            if len(temp) ==0:
                pass
            else:
                remp[cle] = temp
        else:
            pass
    i=1
    #calculating combinatory results. Each list multiplies others...
    nombre = prod([i*len(remp[cle]) for cle in remp.keys() if isinstance(remp[cle], list)  and len(remp[cle])!=0])
    #preparing result dictionnary    
    for num in range(nombre):
        Res[num] = dict()
        for cle in lstCle:   
            if cle not in remp.keys():  # unique content, not list for these keys
                Res[num][cle] = dico[cle]
    # for keys that dico[keys] are lists
    for cle2 in remp.keys():    
        cpt=0
        for content in remp[cle2]* (nombre /len(remp[cle2])):
            #for each content, write it this entry
            Res[cpt][cle2] = content
            #copy also others content for each content from different key 
            #for this entry (cpt)
            for cle3 in remp.keys():
                if cle3 != cle2:      
                    for content2 in remp[cle3]:
                        Res[cpt][cle3] = content2
            #next entry # this should stop at en end of resultset
            cpt+=1
    
#            elif len(remp[cle])>0:         
#                Res[num][cle] = remp[cle][num % len(remp[cle])]
#            else:
#                Res[num][cle] = dico[cle]
#    retour=[]
#    for k in Res.keys():
#        if Res[k] not in retour:
#            retour.append(Res[k]) 
    for bre in Res:
        for cle in lstCle:
            if isinstance(Res[bre][cle], list):
                print "pas glop"
    return Res
    
def SeparateCountryField(pat):
    if "Inventor-Country" in pat.keys():
        if len(pat["Inventor-Country"])>0:
            return pat #no changes
    if "Applicant-Country" in pat.keys():
        if len(pat["Applicant-Country"])>0:
            return pat #no changes
            
  
    PaysInv= [] #new field
    PaysApp = []
    brev = pat
    if not isinstance(pat, dict):
        print "pas gloup"
    if brev['inventor'] is not None:
        
        if isinstance(brev['inventor'], list):
            tempoInv = []
            for inv in brev['inventor']:
                tempPaysInv = inv.split('[')
                if isinstance(tempPaysInv, list):
                    for kk in range(1, len(tempPaysInv), 2):
                        PaysInv.append(tempPaysInv[kk].replace(']',''))
                    tempoInv.append(tempPaysInv[0].strip())
                else:
                    tempoInv.append(tempPaysInv.strip())
            brev["inventor"] = tempoInv
                
        else:
            tempPaysInv = brev['inventor'].split('[')
            if isinstance(tempPaysInv, list):
                for kk in range(1, len(tempPaysInv), 2):
                    PaysInv.append(tempPaysInv[kk].replace(']',''))
                brev["inventor"] = tempPaysInv[0].strip()
            else:
                tempoInv.append(tempPaysInv.strip())
    if brev['applicant'] is not None:
        
        if isinstance(brev['applicant'], list):
            tempoApp = []
            for APP in brev['applicant']:
                tempPaysApp = APP.split('[')
                if isinstance(tempPaysApp, list):
                    for kk in range(1, len(tempPaysApp), 2):
                        PaysApp.append(tempPaysApp[kk].replace(']',''))
                    tempoApp.append(tempPaysApp[0].strip())
                else:
                    tempoApp.append(tempPaysApp.strip())
            brev["applicant"] = tempoApp
        else:

            tempPaysApp = brev['applicant'].split('[')
            if isinstance(tempPaysApp, list):
                for kk in range(1, len(tempPaysApp), 2):
                    PaysApp.append(tempPaysApp[kk].replace(']',''))
                brev["applicant"] = tempPaysApp[0].strip()
            else:
                brev["applicant"] = tempPaysApp.strip()
    brev["Inventor-Country"] = list(set(PaysInv))
    brev["Applicant-Country"] = list(set(PaysApp))
    if len(brev["Inventor-Country"]) == 1:
            brev["Inventor-Country"] = brev["Inventor-Country"][0]
    if len(brev["Applicant-Country"]) == 1:
        brev["Applicant-Country"] = brev["Applicant-Country"][0]
    if isinstance(brev["Inventor-Country"], list) and len(brev["Inventor-Country"]) == 0:
        brev["Inventor-Country"] = ""
    if isinstance(brev["Applicant-Country"], list) and len(brev["Applicant-Country"]) == 0: 
        brev["Applicant-Country"] = ""
    return brev    

def CleanPatentOthers(brev):
    tempo = dict()
    import bs4
    for cle in brev.keys():
        if brev[cle] is not None and brev[cle] != 'N/A' and brev[cle] != 'UNKNOWN':
            if isinstance(brev[cle], list):
                if cle == 'classification':
                    for classif in brev['classification']:
                        tempoClass = ExtractClassificationSimple2(classif)
                        for cle2 in tempoClass.keys():
                            if cle2 == 'classification':
                                if tempo.has_key(cle2) and not isinstance(tempo[cle2], list) and tempoClass[cle2] != tempo[cle]:
                                    tempo[cle2] = [tempo[cle2]]
                                    tempo[cle2].append(tempoClass[cle2])
                                elif tempo.has_key(cle2) and isinstance(tempo[cle2], list) and tempoClass[cle2] not in tempo[cle]:
                                    tempo[cle2].append(tempoClass[cle2])
                                else:
                                    tempo[cle2] = [tempoClass[cle2]]
                            elif cle2 in tempo.keys():
                                if tempoClass[cle2] not in tempo[cle2]:
                                    #tempo[cle] = []
                                    tempo[cle2].append(tempoClass[cle2])
                                else:
                                    pass
#                                if tempoClass[cle2] not in tempo2[cle2]:   
#                                    tempo2[cle2].append(tempoClass[cle2])
#                                else:
#                                    pass
                            else:
                                tempo[cle2] = []
#                                tempo[cle2].append(tempoClass[cle2])
#                                tempo2[cle2].append(tempoClass[cle2])

                else:                
                    temp = [unicode(a) for a in brev[cle]]
                    tempo[cle] = temp
                    
            elif cle =='titre':
                temp = unicode(brev[cle]).replace('[','').replace(']', '').lower().capitalize()
                soup = bs4.BeautifulSoup(temp)
                temp = soup.text
                tempo[cle] = temp
                #tempo2 [cle] = temp
            elif cle =='date' and brev['date'] is not None:
                try:
                    tempo[cle] = str(brev['date'].year) +'-' +  str(brev['date'].month) +'-' + str(brev['date'].day)
                except:
                    tempo[cle] = brev['date'][0:4]
                #tempo2[cle] = str(brev['date'].year) # just the year in Pivottable
            elif cle =='classification' and brev['classification'] != u'':
                tempoClass = ExtractClassificationSimple2(brev['classification'])
                for cle in tempoClass.keys():
                    if cle in tempo.keys() and tempoClass[cle] not in tempo[cle]:
                        if tempoClass[cle] != 'N/A':
                            tempo[cle].append(tempoClass[cle])
                    elif tempoClass[cle] != 'N/A':
                        tempo[cle] = []
                        tempo[cle].append(tempoClass[cle])
                    else:
                        tempo[cle] = ''
            elif isinstance(brev[cle], dict):
                tempo[cle] = brev[cle]
                            
            else:
                temp = unicode(brev[cle])#.replace('[','').replace(']', '')
                soup = bs4.BeautifulSoup(temp)
                temp = soup.text
                tempo[cle] = temp

                
        else:
            tempo[cle] = ''
    
    return tempo

def CleanPatentOthers2(brev):
    tempo = dict()
    import bs4
    for cle in brev.keys():
        if brev[cle] is not None and brev[cle] != 'N/A' and brev[cle] != 'UNKNOWN':
            if isinstance(brev[cle], list):
                if cle == 'classification':
                    for classif in brev['classification']:
                        tempoClass = ExtractClassificationSimple2(classif)
                        for cle2 in tempoClass.keys():
                            if cle2 == 'classification':
                                if tempo.has_key(cle2) and not isinstance(tempo[cle2], list) and tempoClass[cle2] != tempo[cle]:
                                    tempo[cle2] = [tempo[cle2]]
                                    tempo[cle2].append(tempoClass[cle2])
                                elif tempo.has_key(cle2) and isinstance(tempo[cle2], list) and tempoClass[cle2] not in tempo[cle]:
                                    tempo[cle2].append(tempoClass[cle2])
                                else:
                                    tempo[cle2] = [tempoClass[cle2]]
                            elif cle2 in tempo.keys():
                                if tempoClass[cle2] not in tempo[cle2]:
                                    #tempo[cle] = []
                                    tempo[cle2].append(tempoClass[cle2])
                                else:
                                    pass
#                                if tempoClass[cle2] not in tempo2[cle2]:   
#                                    tempo2[cle2].append(tempoClass[cle2])
#                                else:
#                                    pass
                            else:
                                tempo[cle2] = []
#                                tempo[cle2].append(tempoClass[cle2])
#                                tempo2[cle2].append(tempoClass[cle2])

                else:                
                    temp = [unicode(a) for a in brev[cle]]
                    tempo[cle] = temp
                    
            elif cle =='titre':
                temp = unicode(brev[cle]).replace('[','').replace(']', '').lower().capitalize()
                soup = bs4.BeautifulSoup(temp)
                temp = soup.text
                tempo[cle] = temp
                #tempo2 [cle] = temp
            elif cle =='date' and brev['date'] is not None:
                try:
                    tempo[cle] = str(brev['date'].year)# this the only diff with cleanPatentOther +'-' +  str(brev['date'].month) +'-' + str(brev['date'].day)
                except:
                    tempo[cle] = brev['date'][0:4]
                #tempo2[cle] = str(brev['date'].year) # just the year in Pivottable
            elif cle =='classification' and brev['classification'] != u'':
                tempoClass = ExtractClassificationSimple2(brev['classification'])
                for cle in tempoClass.keys():
                    if cle in tempo.keys() and tempoClass[cle] not in tempo[cle]:
                        if tempoClass[cle] != 'N/A':
                            tempo[cle].append(tempoClass[cle])
                    elif tempoClass[cle] != 'N/A':
                        tempo[cle] = []
                        tempo[cle].append(tempoClass[cle])
                    else:
                        tempo[cle] = ''
            elif isinstance(brev[cle], dict):
                tempo[cle] = brev[cle]
                            
            else:
                temp = unicode(brev[cle])#.replace('[','').replace(']', '')
                soup = bs4.BeautifulSoup(temp)
                temp = soup.text
                tempo[cle] = temp
                
        else:
            tempo[cle] = ''
    
    return tempo

def prod(liste):
    Res = 1
    for k in liste:
        Res = Res * k
    return Res
    
def change(NomDeNoeud):
    if NomDeNoeud == 'classification':
        return 'IPCR'
    if NomDeNoeud == 'pays':
        return 'country'
    if NomDeNoeud == 'inventeur':
        return 'inventor'
    return NomDeNoeud

def symbole(IPC):
    if len(IPC) == 1:
        return IPC
    if len(IPC) == 3:
        return IPC
    if len(IPC) == 4:
        return IPC
    
    subclass = IPC[0:4]
    if IPC.count('/')>0:
        maingroup = IPC[4:].split('/')[0] 
        subgroup = IPC[4:].split('/')[1]
    elif len(IPC) ==14:
        maingroup = IPC[4:8]
        subgroup = IPC[8:]
    elif len(IPC) >4 and len(IPC)<14:
        maingroup = IPC[4:]
        subgroup = ''
    else:
        print "not good symbol", IPC
    
    maingroup = re.sub("^0+", "", maingroup)
    maingroup = (4-len(maingroup))*'0' + maingroup
    subgroup = subgroup + (6 - len(subgroup)) * '0'
    return subclass+maingroup+subgroup

def ContractList(liste):
    
    res = []
    for Ens in liste:
        if isinstance(Ens, list):
            for u in Ens:
                if u not in res:
                    res.append(u)
        elif isinstance(Ens, unicode):
            if Ens not in res:
                res.append(Ens)
        else:
            return liste
    return res
    
def ExtractClassificationSimple(data):
    res = []
    if data is not None:
        if isinstance(data, list) and len(data) ==1:
            data = data[0]
        elif isinstance(data, list):
            for classi in data:
                res.append(ExtractClassificationSimple(classi))
        if type(data) == type ("") or type(data) == type (u""):
            Resultat = dict()
            Resultat['classification'] = data
            data = data.replace(' ', '', data.count(' '))
            Resultat['IPCR11'] = data

            Resultat['IPCR1']=data[0]
            if len(data) > 2:
                Resultat['IPCR3']= data[0:3]
            else:
                Resultat['IPCR3'] = ''
            if len(data) > 4:            
                Resultat['IPCR4']= data[0:4]
                if not Resultat['IPCR4'][3].isalpha(): # consistency control
                    Resultat['IPCR4'] = ''
                    
            else:
                Resultat['IPCR4'] = ''
            if data.count('/') >0:
                Resultat['IPCR7']= data.split('/')[0]
            else:
                Resultat['IPCR7'] = ''
            Resultat['status'] = data[len(data)-1:]
            if Resultat['status'] not in Status or data[len(data)-2].isalpha():
                 Resultat['status']= data[len(data)-2:]
                 if Resultat['status'][0] not in Status:
                     Resultat['status'] = ''
                 else:
                     Resultat['IPCR11']= data[0:len(data)-2]
            else:
                Resultat['IPCR11']= data[0:len(data)-1]
            if Resultat['IPCR11'][len(Resultat['IPCR11'])-2:len(Resultat['IPCR11'])].count('0')>1:
                Resultat['IPCR11'] = '' # consistency check : if result endswith 0, means that is an IPCR7
            
            res = Resultat
        else:
            print "should not be here, pb in classification content"
    else:
        print "should not be here, pb in classification content"
    return res
    
def ExtractClassificationSimple2(data):
    res = []
    if data is not None and data !='':
        if isinstance(data, list) and len(data) ==1:
            data = data[0]
        elif isinstance(data, list):
            print "paté" #assert isinstance(data, list)
        if type(data) == type ("") or type(data) == type (u""):
            Resultat = dict()
            
            data = data.replace(' ', '', data.count(' '))
            if data[len(data)-2].isalpha():#checking last two caracter some contains status data... 
                Resultat['IPCR11'] = data[0:len(data)-2]
            elif data[len(data)-1].isalpha():
                Resultat['IPCR11'] = data[0:len(data)-1]
            else:
                Resultat['IPCR11'] = data

           #Resultat['classification'] = Resultat['IPCR11']
            Resultat['IPCR1']=data[0]
            if len(data) > 2:
                Resultat['IPCR3']= data[0:3]
            else:
                Resultat['IPCR3'] = ''
            if len(data) > 4:            
                Resultat['IPCR4']= data[0:4]
                if not Resultat['IPCR4'][3].isalpha(): # consistency control
                    Resultat['IPCR4'] = ''
                    
            else:
                Resultat['IPCR4'] = ''
            if data.count('/') >0:
                Resultat['IPCR7']= data.split('/')[0]
            else:
                Resultat['IPCR7'] = ''
            if Resultat['IPCR11'][len(Resultat['IPCR11'])-2:len(Resultat['IPCR11'])].count('0')>1:
                Resultat['IPCR11'] = Resultat['IPCR7']+'00' # consistency check : if result endswith 0, means that is an IPCR7
            
            res = Resultat
        else:
            print "should not be here, pb in classification content"
    else:
        resultat = dict()
        for ipc in ['IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11']:
            resultat[ipc] = ''
        res = resultat
    return res

def ExtractEquiv(data):
    if isinstance(data, list):
        return [ExtractEquiv(donne) for donne in data]
    else:
        return data[u'publication-reference'][u'document-id'][u'doc-number']
def ExtractAbstract(ch):
    tempo = ch
    TXT = dict()
    if isinstance(tempo, list):
        for abst in tempo:
            if abst.has_key('@lang'):
                lang=abst['@lang']
            if abst.has_key('p'):
                if isinstance(abst['p'], list):
                    for para in abst['p']:
                        if TXT.has_key(lang):
                            TXT[lang] += para['$'] + '\n'
                        else:
                            TXT[lang] = para['$'] + '\n'
                else:
                    TXT[lang] = abst['p']['$'] 
    else:
        if tempo.has_key('@lang'):
            lang=tempo['@lang']
        if tempo.has_key('p'):
            if isinstance(tempo['p'], list):
                for para in tempo['p']:
                    
                    if TXT.has_key(lang):
                        TXT[lang] += para['$'] + '\n'
                    else:
                        TXT[lang] = para['$'] + '\n'
            else:
                TXT[lang] = tempo['p']['$'] + '\n'
    return TXT
    
def ExtractClassification2(data):
    #Brev['classification'] = data
    res = dict()
    if data is not None:
        if isinstance(data, list):
            data2 = []
            data2 = [u for u in data if u not in data2]
            data = data2
    if data is not None:
        if isinstance(data, list):
            for classif in data:
                if isinstance(classif, list):
                    for te in classif:
                        tempo = ExtractClassificationSimple2(te)
                    for cle in tempo.keys():
                        if res.has_key(cle):
                            if tempo[cle] not in res[cle]:
                                res[cle].append(tempo[cle])
                        else:
                            res[cle] = []
                            res[cle].append(tempo[cle])

                else:
                    tempo = ExtractClassificationSimple2(classif)
                    for cle in tempo.keys():
                        if res.has_key(cle):
                            if tempo[cle] not in res[cle]:
                                res[cle].append(tempo[cle])
                        else:
                            res[cle] = []
                            res[cle].append(tempo[cle])
        elif isinstance(data, unicode) or isinstance(data, str):
            tempo = ExtractClassificationSimple2(data)
            for cle in tempo.keys():
                    if res.has_key(cle):
                        if tempo[cle] not in res[cle]:
                            res[cle].append(tempo[cle])
                    else:
                        res[cle] = []
                        res[cle].append(tempo[cle])
        else:
            print "should not be here, pb in classification content"
    else:
        resultat = dict()
        for ipc in ['IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11']:
            resultat[ipc] = []
        res = resultat
#    if isinstance(res, list):
#        
#        resu = dict()
#        if isinstance(res[0], dict):
#            for cle in res[0].keys():
#                resu[cle] = []
#            for dic in res:
#                for cle in dic.keys():
#                    resu[cle].append(dic[cle])
#            for cle in resu.keys():
#                if isinstance(resu[cle], list):
#                    temp = []
#                    temp = [u for u in resu[cle] if u not in temp]
#                    resu[cle] = temp
#        else:
#            print "should nto be here"
##            if isinstance(res[0], list) and len(res[0]) == 1:
##                res[0] = res[0][0]
##                for cle in res[0].keys():
##                    resu[cle] = []
##                for dic in res:
##                    for cle in dic.keys():
##                        resu[cle].append(dic[cle])
##                for cle in resu.keys():
##                    if isinstance(resu[cle], list):
##                        temp = [u for u in resu[cle] if u not in temp]
##                        resu[cle] = temp

    return res
   
def ExtractSubReference(content):
    if content.has_key('patcit'):
        refs = content['patcit'][u'document-id'][0][u'doc-number']['$'] # arbitrary choice of epodoc... What if not present I don't know
    return refs
    
def ExtractReference(pat):
    if "references-cited" in str(pat):
        citing  = pat[u'bibliographic-data']['references-cited'][u'citation']
        if isinstance(citing, list):
            return [ExtractSubReference(cit) for cit in citing]
        else:
            return [ExtractSubReference(citing)]
    else:
        return ["empty"]
            
def ExtractSubCPC(content):
    #content must be in list : patentBib[u'ops:world-patent-data'][u'exchange-documents'][u'exchange-document'][u'bibliographic-data'][u'patent-classifications'][u'patent-classification']
    #entering with patentBib[u'ops:world-patent-data'][u'exchange-documents'][u'exchange-document']
    if content[u'classification-scheme'].has_key(u'@scheme'):
        if content[u'classification-scheme'][u'@scheme'] ==u'CPC':
            #u'classification-value': {u'$': u'I'}, u'section': {u'$': u'F'}, u'subclass': {u'$': u'V'}, u'main-group': {u'$': u'3'}, u'class': {u'$': u'21'}, u'subgroup'
            return content[u'section']['$'] +  content[u'class']['$'] + \
            content[u'subclass']['$'] + content[u'main-group']['$'] + '/' + content[u'subgroup']['$']
        else:
            print "no CPC "
    else:
        return u'empty'
def ExtractCPC(pat):
    if u'patent-classifications' in str(pat):
        con = pat[u'bibliographic-data'][u'patent-classifications'][u'patent-classification']
        if isinstance(con, list):
            CPC = [ExtractSubCPC(co) for co in con]
        else:
            CPC = [ExtractSubCPC(con)]
        return CPC
    else:
        return u'empty'
        

def ExtractClassification(data):
    #Brev['classification'] = data
    res = dict()
    if data is not None:
        if isinstance(data, list):
            data2 = []
            data2 = [u for u in data if u not in data2]
            data = data2
    if data is not None and data!='':
        if isinstance(data, list):
            for classif in data:
                if isinstance(classif, list):
                    for te in classif:
                        tempo = ExtractClassificationSimple(te)
                    for cle in tempo.keys():
                        if res.has_key(cle):
                            if tempo[cle] not in res[cle]:
                                res[cle].append(tempo[cle])
                        else:
                            res[cle] = []
                            res[cle].append(tempo[cle])

                else:
                    tempo = ExtractClassificationSimple(classif)
                    for cle in tempo.keys():
                        if res.has_key(cle):
                            if tempo[cle] not in res[cle]:
                                res[cle].append(tempo[cle])
                        else:
                            res[cle] = []
                            res[cle].append(tempo[cle])
        elif isinstance(data, unicode) or isinstance(data, str):
            tempo = ExtractClassificationSimple(data)
            for cle in tempo.keys():
                    if res.has_key(cle):
                        if tempo[cle] not in res[cle]:
                            res[cle].append(tempo[cle])
                    else:
                        res[cle] = []
                        res[cle].append(tempo[cle])
        else:
            print "should not be here, pb in classification content"
    else:
        resultat = dict()
        for ipc in ["classification", 'IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11', 'status']:
            resultat[ipc] = []
        res = resultat
#    if isinstance(res, list):
#        
#        resu = dict()
#        if isinstance(res[0], dict):
#            for cle in res[0].keys():
#                resu[cle] = []
#            for dic in res:
#                for cle in dic.keys():
#                    resu[cle].append(dic[cle])
#            for cle in resu.keys():
#                if isinstance(resu[cle], list):
#                    temp = []
#                    temp = [u for u in resu[cle] if u not in temp]
#                    resu[cle] = temp
#        else:
#            print "should nto be here"
##            if isinstance(res[0], list) and len(res[0]) == 1:
##                res[0] = res[0][0]
##                for cle in res[0].keys():
##                    resu[cle] = []
##                for dic in res:
##                    for cle in dic.keys():
##                        resu[cle].append(dic[cle])
##                for cle in resu.keys():
##                    if isinstance(resu[cle], list):
##                        temp = [u for u in resu[cle] if u not in temp]
##                        resu[cle] = temp

    return res
    
def cmap_discretize(cmap, N):
   
    """Return a discrete colormap from the continuous colormap cmap.
    
        cmap: colormap instance, eg. cm.jet. 
        N: number of colors.
    
    Example
        x = resize(arange(100), (5,100))
        djet = cmap_discretize(cm.jet, 5)
        imshow(x, cmap=djet)
    """
    import matplotlib
    import numpy as np
    if type(cmap) == str:
        cmap = matplotlib.colors.get_cmap(cmap)
    colors_i = np.concatenate((np.linspace(0, 1., N), (0.,0.,0.,0.)))
    colors_rgba = cmap(colors_i)
    indices = np.linspace(0, 1., N+1)
    cdict = {}
    for ki,key in enumerate(('red','green','blue')):
        cdict[key] = [ (indices[i], colors_rgba[i-1,ki], colors_rgba[i,ki]) for i in xrange(N+1) ]
    # Return colormap object.

    return matplotlib.colors.LinearSegmentedColormap(cmap.name + "_%d"%N, cdict, 1024)

def FormateGephi(chaine):
    """formatte la chaine pour que ce soit un noeud correct pour Gephi et autres outils :
        notation hongroise (ou bulgare :-) : CeciEstUnePhrase."""
    #mem = chaine
    chaine = unicode(chaine)
    assert(isinstance(chaine, unicode))

    if chaine is not None:
        if type(chaine) == type([]):
            res = []
            for ch in chaine:
                temp = FormateGephi(ch)
                res.append(temp)
            return res
        else:
            chaine = chaine.title()
            chaine = chaine.replace(' ', '', chaine.count(' '))
            try:
                chaine = chaine.decode('latin1')
                chaine = chaine.encode('utf8')
                return chaine
            except:
                try:
                    chaine = chaine.decode('cp1252')
                    chaine = chaine.encode('utf8')
                    return chaine
                except:
                    #print "unicode problem in formate"
    #                print chaine
                    pass
            if chaine.count('[')>0:
                return chaine.split('[')[0]
            else:
                return chaine
    else:
        return u''
   
def Formate(chaine, pays):
    """formatte la chaine pour que ce soit un noeud correct pour Gephi et autres outils :
        notation hongroise (ou bulgare :-) : CeciEstUnePhrase.
        Vire le pays le cas échéant"""
    #mem = chaine
    if chaine is not None:
        if type(chaine) == type([]):
            res = []
            for ch in chaine:
                temp = Formate(ch, pays)
                res.append(temp)
            return res
#        elif len(pays) >0:
#            if chaine.count(' '+pays) >0 or chaine.count('[pays]') >0:
#                temp = chaine.replace(pays, '')
#                if temp.count('[]') >0:
#                    temp = temp.replace('[]', '')
#                chaine = temp.strip()
#        chaine = chaine.lower()
#        chaine = chaine.encode('utf8')
#        chaine = chaine.title()
#        chaine = chaine.replace(' ', '', chaine.count(' '))
#        chaine = chaine.replace(u'\xe2\x80\x82', '', chaine.count(u'\xe2\x80\x82'))
#        chaine = chaine.replace(u'\xe2', '', chaine.count(u'\xe2'))
#        chaine = chaine.replace(u'\x80', '', chaine.count(u'\x80'))
#        chaine = chaine.replace(u'\x82', '', chaine.count(u'\x82'))
#        chaine = chaine.replace(u'\xe9', '', chaine.count(u'\xe9'))
#        chaine = chaine.replace(u'\xd6', '', chaine.count(u'\xd6'))
#        chaine = chaine.replace(u'\xd2', '', chaine.count(u'\xd2'))
#        chaine = chaine.replace(u'\xf6', '', chaine.count(u'\xf6'))
#        chaine = chaine.replace(u'\xfc', '', chaine.count(u'\xfc'))
#        chaine = chaine.replace(u'\u2002', '', chaine.count(u'\u2002'))
#        chaine = chaine.replace(u'\xe1', '', chaine.count(u'\xe1'))
#        chaine = chaine.replace(u'\xf3', '', chaine.count(u'\xf3'))
#        chaine = chaine.replace(u'\xed', '', chaine.count(u'\xed'))
#        chaine = chaine.replace(u'\xe4', '', chaine.count(u'\xe4'))
#        chaine = chaine.replace(u'\xe7', '', chaine.count(u'\xe7'))
#        chaine = chaine.replace(u'\xfa', '', chaine.count(u'\xfa'))
#        chaine = chaine.replace(u'\xf1', '', chaine.count(u'\xf1'))
        
        try:
            chaine = chaine.decode('latin1')
            chaine = chaine.encode('utf8')
            return chaine
        except:
            try:
                chaine = chaine.decode('cp1252')
                chaine = chaine.encode('utf8')
                return chaine
            except:
#                print "unicode problem in formate"
#                print chaine
                pass
        #chaine = quote(chaine)
    #    table[chaine] = mem    
#        import urllib
#        chaine = urllib.quote(chaine.replace(u'\u2002', ''), safe='[]')
        return unicode(chaine, 'utf8', 'ignore')
    else:
        return u''

def genAppar (lstBrev, p1, p2):
    res = []
#    if p1 != p2:
    if lstBrev is not None:
            if p1 in lstBrev[0].keys() and p2 in lstBrev[0].keys():
                for Brev in lstBrev:
                    if Brev[p1] is not None and Brev[p2] is not None:
                        if Brev[p1] != 'N/A' and Brev[p2] != 'N/A':
                            if type(Brev[p1]) == type(u"") and type(Brev[p2]) == type(u""):
                                temp = [Brev[p1], Brev[p2], Brev['date']]
                                res.append(temp)
                            elif type(Brev[p1]) == type(u"") and type(Brev[p2]) == type([]):
                                for k in Brev[p2]:
                                    try:
                                        temp = [Brev[p1], k, Brev['date']]
                                        res.append(temp)
                                    except:
                                        try:
                                            temp = [Brev[p1], unicode(k, 'cp1252', "replace"), Brev['date']]
                                            res.append(temp)
                                        except:
                                            try:
                                                temp = [Brev[p1], unicode(k, 'latin1', "replace"), Brev['date']]
                                                res.append(temp)
                                            except:
                                                try:
                                                    temp = [Brev[p1], unicode(k, 'utf8', "replace"), Brev['date']]
                                                    res.append(temp)
                                                except:
                                                    print "first unicode exception in genAppar"
                            elif type(Brev[p1]) == type([]) and type(Brev[p2]) == type(u""):
                                for k in Brev[p1]:
                                    try:
                                        temp = [k, Brev[p2], Brev['date']]
                                        res.append(temp)
                                    except:
                                        try:
                                            temp = [unicode(k, 'utf8', "replace"), Brev[p2], Brev['date']]
                                            res.append(temp)
                                        except:
                                            try:
                                                temp = [unicode(k, 'latin1', "replace"), Brev[p2], Brev['date']]
                                                res.append(temp)
                                            except:
                                                try:
                                                    temp = [unicode(k, 'cp1252', "replace"), Brev[p2], Brev['date']] 
                                                    res.append(temp)
                                                except:
                                                    print "unicode exception"
                                    
                            else:
                                for k1 in Brev[p1]:
                                    cpt = Brev[p1].index(k1)
                                    for i in range(cpt, len(Brev[p2])):
                                        #if k1 != Brev[p2][i]:
                                        try:
                                            temp = [k1, Brev[p2][i], Brev['date']]
                                            res.append(temp)
                                        except:  #cases of k1 is unicode and Brev not and vice et versa not TREATEN !!!
                                            try:
                                                temp = [unicode(k1, 'utf8', "replace"), unicode(Brev[p2][i], 'utf8', "replace"), Brev['date']]
                                                res.append(temp)
                                            except:
                                                try:
                                                    temp = [unicode(k1, 'latin1', "replace"), unicode(Brev[p2][i], 'latin1', "replace"), Brev['date']]
                                                    res.append(temp)
                                                except:
                                                    try:
                                                        temp = [unicode(k1, 'cp1252', "replace"), unicode(Brev[p2][i], 'cp1252', "replace"), Brev['date']]
                                                        res.append(temp)
                                                    except:
                                                        print "another unicode exception"

                                            
#    else:
#        if lstBrev is not None:
#            if p1 in lstBrev[0].keys():
#                for Brev in lstBrev:
#                    if Brev[p1] is not None:
#                        if type(Brev[p1]) == type(u""):
#                            temp = [Brev[p1], Brev[p2], Brev['date']]
#                            res.append(temp)
#                        else:
#                            for k in Brev[p1]:
#                                for k2 in Brev[p1]:
#                                    if k != k2:
#                                        temp = [k, k2, Brev['date']]
#                                        res.append(temp)
    return res

def genAppar2 (lstBrev, p1, p2):
    res = []
#    if p1 != p2:
    if lstBrev is not None:
        if p1 in lstBrev[0].keys() and p2 in lstBrev[0].keys():
            for Brev in lstBrev:
                if isinstance (Brev['date'], list):
                    Brev['date'] = Brev['date'][0]
                if isinstance(Brev[p1], unicode) or isinstance(Brev[p1], str):
                    if isinstance(Brev[p2], unicode) or isinstance(Brev[p2], str):
                        temp= [Brev[p1], Brev[p2], Brev['date']]
                        res.append(temp)
                    elif isinstance(Brev[p2], list):
                        for prop in Brev[p2]:
                            tempo = [Brev[p1], prop, Brev['date']]
                            res.append(tempo)
                    else:
                        print "I dont know what to do"
                 
                elif isinstance(Brev[p1], list):
                    for prop1 in Brev[p1]:
                        if isinstance(Brev[p2], unicode) or isinstance(Brev[p2], str):
                            temp= [prop1, Brev[p2], Brev['date']]
                            res.append(temp)
                        elif isinstance(Brev[p2], list):
                            for prop in Brev[p2]:
                                tempo = [prop1, prop, Brev['date']]
                                res.append(tempo)
                        else:
                            print "I dont know what to do, many times"
                    
    return res

def MakePonderateAndProp(pair, Date, propo, pondere, destroy):
    
    if isinstance(pair[0], list):
        for u in pair[0]:
            propo, pondere, destroy = MakePonderateAndProp((u, pair[1], pair[2]), Date, propo, pondere, destroy)
    elif isinstance(pair[1], list):
        for u in pair[1]:
            propo, pondere, destroy = MakePonderateAndProp((pair[0], u, pair[2]), Date, propo, pondere, destroy)
    elif (Date, pair[0], pair[1]) in pondere.keys():
        pondere[(Date, pair[0], pair[1])] +=1
    elif pair[0] != pair[1]:
        pondere[(Date, pair[0], pair[1])] = 1
        propo[(pair[0], pair[1])] = (Date, pair[2])
    else:
        destroy.append((Date,pair))

    return propo, pondere, destroy
    
def GenereDateLiens(net):
    DateNoeud = dict()    
    for lien in net:
        n1, n2, dat, pipo = lien
        if isinstance(dat, list):
            datum = dat[0]
        else:
            datum = dat
        if isinstance(n1, list) and isinstance(n2, list):
            for kk in n1:
                if DateNoeud.has_key(kk) and datum not in DateNoeud[kk]:

                    DateNoeud[kk].append(dat)
                elif not DateNoeud.has_key(kk):
                    DateNoeud[kk] = [datum]
            for kk in n2:
                if DateNoeud.has_key(kk) and datum not in DateNoeud[kk]:
                    DateNoeud[kk].append(dat)
                elif not DateNoeud.has_key(kk):
                    DateNoeud[kk] = [datum]
        
        elif isinstance(n1, list) and not isinstance(n2, list):
            for kk in n1:
                if DateNoeud.has_key(kk) and datum not in DateNoeud[kk]:
                    DateNoeud[kk].append(dat)
                elif not DateNoeud.has_key(kk):
                    DateNoeud[kk] = [datum]
                if DateNoeud.has_key(n2) and datum not in DateNoeud[n2]:
                    DateNoeud[n2].append(dat)
                elif not DateNoeud.has_key(n2):
                    DateNoeud[n2] = [datum]
        elif not isinstance(n1, list) and isinstance(n2, list):
            for kk in n2:
                if DateNoeud.has_key(kk) and datum not in DateNoeud[kk]:
                    DateNoeud[kk].append(dat)
                elif not DateNoeud.has_key(kk):
                    DateNoeud[kk] = [datum]
                if DateNoeud.has_key(n1) and datum not in DateNoeud[n1]:
                    DateNoeud[n1].append(dat)
                elif not DateNoeud.has_key(n1):
                    DateNoeud[n1] = [datum]
        else:
            if DateNoeud.has_key(n1) and datum not in DateNoeud[n1]:
                DateNoeud[n1].append(dat)
            elif not DateNoeud.has_key(n1):
                DateNoeud[n1] = [datum]
            if DateNoeud.has_key(n2) and datum not in DateNoeud[n2]:
                DateNoeud[n2].append(dat)
            elif not DateNoeud.has_key(n2):
                DateNoeud[n2] = [datum]     
    return DateNoeud

def GenereReseaux3(G, ListeNode, PatentList, apparie, dynamic):
    reseau = []    
    
    today = datetime.datetime.now().date().isoformat()
    for appar in apparie.keys():
        tempo = [appar]
        reseautemp = [(u+tempo) for u in genAppar2(PatentList, apparie[appar][0], apparie[appar][1])]
        for k in reseautemp:
            if k not in reseau:
                reseau.append(k)
    Pondere = dict()
    Prop = dict()
    destroy = []
    DateLien = dict()
    ##cleaning
    tempo = []
    #should be clean now
#    for pair in reseau:
#        
#        if isinstance(pair[0], list):
#            if not isinstance(pair[1], list):
#                for ll in pair[0]:
#                    if ll != 'N/A' and ll != 'UNKNOWN':
#                        tempo.append( [ll, pair[1], pair[2]])
#            else:
#                for ll in pair[0]:
#                    if ll != 'N/A' and ll != 'UNKNOWN':
#                        for uu in pair[1]:
#                            if uu != 'N/A' and uu != 'UNKNOWN':
#                                tempo.append( [ll, uu, pair[2]])
#        elif isinstance(pair[1], list):
#            for ll in pair[1]:
#                    if ll != 'N/A' and ll != 'UNKNOWN':
#                        tempo.append( [pair[0], ll, pair[2]])
#        else:
#            tempo.append(pair)
            
    # unnesting things
    for pair in reseau:
        for ind in range(len(pair)):
            if isinstance(pair[ind], list):
                if len(pair[ind]) ==1:
                    pair[ind] = pair[ind][0]
                else:
                    #print "paté pair ", pair 
                    pass
        try:
            if isinstance(pair[2], list):
                dateUnic = pair[2][0]
                if DateLien.has_key(dateUnic):
                    DateLien[dateUnic].append((pair[0], pair[1], pair[3]))
                else:
                    DateLien[dateUnic] = [(pair[0], pair[1], pair[3])]
            else:    
                if DateLien.has_key(pair[2]):
                    DateLien[pair[2]].append((pair[0], pair[1], pair[3]))
                else:
                    DateLien[pair[2]] = [(pair[0], pair[1], pair[3])]
        except:
            print "why ?"
    lstDate = DateLien.keys()
    lstDate.sort()
    
    cmt = 0
    for Date in lstDate:
        for pair in DateLien[Date]:
            Prop, Pondere, destroy = MakePonderateAndProp(pair, Date, Prop, Pondere, destroy)
        if len(destroy) > 0:
            for uu in destroy:
                try:
                    DateLien[uu[0]].remove(uu[1])
                except:
                    cmt += 1
                    #print uu[1]
    #print "compteur des exceptions = ", cmt
    for k in Pondere.keys():
        source = k[1] 
        target = k[2]
        try:
            G.add_edge(ListeNode.index(source), ListeNode.index(target), attr_dict = {'weight' : Pondere[k]})
        except:
            pass
    for ed in G.edges():
        if (ListeNode[ed[0]], ListeNode[ed[1]]) in Prop.keys():
            date = Prop[(ListeNode[ed[0]], ListeNode[ed[1]])][0]
            G.edge[ed[0]][ed[1]] ['rel'] = Prop[(ListeNode[ed[0]], ListeNode[ed[1]])][1]
            #G.edge[ed[0]][ed[1]] ['time'] = [(1, date.isoformat(), today)] #version simple
            #number = len([u for u in Prop.keys() if u[0] == ListeNode[ed[0]] and u[1] == ListeNode[ed[1]] and Prop[(date, ListeNode[ed[0]], ListeNode[ed[1]])][0] <= date])
            liste = [u for u in Prop.keys() if u[0] == ListeNode[ed[0]] and u[1] == ListeNode[ed[1]]]
            lienExist = [u for u in liste if Prop[u][0] <= date]
           
            G.edge[ed[0]][ed[1]] ['time'] = [(len(lienExist), date, today)] #version simple          
            G.edge[ed[0]][ed[1]] ['deb'] = date #.isoformat()
            G.edge[ed[0]][ed[1]] ['fin'] = today
#            # setting time weight attribute for each node           
#            #defining existing dates before current edge date
#            datesExists =[u for u in lstDate if u<date]
#            # retreiving node apparition in edges before current date
#            lstAppear = [u for u in Prop.keys() if u[0] == ListeNode[ed[0]] or u[1] == ListeNode[ed[0]] and Prop[u][0] in datesExists]
#            
#            #counting those relative to same kind of relation
#            numAppear = len([u for u in lstAppear if Prop[u][1] == Prop[(ListeNode[ed[0]], ListeNode[ed[1]])][1]]) +1 #adding 1 for current occur
#            #should be divided by number of relation types in the network ????? 
#            # and how compute it here... 
#            #setting node time attribute 
#            if not G.node[ed[0]].has_key('time'):#source
#                G.node[ed[0]]['time'] = [(numAppear, date.isoformat(), today)]
#            else:
#                if (numAppear,  date.isoformat(), today) not in G.node[ed[0]]['time']:
#                    G.node[ed[0]]['time'].append((numAppear,  date.isoformat(), today))
#            #same process for target node
#            lstAppear = [u for u in Prop.keys() if u[0] == ListeNode[ed[1]] or u[1] == ListeNode[ed[1]] and Prop[u][0] in datesExists]
#            
#            #counting those relative to same king of relation
#            numAppear = len([u for u in lstAppear if Prop[u][1] == Prop[(ListeNode[ed[0]], ListeNode[ed[1]])][1]])+1 #adding 1 for current occur
##           #setting node time attribute 
#            if not G.node[ed[1]].has_key('time'):#source
#                G.node[ed[1]]['time'] = [(numAppear, date.isoformat(), today)]
#            else:
#                if (numAppear, date.isoformat(), today) not in G.node[ed[1]]['time']:
#                    G.node[ed[1]]['time'].append((numAppear,  date.isoformat(), today))
        else:
            print "this should not append"
        datesExists = [u for u in lstDate if datetime.date(int(u.split('-')[0]), int(u.split('-')[1]), int(u.split('-')[2])) < datetime.date.today()]
        lstAppear = [u for u in Prop.keys() if u[0] == ListeNode[ed[0]] or u[1] == ListeNode[ed[0]] and Prop[u][0] in datesExists]
        G.edge[ed[0]][ed[1]]['NormedWeight'] = float(G.edge[ed[0]][ed[1]]['weight']*100) / len(lstAppear)
    
            # updating datetime, endate is the next startdate
#            listDate = []
#            for entry in G.node[ed[0]]['time']:
#                listDate.append(entry[1])
#            if len(listDate) > 1:
#                listDate.sort()
#                tempoRes = []
#                for i in G.node[ed[0]]['time']:
#                    ind = listDate.index(i[1])
#                    if ind + 1 in range(len(listDate)):
#                        tempo = (i[0], i[1], listDate[ind + 1]) #end time is set to next one
#                    else:
#                        tempo = (i[0], i[1], today)
#                    tempoRes.append(tempo)
#                G.node[ed[0]]['time'] = tempoRes
                   
    return G, reseau, Prop

def FindFather(noeud, liste):
    for k in liste:
        if noeud.count(k)>0:
            return k
    print noeud
    return 

def GenereListeSansDate(ListeBrevet, prop):
    """renvoie la liste des données associées à la propriété pour la liste de dictionnaires"
    """
    res = []
    
    for brev in ListeBrevet:
            if type(brev[prop]) == type([]):
                for k in brev[prop]:
                    if k not in res:
                        res.append(k)
            elif brev[prop] not in res:
                res.append(brev[prop])
    #res = set([u for u in res])   
    return res

def UniClean(ch):
    
#    try: # this work in script but not compiled !!!!
#        string = ch.translate('utf8')
#        string = string.decode('utf8', 'ignore')
#        return string
#    except:
#        try:
#            string = ch.translate('latin1')
#            string = string.decode('utf8', 'ignore')
#            return string
#        except:
    if ch is not None:
        if isinstance(ch, list):
            return [UniClean(cont) for cont in ch]
        else:
            string=ch.replace(u'\xa0', '')
            string=string.replace(u'\xa1', '')
            string=string.replace(u'\xa2', '')
            string=string.replace(u'\xa3', '')
            string=string.replace(u'\xa4', '')
            string=string.replace(u'\xa5', '')
            string=string.replace(u'\xa6', '')
            string=string.replace(u'\xa7', '')
            string=string.replace(u'\xa8', '')
            string=string.replace(u'\xa9', '')
            string=string.replace(u'\xb0', '')
            string=string.replace(u'\xb1', '')
            string=string.replace(u'\xb2', '')
            string=string.replace(u'\xb3', '')
            string=string.replace(u'\xb4', '')
            string=string.replace(u'\xb5', '')
            string=string.replace(u'\xb6', '')
            string=string.replace(u'\xb7', '')
            string=string.replace(u'\xb8', '')
            string=string.replace(u'\xb9', '')
            string=string.replace(u'\xc0', '')
            string=string.replace(u'\xc1', '')
            string=string.replace(u'\xc2', '')
            string=string.replace(u'\xc3', '')
            string=string.replace(u'\xc4', '')
            string=string.replace(u'\xc5', '')
            string=string.replace(u'\xc6', '')
            string=string.replace(u'\xc7', '')
            string=string.replace(u'\xc8', '')
            string=string.replace(u'\xc9', '')
            string=string.replace(u'\xd0', '')
            string=string.replace(u'\xd1', '')
            string=string.replace(u'\xd2', '')
            string=string.replace(u'\xd3', '')
            string=string.replace(u'\xd4', '')
            string=string.replace(u'\xd5', '')
            string=string.replace(u'\xd6', '')
            string=string.replace(u'\xd7', '')
            string=string.replace(u'\xd8', '')
            string=string.replace(u'\xd9', '')
            string=string.replace(u'\xe0', '')
            string=string.replace(u'\xe1', '')
            string=string.replace(u'\xe2', '')
            string=string.replace(u'\xe3', '')
            string=string.replace(u'\xe4', '')
            string=string.replace(u'\xe5', '')
            string=string.replace(u'\xe6', '')
            string=string.replace(u'\xe7', '')
            string=string.replace(u'\xe8', '')
            string=string.replace(u'\xe9', '')
            string=string.replace(u'\xf0', '')
            string=string.replace(u'\xf1', '')
            string=string.replace(u'\xf2', '')
            string=string.replace(u'\xf3', '')
            string=string.replace(u'\xf4', '')
            string=string.replace(u'\xf5', '')
            string=string.replace(u'\xf6', '')
            string=string.replace(u'\xf7', '')
            string=string.replace(u'\xf8', '')
            string=string.replace(u'\xf9', '')
            string=string.replace(u'\xaa', '')
            string=string.replace(u'\xab', '')
            string=string.replace(u'\xac', '')
            string=string.replace(u'\xad', '')
            string=string.replace(u'\xae', '')
            string=string.replace(u'\xaf', '')
            string=string.replace(u'\xba', '')
            string=string.replace(u'\xbb', '')
            string=string.replace(u'\xbc', '')
            string=string.replace(u'\xbd', '')
            string=string.replace(u'\xbe', '')
            string=string.replace(u'\xbf', '')
            string=string.replace(u'\xca', '')
            string=string.replace(u'\xcb', '')
            string=string.replace(u'\xcc', '')
            string=string.replace(u'\xcd', '')
            string=string.replace(u'\xce', '')
            string=string.replace(u'\xcf', '')
            string=string.replace(u'\xda', '')
            string=string.replace(u'\xdb', '')
            string=string.replace(u'\xdc', '')
            string=string.replace(u'\xdd', '')
            string=string.replace(u'\xde', '')
            string=string.replace(u'\xdf', '')
            string=string.replace(u'\xea', '')
            string=string.replace(u'\xeb', '')
            string=string.replace(u'\xec', '')
            string=string.replace(u'\xed', '')
            string=string.replace(u'\xee', '')
            string=string.replace(u'\xef', '')
            string=string.replace(u'\xfa', '')
            string=string.replace(u'\xfb', '')
            string=string.replace(u'\xfc', '')
            string=string.replace(u'\xfd', '')
            string=string.replace(u'\xfe', '')
            string=string.replace(u'\xff', '')
        return string
    else:
        return u'empty'
        
def quote(string):
    import urllib
    
    string=UniClean(string)
    return urllib.quote(string, safe='/\\())')

def Initialize(bool1, bool2):
    if bool1 and bool2:
        return 0
    else:
        return "All"
        
def coupeEnMots(texte):
    "returns a list of words cleaned from punctuation, digits and other signs"
    if isinstance(texte, list):
        texte = ' '.join(texte)
    texte= texte.lower()
    res = re.sub('["\'<>]', ' ', texte) # on vire une partie de la ponctuation
    res = re.sub('\d', ' ', res) # extraction des chiffres
    res = re.findall('\w+', res, re.UNICODE) # extraction des lettres seulement
    return res

def decoupParagraphEnPhrases(paragraph):
    """returns the paragraph splited in phrases ignoring specifics titles. To be completed"""
    import re
    finsDePhrase = re.compile(r"""
        # Split sentences on whitespace between them.
        (?:               # Group for two positive lookbehinds.
          (?<=[.!?])      # Either an end of sentence punct,
        | (?<=[.!?]['"])  # or end of sentence punct and quote.
        )                 # End group of two positive lookbehinds.
        (?<!  Mr\.   )    # Don't end sentence on "Mr."
        (?<!  M\.   )    # Don't end sentence on "M."
        (?<!  Mme\.   )    # Don't end sentence on "Mme."
        (?<!  Mrs\.  )    # Don't end sentence on "Mrs."
        (?<!  Jr\.   )    # Don't end sentence on "Jr."
        (?<!  Dr\.   )    # Don't end sentence on "Dr."
        (?<!  Prof\. )    # Don't end sentence on "Prof."
        (?<!  Sr\.   )    # Don't end sentence on "Sr."
        \s+               # Split on whitespace between sentences.
        """, 
        re.IGNORECASE | re.VERBOSE)
    listeDePhrases  = finsDePhrase.split(paragraph)
    return [ph for ph in listeDePhrases if ph] #non vides

def Update(dicoUpdated, dico):
    for cle in dicoUpdated.keys():
        if cle in dico.keys():
            if isinstance(dicoUpdated, list):
                if isinstance(dico, list):
                    for cont in dico[cle]:
                        if cont not in dicoUpdated[cle]:
                            dicoUpdated[cle].append(cont)
                elif dico[cle] not in dicoUpdated[cle]:
                    dicoUpdated[cle].append(dico[cle])
                else:
                    pass
            else:
                dicoUpdated[cle] = [dicoUpdated[cle]]
                if isinstance(dico, list):
                    for cont in dico[cle]:
                        if cont not in dicoUpdated[cle]:
                            dicoUpdated[cle].append(cont)
                elif dico[cle] not in dicoUpdated[cle]:
                    dicoUpdated[cle].append(dico[cle])
                else:
                    pass
        else:
            pass
    return dicoUpdated

def ExtractPatent(pat, ResultContents, BiblioPatents):
    DejaLa = [bre['label'] for bre in BiblioPatents]
#    for cle in ['inventor', 'applicant', 'date', 'dateDate', 'title']:
#        if cle != 'date' and cle !='dateDate':
#            if pat[cle] == None:
#                pat[cle] = 'empty'
#        else:
#            if cle == 'date' and pat[cle] == None:
#                import datetime
#                pat[cle] = str(datetime.date.today().year) + '-' + str(datetime.date.today().month) + '-' + str(datetime.date.today().day)
#            elif cle == 'dateDate' and pat[cle] == None:
#                import datetime
#                pat[cle] = datetime.date.today().year
#
#    
#    cles = [key for key in pat.keys() if pat[key]==None]
#    for cle in cles:
#        if cle=='date':
#            pat[cle] = unicode(datetime.date.today().year)
#        elif cle=="dateDate":
#            pat[cle] = datetime.date.today()
#        else:
#            bre[cle] = u'empty'

    if None not in pat.values():        
#if Brev['label'] == Brev["prior"]: # just using primary patents not all the family
        if isinstance(pat['classification'], list):
            for classif in pat['classification']:
                tempo2 = ExtractClassificationSimple2(classif)
                for cle in tempo2.keys():
                    if cle in pat.keys() and tempo2[cle] not in pat[cle]:
                        if pat[cle] == '':
                            pat[cle] = []
                        if isinstance(tempo2[cle], list):
                            pat[cle].extend(tempo2[cle])
                        else:
                            pat[cle].append(tempo2[cle])
                    else:
                        pat[cle] = []
                        if isinstance(tempo2[cle], list):
                            pat[cle].extend(tempo2[cle])
                        else:
                            pat[cle].append(tempo2[cle])
                    if pat[cle].count(',')>0:
                        print pat[cle] #hum, strage state
        else:
            tempo2 = ExtractClassificationSimple2(pat['classification'])
            for cle in tempo2.keys():
                if cle in pat.keys() and tempo2[cle] not in pat[cle]:
                    if pat[cle] == '':
                        pat[cle] = []
                    if isinstance(tempo2[cle], list):
                        pat[cle].extend(tempo2[cle])
                    else:
                        pat[cle].append(tempo2[cle])
                else:
                    pat[cle] = []
                    if isinstance(tempo2[cle], list):
                        pat[cle].extend(tempo2[cle])
                    else:
                        pat[cle].append(tempo2[cle])
                if pat[cle].count(',')>0:
                    print pat[cle] #hum, strage state

            
                    #                print classif
        pat = SeparateCountryField(pat)
        for clekey in pat.keys():
            if isinstance(pat[clekey], list):
                pat[clekey] = UnNest(pat[clekey])

        if pat['label'] in DejaLa: #checking multiples status
                tempor = [patent for patent in BiblioPatents if patent['label'] == pat["label"]][0] #should be unique
                BiblioPatents.remove(tempor)
                tempor = Update(tempor, pat)
                for key in tempor.keys():
                    if isinstance(tempor[key], list):
                        tempor[key] = UnNest(tempor[key])
                tempor = CleanPatent(tempor)
                BiblioPatents.append(CleanPatent(tempor))
                
        else:
            for key in pat.keys():
                if isinstance(pat[key], list):
                    pat[key] =  UnNest(pat[key])
            #pat = CleanPatent(pat)
            BiblioPatents.append(pat)
            DejaLa.append(pat['label'])
        return pat, DejaLa, BiblioPatents
    else:#None values avoiding this patent
        print "None value for patent", pat['label']
        print "consider revising"
        if pat.has_key('label'):
            DejaLa.append(pat['label'])
        return None, DejaLa, BiblioPatents

def MakeIram(patent, FileName, patentBibData, AbstractPath):
        if isinstance(patent['IPCR1'], list):
            CIB1 = '-'.join(dat for dat in patent['IPCR1'])
        else:
            CIB1 =  patent['IPCR1']
            
        if isinstance(patent['IPCR3'], list):
            CIB3 = '-'.join(dat for dat in patent['IPCR3'])
        else:
            CIB3 =  patent['IPCR3']
        if isinstance(patent['IPCR4'], list):
            CIB4 = '-'.join(dat for dat in patent['IPCR4'])
        else:
            CIB4 =  patent['IPCR4']
        IRAM = '**** *Label_' + FileName +' *Country_'+patent['country']+ ' *CIB3_'+CIB3 + ' *CIB1_'+CIB1 + ' *CIB4_'+CIB4 + ' *Date_' + str(patent['dateDate'].year) + ' *Applicant_'+UniClean('-'.join(coupeEnMots(patent['applicant'])))[0:12]
        IRAM = IRAM.replace('_ ', '_empty', IRAM.count('_ ')) +'\n'
        TXT=dict()
        if isinstance(patentBibData[u'ops:world-patent-data'][u'exchange-documents'][u'exchange-document'], list):
            for tempo in patentBibData[u'ops:world-patent-data'][u'exchange-documents'][u'exchange-document']:
                if tempo.has_key('abstract'):
                    txtTemp = ExtractAbstract(tempo['abstract'])
                    for cleLang in txtTemp:
                        if TXT.has_key(cleLang):
                            TXT[cleLang] += txtTemp[cleLang]
                        else:
                            TXT[cleLang] = txtTemp[cleLang]
            
        else:
            if patentBibData[u'ops:world-patent-data'][u'exchange-documents'][u'exchange-document'].has_key('abstract'):
                TXT = ExtractAbstract(patentBibData[u'ops:world-patent-data'][u'exchange-documents'][u'exchange-document'][u'abstract'])
                for lang in TXT.keys():                            
                    EcritContenu(IRAM + TXT[lang], AbstractPath+'//'+lang+'-'+FileName+'.txt')
        return


def GetFamilly(client, brev, rep):
    #from OPS2NetUtils2 import ExtractClassificationSimple2, SeparateCountryField, ExtractAbstract, UniClean
    from epo_ops.models import Epodoc, Docdb
    import datetime
    ResultContents = rep
    lstres = []
    comptExcept = 0
    
#    try:
#        url ='http://ops.epo.org/3.1/rest-services/family/publication/docdb/' +brev['label'] +'/biblio'
#        
#        data = requests.get(url, headers = headers)
    dico = None
    try:
        data = client.family('publication', Epodoc(brev['label']), 'biblio')
        data = data.json()
        dico = data[u'ops:world-patent-data'][u'ops:patent-family'][u'ops:family-member']
        #PatentDataFam[brev['label']] = dict()
        if type(dico) == type(dict()):
            dico=[dico]
        cpt = 1
    except:
        try:
            data = client.family('publication', Docdb(brev['label'][2:], brev['label'][0:2],brev['kind']))
            data = data.json()
            dico = data[u'ops:world-patent-data'][u'ops:patent-family'][u'ops:family-member']
            #PatentDataFam[brev['label']] = dict()
            if type(dico) == type(dict()):
                dico=[dico]
            cpt = 1
        except:
            #IF WE ARE HERE? i SUPPOSE THAT EQUIVALENTS PATENTS SHOULD BE CHECKED
            print "nothing found for ", brev
            print "ignoring"
            return None

    if dico is not None:

        for donnee in dico:
            Go =True
            Brevet=dict(dict(dict(dict())))
            Brevet[u'ops:world-patent-data'] =dict()
            Brevet[u'ops:world-patent-data']['ops:biblio-search'] =dict()
            Brevet[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'] =dict()
            Brevet[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'] = donnee #hum no sure that it is a good way
            PatentData = dict()
            Req = Brevet
               
            try:
                PatentData[u'label'] = donnee[u'exchange-document'][u'bibliographic-data'][u'publication-reference'][u'document-id'][1][u'doc-number'][u'$']
            except:
                try:
                    PatentData[u'label'] = donnee[u'publication-reference'][u'document-id'][1][u'doc-number']['$']
                except:
                    print "no label ?"
                    Go = False
                   # print pprint.pprint(donnee)

            if Go:
                #PatentDataFam[PatentData['label']] = dict()
                PatentData[u'titre'] = UniClean(ExtraitTitleEn(Req))                  
#                    print "Patent title(s)", PatentData['titre']
              
                PatentData[u'inventeur'] = UniClean(ExtraitParties(Req, 'inventor', 'epodoc'))
#                    print "Inventors : ",  PatentData['inventor']
                PatentData[u'applicant'] = UniClean(ExtraitParties(Req, 'applicant','epodoc'))
#                    print "Applicants : ", PatentData['applicant']
                PatentData[u'pays'] = ExtraitCountry(Req)
                
                PatentData[u'portee'] = ExtraitKind(Req)
                try:
                    PatentData[u'classification'] = ExtraitIPCR2(Req)
                except:
                    PatentData[u'classification'] = ''
                if isinstance(PatentData[u'classification'], list):
                        for classif in PatentData[u'classification']:
                            PatentData2 = ExtractClassificationSimple2(classif)
                            for cle in PatentData2.keys():
                                if cle in PatentData.keys() and PatentData2[cle] not in PatentData[cle]:
                                    if PatentData[cle] == '':
                                        PatentData[cle] = []
                                    if isinstance(PatentData2[cle], list):
                                        for cont in PatentData2[cle]:
                                            if cont not in PatentData[cle]:
                                                PatentData[cle].append(cont)
                                    else:
                                        if PatentData2[cle] not in PatentData[cle]:
                                            PatentData[cle].append(PatentData2[cle])
                                else:
                                    PatentData[cle] = []
                                    if isinstance(PatentData2[cle], list):
                                        for cont in PatentData2[cle]:
                                            if cont not in PatentData[cle]:
                                                PatentData[cle].append(cont)
                                    else:
                                        PatentData[cle].append(PatentData2[cle])
                elif PatentData[u'classification'] != '':
                        PatentData2 = ExtractClassificationSimple2(PatentData[u'classification'])
                        for cle in PatentData2.keys():
                            if cle in PatentData.keys() and PatentData2[cle] not in PatentData[cle]:
                                if PatentData[cle] == '':
                                    PatentData[cle] = []
                                if isinstance(PatentData2[cle], list):
                                    for cont in PatentData2[cle]:
                                        if cont not in PatentData[cle]:
                                            PatentData[cle].append(cont)
                                else:
                                    PatentData[cle] = []
                                    PatentData[cle].append(PatentData2[cle])
                            elif cle not in PatentData.keys(): 
                                PatentData[cle] = []
                                if isinstance(PatentData2[cle], list):
                                    for cont in PatentData2[cle]:
                                        if cont not in PatentData[cle]:
                                            PatentData[cle].append(cont)
                                else:
                                    if PatentData2[cle] not in PatentData[cle]:
                                        PatentData[cle].append(PatentData2[cle])
                                #                print classif
                del(PatentData[u'classification'])
                #PatentData[u'applicant'] = Formate(PatentData['applicant'], PatentData['country'])
                
                # remember inventor original writing form to reuse in the url property of the node
                #PatentData[u'inventeur'] = Formate(PatentData['inventor'], PatentData['country'])
                PatentData = SeparateCountryField(PatentData)

#            #print "Classification Reduced: ", PatentData['ClassifReduite']
                date = ExtractionDate(Req) #priority claim first date time
                if date is not None and date != "":
                    PatentData[u'date'] = date[0:4] +'-'+ date[4:6] +'-'+ date[6:]
                    PatentData[u'dateDate'] = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:]))
 #                       print "patent date", PatentData['date']
                else:
                    PatentData[u'dateDate'] = datetime.date.today()
                    PatentData[u'date'] = str(datetime.date.today().year) +'-' + str(datetime.date.today().month) + '-' + str(datetime.date.today().day)
                #try: #hum straight forward may be not the good choice
                try:    
                    if u'references-cited' in donnee[u'exchange-document'][u'bibliographic-data'].keys():
                        if "citation"  in donnee[u'exchange-document'][u'bibliographic-data'][u'references-cited'].keys():
                            PatentData[u'citations'] = len(donnee[u'exchange-document'][u'bibliographic-data'][u'references-cited'][u'citation'])
                    else:
                        PatentData[u'citations'] = 0
                except:
                    PatentData[u'citations'] = 0 
                    #it is may be an Application patent. Hence, no CIB, no citation... so I should avoid it
#                        print " *********************************   "
                
                #if cpt == 1:#not the first one !!!!
                try:
                    if donnee[u'priority-claim'][u'priority-active-indicator']['$'] == u'YES':
                        PatentData['priority-active-indicator'] = 1
                except:
                    PatentData['priority-active-indicator'] = 0
                     ## should check what is "active indicator" for patent
                try:
                    if donnee[u'application-reference'][u'@is-representative'] == u'YES':
                        PatentData['representative'] = 1                            
#                            PatentData['representative'] = True
                except:
                    PatentData[u'representative'] = 0
                        # should check what is reprensentativeness for patent
        
                PatentData[u'family lenght'] = len(dico)
                

                for cle in PatentData.keys():
                    if isinstance(PatentData[cle], list):
                        if len(PatentData[cle]) == 1:
                            PatentData[cle] == PatentData[cle][0] #UnNesting
                if None not in PatentData.values():
                    IRAM = '**** *Label_' + PatentData[u'label'] +' *Country_'+PatentData[u'pays']+ ' *CIB3_'+'-'.join(PatentData[u'IPCR3']) + ' *CIB1_'+'-'.join(PatentData[u'IPCR1']) + ' *CIB4_'+'-'.join(PatentData[u'IPCR4']) + ' *Date_' + str(PatentData[u'dateDate'].year) + ' *Applicant_'+'-'.join(coupeEnMots(str(PatentData[u'applicant'])))
                    TXT=dict()
                    if isinstance(donnee[u'exchange-document'], list):
                        for tempo in donnee[u'exchange-document']:
                            if tempo.has_key('abstract'):
                                txtTemp = ExtractAbstract(tempo['abstract'])
                                for cleLang in txtTemp:
                                    if TXT.has_key(cleLang):
                                        TXT[cleLang] += txtTemp[cleLang]
                                    else:
                                        TXT[cleLang] = txtTemp[cleLang]
                    else:
                      if donnee[u'exchange-document'].has_key('abstract'):
                          TXT = ExtractAbstract(donnee[u'exchange-document'][u'abstract'])
                    for lang in TXT.keys():                            
                        EcritContenu(IRAM + ' *Contenu_Abstract \n' + TXT[lang], ResultContents+'//FamiliesAbstracts//'+lang+'-'+PatentData['label']+'.txt')   

                    lstres.append(PatentData)
                    cpt += 1
                else:                        
#                    print "hum... missing values... avoiding this patent"
                    #print "Cleaning data"
                    for key in PatentData.keys():
                        if isinstance(PatentData[key], list):
                            if len(PatentData[key])==1:
                                PatentData[key] = PatentData[key][0]
                        elif isinstance(PatentData[key], unicode):
                            pass
                        elif isinstance(PatentData[key], unicode):
                            PatentData[key] = unicode(PatentData[key])
                        else:
                            PatentData[key] = u''

        datemin = datetime.date(3000, 1, 1)
        
        for brevet in lstres:
            if brevet.has_key('representative'):
                if brevet['dateDate'] < datemin:
                    datemin = brevet['dateDate']
                    prior = brevet['label']
        if 'prior' not in locals():
            prior = brev['label']
        for brevet in lstres:
            brevet['prior'] = prior
#        print "exceptions ", comptExcept
#        print len(lstres), ' patents added'
    return lstres

def RecupAbstract(dico):
    res = dict()
    if u'@lang' in dico.keys():
        if dico[u'@lang'].count(u'fr')>0:
            res[u'resume'] = dico[u'p']
        else:
            res[u'abstract'] = dico[u'p']
        return res    
    else:
        res['abs'] = dico[u'p']
        return res
    #elif u'abstract' in str(dico):
     #   print "where is the key? \n", dico

def EcritContenu(contenu, fic):
    with open(fic, 'w') as ficW:
        ficW.write(contenu.encode('utf8'))
        return 'OK'
        
def MakeText(Thing):
    res = u''
    if isinstance(Thing, list):
        for thing in Thing:
            res += MakeText(thing)
    elif isinstance(Thing, dict):
        if '$' in Thing.keys():
            if isinstance(Thing['$'], str) or isinstance(Thing['$'], unicode):
                return Thing['$'] +'\n'
            elif isinstance(Thing['$'], list):
                for thing in Thing['$']:
                    res += MakeText(thing) +'\n'
            else:
                print "I don't know what to do"
                    
        if 'p' in Thing.keys():
            if isinstance(Thing['p'], str) or isinstance(Thing['p'], unicode):
                return Thing['p']
            elif isinstance(Thing['p'], list):
                for thing in Thing['p']:
                    res += MakeText(thing)
            else:
                print "I don't know what to do"
                    
        elif 'claims' in str(thing):
            try:
                res = MakeText(Thing[u'claims']['claim'][u'claim-text'])
            except:
                print Thing.keys()
        else:
            print "what else ?"
    else:
        print "I don't know what to do"
    return res
        #not fun

def PatentSearch(client, requete, deb = 1, fin = 1):
    requete = requete.replace('/', '\\')
    data = client.published_data_search(requete, deb, fin)
    Brevets = []
    if data.ok:
        data = data.json()
        nbTrouv = int(data[u'ops:world-patent-data'][ u'ops:biblio-search'][u'@total-result-count'])
        patents = data[u'ops:world-patent-data'][ u'ops:biblio-search'][u'ops:search-result'][u'ops:publication-reference']
        if isinstance(patents, list):
            for k in patents:
                if k not in Brevets:
                    Brevets.append(k)

        else: #sometimes its a sole patent
            if patents not in Brevets:
                Brevets.append(patents)
    else:
        print "request not correct, cql language only"
        return None
    return Brevets, nbTrouv
  
def NiceName(content):
    assert isinstance(content, list)
    ContentNice =[FormateGephi(toto).strip() for toto in content]
#    if isinstance(content, list):
#        
#    elif isinstance(content, unicode): # we should never enter here
#        print "content is not a list"
#        ContentNice = FormateGephi(content)
#                #applicant[Brev['applicant']] = FormateGephi(memo)
#    else:
#        ContentNice = u''
    return ContentNice
    
def ProcessBiblio(pat):
    PatentData = dict()
    if "country" in pat.keys():
        PatentData['label'] = pat["country"]['$']+pat[u'doc-number']['$']
    else:
        PatentData['label'] = pat['@country']+pat['@doc-number']
    try:
        PatentData[u'inventor'] = Clean(ExtraitParties(pat, 'inventor', 'epodoc'))
        PatentData[u'inventor-nice'] = NiceName(PatentData[u'inventor'])
        PatentData[u'inventor-url'] = ['http://worldwide.espacenet.com/searchResults?compact=false&ST=advanced&IN='+ quote('"'+ tempoNom.split('[')[0].strip()+'"')+'&locale=en_EP&DB=EPODOC' for tempoNom in PatentData[u'inventor']]
        
    except:
        PatentData[u'inventor'] = [u'empty']
        PatentData[u'inventor-nice'] = [u'empty']
        PatentData[u'inventor-url'] = [u'empty']
    try:
        PatentData[u'applicant'] = Clean(ExtraitParties(pat, 'applicant','epodoc'))
        PatentData[u'applicant-nice'] = NiceName(PatentData[u'applicant'])
        PatentData[u'applicant-url'] = ['http://worldwide.espacenet.com/searchResults?compact=false&ST=advanced&IN='+ quote('"'+ tempoNom.split('[')[0].strip() +'"')+'&locale=en_EP&DB=EPODOC' for tempoNom in PatentData[u'applicant']]

    except:
        PatentData[u'applicant'] = [u'empty']
        PatentData[u'applicant-nice'] = [u'empty']
        PatentData[u'applicant-url'] = [u'empty']
    try:
        PatentData[u'title'] = Clean(ExtraitTitleEn(pat))
    except:
        PatentData[u'title'] = u'empty'
    try:
        PatentData[u'country'] = ExtraitCountry(pat)
    except:
        PatentData[u'country']  = [u'empty']
    try:    
        PatentData[u'kind'] = ExtraitKind(pat)
    except:
        PatentData[u'kind'] = [u'empty']
    date = ExtractionDate(pat)
    
    try:
        PatentData[u'classification'] = UnNest2List(ExtraitIPCR2(pat))
    except:
        PatentData[u'classification'] =''
        
    try:
         PatentData[u'CPC'] = ExtractCPC(pat)
    except:
         PatentData[u'CPC'] = [u'empty']
    PatentData[u'citingDocs'] = ExtractReference(pat)
    
    if str(pat).count(u'abstract')>0:
        if u'abstract' in pat.keys():
            if isinstance(pat[u'abstract'], dict):
                tempor = RecupAbstract(pat[u'abstract'])
                for cle in tempor:
                    PatentData[cle] = tempor[cle] 
            else:
                for resum in pat[u'abstract']:
                    tempor = RecupAbstract(resum)
                    for cle in tempor:
                        PatentData[cle] = tempor[cle] 
        #should intent to recursively find abstract...
    else:
        PatentData[u'abstract'] = ''
    try:
        PatentData[u'citations'] = len(pat[u'bibliographic-data'][u'references-cited']['citation'])
    except:
        PatentData[u'citations'] = 0
    try:
        if pat[u'priority-claim'][u'priority-active-indicator']['$'] == u'YES':
            PatentData[u'priority-active-indicator'] = 1
    except:
        PatentData[u'priority-active-indicator'] = 0
        pass ## should check what is "active indicator" for patent
    try:
        if pat[u'bibliographic-data'][u'application-reference'][u'@is-representative'] == u'YES':
            PatentData[u'representative'] = 1                            
#                            PatentData['representative'] = True
        
    except:
        try:
            PatentData[u'application-ref'] = len(pat[u'bibliographic-data'][u'application-reference'][u'document-id'])/3.0 #epodoc, docdb, original... if one is missing, biais
        except:
            PatentData[u'application-ref'] = 0 # no application
        PatentData[u'representative'] = 0
    try:
        PatentData[u'publication-ref'] = pat[u'bibliographic-data'][u'publication-reference']
    except:
        PatentData[u'publication-ref'] = 0
    
    #doing some cleaning
        #transforming dates string in dates
    if date is not None and date != '':
        PatentData[u'dateDate'] = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:]))
        PatentData[u'date'] = str(date[0:4])+'-'+str(date[4:6])+'-'+str(date[6:])
        PatentData[u'year'] = str(date[0:4])
#        print "patent date", PatentData['date']
    elif date != '':
        tempodate= datetime.date(datetime.date.today().year+2, 1, 1) #adding two year arbitrary
        PatentData[u'dateDate'] = tempodate
        PatentData[u'date'] = str(tempodate.year)+'-'+str(tempodate.month)+'-'+str(tempodate.day)
    else:
        print "no date"

        #cleaning classsications
    #unesting everything
#    for cle in PatentData.keys():
#        if isinstance(PatentData[cle], list):
#            PatentData[cle] = UnNest2List(PatentData[cle])
        
    return PatentData    

def SearchEquiv(data):
    try:
        patentEquiv = data.json()
        dataEquiv = patentEquiv[u'ops:world-patent-data'][u'ops:equivalents-inquiry'][ u'ops:inquiry-result']
    except:
        dataEquiv = ''
    if dataEquiv != "":
        temporar = ExtractEquiv(data)
        if isinstance(temporar, list):
            return temporar
        else:
            return [temporar]
    else:
        return []

    
def Clean(truc):
    if type(truc) == type(u''):
        temp = truc.translate('utf8')
#        temp = truc.replace(u'\x80', '')
#        temp = temp.replace(u'\x82', '')
#        temp = temp.replace(u'\u2002', '')
#        temp = temp.replace(u"\xe2", "")
#        string=temp.replace(u'\x80', '')
#        string=string.replace(u'\x82', '')
#        string=string.replace(u'\xf6', '')
#        string = string.replace(u'\xe2', '', string.count(u'\xe2'))
#        string = string.replace(u'\x80', '', string.count(u'\x80'))
#        string = string.replace(u'\x82', '', string.count(u'\x82'))
#        string = string.replace(u'\xe9', '', string.count(u'\xe9'))
#        string = string.replace(u'\xd6', '', string.count(u'\xd6'))
#        string = string.replace(u'\xd2', '', string.count(u'\xd2'))
#        string = string.replace(u'\xf6', '', string.count(u'\xf6'))
#        string = string.replace(u'\xe4', '', string.count(u'\xe4'))
#        string = string.replace(u'\xe7', '', string.count(u'\xe7'))
#        string = string.replace(u'\xfa', '', string.count(u'\xfa'))
#        string = string.replace(u'\xe1', '', string.count(u'\xe1'))
#        string = string.replace(u'\xf3', '', string.count(u'\xf3'))
#        string = string.replace(u'\xed', '', string.count(u'\xed'))
#        string = string.replace(u'\xe7', '', string.count(u'\xe7'))  
#        string = string.replace(u'\xf1', '', string.count(u'\xf1')) 
#        string = string.replace(u'\xf2', '', string.count(u'\xf2'))    
#        string = string.replace(u'\xf3', '', string.count(u'\xf3')) 
#        string = string.replace(u'\xf4', '', string.count(u'\xf4'))    
#        string = string.replace(u'\xf5', '', string.count(u'\xf5')) 
#        string = string.replace(u'\xf6', '', string.count(u'\xf6'))    
#        string = string.replace(u'\xf7', '', string.count(u'\xf7')) 
#        string = string.replace(u'\xf8', '', string.count(u'\xf8'))
#        string = string.replace(u'\xf9', '', string.count(u'\xf9')) 
#        string = string.replace(u'\xfa', '', string.count(u'\xfa'))
#        string = string.replace(u'\xfb', '', string.count(u'\xfb')) 
#        string = string.replace(u'\xfc', '', string.count(u'\xfc'))
#        string = string.replace(u'\xfd', '', string.count(u'\xfd')) 
#        string = string.replace(u'\xfe', '', string.count(u'\xfe'))     
#        string = string.replace(u'\xeb', '', string.count(u'\xeb'))
#        string = string.replace(u'\xef', '', string.count(u'\xef'))
#        string = string.replace(u'\xc9', '', string.count(u'\xc9'))
#        string = string.replace(u'\xc4', '', string.count(u'\xc4'))
#        string = string.replace(u'\xc3', '', string.count(u'\xc3'))
#        string = string.replace(u'\xc2', '', string.count(u'\xc2'))
#        string = string.replace(u'\xc1', '', string.count(u'\xc1'))
#        string = string.replace(u'\xc5', '', string.count(u'\xc5'))
#        string = string.replace(u'\xc6', '', string.count(u'\xc6'))
#        string = string.replace(u'\xc7', '', string.count(u'\xc7'))
#        string = string.replace(u'\xc8', '', string.count(u'\xc8'))
#        temp = string.replace(u'\xd1', '', string.count(u'\xd1'))
        return temp
    if isinstance(truc, list):
        if len(truc)>1:
            return [Clean(u) for u in truc]
        else:
            return Clean(truc[0])
    else:
        return truc    
        
def ExtractionDate (Brev):
    if u'bibliographic-data' in Brev.keys():
        if u'publication-reference' in Brev[u'bibliographic-data'].keys():
            if u'document-id' in Brev[u'bibliographic-data'][u'publication-reference'].keys():
                tempo = Brev[u'bibliographic-data'][u'publication-reference'][u'document-id']
                if isinstance(tempo, dict):
                    if u'date' in tempo.keys():
                        return tempo[u'date']['$']
                    else:
#                        print "bad date", tempo
                        return ""
                else:
                    if u'date' in tempo[0].keys():
                        return tempo[0][u'date']['$'] #first on should be good
                    else:
#                        print "bad date", tempo
                        return ""
                
                #again retrocompatibility
    try:
        return Brev[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document'][u'bibliographic-data']['priority-claims'][u'priority-claim']['document-id'][0]['date']['$']
    except:
        try:
            return Brev[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document'][u'bibliographic-data']['priority-claims'][u'priority-claim'][0]['document-id'][0]['date']['$']
        except:
            try:
                return Brev[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document'][u'bibliographic-data']['priority-claims'][u'priority-claim']['document-id']['date']['$']
            except:
#                print 'something bad, Date'
                return None
    
def ExtraitKind(Brev):
     if u'@kind' in Brev.keys():
        return Brev[u'@kind']
     else:#retro ompatibility
        try:
            return Brev[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document']['@kind']
        except:
#            print 'something bad, Kind'
            return None

def ExtraitTitleEn(Brev):
    if u'bibliographic-data' in Brev.keys():
        if isinstance(Brev[u'bibliographic-data']['invention-title'], dict):
            return Brev[u'bibliographic-data']['invention-title']['$']
        else: #list are use for multilanguage title support
            #just taking the first one
            return Brev[u'bibliographic-data']['invention-title'][0]['$']
    else: #retro ompatibility
        try:
            return Brev[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document'][u'bibliographic-data']['invention-title'][0]['$']
        except:
            try:
                return Brev[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document'][u'bibliographic-data']['invention-title']['$']
            except:
#                print 'something bad, title'
                return None

def ExtraitCountry(Brev):
    if u'@country' in Brev.keys():
        return Brev[u'@country']
    else: #again retrocompatibility
        try:
            return Brev[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document']['@country']
        except:
#            print 'something bad, country'
            return None

def AlphaTest(chain):
    for let in chain:
        if let.isdigit():
            return False
    return True
    
def UnNest2List(thing):
    CoolType = [str, unicode, int, float]
    if type(thing) in CoolType:
        return thing
    else:
        res = []
        for tt in thing:
            if type(tt) in CoolType:
                res.append(tt)
            else:
                for k in tt:
                    tempo = UnNest2List(k)
                    if type(tempo) in CoolType:
                        if tempo not in res:
                            res.append(tempo)
                    else:
                        for ttt in tempo:
                            res.append(UnNest2List(ttt))
        return res

def ExtraitClassification(DicoOuLst):
    if type(DicoOuLst) == type(dict()):
        temp = DicoOuLst['section']['$'] +DicoOuLst['class']['$'] + DicoOuLst['subclass']['$'] +DicoOuLst['main-group']['$'] + '/' +DicoOuLst['subgroup']['$'] +' '+ DicoOuLst['classification-value']['$']
        return temp
    else:
        res = []
        for Dico in DicoOuLst:
            temp = Dico['section']['$'] +Dico['class']['$'] + Dico['subclass']['$'] +Dico['main-group']['$'] + '/' +Dico['subgroup']['$'] +' '+ Dico['classification-value']['$']
#    section, class, subclass, main-group / subgroup Classif value
            res.append(temp)
    return res

def ExtraitIPCR2(Brevet):
    res = []
    if u'bibliographic-data' in Brevet.keys():
        if u'classifications-ipcr' in Brevet[u'bibliographic-data'].keys():
            if u'classification-ipcr' in Brevet[u'bibliographic-data'][u'classifications-ipcr'].keys():
                tempo = Brevet[u'bibliographic-data'][u'classifications-ipcr'][u'classification-ipcr']
                if isinstance(tempo, dict):
                    if u"text" in tempo.keys():
                            classTemp = tempo['text']['$'].replace(' ','')
                            if AlphaTest(classTemp[len(classTemp)-2:len(classTemp)]):
                                res.append(classTemp[:len(classTemp)-2])
                            else:
                                res.append(classTemp)
                for classif in tempo:
                    if isinstance(classif, dict):
                        if u"text" in classif.keys():
                            classTemp = classif['text']['$'].replace(' ','')
                            if AlphaTest(classTemp[len(classTemp)-2:len(classTemp)]):
                                res.append(classTemp[:len(classTemp)-2])
                            else:
                                res.append(classTemp)
                            
                return res
        elif u'classification-ipc' in Brevet[u'bibliographic-data'].keys():
            if u'text' in Brevet[u'bibliographic-data'][u'classification-ipc'].keys():
                res.append(Brevet[u'bibliographic-data'][u'classification-ipc']['text']['$'])
                return res
        else:
            return None
        
    else: #retrocomp
        try:
            Brev = Brevet[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document'][u'bibliographic-data']['classifications-ipcr']['classification-ipcr']
        except:
#            print 'something bad, IPCR'
            try:        
                return ExtraitClassification(Brevet[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document'][u'bibliographic-data']['patent-classifications']['patent-classification'])
            except:
                return None
        if type(Brev) == type(list()):
            for clas in Brev:
                res.append(clas['text']['$'])
            return res
        else:
            return Brev['text']['$']
    
def ExtraitParties(Brev, content, Format):
    res = []
    if u'bibliographic-data' in Brev.keys():
        Brev = Brev[u'bibliographic-data'][u'parties']
    else: #for retrocompatibility, should be cleaned   
        try:
            Brev = Brev[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document'][u'bibliographic-data'][u'parties']
        except:
            return None
    if Brev.has_key(content+'s'):
        for truc in Brev[content+'s'][content]:
            if truc[u'@data-format'] == Format:
                res.append(truc[content+u'-name'][u'name'][u'$'].replace('\u2002', ' '))
    else:
        return None
    if isinstance(res, list):
        return res
    else:
        return [res]
  
def NomBrevet(Brev):
    """extracts the invention title of a patent bibliographic data"""
    try:
        if Brev.has_key(u'ops:world-patent-data'):
            Brev = Brev[u'ops:world-patent-data']
            if Brev.has_key(u'exchange-documents'):
                Brev = Brev[u'exchange-documents']
                if Brev.has_key(u'exchange-document'):
                    Brev = Brev[u'exchange-document'] 
                    if Brev.has_key(u'bibliographic-data'):
                        Brev = Brev[u'bibliographic-data']
                    else:
                        return None
                else:
                    return None
            else:
                return None
        else:
            return None
        if Brev.has_key(u'invention-title'):
            if type(Brev[u'invention-title']) == type(''):
                return Brev[u'invention-title']
            elif type(Brev[u'invention-title']) == type(dict()):
                if Brev[u'invention-title'].has_key('$'):
                    return Brev[u'invention-title']['$']
            else:
                titre = []
                for tit in Brev[u'invention-title']:
                    if tit.has_key('$'):
                        titre.append(tit['$'])
                return titre
        else:
            return None
    except:
        return None


#############
# tests unitaires
##################
#print ExtractClassification('C10B 01/123')

#DureeBrevet = 20
#SchemeVersion = '20140101'
#
#ListeBrevet = []
#import datetime, os
#today = datetime.datetime.now().date().isoformat()
#dateMini = today
#dateMax = datetime.datetime(1700, 1, 1).isoformat()
#import networkx as nx
#G = nx.DiGraph()
#ResultPath = 'BiblioPatents'
#ResultPathGephi = 'GephiFiles'
#
#Brev = dict()
#
#Brev ["pays"] = u"fr"
#Brev["inventor"] = [u"Me", u"My colleague"]
#Brev["applicant"]= [u'Universite de Toulon']
#Brev["classification"] = u'C101/24A1'
#Brev ["label"] = u'3209934'
#Brev ["date"] = datetime.date(2014,01, 01)
#
#
#if type(Brev['classification']) == type ([]):
#            temp = dict()
#            for key in ['classification', 'IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11', 'status']:
#                temp[key] = []
#            for classif in Brev['classification']:
#                temp['classification'].append(classif.replace(' ', '', classif.count(' ')))
#                temp['IPCR1'].append(classif[0])
#                if len(classif) > 2:
#                    temp['IPCR3'].append(unicode(classif[0:2]))
#                else:
#                    temp['IPCR3'].append('')
#                if len(classif) > 4:
#                    temp['IPCR4'].append(unicode(classif[0:3]))
#                else:
#                    temp['IPCR4'].append('')
#                if classif.count('/') > 0:
#                    temp['IPCR7'].append(unicode(classif.split('/')[0]))
#                else:
#                    temp['IPCR7'].append('')
#                temp['IPCR11'].append(unicode(classif[0:len(classif)-2]))
#                
#                temp['status'].append(unicode(classif[len(classif)-1]))
#                if temp['status'] not in Status:
#                     temp['status']=unicode(classif[len(Brev['classification'])-2])
#                     if temp['status'] not in Status:
#                         temp['status'] = 'N/A'
#            for key in ['classification', 'IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11', 'status']:    
#                if type(temp[key]) == type([]):
#                    Brev[key] = list(set(temp[key]))
#                else:
#                    Brev[key] = temp[key]
#                    
#elif Brev['classification'] is not None:
#            Brev['classification'] = Brev['classification'].replace(' ', '', Brev['classification'].count(' '))
#                        
#            Brev['IPCR1']=(Brev['classification'][0])
#            if len(Brev['classification']) > 2:
#                Brev['IPCR3']=(Brev['classification'][0:3])
#            else:
#                Brev['IPCR3'] = ''
#            if len(Brev['classification']) > 4:            
#                Brev['IPCR4']=(Brev['classification'][0:4])
#            else:
#                Brev['IPCR4'] = ''
#            if Brev['classification'].count('/') >0:
#                Brev['IPCR7']=(Brev['classification'].split('/')[0])
#            else:
#                Brev['IPCR7'] = ''
#            Brev['IPCR11']=(Brev['classification'][0:len(Brev['classification'])-2])
#            Brev['status']=(Brev['classification'][len(Brev['classification'])-1:])
#            if Brev['status'] not in Status:
#                 Brev['status']=(Brev['classification'][len(Brev['classification'])-2])
#                 if Brev['status'] not in Status:
#                     Brev['status'] = 'N/A'
#                     
#else:
#            for ipc in ["classification", 'IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11', 'status']:
#                Brev[ipc] = 'N/A'
#
#ListeBrevet.append(Brev)
#print 
#Pays = set([(u) for u in GenereListeSansDate(ListeBrevet, 'pays')])
#Inventeurs = set([(u) for u in GenereListeSansDate(ListeBrevet, 'inventor')])
#LabelBrevet = set([(u) for u in GenereListeSansDate(ListeBrevet, 'label')])
#Applicant = set([(u) for u in GenereListeSansDate(ListeBrevet, 'applicant')])
#Classification = set([(u) for u in GenereListeSansDate(ListeBrevet, 'classification')])
#IPCR1 = set([(u) for u in GenereListeSansDate(ListeBrevet, 'IPCR1')])
#IPCR3 = set([(u) for u in GenereListeSansDate(ListeBrevet, 'IPCR3')])
#IPCR4 = set([(u) for u in GenereListeSansDate(ListeBrevet, 'IPCR4')])
#IPCR7 = set([(u) for u in GenereListeSansDate(ListeBrevet, 'IPCR7')])
#IPCR11 = set([(u) for u in GenereListeSansDate(ListeBrevet, 'IPCR11')])
#status = set([(u) for u in GenereListeSansDate(ListeBrevet, 'status')])
#listelistes = []
#listelistes.append(list(Pays))
#listelistes.append(list(Inventeurs))
#listelistes.append(list(LabelBrevet))
#listelistes.append(list(Applicant))
#listelistes.append(Classification)
#listelistes.append(list(IPCR1))
#listelistes.append(list(IPCR3))
#listelistes.append(list(IPCR4))
#listelistes.append(list(IPCR7))
#listelistes.append(list(IPCR11))
#listelistes.append(list(status))
#
#ListeNoeuds =[]
#for liste in listelistes:
#        ListeNoeuds += [u for u in liste if u not in ListeNoeuds]
#try:
#    ListeNoeuds.remove('N/A')
#except:
#    pass
#    
# 
#    
#appariement = dict()
#print listelistes
#lstCrit= ['inventor', 'label', 'applicant', 'pays', 'IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11', 'status']
#for i in lstCrit:
#        for j in lstCrit:
#            
#            appariement[change(i)+'-'+change(j)] = [i,j]
#            
#for Brev in ListeBrevet:
#        if 'date' not in Brev.keys():
#            print Brev
#            Brev['date'] = datetime.date(3000, 1, 1)
#            
#G, reseau = GenereReseaux3(G, ListeNoeuds, ListeBrevet, appariement, True)
#
#DateNoeud = dict()
#for lien in reseau:
#        n1, n2, dat, pipo = lien
#        if DateNoeud.has_key(n1):
#            DateNoeud[n1].append(dat)
#        else:
#            DateNoeud[n1] = [dat]
#        if DateNoeud.has_key(n2):
#            DateNoeud[n2].append(dat)
#        else:
#            DateNoeud[n2] = [dat]
#            
#print
#attr = dict()
#liendureseau = [(u, v) for u,v,b ,z in reseau]
#LinkedNodes = []
#for k in liendureseau:
#    LinkedNodes.append(k[0])
#    LinkedNodes.append(k[1])
#    
#for noeud in ListeNoeuds:
#
#    if noeud is not None:
#        if noeud in Pays:
#            attr['label'] = 'pays'
#            attr['url'] = ''
##            elif noeud in Classification:
##                attr['label'] = 'IPCR'
##                if noeud.count('/') > 0:
##                    ind = noeud[4:].index('/')
##                    mask = 4 - ind
##                    mask2 = len(noeud[5+ind:len(noeud)-2])
##                
##                    attr['url'] = "http://web2.wipo.int/ipcpub#lang=fr&menulang=FR&refresh=symbol&notion=scheme&version=20140101&symbol="+noeud[0:4]+str(0)*mask+noeud[4:4+ind]+noeud[5+ind:len(noeud)-2]+'000' + (3-mask2)*str('0')
##                else:
##                    attr['url'] = "http://web2.wipo.int/ipcpub#lang=fr&menulang=FR&refresh=symbol&notion=scheme&version=20140101&symbol="+noeud[0:4]
#        elif noeud in Inventeurs:
#            
#            attr['label'] = 'Inventeur'
#            attr['url'] ='http://worldwide.espacenet.com/searchResults?compact=false&ST=advanced&IN='+quote(noeud)+'&locale=en_EP&DB=EPODOC'
#            #attr['url'] = 'http://patentscope.wipo.int/search/en/result.jsf?currentNavigationRow=2&prevCurrentNavigationRow=1&query=IN:'+quote(noeud)+'&office=&sortOption=Pub%20Date%20Desc&prevFilter=&maxRec=38&viewOption=All'
#        elif noeud in LabelBrevet:
#            attr['label'] = 'Brevet'
#            attr['Class'] = getClassif(noeud, ListeBrevet)
#            if attr['Class'] is not None:
#                attr['ReductedClass'] = getClassif(noeud, ListeBrevet)[0:4]
#                tempotemp = "http://worldwide.espacenet.com/searchResults?compact=false&ST=singleline&query="+noeud+"&locale=en_EP&DB=EPODOC"
#            
#                attr['url'] = tempotemp
#            else:
#                attr['ReductedClass'] = ""
#        elif noeud in Applicant:
#            attr['label'] = 'Applicant'
#            attr['url'] ='http://worldwide.espacenet.com/searchResuldengue-grupos.jsonts?compact=false&ST=advanced&locale=en_EP&DB=EPODOC&PA='+quote(noeud)
#            #attr['url'] = 'http://patentscope.wipo.int/search/en/result.jsf?currentNavigationRow=2&prevCurrentNavigationRow=1&query=PA:'+quote(noeud)+'&office=&sortOption=Pub%20Date%20Desc&prevFilter=&maxRec=123897&viewOption=All'
#        elif noeud in IPCR1:
#            if noeud in IPCRCodes.keys():
#                attr['label'] = 'IPCR1'
#                attr['name'] = IPCRCodes[noeud]
#                attr['url'] = 'http://web2.wipo.int/ipcpub#lang=enfr&menulang=FR&refresh=page&notion=scheme&version='+SchemeVersion+'&symbol=' +noeud
#            else:
#                pass #node is may be a status node
#        elif noeud in IPCR7:
#            attr['label'] = 'IPCR7'
#            attr['url'] =  'http://web2.wipo.int/ipcpub#lang=enfr&menulang=FR&refresh=page&notion=scheme&version='+SchemeVersion+'&symbol=' +noeud
#    
#        elif noeud in IPCR3:
#            attr['label'] = 'IPCR3'
#            attr['url'] = 'http://web2.wipo.int/ipcpub#lang=enfr&menulang=FR&refresh=page&notion=scheme&version='+SchemeVersion+'&symbol=' +noeud
#        elif noeud in IPCR4:
#            attr['label'] = 'IPCR4'
#            attr['url'] = 'http://web2.wipo.int/ipcpub#lang=enfr&menulang=FR&refresh=page&notion=scheme&version='+SchemeVersion+'&symbol=' +noeud
#
#        elif noeud in IPCR11:
#            attr['label'] = 'IPCR11'
#            attr['url'] = ''
#        elif noeud in status:
#            attr['label'] = 'status'
#            
#        if noeud in ListeNoeuds:
#            G.add_node(ListeNoeuds.index(noeud))
#
#            G.node[ListeNoeuds.index(noeud)]['label'] = noeud
#            
#            G.node[ListeNoeuds.index(noeud)]['category'] = attr['label']
#            G.node[ListeNoeuds.index(noeud)]['url'] = attr['url']
#            G.node[ListeNoeuds.index(noeud)]['weight'] = LinkedNodes.count(noeud)
#            G.node[ListeNoeuds.index(noeud)]['start'] = min(DateNoeud[G.node[ListeNoeuds.index(noeud)]['label']]).isoformat()
#            G.node[ListeNoeuds.index(noeud)]['end'] = max(DateNoeud[G.node[ListeNoeuds.index(noeud)]['label']]).isoformat()
#            if dateMini > G.node[ListeNoeuds.index(noeud)]['start']:
#                dateMini = G.node[ListeNoeuds.index(noeud)]['start']
#            if dateMax < G.node[ListeNoeuds.index(noeud)]['end']:
#                dateMax = G.node[ListeNoeuds.index(noeud)]['end']
#            
#            if len(G.node[ListeNoeuds.index(noeud)]['time']) >1:
#                lst = [u[1] for u in G.node[ListeNoeuds.index(noeud)]['time']]
#                lst.sort()
#                lsttemp = []
#                cpt=0
#                for kk in range(len(lst)):
#                    for nb in range(len(G.node[ListeNoeuds.index(noeud)]['time'])):                 
#                        if G.node[ListeNoeuds.index(noeud)]['time'][nb][1] == lst[kk]:
#                            if G.node[ListeNoeuds.index(noeud)]['time'][nb] not in lsttemp:
#                                if cpt>0:
#                                    
#                                    lsttemp[cpt-1] = (lsttemp[cpt-1][0], lsttemp[cpt-1][1], G.node[ListeNoeuds.index(noeud)]['time'][nb][1] )#enddate is startdate of current datetime
#                                lsttemp.append(G.node[ListeNoeuds.index(noeud)]['time'][nb])
#                                cpt+=1
#                G.node[ListeNoeuds.index(noeud)]['time'] = lsttemp         
#            G.node[ListeNoeuds.index(noeud)]['deb'] = G.node[ListeNoeuds.index(noeud)]['start']
#            G.node[ListeNoeuds.index(noeud)]['fin']= dateMax#G.node[ListeNoeuds.index(noeud)]['end']
#            G.node[ListeNoeuds.index(noeud)]['val'] = sum([u[0] for u in G.node[ListeNoeuds.index(noeud)]['time']])
#            del(G.node[ListeNoeuds.index(noeud)]['end'])
#            del(G.node[ListeNoeuds.index(noeud)]['start'])
#            del(G.node[ListeNoeuds.index(noeud)]['weight'])               
#            if noeud not in IPCR1:
#                pass
#            else:
#                G.node[ListeNoeuds.index(noeud)]['label'] = noeud + '-' +attr['name']
#        else:
#            print "on devrait pas être là, never", noeud
#            #G.node[ListeNoeuds.index(noeud)]['end'] = ExtraitMinDate(G.node[ListeNoeuds.index(noeud)]) + DureeBrevet
#            #G.node[ListeNoeuds.index(noeud)]['start'] = 
#        G.graph['defaultedgetype'] = "directed"
#        G.graph['timeformat'] = "date"
#        G.graph['mode'] = "dynamic"
#        G.graph['start'] = dateMini
#        G.graph['end'] = dateMax
#
#
#ndf = 'test'
#nx.write_gexf(G, ResultPathGephi+'\\'+ndf + ".gexf", version='1.2draft')
#fic = open(ResultPathGephi+'\\'+ndf+'.gexf', 'r')
##
## Next is a hack to correct the bad writing of the header of the gexf file
## with dynamics properties
#fictemp=open(ResultPathGephi+'\\'+"Good"+ndf+'.gexf', 'w')
#fictemp.write("""<?xml version="1.0" encoding="utf-8"?><gexf version="1.2" xmlns="http://www.gexf.net/1.2draft" xmlns:viz="http://www.gexf.net/1.2draft/viz" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.w3.org/2001/XMLSchema-instance">
#  <graph defaultedgetype="directed" mode="dynamic" timeformat="date">
#<attributes class="edge" mode="static">
#  <attribute id="6" title="deb" type="string" />
#  <attribute id="7" title="fin" type="string" />
#  <attribute id="8" title="rel" type="string" />
#    </attributes>
#    <attributes class="edge" mode="dynamic">
#  <attribute id="9" title="time" type="integer" />
#</attributes>
#<attributes class="node" mode="static">
#  <attribute id="0" title="category" type="string" />
#  <attribute id="1" title="val" type="integer" />
#  <attribute id="3" title="url" type="string" />
#  <attribute id="4" title="deb" type="string" />
#  <attribute id="5" title="fin" type="string" />
#</attributes>
#    <attributes class="node" mode="dynamic">
#        <attribute id="2" title="time" type="integer" />
#    </attributes>
#""")
#ecrit  =False
#for lig in fic.readlines():
#    if lig.count('<nodes>'):
#        ecrit = True
#    if ecrit:
#        fictemp.write(lig)
#fictemp.close()
#fic.close()
#os.remove(ResultPathGephi+'\\'+ndf+'.gexf')
#
#os.rename(ResultPathGephi+'\\'+"Good"+ndf+'.gexf', ResultPathGephi+'\\'+ndf+'.gexf')
#print "Network file writen in ",  ResultPathGephi+' directory.\n See file: '+ndf + ".gexf"