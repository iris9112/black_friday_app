import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn import ensemble
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from django.conf import settings

from .models import Document


def previewDataFrame(doc):
    """
    preview a dataframe from model document in a template
    """
    # creando el data frame
    df = pd.read_csv(doc.document.path)
    df.drop('Product_Category_2', axis=1, inplace=True)
    df.drop('Product_Category_3', axis=1, inplace=True)

    print(doc.document.path)

    return df.head().to_html(classes="table", index=False)


def read_csv(doc):
    """
    Lee un archivo css de la carpeta media/documents y lo convierte en un dataframe
    """
    df = pd.read_csv(settings.MEDIA_ROOT + '/documents/' + doc, sep=',', converters={'Purchase':str})
    return df


def prediction(doc):
    """
    Modelo de prediccion para ventas del blackfriday
    """
    # cargar datos
    doc = Document.objects.all().last()
    df = pd.read_csv(doc.document.path)

    # eliminar columnas innecesarias
    df.drop('Product_Category_2', axis=1, inplace=True)
    df.drop('Product_Category_3', axis=1, inplace=True)

    # dividir dataset para entrenamiento y pruebas
    df_train, df_test = train_test_split(df)

    print(df.shape)
    print(df_train.shape)
    print(df_test.shape)

    # columnas categorias
    categorical_columns = ["Product_ID", "Gender", "Age", "City_Category", "Stay_In_Current_City_Years"]

    # seleccionando el target y separando los datos

    train_y = np.array(df_train["Purchase"])
    test_y = np.array(df_test["Purchase"])

    train_X = df_train.copy()
    test_X = df_test.copy()

    # eliminando el target del dataframe
    train_X.drop('Purchase', axis=1, inplace=True)
    test_X.drop('Purchase', axis=1, inplace=True)

    # Normalizando los datos
    # en lugar de usar la funcion apply como vimos antes, vamos a encodificar las variables categoricas

    for var in categorical_columns:
        lb = LabelEncoder()
        full_var_data = pd.concat((train_X[var], test_X[var]), axis=0).astype('str')
        lb.fit( full_var_data )
        train_X[var] = lb.transform(train_X[var].astype('str'))
        test_X[var] = lb.transform(test_X[var].astype('str'))

    print("Train shape is : ", train_X.shape)
    print("Test shape is : ", test_X.shape)

    # definiendo los parametros necesarios para el modelo de regresion lineal con X
    params = {}
    params["objective"] = "reg:linear"
    params["eta"] = 0.05
    params["seed"] = 0
    params["max_depth"] = 3 # 5
    plst = list(params.items())

    xgtrain = xgb.DMatrix(train_X, label=train_y)
    xgtest = xgb.DMatrix(test_X)

    num_rounds = 100 # 5667
    model = xgb.train(plst, xgtrain, num_rounds)
    pred_test_y_xgb1 = model.predict(xgtest)

    # TODO: max_depth = 5 y num_rounds = 5660 tienen un mejor rendimiento

    # columnas deseadas en dataframe de salida
    columns_out = ['User_ID','Product_ID', 'Gender', 'Age', 'Occupation', 'City_Category',
               'Stay_In_Current_City_Years','Marital_Status', 'Product_Category_1','Purchase']

    test_X['Purchase'] = pred_test_y_xgb1
    test_X.to_csv(settings.MEDIA_ROOT + '/documents/solution.csv',columns = columns_out, index = False)

    # guardar codificacion de datos de entrenamiento
    train_X['Purchase']=train_y
    train_X.to_csv(settings.MEDIA_ROOT + '/documents/train_encode.csv')

    return test_X.head().to_html(classes="table table-bordered", index=False)


def units_per_product(df):
    """
    metodo para calcular el total de unidades vendidas por cada producto
    :param: dataframe
    :return: dataframe
    """
    # filtro variables del problema
    df_one = df.filter(['Product_ID', 'User_ID'], axis=1).groupby(['Product_ID']).count()
    df_one = df_one.reset_index()
    # defino etiquetas y ordeno el dataframe
    df_one.columns = ['Product_ID', 'Unidades x Producto']
    df_one = df_one.sort_values('Unidades x Producto', ascending=False)
    return df_one


def top_sales(df):
    """
    metodo para calcular el valor de las ventas de cada producto
    :param: dataframe
    :return: dataframe
    """
    # problema de formato de numero al leer el archivo csv 
    df['Purchase'] = df['Purchase'].apply(lambda x: x.replace('.', ''))
    # filtro variables del problema
    df = df.filter(['Product_ID', 'Purchase'], axis=1)
    df['Purchase'] = df['Purchase'].astype(int)
    df_two = df.groupby(['Product_ID']).sum()
    df_two = df_two.reset_index()
    df_two.Purchase = df_two.Purchase.apply(lambda x: round(x))
     # defino etiquetas y ordeno el dataframe
    df_two.columns = ['Product_ID', 'Valor Ventas']
    df_two = df_two.sort_values('Valor Ventas', ascending=False)
    return df_two


def top_user(df):
    """
    metodo para calcular el top de compradores
    :param: dataframe
    :return: dataframe
    """
    df['Purchase'] = df['Purchase'].apply(lambda x: x.replace('.', ''))
    df = df.filter(['User_ID', 'Purchase'], axis=1)

    df['Purchase'] = df['Purchase'].astype(int)

    df_three = df.groupby(['User_ID']).sum()
    df_three = df_three.reset_index()
    df_three.Purchase = df_three.Purchase.apply(lambda x: round(x))
    df_three = df_three.sort_values('Purchase', ascending=False)
    df_three.columns = ['Usuario', 'Valor compras']
    return df_three
