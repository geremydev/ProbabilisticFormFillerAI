#pip install selenium
#pip install numpy
#pip install pandas
#pip install seaborn
#pip install bs4
#pip install urllib3
#pip install datetima
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import seaborn as sns
import time as t
import urllib3
import datetime as dt
import time 
urllib3.disable_warnings()
options = Options()
#options.add_experimental_option("detach", True)
options.add_argument('--allow-running-insecure-content')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-insecure-localhost')
options.add_argument('--disable-extensions')
options.add_argument('--log-level=3')

url = 'https://forms.office.com/Pages/ResponsePage.aspx?id=v9NWkZ3Ty0Kr9rfeykoIknOLpz0hQllGpcwMewPUh5JUNkhBWDhETUhWS1IzV1RJRlVGSUJJTUZQWS4u'

class Forms:
    def __init__(self, preguntas, respuestas):
        self.preguntasdic = {
            int(preguntas[0].text[0]): [],
            int(preguntas[1].text[0]): respuestas[0:9],
            int(preguntas[2].text[0]):respuestas[9:15],
            int(preguntas[3].text[0]):respuestas[15:25],
            int(preguntas[4].text[0]):respuestas[25:27],
            int(preguntas[5].text[0]):respuestas[27:29],
            int(preguntas[6].text[0]):respuestas[29:31],
            int(preguntas[7].text[0]):respuestas[31:36],
            int(preguntas[8].text[0]):respuestas[36:41],
            int(preguntas[9].text[0:2]):respuestas[41:46],
            int(preguntas[10].text[0:2]):respuestas[46:53],
            int(preguntas[11].text[0:2]):respuestas[53:63],
            int(preguntas[12].text[0:2]):respuestas[63:71],
            int(preguntas[13].text[0:2]):respuestas[71:81],
            int(preguntas[14].text[0:2]):respuestas[81:83],
            int(preguntas[15].text[0:2]):respuestas[83:89],
            int(preguntas[16].text[0:2]):respuestas[89:91],
            int(preguntas[17].text[0:2]):respuestas[91:99],
            int(preguntas[18].text[0:2]):[]
        }
    def PrintFormulario(self):
        for i in range(1,len(Formulario.preguntasdic)+ 1):
            if(not (i == 1 or i == 19)):
                print(f"Pregunta No.{i}: {preguntas[i-1].text[3::]}")
                print("Posibles respuestas")
                for z in range(len(Formulario.preguntasdic[i])):
                    print(Formulario.preguntasdic[i][z].accessible_name)
            print("\n\n")

#Aquí definirá el orden de las matrices probabilísticas sobre los cuales va a iterar
CSVs = ['Semanas CSV\Semana 3 CSV.csv', 'Semanas CSV\Semana 4 CSV.csv', 'Semanas CSV\Semana 5 (PA) CSV.csv', 'Semanas CSV\Semana 6 CSV.csv', 'Semanas CSV\Semana 7 CSV.csv', 'Semanas CSV\Semana 8 CSV.csv', 'Semanas CSV\Semana 9 CSV.csv', 'Semanas CSV\Semana 10 (PA) CSV.csv', 'Semanas CSV\Semana 11 CSV.csv']



