# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import importlib

import sicep





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    importlib.reload(sicep)
    convocatorias = sicep.cargar_convocatorias()
    convocatorias.at[90, 'rutas'] = r"https://sicep.xm.com.co/public-announcements/electronic-file/CP-EEPC2020-002/EEP%28PEREIRA%29/EEPC/01%2F09%2F2020/31%2F12%2F2025"
    convocatorias.at[99, 'rutas'] = r"https://sicep.xm.com.co/public-announcements/electronic-file/CP-EEPC2020-001/EEP%28PEREIRA%29/EEPC/01%2F06%2F2020/31%2F12%2F2025"
    resultados = sicep.obtener_resultados(convocatorias)
    resultados['convocatoria'] = resultados.Productos.str[0:15]
    resultados.fillna(0, inplace=True)
    resultados.columns = ['producto', 'energia_dem_gwh', 'energia_adj_gwh', 'precio', 'convocatoria']
    resultados.to_excel("resultados_sicep.xlsx", index=False)

    prod_por_conv = pd.DataFrame(resultados.groupby(by='convocatoria').producto.count()).reset_index(drop=False)
    convocatorias = convocatorias.merge(prod_por_conv, left_on='CodigoConvocatoria', right_on='convocatoria')
    prod_fin = sicep.definir_productos(convocatorias)

    productos_finales = pd.read_excel("productos_finales.xlsx")
    productos_finales = productos_finales.merge(convocatorias, left_on='convocatoria_x',
                                                right_on='CodigoConvocatoria')
    # productos_finales.ini_con = productos_finales.ini_con.apply(dt.datetime.strptime, args=("%d/%m/%Y",))
    # productos_finales.fin_con = productos_finales.fin_con.apply(dt.datetime.strptime, args=("%d/%m/%Y",))
    productos_finales['duracion_prod'] = (productos_finales.fin_con - productos_finales.ini_con).dt.days / 365

    idx_con_precio = productos_finales.precio > 0
    prod_analisis = productos_finales[idx_con_precio]
    print(np.corrcoef(prod_analisis.duracion_prod, prod_analisis.precio))

    gPrec = sns.lmplot(data=prod_analisis, x="duracion_prod", y="precio", legend=False)
    ax1 = plt.gca()
    ax1.set_title('PPA Price vs. Duration')
    ax1.set_ylabel(ylabel='PPA Price (COP/kWh)')
    ax1.set_xlabel(xlabel='PPA Duration (years)')
    ax1.set(xlim=(0,16))
    sns.set_theme()
    sns.set_style(style='ticks')
    plt.grid()
    plt.show()

    gDur = sns.histplot(data=prod_analisis, x='duracion_prod', kde=True,
                        bins=15, multiple='stack', stat='density', cumulative=True)
    ax1 = plt.gca()

    ax1.set_title('Distribution of PPA Duration')
    ax1.set_xlabel(xlabel='PPA Duration (years)')
    sns.set_style(style='ticks')
    sns.set_theme()
    plt.show()
    plt.grid()

    cantidaes_anio, precios_anio = sicep.obtener_precios_anio(productos_finales)
    # resultados = sicep.obtener_resultados(convocatorias.iloc[90:, :])

    aux_cant = cantidaes_anio.melt(id_vars=['producto'], value_vars=list(cantidaes_anio.columns[1:18]))
    aux_cant.value.replace(0, np.nan, inplace=True)

    precio_prom_anio = sicep.promedio_pond( precios_anio.iloc[:, 1:], cantidaes_anio.iloc[:, 1:])
    precio_prom_anio.to_excel('precios.xlsx')


