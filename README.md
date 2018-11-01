# Predicción de ventas para el Black Friday

## Problema

Un alto directivo de la empresa X está solicitando a nuestro equipo de ingenieros desarrollar un sistema que permita predecir información relevante para el próximo Blackfriday que se llevará a cabo en noviembre 23 del 2018, tomando como base los datos de ventas del blackfriday del año pasado que se llevó a cabo en noviembre 24 2017. 

El sistema debe ser capaz de responder las siguientes preguntas de forma gráfica y tabular (en tablas):

1. Unidades que se venderán por producto.
2. Total de ventas (valor de ventas) por producto en pesos. 
3. Top de compradores. 
4. ¿Nos comprarán más las personas solteras o las personas casadas? (en el dataset asumimos casadas como 1).
5. ¿Nos comprarán más los hombres o las mujeres? 
6. Clasifique por edades, que producto que se venderá más.

Para calcular los pesos se debe predecir el valor del dólar efectuando una regresión con los datos de dataset: TRM_Historico.xls 
* Se recomienda la librería [Bokeh](https://bokeh.pydata.org/en/latest/)

## Requerimientos

- El sistema debe usar ML para resolver las preguntas.
- Django 2.1 y Python 3.7 (librerías de ML)
- Postgress, en caso de requerir el uso de una BD

## Observaciones

#### TRM
La TRM es la Tasa Representativa del Mercado cambiario de Colombia y representa el valor que tiene un dólar estadounidense en pesos colombianos. 

#### Limitantes
- Detalle del crecimiento de la población:
Esta predicción no toma en cuenta nuevos usuarios ni el crecimiento de la población de usuarios que accedio a la tienda en el último año. Se asume que no disminuirá el tamaño de la población.

#### Versión de Django
Se actualiza la versión del _framework Django_ a la **2.1.2** debido a que en la versión **2.1** se reporto recientemente un fuerte problema de seguridad.

#### Base de datos
Por rapidez se trabaja con sqlite, ya que solo se requiere para guardar el conjunto de datos.

# Solución

## 1. Predicción del valor del dolar

Vamos a realizar una regresión lineal con los datos de dataset: *TRM_Historico.xls* para predecir el valor del dolar el día 23-nov-2018, día en que se realizará el evento.


## 2. Exploración del dataset black friday

Vamos a explorar el conjunto de datos *BlackFriday.csv* para conocer los datos y encontrar relación entre ellos. Esto nos permite saber:
 - Tamaño del data set
 - Cantidad y nombre de las caracteristicas
 - Tipos de datos
 - Valores nulos
 - Identificar nuestro **target**


## 3. preprocesar los datos

De la exploración de datos identificamos las siguientes variables del conjunto:

- User_ID: identificador del usuario. Variable tipo `int`.
- Product_ID: identificador del producto. Se utiliza como característica sin procesar.
- Gender: Genero del usuario. Se convierte en una variable binaria.
- Age: Rango de edad del usuario. Se normaliza a variable tipo `int`.
- Occupation: id de la ocupación del usuario. Variable tipo `int`.
- City_Category: Categoria de la ciudad. Se usa la codificación One-Hot.
- Stay_In_Current_City_Years: Número de años que ha estado en la ciudad. Se normaliza a variable tipo `int`.
- Marital_Status: Estado civil. Es una variable binaria. 
- Product_Category_1: Categoria del producto. Variable tipo `int`.
- Product_Category_2 y Product_Category_3: Son categorias del producto. Tienen valores nulos y no es significativa para la predicción, por lo que la eliminaremos del conjunto de datos
- Purchase: precio de la compra del producto. Variable tipo `int`. Nuestro TARGET

Variables a generar:
- user_count: cantidad de registros de compra de cada usuario.
- Product_count: cantidad de registros de compra de cada producto.
- Product_mean: cantidad promedio de compra de cada producto.
- user_high: Proporción de veces que el usuario compra productos a  un monto mayor que el monto promedio de compra del producto.

Para preprocesar los datos lo primero es normalizarlos:

```python
gender_dict = {'F':0, 'M':1}
age_dict = {'0-17':0, '18-25':1, '26-35':2, '36-45':3, '46-50':4, '51-55':5, '55+':6}
city_dict = {'A':0, 'B':1, 'C':2}
stay_city_years_dict = {'0':0, '1':1, '2':2, '3':3, '4+':4}
```

## 4. Generar modelos de predicción

Antes de realizar los modelos, separamos el conjunto en datos de entrenamiento y datos de prueba.
Se utilizaron modelos de regresión lineal, cross validation y XGBoost


## 5. Bringing it all together
Vamos a realizar un backend con django para responder a las preguntas de forma gráfica.

## Pasos para ejecutar el proyecto:

1. Instalar dependencias en un entorno virtual (libre elección)
```python
    pip install -r requirements.txt
```

2. Descargar el codigo de la carpeta site_prediction

3. Hacer migraciones 
```python
    python manage.py makemigrations
```

4. Correr migraciones
```python
    python manage.py migrate
```

5. Cargar conjunto de datos
```python
    pip script_initial.py
```

6. Correr el proyecto
```python
    python manage.py runserver
```