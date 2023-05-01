import argparse
import pandas as pd
import os.path
from openpyxl.workbook import Workbook

def get_args():
    my_parser = argparse.ArgumentParser("compare two csv's")
    my_parser.add_argument("--f1",help="first excel file")
    my_parser.add_argument("--f2",help="second excel file")
    my_parser.add_argument("--output",help="path to store the output csv's")
    return my_parser.parse_args()

def generate_csv(ans_2010,ans_2011,topic,header_=False):
    sheet_active = "summary"
    output_dest = get_args()
    growth = ((ans_2011 - ans_2010)/ans_2010)*100
    df = pd.DataFrame({2010:ans_2010, 2011:ans_2011, "growth_rate":f"{round(growth,3)}%" }, index =[f"{topic}"])
    check_file_path = os.path.isfile(f"{output_dest.output}")
    if check_file_path:
        df2=pd.read_excel(output_dest.output, index_col=0) 
        df_merged = pd.concat([df, df2])
        df_merged.to_excel(output_dest.output) 
    else:
        df.to_excel(output_dest.output, index=True, header=header_,sheet_name='sheet_active') 

def top_shop_country(df_2010,df_2011):
    country_2010 = df_2010.groupby(["Country"])["Country"].count().reset_index(name='Count').sort_values(["Count"],ascending=0)
    country_2010.reset_index(drop=True, inplace=True)
    country_2010.index += 1

    country_2011 = df_2011.groupby(["Country"])["Country"].count().reset_index(name='Count').sort_values(["Count"],ascending=0)
    country_2011.reset_index(drop=True, inplace=True)
    country_2011.index += 1

    nw =  pd.concat([country_2010, country_2011], axis=1, ignore_index=True)
    nw.rename(columns = {0:'Country_2010',1:"Count_2010",2:'Country_2011',3:"Count_2011"}, inplace = True)

    nw.to_csv("../diff_reports/top_shopping_country.csv",index=False)

def avg_cart_value(df_2010,df_2011):
    df_2010["bill_for_product"] = df_2010["Quantity"]*df_2010["UnitPrice"]
    df_2011["bill_for_product"] = df_2011["Quantity"]*df_2011["UnitPrice"]

    cart_total1 = df_2010.groupby("InvoiceNo")["bill_for_product"].sum()
    cart_total2 = df_2011.groupby("InvoiceNo")["bill_for_product"].sum()

    # mean values
    m1 = cart_total1.mean()
    m2 = cart_total2.mean()
    topic = "average expenditure per cart (in $)"
    generate_csv(m1,m2,topic,True)
    
    # total revenue in that year
    r1 = df_2010["bill_for_product"].sum()
    r2 = df_2011["bill_for_product"].sum()
    topic = "total revenue generated  (in $)"
    generate_csv(r1,r2,topic)

def invoices_generated(df_2010,df_2011):
    t_invoices_2010 = len(df_2010["InvoiceNo"].unique())
    t_invoices_2011 = len(df_2011["InvoiceNo"].unique())
    topic = "total invoices generated"
    generate_csv(t_invoices_2010,t_invoices_2011,topic)

def total_inventory(df_2010,df_2011):
    prod_2010 = df_2010["StockCode"].value_counts().sum()
    prod_2011 = df_2011["StockCode"].value_counts().sum()
    topic = "total inventory"
    generate_csv(prod_2010,prod_2011,topic)

def read_csv():
    para = get_args()
    df_2010 = pd.read_csv(para.f1)
    df_2011 = pd.read_csv(para.f2)

    # calling functions
    avg_cart_value(df_2010,df_2011)
    top_shop_country(df_2010,df_2011)
    invoices_generated(df_2010,df_2011)
    total_inventory(df_2010,df_2011)

if __name__ == "__main__":
    read_csv()

    

