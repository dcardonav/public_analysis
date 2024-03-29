## Base de Datos Pública - SICEP
Este archivo Excel incluye las convocatorias cerradas y adjudicadas con corte a **mayo 31 de 2021**. La información se obtuvo mediante procesos automáticos de **web scrapping** y no de manera manual por lo que son posibles las inconsistencias (se revisaron tres de manera manual y la información coincidió). Espero que esta información sea de utilidad e incentive la realización de análisis y comparaciones respecto al impacto del SICEP en el mercado de contratos de largo plazo.

**Usar bajo su propia responsabilidad**

A continuación se presenta una breve descripción de los campos que contiene el archivo:
- **convocatoria:** Identficador de la convocatoria en la plataforma
- **producto:** Código de cada uno de los productos (conrtatos) de las convocatorias
- **energia_dem_gwh:** Energía demandada para cada producto en GWh de acuerdo con la tabla resumen publicada por el Administrador del SICEP
- **energia_adj_gwh:** Energía adjudicada para cada producto en GWh de acuerdo con la tabla resumen publicada por el Administrador del SICEP
- **precio:** Precio promedio del producto acuerdo con la tabla resumen publicada por el Administrador del SICEP
- **tipo_con:** Tipo de negociación bilateral (PD, PC)
- **ini_con:** Fecha inicio del producto
- **fin_con:** Fecha fin del producto
- **tamanio_con:** Tamaño del producto en MWh de acuerdo con la publicación inicial de términos. En caso de adendas o modificaciones, pueden no verse reflejadas en este valor.
- **fecha_ini:** Fecha de inicio de la **convocatoria**
- **fecha_fin:** Fecha de fin de la **convocatoria**
