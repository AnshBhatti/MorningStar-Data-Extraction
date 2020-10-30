import tabula
import pandas as pd
df=pd.DataFrame(columns=["Company Name","Ticker","Exchange","Equity Style","Russell Sub-Sector","Russell Industry"])
for page in range(2,34):
    try:
        table=tabula.read_pdf("stock_list-converted.pdf",pages=page)[0]
    except IndexError:
        print("Table undetected: Page "+str(page))
        continue
    company_name=table.columns[0]
    ticker=table.columns[1]
    exchange=table.columns[2]
    equity=table.columns[3]
    sub=table.columns[4]
    ind=table.columns[5]
    for i in range(table.shape[0]):
        name=table.iat[i,0]
        tick=table.iat[i,1]
        exc=table.iat[i,2]
        eqt=table.iat[i,3]
        subs=table.iat[i,4]
        inds=table.iat[i,5]
        if type(tick)!=float:
            new_row={"Company Name":company_name,"Ticker":ticker,"Exchange":exchange,"Equity Style":equity,"Russell Sub-Sector":sub,"Russell Industry":ind}
            company_name=name
            ticker=tick
            exchange=exc
            equity=eqt
            sub=subs
            ind=inds
            df=df.append(new_row,ignore_index=True)
        else:
            if type(name)!=float:
                company_name+=' '+name
            if type(exc)!=float:
                exchange+=' '+exc
            if type(eqt)!=float:
                equity+=' '+eqt
            if type(subs)!=float:
                sub+=' '+subs
            if type(inds)!=float:
                ind+=' '+inds
    new_row={"Company Name":company_name,"Ticker":ticker,"Exchange":exchange,"Equity Style":equity,"Russell Sub-Sector":sub,"Russell Industry":ind}
    df=df.append(new_row,ignore_index=True)
print(df)