#for semana in CSVs:
if 1==1:
    dataframe = pd.read_csv('Semanas CSV\Semana 9 CSV.csv')
    dataframe = dataframe[["Prob(1)", "Prob(2)", "Prob(3)", "Prob(4)", "Prob(5)", "Prob(6)", "Prob(7)", "Prob(8)", "Prob(9)", "Prob(10)" ]]

    
    for repeticiónPorSemana in range(1):
        try:
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            t.sleep(10)
            action = webdriver.ActionChains(driver)
            respuestas = driver.find_elements(By.CLASS_NAME, '--x-77')
            preguntas = driver.find_elements(By.CLASS_NAME, '--d-51')
            if(len(preguntas) == 19):
                Formulario = Forms(preguntas, respuestas)
                probs = dataframe.values
                #Asigna las probabilidades a sus respectivas preguntas.
                preguntas_prob = {}
                for i,x in zip(Formulario.preguntasdic, probs):
                    preguntas_prob[i] = x

                hAcostarse = None
                hLevantarse = None
                NightShift = None
                EstudioAntesDormir = None
                OcioAntesDormir = None
                TiempoOcio = None
                SituaciónExtraordinaria = None
                DificultadConciliarSueño = None
                horasSueño = None
                CalidadSueño = None
                for preg in Formulario.preguntasdic:
                    opciones = Formulario.preguntasdic[preg]
                    probabilidades = preguntas_prob.get(preg, None)

                    # Verifica si hay opciones y probabilidades
                    if opciones and probabilidades is not None:

                        # Ajusta las probabilidades para que coincidan con la longitud de las opciones
                        probabilidades_ajustadas = probabilidades[:len(opciones)]
                        if(not preg == 17):
                            rnd = np.random.choice(opciones, p=probabilidades_ajustadas)
                        if(preg == 5):
                            NightShift = rnd.text
                        elif(preg == 7):
                            OcioAntesDormir = rnd.text
                        elif(preg == 8 and OcioAntesDormir=="No"):
                            continue
                        elif(preg == 9):
                            hAcostarse = rnd
                        elif(preg == 10):
                            hLevantarse = rnd
                        #Solo para la pregunta 8 y 15 que no son probabilisticas sino relacionadas
                        if(preg == 11):
                            match hAcostarse.text:
                                case "Antes de las 9pm.":
                                    hAcostarse = dt.time(20,0,0)
                                case "De 9 pm a 11pm.":
                                    hAcostarse = dt.time(22,0,0)
                                case "De 11pm a 1am.":
                                    hAcostarse = dt.time(0,0,0)
                                case "De 1am a 3am.":
                                    hAcostarse = dt.time(2,0,0)
                                case "Luego de las 3am.":
                                    hAcostarse = dt.time(4,0,0)
                            match hLevantarse.text:
                                case "Antes de las 5am.":
                                    hLevantarse = dt.time(4,0,0)
                                case "De 5am a 7am.":
                                    hLevantarse = dt.time(6,0,0)
                                case "De 7am a 9am.":
                                    hLevantarse = dt.time(8,0,0)
                                case "De 9am a 11am.":
                                    hLevantarse = dt.time(10,0,0)
                                case "Después de las 11am.":
                                    hLevantarse = dt.time(12,30,0)

                            fecha_actual = dt.date.today()
                            dtAcostarse = dt.datetime.combine(fecha_actual, hAcostarse)
                            dtLevantarse = dt.datetime.combine(fecha_actual, hLevantarse)

                            horasSueño = dtLevantarse - dtAcostarse
                            horasSueño = horasSueño.seconds // 3600

                            if(NightShift == "No"):
                                horasSueño -= 0.15
                            if(OcioAntesDormir == "Si"):
                                horasSueño -= 1
                            if(horasSueño<4):
                                probabilidades_ajustadas = [1,0,0,0,0,0,0]
                                probabilidades_ajustadas = probabilidades_ajustadas[:len(opciones)]
                                rnd = np.random.choice(opciones, p=probabilidades_ajustadas)
                            elif(horasSueño<5):
                                probabilidades_ajustadas = [0,1,0,0,0,0,0]
                                probabilidades_ajustadas = probabilidades_ajustadas[:len(opciones)]
                                rnd = np.random.choice(opciones, p=probabilidades_ajustadas)
                            elif(horasSueño<6):
                                probabilidades_ajustadas = [0,0,1,0,0,0,0]
                                probabilidades_ajustadas = probabilidades_ajustadas[:len(opciones)]
                                rnd = np.random.choice(opciones, p=probabilidades_ajustadas)
                            elif(horasSueño<7):
                                probabilidades_ajustadas = [0,0,0,1,0,0,0]
                                probabilidades_ajustadas = probabilidades_ajustadas[:len(opciones)]
                                rnd = np.random.choice(opciones, p=probabilidades_ajustadas)
                            elif(horasSueño<8):
                                probabilidades_ajustadas = [0,0,0,0,1,0,0]
                                probabilidades_ajustadas = probabilidades_ajustadas[:len(opciones)]
                                rnd = np.random.choice(opciones, p=probabilidades_ajustadas)
                            elif(horasSueño<9):
                                probabilidades_ajustadas = [0,0,0,0,0,1,0]
                                probabilidades_ajustadas = probabilidades_ajustadas[:len(opciones)]
                                rnd = np.random.choice(opciones, p=probabilidades_ajustadas)
                            elif(horasSueño>=9):
                                probabilidades_ajustadas = [0,0,0,0,0,0,1]
                                probabilidades_ajustadas = probabilidades_ajustadas[:len(opciones)]
                                rnd = np.random.choice(opciones, p=probabilidades_ajustadas)
                            rnd.click()
                            continue
                        elif(preg == 12):
                            CalidadSueño = int(rnd.text)
                        elif(preg == 15):
                            SituaciónExtraordinaria = rnd.text
                        elif(preg == 16 and SituaciónExtraordinaria == "No"):
                            continue
                        elif(preg == 17):
                            if(NightShift == "No" and horasSueño < 5 and CalidadSueño<5):
                                probabilidades_ajustadas = [1,0,0,0,0,0,0]
                                probabilidades_ajustadas = probabilidades_ajustadas[:len(opciones)]
                                rnd = np.random.choice(opciones, p=probabilidades_ajustadas)
                            elif(horasSueño<6 and CalidadSueño < 6):
                                probabilidades_ajustadas = [0.5,0.5,0,0,0,0,0]
                                probabilidades_ajustadas = probabilidades_ajustadas[:len(opciones)]
                                rnd = np.random.choice(opciones, p=probabilidades_ajustadas)
                            else:
                                probabilidades_ajustadas = [0.2,0.8,0,0,0,0,0]
                                probabilidades_ajustadas = probabilidades_ajustadas[:len(opciones)]
                                rnd = np.random.choice(opciones, p=probabilidades_ajustadas)
                            rnd.click()
                            continue
                        elif(preg == 18 and DificultadConciliarSueño == "No"):
                            continue
                        rnd.click()
                    else:
                        print(f"Error: No hay opciones para la pregunta {preg}")
                #driver.find_element(By.CLASS_NAME, 'css-180').click()
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-automation-id='submitButton']"))).click()
            else:
                print("No se obtuvieron los elementos necesarios, saltando a la siguiente iteración.")
            driver.quit()
        except(TimeoutException):
            print("Los elementos no fueron obtenidos correctamente, saltandoa  la siguiente iteración.")