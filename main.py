from selenium import webdriver
import selenium
import pandas as pd
from time import sleep, time
from contextlib import suppress
browser=webdriver.Chrome("C:/Users/Ansh/Documents/chromedriver.exe")
browser.implicitly_wait(20)
browser.get("https://www.morningstar.com")
quotes=["Key Ratios","Short Interest"]
exc={'Toronto Stock Exchange': 'xtse', 'Nasdaq': 'xnas', 'Shenzhen Stock Exchange': 'xshe', 'BSE LTD': 'xbom', 'New York Stock Exchange, Inc.': 'xnys', 'Shanghai Stock Exchange': 'xshg', 'Hong Kong Exchanges And Clearing Ltd': 'xhkg', 'London Stock Exchange': 'xlon', 'B3 S.A. - Brasil, Bolsa, Balcão': 'xbsp'}
#stock_list=['AAPL','TSLA','GOOGL']
stock_list=pd.read_csv("stocks_final.csv")
data={"Price":[]}
stock_list["Unique"]=[stock_list["Company Name"][i]+' '+stock_list["Ticker"][i] for i in range(stock_list.shape[0])]
stocks=pd.DataFrame(index=stock_list["Unique"],columns=["Price"])
price_sales=pd.DataFrame(index=stock_list["Unique"],columns=[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,'Current','5-Yr','Index'])
price_earnings=pd.DataFrame(index=stock_list["Unique"],columns=[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,'Current','5-Yr','Index'])
price_cashflow=pd.DataFrame(index=stock_list["Unique"],columns=[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,'Current','5-Yr','Index'])
price_book=pd.DataFrame(index=stock_list["Unique"],columns=[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,'Current','5-Yr','Index'])
price_forwardearnings=pd.DataFrame(index=stock_list["Unique"],columns=[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,'Current','5-Yr','Index'])
peg_ratio=pd.DataFrame(index=stock_list["Unique"],columns=[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,'Current','5-Yr','Index'])
earnings_yield=pd.DataFrame(index=stock_list["Unique"],columns=[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,'Current','5-Yr','Index'])
value_bil=pd.DataFrame(index=stock_list["Unique"],columns=[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,'Current','5-Yr','Index'])
value_ebit=pd.DataFrame(index=stock_list["Unique"],columns=[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,'Current','5-Yr','Index'])
value_ebitda=pd.DataFrame(index=stock_list["Unique"],columns=[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,'Current','5-Yr','Index'])
'''
stocks=pd.read_excel("stocks.xlsx")stocks
price_sales=pd.read_excel("price_sales.xlsx")
price_earnings=pd.read_excel("price_earnings.xlsx")
price_cashflow=pd.read_excel("price_cashflow.xlsx")
price_book=pd.read_excel("price_book.xlsx")
p'''
name='AAPL'
undetected=[0]
num=[0]
def get_stock(i):
    name=stock_list["Unique"][i]
    name2=stock_list["Ticker"][i]
    name1=name2
    if name1.isdigit():
        while len(name1)<6:
            name1='0'+name1
    exchange=exc[stock_list["Exchange"][i]]
    browser.get("https://www.morningstar.com/stocks/"+exchange+'/'+name1)
    if "404 Error" in browser.page_source:
        print("Stock "+name+" undetected")
        undetected[0]+=1
        num[0]+=1
        for each in data:
            data[each].append("N/A")
        return 0
    sleep(5)
    price='N/A'
    t1=time()
    while price=='N/A':
        with suppress(selenium.common.exceptions.NoSuchElementException):
            elem=browser.find_element_by_id("message-box-price")
            price=elem.text
            break
        t2=time()
        if t2-t1>4:
            break
    print(price)
    data["Price"].append(price)
    stocks["Price"][name]=price
    for category in quotes:
        btn=''
        while btn=='':
            with suppress(selenium.common.exceptions.NoSuchElementException):
                btn=browser.find_element_by_xpath("//input[@value='"+category+"']")
        btn.click()
        sleep(2)
        elems=browser.find_elements_by_xpath("//div[@class='dp-value ng-binding']")
        elems1=browser.find_elements_by_xpath("//div[@class='dp-name ng-binding']")
        if category=="Quote":
            first=browser.find_element_by_xpath("//div[@class='dp-value price-down ng-binding ng-scope']")
            second=browser.find_element_by_xpath("//div[@class='dp-value price-up ng-binding ng-scope']")
            thirds=browser.find_elements_by_xpath("//div[@class='dp-value ng-binding ng-scope']")
            elems=[first,second]+elems[:1]+thirds+elems[1:]
        elif category=="Key Ratios":
            elems1=elems1[12:]
            elems=elems[8:]
        else:
            elems=elems[16:]
            elems1=elems1[20:]
        quote_info={elems1[i].text:elems[i].text for i in range(len(elems))}
        for each in quote_info:
            if each not in stocks.columns:
                stocks[each]=['' for i in range(stock_list.shape[0])]
                data[each]=["N/A" for i in range(num[0])]
            data[each].append(quote_info[each])
            stocks[each][name]=quote_info[each]
    browser.get("https://www.morningstar.com/stocks/"+exchange+'/'+name1+"/financials")
    elems=browser.find_elements_by_xpath("//div[@class='dp-value ng-binding']")
    elems1=browser.find_elements_by_xpath("//div[@class='dp-name ng-binding']")
    financials_info={elems1[i].text:elems[i].text for i in range(len(elems))}
    for each in financials_info:
        if each not in stocks.columns:
            stocks[each]=['' for i in range(len(stock_list))]
            data[each]=["N/A" for i in range(num[0])]
        data[each].append(financials_info[each])
        stocks[each][name]=financials_info[each]
    browser.get("https://www.morningstar.com/stocks/"+exchange+'/'+name1+"/valuation")
    sleep(7)
    f=True
    while f:
        try:
            table=pd.read_html(browser.page_source)[0]
            f=False
        except IndexError:
            pass
    table.columns=table.loc[0]
    table=table.drop([0,1])
    table.index=table["Calendar"]
    del table["Calendar"]
    try:
        price_sales.loc[name]=table.loc["Price/Sales"]
    except KeyError:
        price_sales.loc[name]="N/A"
    try:
        price_earnings.loc[name]=table.loc["Price/Earnings"]
    except KeyError:
        price_earnings.loc[name]="N/A"
    try:    
        price_cashflow.loc[name]=table.loc["Price/Cash Flow"]
    except KeyError:
        price_cashflow.loc[name]="N/A"
    try:
        price_book.loc[name]=table.loc["Price/Book"]
    except KeyError:
        price_book.loc[name]="N/A"
    try:
        price_forwardearnings.loc[name]=table.loc["Price/Forward Earnings"]
    except KeyError:
        price_forwardearnings.loc[name]="N/A"
    try:
        peg_ratio.loc[name]=table.loc["PEG Ratio"]
    except KeyError:
        peg_ratio.loc[name]="N/A"
    try:
        earnings_yield.loc[name]=table.loc["Earnings Yield %"]
    except KeyError:
        earnings_yield.loc[name]="N/A"
    try:
        value_bil.loc[name]=table.loc["Enterprise Value (Bil)"]
    except KeyError:
        value_bil.loc[name]="N/A"
    try:
        value_ebit.loc[name]=table.loc["Enterprise Value/EBIT"]
    except KeyError:
        value_ebit.loc[name]="N/A"
    try:
        value_ebitda.loc[name]=table.loc["Enterprise Value/EBITDA"]
    except KeyError:
        value_ebitda.loc[name]="N/A"
    num[0]+=1
    for each in data:
        for x in range(len(data[each]),num[0]):
            data[each].append("N/A")
#print(get_stock("AAPL"))
for i in range(stock_list.shape[0]):
    get_stock(i)
'''
price_sales.to_excel("price_sales.xlsx",ignore_index=True)
price_earnings.to_excel("price_earnings.xlsx",ignore_index=True)
price_cashflow.to_excel("price_cashflow.xlsx",ignore_index=True)
price_book.to_excel("price_book.xlsx",ignore_index=True)'''
