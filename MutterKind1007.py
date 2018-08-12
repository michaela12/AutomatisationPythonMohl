###
#
# Von Michaela Mohl mohl@in.tum.de
# Betreut von Larissa Wolkenstein Larissa.Wolkenstein@psy.lmu.de
# Betreut von Kira-marlene Torney kira-marlene.torney@student.uni-tuebingen.de
#
###
#
# Dieses Porgramm erstellt 2 Output Tabellen für Input von dem Mutter Kind Projekt
#
###



import csv
import pandas as pd
import datetime as dt
import xlrd as x 
import os
import numpy as np
import math
from decimal import *


pd.set_option('display.max_rows', 10)
print('Das ist die Exe zur Datenauswertung des Mutter Kind Experiments')


ReckOrExpl = ['Reck_','Expl_']
#DEBUG
for bigI in range(0,len(ReckOrExpl)):
    if(bigI == 0):
        Reck = True
        Expl = False
        print('Aktuell werden die Ergenisse nach Reck berechnet')
    if(bigI == 1):
        Reck = False
        Expl = True
        print('Aktuell werden die Ergenisse exploratorisch berechnet')
    
    ### Hier wird die Output Tabelle erstellt 
    def createOutput():
        VariablenAnfang = ['pos_s_ms','object_s_ms','Negativ_s_ms','Komp_M_Cpvc_s_ms','Komp_K_ipos_s_ms','still_K_sum_s_ms']

                    
        for i in range(0,len(VariablenAnfang)-1):
            VariablenAnfang[i] = 'Match_' +VariablenAnfang[i]

        VariablenEnde = ['proportion_matching_states_percentage','reperation_rate_frequency','Interactive_Repair_Latency_mean','First_Match_Latency_sec']
        ReckOrExpl = ['Reck_','Expl_']
        if(Reck == True):
                for i in range(0,len(VariablenEnde)):
                    VariablenEnde[i] = ReckOrExpl[0] + VariablenEnde[i]
        if(Expl == True):
                for i in range(0,len(VariablenEnde)):
                    VariablenEnde[i] = ReckOrExpl[1] + VariablenEnde[i]
        AllCols = ['Match_t2','Match_t3']

        Phases = ['1','2','3']

        Output = VariablenAnfang + VariablenEnde
        OutputPhase1 = VariablenAnfang + VariablenEnde
        OutputPhase2 = VariablenAnfang + VariablenEnde
        OutputPhase3 = VariablenAnfang + VariablenEnde

        for i in range(0,len(Output)):
            OutputPhase1[i] = Phases[0] +'_'+ Output[i]
        for i in range(0,len(Output)):
            OutputPhase2[i] = Phases[1] +'_'+ Output[i]
        for i in range(0,len(Output)):
            OutputPhase3[i] = Phases[2] +'_'+ Output[i]

        Output1 = OutputPhase1+OutputPhase2+OutputPhase3
        Output2 = OutputPhase1+OutputPhase2+OutputPhase3

        for i in range(0,len(Output1)):
            Output1[i] = AllCols[0] +'_'+ Output1[i]
        for i in range(0,len(Output2)):
            Output2[i] = AllCols[1] +'_'+ Output2[i]

        Output = Output1+Output2
        Thisindex = list((range(1,134)))

        def foo(l, dtype):
            return map(dtype, l)

        Thisindex = foo(Thisindex,str)

        Thisindex = [x+'999' for x in Thisindex]
        #print(Output)
        df_Output = pd.DataFrame(columns =Output, index = Thisindex)
        #print(Output)
        df_Output = df_Output.astype(float)

        return df_Output


    df_Output = createOutput()



    # Hierbei ist nameOfTheFile der Name in der Datei, nameOfThePage ist der Name des Blattes <br>
    # Im folgenden wird dargestellt wie die aktuelle Datei im Programm aussehen sollte.
    testPath = os.getcwd()

    inputPath = testPath +'\Input'
    if not os.path.exists(inputPath):
        os.makedirs(inputPath)
        

    print('Von hier werden die Datein eingezogen')
    print(inputPath)
    
    ###
    ### Pulling in die Input Files
    ### 

    files = [f for f in os.listdir(inputPath) if f.endswith("999.xlsx")] #if os.path.isfile(f)]# ]

    print('Hier die Liste von allen Excel Dateien die eingelesen wurden:')
    print(files)


    ### DEBUG
    #for i in range(0,1):
    ### REAL 
    for i in range(0,len(files)):
        #print(files[i])
        name = files[i]
        #name = '4999.xlsx'


    ###
    ### Import the file itself   nameOfTheFile = name+'.xlsx'
    ###

        nameOfTheFile = name
        print('Datei an der gerade gearbeitet wird')
        print(nameOfTheFile)
        name = name[:-5]
        def fileImport(nameOfTheFile):
            nameOfThePage = '39993_R1_Excel'
            xlsx =pd.ExcelFile('Input/'+nameOfTheFile)
            namesUsed = ['T1 Begin Code','T1 C1 Ende Code','T1 C2 Dauer Code',
                        'T1 C3 Code','T2 Begin Code','T2 C1 Ende Code',
                        'T2 C2 Dauer Code','T2 C3 Code','Unnamed: 8','Unnamed: 9']
            df = pd.read_excel(xlsx, nameOfThePage, names =namesUsed, header = None)    
            NeedsReformation = False
            #if T1 ein spalten name ist dann das alte Zeugs
            if (name == '2999'):
                NeedsReformation = False
            dfZusatz=df[['Unnamed: 8','Unnamed: 9']]
            return df,NeedsReformation,dfZusatz

        df, NeedsReformation,dfZusatz = fileImport(nameOfTheFile)


        # 3) Umformen der reingeladenen Datei <br>
        # In der nächsten Zelle werden von der Originaltabelle die Spalten umgenannt, und nichtgebrauchte Spalten und Zeilen werden gelöscht (gedroppt)
        # 

        # In[144]:

    ### 
    ### Gesamt Zeiten rausnehmen
    ###

        def getStillSums(NeedsReformation, dfZusatz, T2orT3):
            Still_sums = np.array([0.0,0,0,0])
            if(NeedsReformation == True):
                if(T2orT3 == 'T2'):
                    Still_times = ['Still_t2_K_1_sum','Still_t2_K_2_sum','Still_t2_K_3_sum','Still_t2_K_kontr_i_sum']
                if(T2orT3 == 'T3'):
                    Still_times = ['Still_t3_K_1_sum','Still_t3_K_2_sum','Still_t3_K_3_sum','Still_t3_K_kontr_i_sum']
            if(NeedsReformation == False):
                if(T2orT3 == 'T2'):
                    Still_times = ['SF_t2_K_1_sum','SF_t2_K_2_sum','SF_t2_K_3_sum','SF_t2_K_kontr_i_sum']
                if(T2orT3 =='T3'):
                    Still_times = ['SF_t3_K_1_sum','SF_t3_K_2_sum','SF_t3_K_3_sum','SF_t3_K_kontr_i_sum']
            if(name =='2999'):
                if(T2orT3 =='T2'):
                #print('im here')
                #print(name)
                    Still_sums[0] = dfZusatz.loc[df['Unnamed: 8'] == 'Still_t2_K_1_sum']['Unnamed: 9'].values
                    Still_sums[1] = dfZusatz.loc[df['Unnamed: 8'] == 'Still_t2_K_2_sum']['Unnamed: 9'].values
                    Still_sums[2] = dfZusatz.loc[df['Unnamed: 8'] == 'Still_t2_K_3_sum']['Unnamed: 9'].values
                    Still_sums[3] = dfZusatz.loc[df['Unnamed: 8'] == 'Still_t2_K_kontr_i_sum']['Unnamed: 9'].values
                if(T2orT3 =='T3'):
                #print('im here')
                #print(name)
                    Still_sums[0] = dfZusatz.loc[df['Unnamed: 8'] == 'Still_t3_K_1_sum']['Unnamed: 9'].values
                    Still_sums[1] = dfZusatz.loc[df['Unnamed: 8'] == 'Still_t3_K_2_sum']['Unnamed: 9'].values
                    Still_sums[2] = dfZusatz.loc[df['Unnamed: 8'] == 'Still_t3_K_3_sum']['Unnamed: 9'].values
                    Still_sums[3] = dfZusatz.loc[df['Unnamed: 8'] == 'Still_t3_K_kontr_i_sum']['Unnamed: 9'].values
            if(name != '2999'):
                for i in range(0,len(Still_times)):
                    Still_sums[i] = dfZusatz.loc[df['Unnamed: 8'] == Still_times[i]]['Unnamed: 9'].values   
            return Still_sums

        Still_t2_K_sums = getStillSums(NeedsReformation, dfZusatz,'T2')
        #print(Still_t2_K_sums)
        
        Still_t3_K_sums = getStillSums(NeedsReformation, dfZusatz,'T3')
        #print(Still_t3_K_sums)

     


        # In[145]:

        ###
        ### Get M Zeiten
        ###
        def getMStillSums(NeedsReformation, dfZusatz, T2orT3):
            MStilSums = np.array([0.0,0,0,0])
            if(T2orT3 =='T2'):
                if(NeedsReformation == True ):
                    indexOFM1 = dfZusatz[dfZusatz['Unnamed: 8'] == 'Still_t2_M_1_sum'].index.tolist()
                if(NeedsReformation == False):
                    indexOFM1 = dfZusatz[dfZusatz['Unnamed: 8'] == 'SF_t2_M_1_sum'].index.tolist()
                indexOFM1 = int(indexOFM1[0])
                for i in range(0,4):
                    MStilSums[i] = dfZusatz.loc[indexOFM1,'Unnamed: 9']
                    indexOFM1 = indexOFM1 +1
            if(T2orT3 =='T3'):
                if(NeedsReformation == True):
                    indexOFM1 = dfZusatz[dfZusatz['Unnamed: 8'] == 'Still_t3_M_1_sum'].index.tolist()
                if(NeedsReformation == False):
                    indexOFM1 = dfZusatz[dfZusatz['Unnamed: 8'] == 'SF_t3_M_1_sum'].index.tolist()
                indexOFM1 = int(indexOFM1[0])
                for i in range(0,4):
                    MStilSums[i] = dfZusatz.loc[indexOFM1,'Unnamed: 9']
                    indexOFM1 = indexOFM1 +1
            return(MStilSums)
        
        if(False):              
            Still_t2_M_sums = getMStillSums(NeedsReformation,dfZusatz,'T2')
            Still_t3_M_sums = getMStillSums(NeedsReformation,dfZusatz,'T3')
            test = abs(Still_t2_M_sums[3]-Still_t2_K_sums[3])
            test2 = abs(Still_t3_M_sums[3]-Still_t3_K_sums[3])
            if(True):
                print(name)
                print('Die T2 K Summen 1 2 3 und Gesamt')
                print(Still_t2_K_sums)
                print('Die T2 M Summen 1 2 3 und Gesamt')
                print(Still_t2_M_sums)
                print('Die T3 K Summen 1 2 3 und Gesamt')
                print(Still_t3_K_sums)
                print('Die T3 M Summen 1 2 3 und Gesamt')
                print(Still_t3_M_sums)
            continue

        # 3) <br>
        # In der nächsten Zelle wird von der Original Tabelle das erste Experiment (genannt T1) abgetrennt, darüber hinaus werden noch die leeren Zeilen am ende abgeschnitten

        # In[146]:

        def reshape(df):
            if(NeedsReformation == True):
                df = df.drop(0)
                df = df.drop(1)
                df = df.drop(2)
                df =  df.reset_index(drop = True)
            df = df.drop('Unnamed: 8',1)
            df = df.drop('Unnamed: 9',1)
            return df

        df = reshape(df)


        # 3) <br>
        # In der nächsten Zelle wird von der Original Tabelle das zweite Experiment (genannt T2) abgetrennt, darüber hinaus werden noch die leeren Zeilen am ende abgeschnitten

        # In[147]:

        def splitPartsOf(df):
            ###
            ### Split the first experiment  T1  off 
            ###
            T1 = df
            T1 = T1.drop('T2 C1 Ende Code',1)
            T1 = T1.drop('T2 C2 Dauer Code',1)
            T1 = T1.drop('T2 C3 Code',1)
            T1 = T1.drop('T2 Begin Code',1)
            T1
            ###
            ### Cutting the empty values of T1
            ###
            for index, row in T1.iterrows():
                x = float(row['T1 Begin Code'])
                y = float(row['T1 C1 Ende Code'])
                z = float(row['T1 C2 Dauer Code'])

                if math.isnan(x) and math.isnan(y) and math.isnan(z): 
                    T1.drop(index, inplace = True)
            ###
            ### Split the first experiment  T2  off 
            ###
            T2 = df
            T2 = T2.drop('T1 Begin Code',1)
            T2 = T2.drop('T1 C1 Ende Code',1)
            T2 = T2.drop('T1 C2 Dauer Code',1)
            T2 = T2.drop('T1 C3 Code',1)
            ###
            ### Cutting the empty values of T2
            ###
            for index, row in T2.iterrows():
                x = float(row['T2 Begin Code'])
                y = float(row['T2 C1 Ende Code'])
                z = float(row['T2 C2 Dauer Code'])

                if math.isnan(x) and math.isnan(y) and math.isnan(z): 
                    T2.drop(index, inplace = True)    
            return(T1,T2)

        T1, T2 = splitPartsOf(df)


        # Testen ob T1 oder T2 leer sind  
        T1empty = T1.empty   
        T2empty = T2.empty 
        #if(T1.empty or T2.empty):
            #print('Eine T Empty')

        # 4) Abtrennen der einzelnen Experimente in den ChildCarer und Infant Teil 

        # In[148]:

        def TabelleTeilen(df, beginCodeString):
            test = df.get_value(index = 0, col = beginCodeString)
            BeginCodes = df[df[beginCodeString] == test].index.tolist()
            if(len(BeginCodes)==2):
                dfChildCarer = df.loc[BeginCodes[0]:BeginCodes[1]-1]
                dfInfant = df.loc[BeginCodes[1]::] 
            else:
                dfChildCarer = df.loc[BeginCodes[0]:BeginCodes[1]-1]
                dfInfant = df.loc[BeginCodes[1]:BeginCodes[2]-1]
            return(dfChildCarer, dfInfant)
        if(not(T1empty)):
            T1ChildCarer,T1Infant = TabelleTeilen(T1,'T1 Begin Code')
        if(not(T2empty)):
            T2ChildCarer,T2Infant = TabelleTeilen(T2,'T2 Begin Code')


        # 5) Die Childcarer bzw Infant Tabellen nochmals in 3 Phasen (also von Klopfen bis eins vorm klopfen abtrennen)

        # In[149]:

        def PhasenUnterteilung(TPhasePartDF, TextCode):
            Klopfen = TPhasePartDF[TPhasePartDF[TextCode].str.contains('klopfen')].index.tolist()
            Phase1 = TPhasePartDF.loc[Klopfen[0]:Klopfen[1]-1]
            Phase2 = TPhasePartDF.loc[Klopfen[1]:Klopfen[2]-1]
            Phase3 = TPhasePartDF.loc[Klopfen[2]::]
            return(Phase1, Phase2, Phase3)

        ###
        ###  T1 Childcarer nochmal in Phasen unterteilenA
        ###
        if(not(T1empty)):
            T1CCPhase1, T1CCPhase2, T1CCPhase3 = PhasenUnterteilung(T1ChildCarer,'T1 C3 Code')
            ###  T1 Infant teilen
            T1IPhase1, T1IPhase2, T1IPhase3 = PhasenUnterteilung(T1Infant,'T1 C3 Code')

        ###
        ### T2 CC in Phasen teilen
        ###
        if(not(T2empty)):
            T2CCPhase1, T2CCPhase2, T2CCPhase3 = PhasenUnterteilung(T2ChildCarer,'T2 C3 Code')
            ### T2 in Infant Phasen
            T2IPhase1, T2IPhase2, T2IPhase3 = PhasenUnterteilung(T2Infant,'T2 C3 Code')


        # 5) Jetzt kommen die endgültigen Machtes <br>
        # Dies ist für T1
        # CC steht für ChildCarer und I für Infant <br>
        # a)
        # Ertmal werden für alle Matcharten neue Ergebniss Tabellen ersten. Hierbei gibt es fünf Matcharten <br>
        # und für jede Matchart gibt es zwei Tabellen, eine für den CC und einen für den I. <br>
        # Die Tabellen sind die Folgenden <br>
        # 
        # Das Vorgehen ist wie folgt: 
        # Es wird die Childcarer Tabelle iteriert, also jede Zeile wird durchgegangen. Für jede Zeile wird der Code <br> betrachtet, wenn der Code ein interesanter (zB Für positive Matches CPVC) ist wird die komplette Infant Tabelle iteriert und kontrolliert: gibt es den dazu passenden Match (zB für positive Matches INEU) der in einer passenden Zeitrahmen ist. <br>
        # Der Zeitrahmen ist in 4 Fälle aufgetrennt: <br>
        # Der Zeitraum der CC liegt im I Zeitraum.<br>
        # Der Zeitraum der I liegt im CC Zeitraum <br>
        # Der Beginn der CC ist vor dem I Begin, das Ende der CC liegt im Interval von I. <br>
        # Der Begin der I ist vor dem CC Begin, das Ende der I liegt im Interval von I. <br>
        # Bei den letzten beiden fällen werden abweichungen von 1 Sekunde betrachtet. <br>
        # <br>
        # Wenn einer dieser Fälle zu trifft, dann wird die komplette Zeile aus der T1ChildCarer in die Ergbniss Tabelle gespeichert (zB bei Positiven Matches in T1matchesPositv) und die komplette Zeile aus T1Infant wird in die Ergebniss Tabelle für Infant Matches eingefügt. (zB bei Positiven Matches T1matchesPositivInfant) <br>
        # 
        # 
        # <br>
        # Für die Postiven Matches würden die folgenden Codes verglichen: <br>
        # cpvc oder cpos und ineu oder ipos <br>
        # T1matchesPositiv <br>
        # T1matchesPositivInfant<br>
        # 
        # cneu oder cpvc oder cpos und inon
        # T1matchesObjekt<br> 
        # T1matchesObjektInfant<br> 
        # 
        # T1matchesNegativ<br>
        # T1matchesNegativInfant <br>
        # 
        # T1matchesKompCPVC <br>
        # T1matchesKompCPVCInfant <br>
        # 
        # T1matchesKompCNON <br>
        # T1matchesKompCNONInfant<br>
        # 

        # In[150]:

        def helperFunctionForMatches(T1OrT2Childcarer, T1OrT2Infant, CCCodesList, ICodeList, T1orT2):
            MatchesCC = pd.DataFrame()
            MatchesI = pd.DataFrame()
            if(T1orT2 == 'T1'):
                Variables = ['T1 Begin Code','T1 C1 Ende Code', 'T1 C2 Dauer Code','T1 C3 Code']
            if(T1orT2 =='T2'):
                Variables = ['T2 Begin Code','T2 C1 Ende Code', 'T2 C2 Dauer Code','T2 C3 Code']
            for index, row in T1OrT2Childcarer.iterrows():
                CCBeginCode = row[Variables[0]]
                CCEndeCode = row[Variables[1]]
                CCDauerCode = row[Variables[2]]
                CCCode = row[Variables[3]]
                if any(code in CCCode for code in CCCodesList):
                    for index1, row1 in T1OrT2Infant.iterrows():
                        IBeginCode = row1[Variables[0]]
                        IEndeCode = row1[Variables[1]]
                        IDauerCode = row1[Variables[2]]
                        ICode = row1[Variables[3]]
                        if any(code in ICode for code in ICodeList):
                            ### 1. CC fängt zuerst and und endet im I Code
                            ### 2. CC begint im I Code und endet danach
                            ### 3. CC liegt komplett im I Code
                            ### 4. I liegt komplett in CC Code
                            boolZeitGleich = ((CCBeginCode <= IBeginCode and IBeginCode <= CCEndeCode <= IEndeCode) 
                            or (IBeginCode <= CCBeginCode <= IEndeCode and IEndeCode <= CCEndeCode) 
                            or (IBeginCode <= CCBeginCode <= IEndeCode and IBeginCode <= CCEndeCode <= IEndeCode) 
                            or (CCBeginCode <= IBeginCode <= CCEndeCode and CCBeginCode <= IEndeCode <= CCEndeCode))
                            if(boolZeitGleich): 
                                MatchesCC = MatchesCC.append(row, True, False)
                                MatchesI = MatchesI.append(row1, True, False)
            resultMatch = pd.concat([MatchesCC, MatchesI], axis =1)
            if(T1orT2 == 'T1'):
                if(not(resultMatch.empty)):
                    resultMatch.columns =['T1 CC Begin Code','T1 CC Ende Code','T1 CC Dauer Code','T1 CC Code','T1 I Begin Code','T1 I Ende Code','T1 I Dauer Code','T1 I Code']
            if(T1orT2 == 'T2'):
                if(not(resultMatch.empty)): 
                    resultMatch.columns =['T2 CC Begin Code','T2 CC Ende Code','T2 CC Dauer Code','T2 CC Code','T2 I Begin Code','T2 I Ende Code','T2 I Dauer Code','T2 I Code']
            return resultMatch


        # In[151]:

        ###
        ### Create Matches as a function
        ###

        def createMatches(T1OrT2Childcarer,T1OrT2Infant, T1orT2):
            CCPositivCodes = ['cpvc','cpos']
            IPositivCodes = ['ineu','ipos']    
            ResultMatchesPositiv = helperFunctionForMatches(T1OrT2Childcarer, T1OrT2Infant, CCPositivCodes, IPositivCodes,T1orT2)

            CCObjektCodes = ['cneu','cpvc','cpos']
            IObjektCodes = ['inon']
            ResultMatchesObjekt = helperFunctionForMatches(T1OrT2Childcarer, T1OrT2Infant, CCObjektCodes, IObjektCodes, T1orT2)

            CCNegativCodes = ['cwit','cint','chos']
            INegativCodes = ['ipro','iwit']
            ResultMatchesNegativ = helperFunctionForMatches(T1OrT2Childcarer, T1OrT2Infant, CCNegativCodes,INegativCodes,T1orT2)

            CCKompCPVCCodes = ['cpvc']
            IKompCPVCCodes =['ipro','iwit']
            ResultMatchesKompCPVC = helperFunctionForMatches(T1OrT2Childcarer, T1OrT2Infant, CCKompCPVCCodes, IKompCPVCCodes, T1orT2)

            CCKompCNONCodes = ['cnon']
            IKompCNONCodes =['ipos','ineu']
            ResultMatchesKompCNON = helperFunctionForMatches(T1OrT2Childcarer, T1OrT2Infant, CCKompCNONCodes, IKompCNONCodes, T1orT2)

            #CCPosExpCodes = ['cpcv','cpos']
            #IPosExpCodes =['ipos']
            #ResultMatchesPosExp = helperFunctionForMatches(T1OrT2Childcarer, T1OrT2Infant, CCPosExpCodes, IPosExpCodes, T1orT2)
            
            return(ResultMatchesPositiv,ResultMatchesObjekt,ResultMatchesNegativ,ResultMatchesKompCPVC,ResultMatchesKompCNON)

        if(not(T1empty)):
            ResultT1matchesPositiv, ResultT1matchesObjekt, ResultT1matchesNegativ, ResultT1matchesKompCPVC, ResultT1matchesKompCNON = createMatches(T1ChildCarer,T1Infant,'T1')
        if(not(T2empty)):
            ResultT2matchesPositiv, ResultT2matchesObjekt, ResultT2matchesNegativ, ResultT2matchesKompCPVC, ResultT2matchesKompCNON = createMatches(T2ChildCarer,T2Infant,'T2')




        ### Die Intervall Zeiten von Oben nehmen und umbennen zum weiterarbeitn
        ###
        ### Die Gesamt Zeit im Experiment T1
        ###
        IntervalSumT1 = Still_t2_K_sums[3]
        ###
        ### Die Gesamt Zeit im Experiment T2
        ###
        IntervalSumT2 = Still_t3_K_sums[3]
        ###
        ### Die Teilzeiten für die Phasen! T1
        ###
        T1CompleteSum = [0,0,0]
        for i in range(0,3):
            T1CompleteSum[i] = Still_t2_K_sums[i]   
        ###
        ### Die Teilzeiten für die Phasen! T2
        ###
        T2CompleteSum = [0,0,0]
        for i in range(0,3):
            T2CompleteSum[i] = Still_t3_K_sums[i]



        ###
        ### Die Matches
        ###
        def matchCreation(matchtable):
            #
            #
            #
            for index, row in matchtable.iterrows():

                CCBeginCode  = row.ix[0]
                CCEndeCode   = row.ix[1]
                CCDauerCode  = row.ix[2]
                CCCode       = row.ix[3]

                IBeginCode   = row.ix[4]
                IEndeCode    = row.ix[5]
                IDauerCode   = row.ix[6]
                ICode        = row.ix[7]


                ### Begin Fälle
                ### Wenn CC Intervall in I Intervall
                ###
                if(CCBeginCode >= IBeginCode and CCEndeCode <= IEndeCode):
                    DauerMatch = CCDauerCode
                    matchtable.loc[index,'DauerMatch'] = DauerMatch



                ###
                ### Wenn I Intervall in CC Intervall
                ###
                if(CCBeginCode <= IBeginCode and CCEndeCode >= IEndeCode):           
                    DauerMatch = IDauerCode
                    matchtable.loc[index,'DauerMatch'] = DauerMatch

                ###
                ### Die logischen Reste
                ###
                if(CCBeginCode < IBeginCode and CCEndeCode < IEndeCode):
                    #print("test2")
                    DauerMatch = CCEndeCode - IBeginCode
                    DauerMatch = round(DauerMatch,3)
                    matchtable.loc[index,'DauerMatch'] = DauerMatch


                ###
                ### Logischer Rest teil2
                ###
                if(CCBeginCode > IBeginCode and CCEndeCode > IEndeCode):  
                    #print("test3")
                    DauerMatch = IEndeCode - CCBeginCode
                    DauerMatch = round(DauerMatch,3)
                    matchtable.loc[index,'DauerMatch'] = DauerMatch

            return;


        # In[154]:

        ###
        ### Call the functions for MatchCreation T1
        ###
        #dataframeList =[ResultT1matchesPositiv,ResultT1matchesObjekt,ResultT1matchesNegativ,ResultT1matchesKompCPVC,ResultT1matchesKompCNON,ResultT2matchesPositiv,ResultT2matchesObjekt,ResultT2matchesNegativ,ResultT2matchesKompCPVC,ResultT2matchesKompCNON]
        if(not(T1empty)):
            matchCreation(ResultT1matchesPositiv)
            matchCreation(ResultT1matchesObjekt)
            matchCreation(ResultT1matchesNegativ)
            matchCreation(ResultT1matchesKompCPVC)
            matchCreation(ResultT1matchesKompCNON)

        ###
        ### All for T2
        ###
        if(not(T2empty)):
            matchCreation(ResultT2matchesPositiv)
            matchCreation(ResultT2matchesObjekt)
            matchCreation(ResultT2matchesNegativ)
            matchCreation(ResultT2matchesKompCPVC)
            matchCreation(ResultT2matchesKompCNON)


        # In[155]:

        ###
        ### Set up tha split along the phases of T1 along the ResultMatch DF
        ###
        def amountAndTime(dataframe,stringA): 
            intermed = [0,0,0]   #dataframe der aktuell genutz wird
            TimeMatches = pd.DataFrame(columns =['Time per index+1'])
            AmountMatches = pd.DataFrame(columns =['Amount per index+1'])
            for i in range(0,3):
                string = str(i+1)
                intermed[i] =  dataframe[dataframe[stringA].str.contains(string)]
                AmountMatches.loc[i,'Amount per index+1'] = len(intermed[i])
                df =intermed[i]
                zwischen = sum(df['DauerMatch'])
                TimeMatches.loc[i,'Time per index+1'] =zwischen
            return TimeMatches,AmountMatches


        # In[156]:

        ###
        ### InterValSum = IntervalSumT1 oder IntervalSumT2 von den ganzen phasen
        ### CompleteSum = T1CompleteSum oder T2CompleteSum für 1 2 3
        def IntervallLength(Summarydataframe, IntervalSum, CompleteSum):
            Summarydataframe.loc[3,'Gesamtdauer dieser Phase']=IntervalSum
            for i in range(0,3):
                Summarydataframe.loc[i,'Gesamtdauer dieser Phase'] =CompleteSum[i]
            return Summarydataframe

        def fillingMatchvalues(Summarydataframe,OriginalDataframe, whichCode, IntervalSum,CompleteSum):
            if(not(OriginalDataframe.empty)):
                AMTResult = amountAndTime(OriginalDataframe,whichCode)
                Time = AMTResult[0]
                Amount = AMTResult[1]
                for i in range(0,3):
                    Summarydataframe.loc[i,'Gesamtanzahl Matches dieser Art'] = Amount.loc[i,'Amount per index+1']
                    Summarydataframe.loc[i,'Gesamtdauer aller Matches dieser Art'] = round(Time.loc[i,'Time per index+1'],3)
                    Summarydataframe.loc[i,'Prozentsatz'] = round((Time.loc[i,'Time per index+1']/CompleteSum[i])*100,3)
                
                timeOfMatches = round(sum(OriginalDataframe['DauerMatch']),3)
                timeOfMatchesRounded = round(timeOfMatches,3)
                Summarydataframe.loc[3,'Gesamtdauer aller Matches dieser Art'] = timeOfMatchesRounded
                
                prozentsatz = (timeOfMatches/IntervalSum)*100
                prozentsatz = round(prozentsatz,3)
                Summarydataframe.loc[3,'Prozentsatz'] = prozentsatz
                
                Summarydataframe.loc[3,'Gesamtanzahl Matches dieser Art'] = len(OriginalDataframe)
            return Summarydataframe
                    


        # In[157]:

        ### 
        ### Erstellt eine neue summary table mit Namen und Zeiten dieser Phase
        ###

        def fillSummaryTable(T2orT3, Typ):
            if(T2orT3 =='T2'):
                summary = pd.DataFrame({'Name':[0,0,0,0],
                    'Gesamtanzahl Matches dieser Art': [0,0,0,0],
                    'Gesamtdauer aller Matches dieser Art':[0,0,0,0],
                    'Gesamtdauer dieser Phase':Still_t2_K_sums.round(decimals = 3),
                    'Prozentsatz':[0,0,0,0]})
            if(T2orT3 =='T3'):
                summary = pd.DataFrame({'Name':[0,0,0,0],
                    'Gesamtanzahl Matches dieser Art': [0,0,0,0],
                    'Gesamtdauer aller Matches dieser Art':[0,0,0,0],
                    'Gesamtdauer dieser Phase':Still_t3_K_sums.round(decimals = 3),
                    'Prozentsatz':[0,0,0,0]})
            for i in range(0,4):
                if (i == 3):
                    summary.loc[i,'Name'] = T2orT3+'matches '+Typ+' Gesamt'
                else:
                    summary.loc[i,'Name'] = T2orT3 +'matches '+Typ+' Phase'+str(i+1)
            return summary



        # In[158]:
        if(not(T1empty)):
            ### Summary Table aufsetzten  T1 Positiv  DAS WIRD NUN T2
            summaryT1Pos = fillSummaryTable('T2','Positiv')
            summaryT1Pos = fillingMatchvalues(summaryT1Pos,ResultT1matchesPositiv, 'T1 CC Code',IntervalSumT1,T1CompleteSum)

            ### Summary Table aufsetzten  T1 Objekt
            summaryT1Objekt = fillSummaryTable('T2','Objekt')
            summaryT1Objekt = fillingMatchvalues(summaryT1Objekt,ResultT1matchesObjekt, 'T1 CC Code',IntervalSumT1,T1CompleteSum)

            ### Summary Table aufsetzten  T1 Negativ
            summaryT1Neg = fillSummaryTable('T2','Negativ')
            summaryT1Neg = fillingMatchvalues(summaryT1Neg,ResultT1matchesNegativ, 'T1 CC Code',IntervalSumT1,T1CompleteSum)

            ### Summary Table aufsetzten  T1 KompCPVC
            summaryT1KompCPVC = fillSummaryTable('T2','KompCPVC')
            summaryT1KompCPVC = fillingMatchvalues(summaryT1KompCPVC,ResultT1matchesKompCPVC, 'T1 CC Code',IntervalSumT1,T1CompleteSum)

            ### Summary Table aufsetzten  T1 ResultT1matchesKompCNON
            summaryT1KompCNON = fillSummaryTable('T2','KompCNON')
            summaryT1KompCNON = fillingMatchvalues(summaryT1KompCNON,ResultT1matchesKompCNON, 'T1 CC Code',IntervalSumT1,T1CompleteSum)

            #alle Zusammenfassen
            T1Frames = [summaryT1Pos,summaryT1Objekt,summaryT1Neg,summaryT1KompCPVC,summaryT1KompCNON]
            summaryT1 = pd.concat(T1Frames,ignore_index=True)
            #summaryT1


        # In[159]:

        ### Summary Table aufsetzten  T2 Positiv  DAS WIRD NUN T3
        if(not(T2empty)):
            summaryT2Pos = fillSummaryTable('T3','Positiv')
            summaryT2Pos = fillingMatchvalues(summaryT2Pos,ResultT2matchesPositiv, 'T2 CC Code',IntervalSumT2,T2CompleteSum)

            ### Summary Table aufsetzten  T2 Objekt
            summaryT2Objekt = fillSummaryTable('T3', 'Objekt')
            summaryT2Objekt = fillingMatchvalues(summaryT2Objekt,ResultT2matchesObjekt, 'T2 CC Code',IntervalSumT2,T2CompleteSum)

            ### Summary Table aufsetzten  T2 Negativ
            summaryT2Neg = fillSummaryTable('T3','Negativ')
            summaryT2Neg = fillingMatchvalues(summaryT2Neg,ResultT2matchesNegativ, 'T2 CC Code',IntervalSumT2,T2CompleteSum)

            ### Summary Table aufsetzten  T2 KompCPVC
            summaryT2KompCPVC = fillSummaryTable('T3', 'KompCPVC')
            summaryT2KompCPVC = fillingMatchvalues(summaryT2KompCPVC,ResultT2matchesKompCPVC, 'T2 CC Code',IntervalSumT2,T2CompleteSum)

            ### Summary Table aufsetzten  T2 ResultT1matchesKompCNON
            summaryT2KompCNON = fillSummaryTable('T3', 'KompCNON')
            summaryT2KompCNON = fillingMatchvalues(summaryT2KompCNON,ResultT2matchesKompCNON, 'T2 CC Code',IntervalSumT2,T2CompleteSum)

            T2Frames = [summaryT2Pos,summaryT2Objekt,summaryT2Neg,summaryT2KompCPVC,summaryT2KompCNON]
            summaryT2 = pd.concat(T2Frames, ignore_index=True)
            #summaryT2


        # In[160]:
        if(not(T1empty) and not(T2empty)): 
            summary = pd.DataFrame({'Name':[0,0,0,0,0,0,0,0,0,0], 'Gesamtanzahl Matches dieser Art': [0,0,0,0,0,0,0,0,0,0],'Gesamtdauer aller Matches dieser Art':[0,0,0,0,0,0,0,0,0,0],'Gesamtdauer dieser T':[IntervalSumT1,IntervalSumT1,IntervalSumT1,IntervalSumT1,IntervalSumT1,IntervalSumT2,IntervalSumT2,IntervalSumT2,IntervalSumT2,IntervalSumT2],'Prozentsatz':[0,0,0,0,0,0,0,0,0,0]})

            summary.loc[0,'Name'] = 'ResultT2matchesPositiv'
            summary.loc[1,'Name'] = 'ResultT2matchesObjekt'
            summary.loc[2,'Name'] = 'ResultT2matchesNegativ'
            summary.loc[3,'Name'] = 'ResultT2matchesKompCPVC'
            summary.loc[4,'Name'] = 'ResultT2matchesKompCNON'
            summary.loc[5,'Name'] = 'ResultT3matchesPositiv'
            summary.loc[6,'Name'] = 'ResultT3matchesObjekt'
            summary.loc[7,'Name'] = 'ResultT3matchesNegativ'
            summary.loc[8,'Name'] = 'ResultT3matchesKompCPVC'
            summary.loc[9,'Name'] = 'ResultT3matchesKompCNON'


            summary.loc[0,'Gesamtanzahl Matches dieser Art'] = len(ResultT1matchesPositiv)
            summary.loc[1,'Gesamtanzahl Matches dieser Art'] = len(ResultT1matchesObjekt)
            summary.loc[2,'Gesamtanzahl Matches dieser Art'] = len(ResultT1matchesNegativ)
            summary.loc[3,'Gesamtanzahl Matches dieser Art'] = len(ResultT1matchesKompCPVC)
            summary.loc[4,'Gesamtanzahl Matches dieser Art'] = len(ResultT1matchesKompCNON)
            summary.loc[5,'Gesamtanzahl Matches dieser Art'] = len(ResultT2matchesPositiv)
            summary.loc[6,'Gesamtanzahl Matches dieser Art'] = len(ResultT2matchesObjekt)
            summary.loc[7,'Gesamtanzahl Matches dieser Art'] = len(ResultT2matchesNegativ)
            summary.loc[8,'Gesamtanzahl Matches dieser Art'] = len(ResultT2matchesKompCPVC)
            summary.loc[9,'Gesamtanzahl Matches dieser Art'] = len(ResultT2matchesKompCNON)

            ###
            ### jetzt müssen != empytest beginnen
            ###

            ###t1
            if(not(ResultT1matchesPositiv.empty)):
                timeOfMatches = round(sum(ResultT1matchesPositiv['DauerMatch']),3)
                timeOfMatchesRounded = round(timeOfMatches,3)
                summary.loc[0,'Gesamtdauer aller Matches dieser Art'] = timeOfMatchesRounded
                prozentsatz = (timeOfMatches/IntervalSumT1)*100
                prozentsatz = round(prozentsatz,3)
                summary.loc[0,'Prozentsatz'] = prozentsatz
            if(not(ResultT1matchesObjekt.empty)):
                timeOfMatches = round(sum(ResultT1matchesObjekt['DauerMatch']),3)
                timeOfMatchesRounded = round(timeOfMatches,3)
                summary.loc[1,'Gesamtdauer aller Matches dieser Art'] = timeOfMatchesRounded
                prozentsatz = (timeOfMatches/IntervalSumT1)*100
                prozentsatz = round(prozentsatz,3)
                summary.loc[1,'Prozentsatz'] = prozentsatz
            if(not(ResultT1matchesNegativ.empty)):    
                timeOfMatches = round(sum(ResultT1matchesNegativ['DauerMatch']),3)
                timeOfMatchesRounded = round(timeOfMatches,3)
                summary.loc[2,'Gesamtdauer aller Matches dieser Art'] = timeOfMatchesRounded
                prozentsatz = (timeOfMatches/IntervalSumT1)*100
                prozentsatz = round(prozentsatz,3)
                summary.loc[2,'Prozentsatz'] = prozentsatz
            if(not(ResultT1matchesKompCPVC.empty)):
                timeOfMatches = round(sum(ResultT1matchesKompCPVC['DauerMatch']),3)
                timeOfMatchesRounded = round(timeOfMatches,3)
                summary.loc[3,'Gesamtdauer aller Matches dieser Art'] = timeOfMatchesRounded
                prozentsatz = (timeOfMatches/IntervalSumT1)*100
                prozentsatz = round(prozentsatz,3)
                summary.loc[3,'Prozentsatz'] = prozentsatz
            if(not(ResultT1matchesKompCNON.empty)):
                timeOfMatches = round(sum(ResultT1matchesKompCNON['DauerMatch']),3)
                timeOfMatchesRounded = round(timeOfMatches,3)
                summary.loc[4,'Gesamtdauer aller Matches dieser Art'] = timeOfMatchesRounded
                prozentsatz = (timeOfMatches/IntervalSumT1)*100
                prozentsatz = round(prozentsatz,3)
                summary.loc[4,'Prozentsatz'] = prozentsatz    



            ###t2
            if(not(ResultT2matchesPositiv.empty)):
                timeOfMatches = round(sum(ResultT2matchesPositiv['DauerMatch']),3)
                timeOfMatchesRounded = round(timeOfMatches,3)
                summary.loc[5,'Gesamtdauer aller Matches dieser Art'] = timeOfMatchesRounded
                prozentsatz = (timeOfMatches/IntervalSumT2)*100
                prozentsatz = round(prozentsatz,3)
                summary.loc[5,'Prozentsatz'] = prozentsatz
            if(not(ResultT2matchesObjekt.empty)):
                timeOfMatches = round(sum(ResultT2matchesObjekt['DauerMatch']),3)
                timeOfMatchesRounded = round(timeOfMatches,3)
                summary.loc[6,'Gesamtdauer aller Matches dieser Art'] = timeOfMatchesRounded
                prozentsatz = (timeOfMatches/IntervalSumT2)*100
                prozentsatz = round(prozentsatz,3)
                summary.loc[6,'Prozentsatz'] = prozentsatz
            if(not(ResultT2matchesNegativ.empty)):    
                timeOfMatches = round(sum(ResultT2matchesNegativ['DauerMatch']),3)
                timeOfMatchesRounded = round(timeOfMatches,3)
                summary.loc[7,'Gesamtdauer aller Matches dieser Art'] = timeOfMatchesRounded
                prozentsatz = (timeOfMatches/IntervalSumT2)*100
                prozentsatz = round(prozentsatz,3)
                summary.loc[7,'Prozentsatz'] = prozentsatz
            if(not(ResultT2matchesKompCPVC.empty)):
                timeOfMatches = round(sum(ResultT2matchesKompCPVC['DauerMatch']),3)
                timeOfMatchesRounded = round(timeOfMatches,3)
                summary.loc[8,'Gesamtdauer aller Matches dieser Art'] = timeOfMatchesRounded
                prozentsatz = (timeOfMatches/IntervalSumT2)*100
                prozentsatz = round(prozentsatz,3)
                summary.loc[8,'Prozentsatz'] = prozentsatz
            if(not(ResultT2matchesKompCNON.empty)):
                timeOfMatches = round(sum(ResultT2matchesKompCNON['DauerMatch']),3)
                timeOfMatchesRounded = round(timeOfMatches,3)
                summary.loc[9,'Gesamtdauer aller Matches dieser Art'] = timeOfMatchesRounded
                prozentsatz = (timeOfMatches/IntervalSumT2)*100
                prozentsatz = round(prozentsatz,3)
                summary.loc[9,'Prozentsatz'] = prozentsatz

            #summary




        ### Take all Matches T1
        if(not(T1empty)):
            if(Reck == True):
                framesT1 = [ResultT1matchesPositiv, ResultT1matchesObjekt,ResultT1matchesNegativ]
            if(Expl == True):
                framesT1 = [ResultT1matchesPositiv, ResultT1matchesObjekt,ResultT1matchesNegativ,ResultT1matchesKompCPVC,ResultT1matchesKompCNON]
            AllMatchesT1 = pd.concat(framesT1, ignore_index=True)
            if(AllMatchesT1.empty):            
                AllMatchesT1 = pd.DataFrame()            
            else:
                AllMatchesT1 = AllMatchesT1.sort_values('T1 CC Begin Code')
        if(T1empty):
            AllMatchesT1 = pd.DataFrame()
        ### Take all Matches T2 (aka T3)
        if(not(T2empty)):
            if(Reck == True):
                framesT2 = [ResultT2matchesPositiv, ResultT2matchesObjekt,ResultT2matchesNegativ]
            if(Expl == True):
                framesT2 = [ResultT2matchesPositiv, ResultT2matchesObjekt,ResultT2matchesNegativ,ResultT2matchesKompCPVC,ResultT2matchesKompCNON]
            AllMatchesT2 = pd.concat(framesT2, ignore_index=True)
            if(AllMatchesT2.empty):
                print('keine T2/T3 matches')
            AllMatchesT2 = AllMatchesT2.sort_values('T2 CC Begin Code')



        ### Start und Ende Zeit zu allen Matches hinzufügen
        def startCodeEndeCode(dataframe):
            if(not(dataframe.empty)):
                for index, row in dataframe.iterrows():
                    CCBeginCode  = row.ix[0]
                    CCEndeCode   = row.ix[1]
                    CCDauerCode  = row.ix[2]
                    CCCode       = row.ix[3]

                    IBeginCode   = row.ix[4]
                    IEndeCode    = row.ix[5]
                    IDauerCode   = row.ix[6]
                    ICode        = row.ix[7]

                    DauerMatch = row.ix[8]

            #        if(DauerMatch < 0):
            #            dataframe.loc[index,'Start Code'] = 0
            #            dataframe.loc[index,'Ende Code'] = 0
            #        else:
                    ### 
                    ### CC im I Code
                    ###
                    if(CCBeginCode >= IBeginCode and CCEndeCode <= IEndeCode):
                        dataframe.loc[index,'Start Code'] = CCBeginCode
                        dataframe.loc[index,'Ende Code'] = CCEndeCode  
                    ###
                    ### Wenn I Intervall in CC Intervall
                    ###
                    if(CCBeginCode <= IBeginCode and CCEndeCode >= IEndeCode):           
                        dataframe.loc[index,'Start Code'] = IBeginCode
                        dataframe.loc[index,'Ende Code'] = IEndeCode  
                    ###
                    ### Die logischen Reste
                    ###
                    if(CCBeginCode < IBeginCode and CCEndeCode < IEndeCode):
                        dataframe.loc[index,'Start Code'] = IBeginCode
                        dataframe.loc[index,'Ende Code'] = CCEndeCode  
                    ###
                    ### Logischer Rest teil2
                    ###
                    if(CCBeginCode > IBeginCode and CCEndeCode > IEndeCode):  
                        dataframe.loc[index,'Start Code'] = CCBeginCode
                        dataframe.loc[index,'Ende Code'] = IEndeCode        

            #dataframe = dataframe.sort_values(['Start Code','Ende Code'])
            return dataframe
            #        if(CCBeginCode >= IBeginCode):
            #            if((CCBeginCode-1) <0):
            #                dataframe.loc[index,'Start Code'] = 0
            #            else:
            #                dataframe.loc[index,'Start Code'] = round(CCBeginCode-1,3)

            #        if(IBeginCode >= CCBeginCode):
            #            if((IBeginCode-1) <0):
            #                dataframe.loc[index,'Start Code'] = 0
            #            else:
            #                dataframe.loc[index,'Start Code'] = round(IBeginCode-1,3)


                    ### Der der früher aufhört Ende +1
                    ###
                    ### 

            #        if(CCEndeCode >= IEndeCode):
            #            dataframe.loc[index,'Ende Code'] = IEndeCode+1  

            #        if(IEndeCode >= CCEndeCode):
            #            dataframe.loc[index,'Ende Code'] = CCEndeCode+1        

        if(not(T1empty)):
            AllMatchesT1 = startCodeEndeCode(AllMatchesT1)
        if(not(T2empty)):
            AllMatchesT2 = startCodeEndeCode(AllMatchesT2)

        ###
        ### Alle Matches Nochmal in die Phasen Teilen
        ### 
        def PhasesTeilen(dataframe, strCode):
            dataframe = dataframe.sort_values('Start Code')
            dataframe = dataframe.reset_index(drop = True)
            Phase1 = dataframe[dataframe[strCode].str.contains('1')]
            Phase2 = dataframe[dataframe[strCode].str.contains('2')]
            Phase3 = dataframe[dataframe[strCode].str.contains('3')]
            return(Phase1, Phase2, Phase3,dataframe)

        ### Get First match von jeder Phase in T1

        def getFirstMatches(Tempty, AllMatchesT,TCode):
            if(not(Tempty) and not(AllMatchesT.empty)):
                MatchesPhase1, MatchesPhase2, MatchesPhase3, AllMatchesT = PhasesTeilen(AllMatchesT,TCode)
                if(MatchesPhase1.empty):
                    MatchesPhase1FirstMatch = pd.DataFrame()
                    MatchesPhase2FirstMatch = MatchesPhase2.head(1)
                    MatchesPhase3FirstMatch = MatchesPhase3.head(1)
                if(MatchesPhase2.empty):
                    MatchesPhase1FirstMatch = MatchesPhase1.head(1)
                    MatchesPhase2FirstMatch = pd.DataFrame()
                    MatchesPhase3FirstMatch = MatchesPhase3.head(1)
                if(MatchesPhase3.empty):
                    MatchesPhase1FirstMatch = MatchesPhase1.head(1)
                    MatchesPhase2FirstMatch = MatchesPhase2.head(1)
                    MatchesPhase3FirstMatch= pd.DataFrame()
                else:
                    MatchesPhase1FirstMatch = MatchesPhase1.head(1)
                    MatchesPhase2FirstMatch = MatchesPhase2.head(1)
                    MatchesPhase3FirstMatch = MatchesPhase3.head(1)
                return(MatchesPhase1, MatchesPhase1FirstMatch, MatchesPhase2, MatchesPhase2FirstMatch,MatchesPhase3, MatchesPhase3FirstMatch, AllMatchesT)
            else:
                return(pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame())
        
        MatchesT1Phase1,MatchesT1Phase1FirstMatch,MatchesT1Phase2,MatchesT1Phase2FirstMatch,MatchesT1Phase3,MatchesT1Phase3FirstMatch,AllMatchesT1 = getFirstMatches(T1empty, AllMatchesT1, 'T1 CC Code')
        MatchesT2Phase1,MatchesT2Phase1FirstMatch,MatchesT2Phase2,MatchesT2Phase2FirstMatch,MatchesT2Phase3,MatchesT2Phase3FirstMatch,AllMatchesT2 = getFirstMatches(T2empty, AllMatchesT2,'T2 CC Code')

        if(False):        
            if(not(T1empty) and not(AllMatchesT1.empty)):
                MatchesT1Phase1, MatchesT1Phase2, MatchesT1Phase3,AllMatchesT1 = PhasesTeilen(AllMatchesT1,'T1 CC Code')
                if(MatchesT1Phase1.empty):            
                    #print('MatchesT1Phase1 empty')
                    MatchesT1Phase1FirstMatch = pd.DataFrame()
                    MatchesT1Phase2FirstMatch = MatchesT1Phase2.head(1)
                    MatchesT1Phase3FirstMatch = MatchesT1Phase3.head(1)
                    #continue
                if(MatchesT1Phase2.empty):
                    #print('MatchesT1Phase2 empty')
                    MatchesT1Phase1FirstMatch = MatchesT1Phase1.head(1)
                    MatchesT1Phase2FirstMatch = pd.DataFrame()
                    MatchesT1Phase3FirstMatch = MatchesT1Phase3.head(1)
                    #continue
                if(MatchesT1Phase3.empty):        
                    #print('MatchesT1Phase3 empty')
                    MatchesT1Phase1FirstMatch = MatchesT1Phase1.head(1)
                    MatchesT1Phase2FirstMatch = MatchesT1Phase2.head(1)
                    MatchesT1Phase3FirstMatch = pd.DataFrame()
                    #continue
                else:
                    MatchesT1Phase1FirstMatch = MatchesT1Phase1.head(1)
                    MatchesT1Phase2FirstMatch = MatchesT1Phase2.head(1)
                    MatchesT1Phase3FirstMatch = MatchesT1Phase3.head(1)

            ### Get First Macht von jeder Phase in T2
            if(not(T2empty) and not(AllMatchesT2.empty)):
                MatchesT2Phase1, MatchesT2Phase2, MatchesT2Phase3,AllMatchesT2 = PhasesTeilen(AllMatchesT2,'T2 CC Code')
                if(MatchesT2Phase1.empty):            
                    MatchesT2Phase1FirstMatch = pd.DataFrame()
                    MatchesT2Phase2FirstMatch = MatchesT2Phase2.head(1)
                    MatchesT2Phase3FirstMatch = MatchesT2Phase3.head(1)
                if(MatchesT2Phase2.empty):
                    MatchesT2Phase1FirstMatch = MatchesT2Phase1.head(1)
                    MatchesT2Phase2FirstMatch = pd.DataFrame()
                    MatchesT2Phase3FirstMatch = MatchesT2Phase3.head(1)
                if(MatchesT2Phase3.empty):        
                    MatchesT2Phase1FirstMatch = MatchesT2Phase1.head(1)
                    MatchesT2Phase2FirstMatch = MatchesT2Phase2.head(1)
                    MatchesT2Phase3FirstMatch = pd.DataFrame()
                else:
                    MatchesT2Phase1FirstMatch = MatchesT2Phase1.head(1)
                    MatchesT2Phase2FirstMatch = MatchesT2Phase2.head(1)
                    MatchesT2Phase3FirstMatch = MatchesT2Phase3.head(1)


        

        ### Klopfen von T1/ T2 in tabelle (nur ersten 3 benötigt)
        if(not(T1empty)):
            KlopfenT1 = T1[T1['T1 C3 Code'] == 'klopfen'].head(3)
            TransT1 = T1[T1['T1 C3 Code'] == 'trans'].head(1)

        ### Trans von T1/ T2 für die Phase 2 benötigt
        if(not(T2empty)):    
            TransT2 = T2[T2['T2 C3 Code'] == 'trans'].head(1)
            KlopfenT2 = T2[T2['T2 C3 Code'] == 'klopfen'].head(3)

        ### 
        ### LatenzHinzufügen von den Matches Def: Ende Klopfen (für Phase1 und 3) oder ENde Trans für Phase2
        ###
        def LatenzHinzufugen(klopfenDF, FirstMatchDF,klopfenString,KlopfenInt):
            KlopfenEnde = klopfenDF[klopfenString].iloc[KlopfenInt]
            CodeAnfang = FirstMatchDF['Start Code'].iloc[0]
            Latenz = CodeAnfang - KlopfenEnde
            if(Latenz < 0):
                Latenz = 0
            FirstMatchDF.insert(0,'Latenz',round(Latenz,3))

        if(not(T1empty) and not(AllMatchesT1.empty)):
            if(not(MatchesT1Phase1.empty)):
                LatenzHinzufugen(KlopfenT1, MatchesT1Phase1FirstMatch,'T1 C1 Ende Code',0)
            if(not(MatchesT1Phase2.empty)):
                LatenzHinzufugen(TransT1, MatchesT1Phase2FirstMatch,'T1 C1 Ende Code',0)
            if(not(MatchesT1Phase3.empty)):
                LatenzHinzufugen(KlopfenT1, MatchesT1Phase3FirstMatch,'T1 C1 Ende Code',2)
                
        if(not(T2empty) and not (AllMatchesT2.empty)):
            if(not(MatchesT2Phase1.empty)):
                LatenzHinzufugen(KlopfenT2, MatchesT2Phase1FirstMatch,'T2 C1 Ende Code',0)
            if(not(MatchesT2Phase2.empty)):
                LatenzHinzufugen(TransT2, MatchesT2Phase2FirstMatch,'T2 C1 Ende Code',0)
            if(not(MatchesT2Phase3.empty)):
                LatenzHinzufugen(KlopfenT2, MatchesT2Phase3FirstMatch,'T2 C1 Ende Code',2)

        ###
        ### Tabellenspalten Umnennen in das T2 T3 Ziel und reindexen
        ###
        def renameTabelleT2(dataframe):
            result = dataframe.rename(columns ={'T2 CC Begin Code':'T3 CC Begin Code', 'T2 CC Ende Code':'T3 CC Ende Code', 
                                                'T2 CC Dauer Code':'T3 CC Dauer Code', 'T2 CC Code':'T3 CC Code', 
                                                'T2 I Begin Code': 'T3 I Begin Code', 'T2 I Ende Code':'T3 I Ende Code',
                                               'T2 I Dauer Code':'T3 I Dauer Code', 'T2 I Code':'T3 I Code',
                                               })
            result = result.reset_index(drop = True)
            return result

        def renameTabelleT1(dataframe):
            result = dataframe.rename(columns ={'T1 CC Begin Code':'T2 CC Begin Code', 'T1 CC Ende Code':'T2 CC Ende Code', 
                                                'T1 CC Dauer Code':'T2 CC Dauer Code', 'T1 CC Code':'T2 CC Code', 
                                                'T1 I Begin Code': 'T2 I Begin Code', 'T1 I Ende Code':'T2 I Ende Code',
                                               'T1 I Dauer Code':'T2 I Dauer Code', 'T1 I Code':'T2 I Code',
                                               })
            result = result.reset_index(drop = True)
            return result


        # In[170]:

        ###
        ### Renaming the cols
        ###
        if(not(T1empty) and not(AllMatchesT1.empty)):
            if(not(MatchesT1Phase1.empty)):
                MatchesT1Phase1FirstMatch = renameTabelleT1(MatchesT1Phase1FirstMatch)
            if(not(MatchesT1Phase2.empty)):
                MatchesT1Phase2FirstMatch = renameTabelleT1(MatchesT1Phase2FirstMatch)
            if(not(MatchesT1Phase3.empty)):
                MatchesT1Phase3FirstMatch = renameTabelleT1(MatchesT1Phase3FirstMatch)
            FirstMatchesT1 = [MatchesT1Phase1FirstMatch,MatchesT1Phase2FirstMatch,MatchesT1Phase3FirstMatch]
            FirstMatchesT1 = pd.concat(FirstMatchesT1, ignore_index=True)
        else: 
            FirstMatchesT1 = pd.DataFrame()

            
        if(not(T2empty) and not(AllMatchesT2.empty)):
            if(not(MatchesT2Phase1.empty)):
                MatchesT2Phase1FirstMatch = renameTabelleT2(MatchesT2Phase1FirstMatch)
            if(not(MatchesT2Phase2.empty)):
                MatchesT2Phase2FirstMatch = renameTabelleT2(MatchesT2Phase2FirstMatch)
            if(not(MatchesT2Phase3.empty)):
                MatchesT2Phase3FirstMatch = renameTabelleT2(MatchesT2Phase3FirstMatch)
            FirstMatchesT2 = [MatchesT2Phase1FirstMatch,MatchesT2Phase2FirstMatch,MatchesT2Phase3FirstMatch]
            FirstMatchesT2 = pd.concat(FirstMatchesT2, ignore_index=True)
        else: 
            FirstMatchesT2 = pd.DataFrame()


        ###
        ### Zeit zwischen Matches rausfinden
        ###
        def insertRepairTime(dataframe,FirstMatchesDF, FirstMatchesInt):
            dataframe = dataframe.sort_values('Start Code')
            dataframe = dataframe.reset_index(drop = True)
            for index, row in dataframe.iterrows():
                if (index == 0):
                    dataframe.insert(0,'Latenz',(round(FirstMatchesDF.loc[FirstMatchesInt,'Latenz'],3)))
                else:
                    dataframe.loc[index,'Latenz'] =   round(dataframe.loc[index,'Start Code'] - dataframe.loc[index-1,'Ende Code'],3)
            return dataframe    

        def fillIntoInsertRepairTime(Tempty, AllMatches, FirstMatchesT, MatchesPhase1, MatchesPhase2, MatchesPhase3):
            if(not(Tempty) and not(AllMatches.empty)):
                if(not(MatchesPhase1.empty)):
                    MatchesPhase1 = insertRepairTime(MatchesPhase1, FirstMatchesT, 0)
                if(not(MatchesPhase2.empty)):
                    MatchesPhase2 = insertRepairTime(MatchesPhase2, FirstMatchesT, 1)
                if(not(MatchesPhase3.empty)):
                    if(MatchesPhase2.empty):
                        MatchesPhase3 = insertRepairTime(MatchesPhase3, FirstMatchesT,1)
                    else:
                        MatchesPhase3 = insertRepairTime(MatchesPhase3, FirstMatchesT,2)
            return(MatchesPhase1, MatchesPhase2, MatchesPhase3)

        MatchesT1Phase1, MatchesT1Phase2, MatchesT1Phase3 = fillIntoInsertRepairTime(T1empty, AllMatchesT1, FirstMatchesT1, MatchesT1Phase1, MatchesT1Phase2, MatchesT1Phase3)
        MatchesT2Phase1, MatchesT2Phase2, MatchesT2Phase3 = fillIntoInsertRepairTime(T2empty, AllMatchesT2, FirstMatchesT2, MatchesT2Phase1, MatchesT2Phase2, MatchesT2Phase3)

     
        ### Erstellt den Rahmen für die Latency Table
        def fillLatencyTable(T2orT3):
            if(T2orT3 =='T2'):
                summary = pd.DataFrame({
                            'Reperation Rate': [0,0,0,0],
                            'Interactive Repair Rate':[0,0,0,0],
                            'Gesamtdauer dieser Phase':Still_t2_K_sums.round(decimals = 3)})
            if(T2orT3 =='T3'):
                summary = pd.DataFrame({
                            'Reperation Rate': [0,0,0,0],
                            'Interactive Repair Rate':[0,0,0,0],
                            'Gesamtdauer dieser Phase':Still_t3_K_sums.round(decimals = 3)})
            return summary

        ### Füllt Werte (Interactive Repair und Reperation Rate) in die Latency Table
        def insertLatencyTable(Tempty, AllMatchesT, T2orT3, MatchesPhase1, MatchesPhase2, MatchesPhase3, Still_sums):
            if(not(Tempty) and not(AllMatchesT.empty)):
                LatencyTable = fillLatencyTable(T2orT3)
                MatchesPhase =[MatchesPhase1, MatchesPhase2, MatchesPhase3]
                for i in range(0,len(MatchesPhase)):
                    if(not(MatchesPhase[i].empty)):
                        LatencyTable.loc[i, 'Interactive Repair Rate'] = (MatchesPhase[i]['Latenz'].sum())/Still_sums[i]
                        LatencyTable.loc[i, 'Reperation Rate'] = (len(MatchesPhase[i].loc[MatchesPhase[i]['Latenz']>0]))/Still_sums[i]
                AllMatchesWithLatency = pd.concat(MatchesPhase)
                if(not(AllMatchesWithLatency.empty)):
                    LatencyTable.loc[3,'Interactive Repair Rate'] = (AllMatchesWithLatency['Latenz'].sum())/Still_sums[3]
                    LatencyTable.loc[3, 'Reperation Rate'] = (len(AllMatchesWithLatency.loc[AllMatchesWithLatency['Latenz']>0]))/Still_sums[3]
            ### Wenn T leer ist oder keine Matches in der T existieren
            else:
                LatencyTable = pd.DataFrame()
                AllMatchesWithLatency = pd.DataFrame()
            return(LatencyTable, AllMatchesWithLatency)


        LatencyT2, AllMatchesT2WithLatency = insertLatencyTable(T1empty, AllMatchesT1, 'T2', MatchesT1Phase1, MatchesT1Phase2, MatchesT1Phase3, Still_t2_K_sums)
        LatencyT3, AllMatchesT3WithLatency = insertLatencyTable(T2empty, AllMatchesT2, 'T3', MatchesT2Phase1, MatchesT2Phase2, MatchesT2Phase3, Still_t3_K_sums)

                    
        ###
        ###   Wird von fill OutputTable Aufgerufen
        ### 
        def fillOutputTableHelper(df_Output,summaryT, Phase,T2OrT3, Still_sums, LatencyT, MatchesTPhaseXFirstMatch):
            VariablenAnfang = ['_Match_pos_s_ms','_Match_object_s_ms','_Match_Negativ_s_ms','_Match_Komp_M_Cpvc_s_ms','_Match_Komp_K_ipos_s_ms']
            AllCols = ['Match_t2','Match_t3']
            Begriffe = ['Positiv ', 'Objekt ','Negativ ','KompCPVC ','KompCNON ']
            
            PhaseWithNum = 'Phase'+Phase
            Summe = 0
            for i in range(0,len(VariablenAnfang)):
                VariablenAnfang[i] = Phase + VariablenAnfang[i]

            if(T2OrT3 == 'T2'):
                AllColsValue = AllCols[0]
            if(T2OrT3 == 'T3'):
                AllColsValue = AllCols[1]            
            if(Reck == True):
                PropMatRate = AllColsValue+'_'+Phase+'_'+ReckOrExpl[0]+'proportion_matching_states_percentage'
                RepeRate = AllColsValue+'_'+Phase+'_'+ReckOrExpl[0]+'reperation_rate_frequency'
                InterReLa = AllColsValue+'_'+Phase+'_'+ReckOrExpl[0]+'Interactive_Repair_Latency_mean'
                FirstMaLa =  AllColsValue+'_'+Phase+'_'+ReckOrExpl[0]+'First_Match_Latency_sec'
            if(Expl == True):
                PropMatRate = AllColsValue+'_'+Phase+'_'+ReckOrExpl[1]+'proportion_matching_states_percentage'
                RepeRate = AllColsValue+'_'+Phase+'_'+ReckOrExpl[1]+'reperation_rate_frequency'
                InterReLa = AllColsValue+'_'+Phase+'_'+ReckOrExpl[1]+'Interactive_Repair_Latency_mean'
                FirstMaLa =  AllColsValue+'_'+Phase+'_'+ReckOrExpl[1]+'First_Match_Latency_sec'
            #PropMatRate = AllColsValue+'_'+Phase+'_proportion_matching_states_percentage'
            for i in range(0,len(VariablenAnfang)):
                VariablenAnfang[i] = AllColsValue +'_'+ VariablenAnfang[i]
            for i in range(0,len(VariablenAnfang)):
                df_Output.loc[name,VariablenAnfang[i]] = summaryT.loc[summaryT['Name'].str.contains(Begriffe[i]+PhaseWithNum),'Gesamtdauer aller Matches dieser Art'].iloc[0] 
                if(Reck == True):
                    if(i == 0 or i == 1 or i == 2):
                        Summe = Summe + summaryT.loc[summaryT['Name'].str.contains(Begriffe[i]+PhaseWithNum),'Gesamtdauer aller Matches dieser Art'].iloc[0] 
                if(Expl == True):
                    Summe = Summe + summaryT.loc[summaryT['Name'].str.contains(Begriffe[i]+PhaseWithNum),'Gesamtdauer aller Matches dieser Art'].iloc[0] 
            PhaseAsInt = int(Phase)
            df_Output.loc[name,PropMatRate] = (Summe/Still_sums[PhaseAsInt-1])*100

            ### TODO reperation_rate einfügen
            phaseAsInt = int(Phase)
            df_Output.loc[name,RepeRate] = LatencyT.loc[phaseAsInt-1,'Reperation Rate']
            ### TODO Interactive Repair Rate einfügen
            df_Output.loc[name,InterReLa] = LatencyT.loc[phaseAsInt-1,'Interactive Repair Rate']
            ### TODO Latency Fist Match einfügen
            LatenzWert = MatchesTPhaseXFirstMatch.loc[0,'Latenz']
            if(LatenzWert >= 120):
                df_Output.loc[name, FirstMaLa] = 120
            else:
                df_Output.loc[name, FirstMaLa] = MatchesTPhaseXFirstMatch.loc[0,'Latenz']

        ###
        ### Output Tabelle füllen hier wird die Ts und Phasen eingeteilt
        ###
        def fillOutputTable(df_Output):
            if(Expl == True):
                FirstMatchNamesT2 = ['Match_t2_1_Expl_First_Match_Latency_sec','Match_t2_2_Expl_First_Match_Latency_sec','Match_t2_3_Expl_First_Match_Latency_sec']
                FirstMatchNamesT3 = ['Match_t3_1_Expl_First_Match_Latency_sec','Match_t3_2_Expl_First_Match_Latency_sec','Match_t3_3_Expl_First_Match_Latency_sec']
            if(Reck == True):
                FirstMatchNamesT2 = ['Match_t2_1_Reck_First_Match_Latency_sec','Match_t2_2_Reck_First_Match_Latency_sec','Match_t2_3_Reck_First_Match_Latency_sec']
                FirstMatchNamesT3 = ['Match_t3_1_Reck_First_Match_Latency_sec','Match_t3_2_Reck_First_Match_Latency_sec','Match_t3_3_Reck_First_Match_Latency_sec']
            sizeCol = df_Output.shape[1]
            ### Wenn T1 leer ist 
            if(T1empty):
                ### Die erste Hälfte mit 3333 füllen
                df_Output.loc[name,0:int(sizeCol/2)] = 3333
                
            ### Wenn T1 nicht leer ist
            if(not(T1empty)):
                df_Output.loc[name,'Match_t2_1_still_K_sum_s_ms'] = Still_t2_K_sums[0]
                df_Output.loc[name,'Match_t2_2_still_K_sum_s_ms'] = Still_t2_K_sums[1]
                df_Output.loc[name,'Match_t2_3_still_K_sum_s_ms'] = Still_t2_K_sums[2]
                ### Wenn es Matches in der T1 gibt
                if(not(AllMatchesT1.empty)):

                    ### Wenn es Matches in der T1 Phase 1 gibt
                    if(not(MatchesT1Phase1.empty)):
                        fillOutputTableHelper(df_Output,summaryT1, '1','T2',Still_t2_K_sums,LatencyT2,MatchesT1Phase1FirstMatch)

                    ### Wenn es keine Matches in der T1 Phase 2 gibt    
                    if(MatchesT1Phase1.empty):
                        df_Output.loc[name,0*int(sizeCol/6):1*int(sizeCol/6)]=0
                        df_Output.loc[name,'Match_t2_1_still_K_sum_s_ms'] = Still_t2_K_sums[0]
                        df_Output.loc[name,FirstMatchNamesT2[0]] = 120
                    ### Wenn es Matches in der T1 Phase 2 gibt    
                    if(not(MatchesT1Phase2.empty)):                    
                        fillOutputTableHelper(df_Output,summaryT1, '2','T2',Still_t2_K_sums,LatencyT2,MatchesT1Phase2FirstMatch)

                    ### Wenn es keine Matches in der T1 Phase 2 gibt
                    if(MatchesT1Phase2.empty):
                        df_Output.loc[name,1*int(sizeCol/6):2*int(sizeCol/6)]=0
                        df_Output.loc[name,'Match_t2_2_still_K_sum_s_ms'] = Still_t2_K_sums[1]
                        df_Output.loc[name,FirstMatchNamesT2[1]] = 120
                    ### Matches in T1 3    
                    if(not(MatchesT1Phase3.empty)):
                        fillOutputTableHelper(df_Output,summaryT1,'3','T2',Still_t2_K_sums,LatencyT2,MatchesT1Phase3FirstMatch)

                    ### Keine Matches in T1 3
                    if(MatchesT1Phase3.empty):
                        df_Output.loc[name,2*int(sizeCol/6):3*int(sizeCol/6)]=0
                        df_Output.loc[name,'Match_t2_3_still_K_sum_s_ms'] = Still_t2_K_sums[2]
                        df_Output.loc[name,FirstMatchNamesT2[2]] = 120

                ### Keine Matches in der ganzen T1
                else:
                    print('Keine Matches in der T1/T2')
                    df_Output.loc[name,0:int(sizeCol/2)] = 0
                    df_Output.loc[name,'Match_t2_1_still_K_sum_s_ms'] = Still_t2_K_sums[0]
                    df_Output.loc[name,'Match_t2_2_still_K_sum_s_ms'] = Still_t2_K_sums[1]
                    df_Output.loc[name,'Match_t2_3_still_K_sum_s_ms'] = Still_t2_K_sums[2]

                    for i in range(0,len(FirstMatchesNamesT2)):
                        df_Output.loc[name,FirstMatchesNamesT2[i]] = 120
            ###
            ### Wenn T2 leer ist
            ###
            if(T2empty):
                df_Output.loc[name,int(sizeCol/2)::] = 3333

            ### Wenn T2 nicht leer ist     
            if(not(T2empty)):
                ### Wenn es Matches in der T2 gibt
                df_Output.loc[name,'Match_t3_1_still_K_sum_s_ms'] = Still_t3_K_sums[0]
                df_Output.loc[name,'Match_t3_2_still_K_sum_s_ms'] = Still_t3_K_sums[1]
                df_Output.loc[name,'Match_t3_3_still_K_sum_s_ms'] = Still_t3_K_sums[2]
                if(not(AllMatchesT2.empty)):

                    ### Wenn es Matches in T2 1 gibt
                    if(not(MatchesT2Phase1.empty)):
                        fillOutputTableHelper(df_Output,summaryT2, '1','T3',Still_t3_K_sums,LatencyT3,MatchesT2Phase1FirstMatch)
                    ### Wenn es keine Matches in der T2 1 gibt    
                    if(MatchesT2Phase1.empty):
                        df_Output.loc[name,3*int(sizeCol/6):4*int(sizeCol/6)]=0
                        df_Output.loc[name,'Match_t3_1_still_K_sum_s_ms'] = Still_t3_K_sums[0]
                        df_Output.loc[name,FirstMatchNamesT3[0]] = 120
                    ### Wenn es Matches in der T2 2 gibt    
                    if(not(MatchesT2Phase2.empty)):                    
                        fillOutputTableHelper(df_Output,summaryT2, '2','T3',Still_t3_K_sums,LatencyT3,MatchesT2Phase2FirstMatch)
                    ### Wenn es keine Matches in der T2 2 gibt
                    if(MatchesT2Phase2.empty):                    
                        df_Output.loc[name,4*int(sizeCol/6):5*int(sizeCol/6)]=0
                        df_Output.loc[name,'Match_t3_2_still_K_sum_s_ms'] = Still_t3_K_sums[1]
                        df_Output.loc[name,FirstMatchNamesT3[1]] = 120
                    ### Wenn es Matches in der T2 3 gibt    
                    if(not(MatchesT2Phase3.empty)):
                        fillOutputTableHelper(df_Output,summaryT2, '3','T3',Still_t3_K_sums,LatencyT3,MatchesT2Phase3FirstMatch)
                    ### Wenn es keine Matches in der T2 3 gibt
                    if(MatchesT2Phase3.empty):
                        df_Output.loc[name,5*int(sizeCol/6):6*int(sizeCol/6)]=0
                        df_Output.loc[name,'Match_t3_3_still_K_sum_s_ms'] = Still_t3_K_sums[2]
                        df_Output.loc[name,FirstMatchNamesT3[2]] = 120
                ### Keine Matches in der T2 
                else:            
                    df_Output.loc[name,int(sizeCol/2)::] = 0
                    df_Output.loc[name,'Match_t3_1_still_K_sum_s_ms'] = Still_t3_K_sums[0]
                    df_Output.loc[name,'Match_t3_2_still_K_sum_s_ms'] = Still_t3_K_sums[1]
                    df_Output.loc[name,'Match_t3_3_still_K_sum_s_ms'] = Still_t3_K_sums[2]

                    for i in range(0,len(FirstMatchesT3)):
                        df_Output.loc[name,FirstMatchesT3[i]] = 120
    

            return df_Output
        
        df_Output = fillOutputTable(df_Output)

        #def is_df_sorted(df, colname):
            #return pd.Index(df[colname]).is_monotonic
    
        #if(not(T1.empty) and not(AllMatchesT2WithLatency.empty)):
            #print(is_df_sorted(AllMatchesT2WithLatency,'Start Code'))
            #print(is_df_sorted(AllMatchesT2WithLatency,'Ende Code'))
            
        #if(not(AllMatchesT3WithLatency.empty)):
            #print(is_df_sorted(AllMatchesT3WithLatency,'Start Code'))
            #print(is_df_sorted(AllMatchesT3WithLatency,'Ende Code'))
        ### 
        ### Sachen speichern 
        ###    
        testPath = os.getcwd()    
        newpath = testPath +'\Output'
        if not os.path.exists(newpath):
            os.makedirs(newpath)


        def createCSVs():

            newpath = testPath +'\Output\Ergebnisse'+name
            if not os.path.exists(newpath):
                os.makedirs(newpath)

            printNameT1 = newpath+'/summaryT2.csv'
            printNameT2 = newpath+'/summaryT3.csv'

            if(not(T1empty)):
                summaryT1.to_csv(printNameT1, sep=';',decimal=',')
            if(not(T2empty)):
                summaryT2.to_csv(printNameT2, sep=';',decimal=',')
            #summary.to_csv('Ergebnisse/summaryof2999.csv', sep=';')
            FirstMatchesT1.to_csv(newpath+'/FirstMatchesT2.csv', sep=';',decimal=',')
            FirstMatchesT2.to_csv(newpath+'/FirstMatchesT3.csv', sep=';',decimal=',')

            LatencyT2.to_csv(newpath+'/LatencyT2.csv', sep=';',decimal=',')
            LatencyT3.to_csv(newpath+'/LatencyT3.csv', sep=';',decimal=',')

            MatchesT1Phase1FirstMatch.to_csv(newpath+'/MatchesT2Phase1FirstMatch.csv', sep=';')
            MatchesT1Phase2FirstMatch.to_csv(newpath+'/MatchesT2Phase2FirstMatch.csv', sep=';')
            MatchesT1Phase3FirstMatch.to_csv(newpath+'/MatchesT2Phase3FirstMatch.csv', sep=';')

            MatchesT2Phase1FirstMatch.to_csv(newpath+'/MatchesT3Phase1FirstMatch.csv', sep=';')
            MatchesT2Phase2FirstMatch.to_csv(newpath+'/MatchesT3Phase2FirstMatch.csv', sep=';')
            MatchesT2Phase3FirstMatch.to_csv(newpath+'/MatchesT3Phase3FirstMatch.csv', sep=';')

            MatchesT1Phase1.to_csv(newpath+'/MatchesT2Phase1.csv', sep=';',decimal=',')
            MatchesT1Phase2.to_csv(newpath+'/MatchesT2Phase2.csv', sep=';',decimal=',')
            MatchesT1Phase3.to_csv(newpath+'/MatchesT2Phase3.csv', sep=';',decimal=',')

            MatchesT2Phase1.to_csv(newpath+'/MatchesT3Phase1.csv', sep=';',decimal=',')
            MatchesT2Phase2.to_csv(newpath+'/MatchesT3Phase2.csv', sep=';',decimal=',')
            MatchesT2Phase3.to_csv(newpath+'/MatchesT3Phase3.csv', sep=';',decimal=',')
            ###
            AllMatchesT1 = renameTabelleT1(AllMatchesT2WithLatency)
            AllMatchesT2 = renameTabelleT2(AllMatchesT3WithLatency)
            AllMatchesT1.to_csv(newpath+'/T2AlleMatches.csv',sep=';',decimal=',')
            AllMatchesT2.to_csv(newpath+'/T3AlleMatches.csv',sep=';',decimal=',')

            #if((not(T1dfKindZuerstEnde.empty) or not(T1dfMutterZuerstEnde.empty))):
                #ZeitlicheMissMatchesT1 = pd.concat([T1dfMutterZuerstEnde, T1dfKindZuerstEnde])
                #ZeitlicheMissMatchesT1 = renameTabelleT1(ZeitlicheMissMatchesT1)
                #ZeitlicheMissMatchesT1.to_csv(newpath+'/T2MatchesOhneZeitlicheUeberschneidung.csv', sep =';',decimal=',')
            #if((not(T2dfKindZuerstEnde.empty) or not(T2dfMutterZuerstEnde.empty))):
                #ZeitlicheMissMatchesT2 = pd.concat([T2dfMutterZuerstEnde, T2dfKindZuerstEnde])
                #ZeitlicheMissMatchesT2 = renameTabelleT2(ZeitlicheMissMatchesT2)
                #ZeitlicheMissMatchesT2.to_csv(newpath+'/T3MatchesOhneZeitlicheUeberschneidung.csv', sep =';',decimal=',')

        createCSVs()
    def createCSVOutputFile(df_Output):
        newpathOhneErgebnisse = testPath +'\Output'
        if(Reck == True):
            printName = '/Output_Reck.csv'
        if(Expl == True):
            printName = '/Output_Expl.csv'
        with open(newpathOhneErgebnisse+printName, 'w') as f:
            df_Output.to_csv(f, index=True, header=True, sep=';',decimal =',',float_format='%g')

    createCSVOutputFile(df_Output)
    

    
def wait():
    m.getch()
input("Drücken Sie Enter um das Fenster zu schliesen...")





