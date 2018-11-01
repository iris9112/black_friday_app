import pandas as pd

from .models import Document 

def previewDataFrame():
    d = Document.objects.all().last()
    # creando el data frame
    df = pd.read_csv(d.document.path)

    columns = ['User_ID', 'Product_ID', 'Gender', 'Age', 'Occupation', 'City_Category',
               'Stay_In_Current_City_Years', 'Marital_Status', 'Product_Category_1',
               'Product_Category_2', 'Product_Category_3', 'Purchase']
    return df.head().to_html()
