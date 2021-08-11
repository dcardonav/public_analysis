import numpy as np
import pandas as pd
from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import datetime as dt
import time



ruta_expedientes = r"https://sicep.xm.com.co/public-announcements/electronic-file/"
patron_expediente = r"{0}/{1}/{2}/{3}%2F{4}%2F{5}/{6}%2F{7}%2F{8}"
datos_finales = pd.DataFrame()
productos_finales = pd.DataFrame()

def cargar_convocatorias():

    df_conv = pd.read_excel("ConvocatoriasPublicas.xlsx")
    periodos = df_conv.PeriodoAContratar.str.split()
    aux_fechas = periodos.apply(extraer_periodo)
    fechas = pd.DataFrame.from_records(aux_fechas, columns=['fecha_ini', 'fecha_fin'])
    df_conv['fecha_ini'] = fechas.fecha_ini
    df_conv['fecha_fin'] = fechas.fecha_fin

    df_conv.FechaPublicacionAviso = df_conv.FechaPublicacionAviso.apply(dt.datetime.strptime, args=['%d/%m/%Y'])
    df_conv.drop(columns=['PeriodoAContratar'], inplace=True)

    df_conv['rutas'] = ruta_expedientes + df_conv.apply(construir_ruta, axis=1)

    return df_conv

def extraer_periodo(periodo):

    aux_ini = periodo[0]
    aux_fin = periodo[2]

    fecha_ini = dt.date(int(aux_ini[-4:]), int(aux_ini[-7:-5]), int(aux_ini[-10:-8]))
    fecha_fin = dt.date(int(aux_fin[-4:]), int(aux_fin[-7:-5]), int(aux_fin[-10:-8]))

    return fecha_ini, fecha_fin

def construir_ruta(convocatoria):

    ruta = patron_expediente.format(convocatoria.CodigoConvocatoria, convocatoria.NombreAgenteComprador,
                             convocatoria.CodigoSicAgente, convocatoria.fecha_ini.strftime('%d'),
                             convocatoria.fecha_ini.strftime('%m'), convocatoria.fecha_ini.strftime('%Y'),
                             convocatoria.fecha_fin.strftime('%d'), convocatoria.fecha_fin.strftime('%m'),
                             convocatoria.fecha_fin.strftime('%Y'))

    return ruta

def definir_productos(convocatorias):
    global productos_finales

    idx_cerr_adj = convocatorias.Estado == "Cerrada y adjudicada"
    browser = webdriver.Firefox()

    for (idx, convocatoria) in convocatorias.iterrows():

        aux = obtener_productos(convocatoria.rutas, convocatoria.producto, browser)
        productos_finales = productos_finales.append(aux)

    return productos_finales

def obtener_productos(ruta, productos, browser=None):
    global productos_finales

    opts = Options()
    opts.headless = True
    cerrar = False

    print(ruta)

    fp = FirefoxProfile()
    if browser == None:
        cerrar = True
        browser = webdriver.Firefox()

    browser.get(ruta)

    delay = 9  # seconds
    try:
        myElem = WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id=\"ui-accordiontab-0\"]')))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")
    time.sleep(3)
    b = browser.find_element_by_xpath("//*[@id=\"ui-accordiontab-0\"]").click()

    prod_conv = pd.DataFrame(columns=['convocatoria', 'producto', 'tipo_cont', 'ini_con', 'fin_con', 'tamanio_con'])
    for i in range(1, productos+1):
        time.sleep(3)

        try:
            aux_prod = browser.find_element_by_xpath(
            r"/html/body/app-root/app-body/div/div[2]/div/div/div/div/app-electronic-file/div[2]/div/p-accordion/div/p-accordiontab[1]/div[2]/div/app-detail-announcement/div[2]/div/div[" + str(
                i+1) + "]/a").text
            browser.find_element_by_xpath(r"/html/body/app-root/app-body/div/div[2]/div/div/div/div/app-electronic-file/div[2]/div/p-accordion/div/p-accordiontab[1]/div[2]/div/app-detail-announcement/div[2]/div/div["+str(i+1)+"]/a").click()
            time.sleep(4)
            aux_tipo = browser.find_element_by_xpath("/html/body/p-dynamicdialog/div[2]/div[2]/app-product-summary-detail/div/div[2]/div[1]/p").text
            aux_ini = browser.find_element_by_xpath(
                "/html/body/p-dynamicdialog/div[2]/div[2]/app-product-summary-detail/div/div[3]/div[1]/p").text
            aux_fin = browser.find_element_by_xpath(
                "/html/body/p-dynamicdialog/div[2]/div[2]/app-product-summary-detail/div/div[4]/div[1]/p").text
            aux_tam = browser.find_element_by_xpath(
                "/html/body/p-dynamicdialog/div[2]/div[2]/app-product-summary-detail/div/div[5]/div[1]/p").text

            aux_series = pd.Series(['', aux_prod, aux_tipo, aux_ini, aux_fin, aux_tam],
                                   index=prod_conv.columns)
            prod_conv = prod_conv.append(aux_series, ignore_index=True)
            browser.find_element_by_xpath(r"//*[@id='btnCerrarModalProductSummary']").click()
            time.sleep(3)
        except:
            continue


    if cerrar:
        browser.close()

    return prod_conv


def obtener_resultados(convocatorias):

    idx_cerr_adj = convocatorias.Estado == "Cerrada y adjudicada"
    browser = webdriver.Firefox()
    resultados = convocatorias[idx_cerr_adj].rutas.apply(obtener_resultado, args=(browser,))

    return resultados


def obtener_resultado(ruta, browser=None):
    global datos_finales

    opts = Options()
    opts.headless = True
    cerrar = False

    print(ruta)

    fp = FirefoxProfile()
    if browser == None:
        cerrar = True
        browser = webdriver.Firefox()

    browser.get(ruta)

    delay = 9  # seconds
    try:
        myElem = WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id=\"ui-accordiontab-0\"]')))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")
    # a = browser.find_element_by_xpath("//p-accordiontab[@header=\"Convocatoria\"]")
    time.sleep(4)
    b = browser.find_element_by_xpath("//*[@id=\"ui-accordiontab-0\"]")
    time.sleep(2)
    c = browser.find_element_by_xpath("//*[@id=\"ui-accordiontab-6\"]")
    c.click()
    time.sleep(2)
    d = browser.find_element_by_xpath(
        "/html/body/app-root/app-body/div/div[2]/div/div/div/div/app-electronic-file/div[2]/div/p-accordion/div/p-accordiontab[7]/div[2]/div/app-publication-information/div/div[2]/div[3]/p-table/div/div/table")
    datos_conv = pd.read_html(d.get_attribute("outerHTML"))[0]
    datos_finales = datos_finales.append(datos_conv)

    if cerrar:
        browser.close()

    return datos_conv

def obtener_precios_anio(productos_finales):


    rango_anios = range(2020, 2036 + 1)
    df_cantidades = pd.DataFrame(columns=['producto'] + list(rango_anios))
    df_precios = pd.DataFrame(columns=['producto'] + list(rango_anios))

    for idx, p in productos_finales.iterrows():

        aux_p = [p.producto_x]
        aux_c = [p.producto_x]
        anios_aux = np.arange(p.ini_con.year, p.ini_con.year + np.round(p.duracion_prod))
        for i in rango_anios:

            if i in anios_aux:
                aux_c.append(p.energia_adj_gwh)
                aux_p.append(p.precio)
            else:
                aux_p.append(0)
                aux_c.append(0)

        aux_series_c = pd.Series(aux_c, index=df_cantidades.columns)
        aux_series_p = pd.Series(aux_p, index=df_precios.columns)
        df_precios = df_precios.append(aux_series_p, ignore_index=True)
        df_cantidades = df_cantidades.append(aux_series_c, ignore_index=True)

        df_cantidades = df_cantidades.reset_index(drop=True)
        df_precios = df_precios.reset_index(drop=True)

        for col in df_cantidades.columns[1:]:
            df_cantidades[col] = df_cantidades[col].astype('float')
            df_precios[col] = df_precios[col].astype('float')

    return df_cantidades, df_precios



