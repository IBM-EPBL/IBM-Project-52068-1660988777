
from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re
from markupsafe import escape
conn =ibm_db.connect("DATABASE=bludb;HOSTNAME=0c77d6f2-5da9-48a9-81f8-86b520b87518.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31198;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=hgt43191;PWD=pG1XZqjaI1xcDGA8",'','')

app = Flask(__name__)
app.secret_key ='shreesathyam'

def sub(h,na):
    print(h)
    pd = []
    
    sql = f"SELECT QTY_STOCK FROM product WHERE name='{escape(na)}'"
    stmt = ibm_db.exec_immediate(conn, sql)  
    dict = ibm_db.fetch_both(stmt)
    
    while dict != False:
        pd.append(dict)
        dict = ibm_db.fetch_both(stmt)
    
    for row in pd:
        v=int(row['QTY_STOCK'])
        
    v=v-h
    sql = f"UPDATE product SET QTY_STOCK ={v} WHERE name = '{escape(na)}';"
    ibm_db.exec_immediate(conn, sql)
    
def fetchqs(name):
    pd = []
    
    sql = f"SELECT QUNATITY FROM ADDSALE WHERE name='{escape(name)}'"
    stmt = ibm_db.exec_immediate(conn, sql)  
    dict = ibm_db.fetch_both(stmt)
    
    while dict != False:
        pd.append(dict)
        dict = ibm_db.fetch_both(stmt)
    
    return(pd)

def fetchq(name):
    pd = []
    
    sql = f"SELECT QTY_STOCK FROM product WHERE name='{escape(name)}'"
    stmt = ibm_db.exec_immediate(conn, sql)  
    dict = ibm_db.fetch_both(stmt)
    
    while dict != False:
        pd.append(dict)
        dict = ibm_db.fetch_both(stmt)
    
    return(pd)


def fetch(name):
    pd = []
    
    sql = f"SELECT * FROM product WHERE name='{escape(name)}'"
    stmt = ibm_db.exec_immediate(conn, sql)  
    dict = ibm_db.fetch_both(stmt)
    
    while dict != False:
        pd.append(dict)
        dict = ibm_db.fetch_both(stmt)
        
        
    for row in pd:
        row['DATE_STOCK_IN']='0'
        
    return(pd)

       
        

def fetch(name,cname):
    pd = []
    
    sql = f"SELECT * FROM product WHERE name='{escape(name)}'"
    stmt = ibm_db.exec_immediate(conn, sql)  
    dict = ibm_db.fetch_both(stmt)
    
    while dict != False:
        pd.append(dict)
        dict = ibm_db.fetch_both(stmt)
        
        
    for row in pd:
        row['DATE_STOCK_IN']='0'
        row['CATEGORY_ID']=cname
    
    

    return(pd)

def invtcheck(name,quantity):
    pd = []
    sql = f"SELECT * FROM product WHERE EXISTS(SELECT * FROM product WHERE NAME='{escape(name)}') "
    stmt = ibm_db.exec_immediate(conn, sql)  
    dict = ibm_db.fetch_both(stmt)
    
    while dict != False:
        pd.append(dict)
        dict = ibm_db.fetch_both(stmt)
    
    if pd:
        for row in pd:
            if row['NAME']==name:
                quantity+=int(row['QTY_STOCK'])
                sql = f"UPDATE product SET QTY_STOCK ={quantity} WHERE name = '{escape(name)}';"
                stmt = ibm_db.exec_immediate(conn, sql) 
                return False
    
    return True
        
def setqt(name,prod3):
  for row in prod3:
    if(name==row['NAME']):
      return row['QUNATITY']
    
  return 0

def select():
    prod3=[]
    sql1="select * from addsale"
    stmt1 = ibm_db.exec_immediate(conn, sql1)
        
    dictionary3 = ibm_db.fetch_both(stmt1)
    while dictionary3 != False:
        prod3.append(dictionary3)
        dictionary3 = ibm_db.fetch_both(stmt1)
        
    return fetchinfo(prod3)

def fetchinfo(prod3):
    pd=[]
    total=0
    for row in prod3:
        pd.append(fetch(row['NAME'],row['CNAME']))
    cost=0
    for row in pd:   
        
        for row2 in row:
            row2['QTY_STOCK']=setqt(row2['NAME'],prod3)
            row2['ON_HAND']=row2['PRICE']*row2['QTY_STOCK']
            row2['DATE_STOCK_IN']=int(row2['ON_HAND'])+int(row2['DATE_STOCK_IN'])
            cost=int(row2['DATE_STOCK_IN'])+cost
          
            print(row2['DATE_STOCK_IN'])
            
            

    print(cost)
    return(pd,cost)
        
        




        
    

 
@app.route('/')
def signin():
    return render_template('signin.html')





@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        un = request.form['username']
        pd = request.form['password_1']
        sql = "SELECT * FROM register WHERE username =? AND password_1=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,un)
        ibm_db.bind_param(stmt,2,pd)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid=  account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in successfully !'
            
            return render_template('blog/home.html')
        else:
            msg = 'Incorrect username / password !'
    return render_template('signin.html', msg = msg)

        
@app.route('/accessbackend', methods=['POST','GET'])
def accessbackend():
    mg=''
    if request.method == "POST":
        username=request.form['username']
        email=request.form['email']
        pw=request.form['password'] 
        sql='SELECT * FROM register WHERE email =?'
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        acnt=ibm_db.fetch_assoc(stmt)
        print(acnt)
            
        if acnt:
            mg='Account already exits!!'
            
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mg='Please enter the avalid email address'
        elif not re.match(r'[A-Za-z0-9]+', username):
            ms='name must contain only character and number'
        else:
            insert_sql='INSERT INTO register VALUES (?,?,?,?,?,?)'
            pstmt=ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(pstmt,1,username)
            ibm_db.bind_param(pstmt,2,"firstname")
            ibm_db.bind_param(pstmt,3,"lastname")
            ibm_db.bind_param(pstmt,4,"123456789")
            ibm_db.bind_param(pstmt,5,email)
            ibm_db.bind_param(pstmt,6,pw)
            ibm_db.execute(pstmt)
            mg='You have successfully registered click signin!!'
            return render_template("signin.html")    

            
            
         
    elif request.method == 'POST':
        msg="fill out the form first!"
    return render_template("signup.html",meg=mg)


    

@app.route("/home")
def home():
    p=[]
    p1=[]
    p3=[]
    p4=[]
    
    sql="SELECT COUNT(NAME) FROM PRODUCT;"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        p.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)
    
    sql1="SELECT COUNT(FIRST_NAME) FROM CUSTOMER;"
    stmt = ibm_db.exec_immediate(conn, sql1)
    dictionary1 = ibm_db.fetch_both(stmt)
    while dictionary1 != False:
        p1.append(dictionary1)
        dictionary1 = ibm_db.fetch_both(stmt)
    
    sql2="SELECT COUNT(COMPANY_NAME) FROM SUPPLIER;"
    stmt = ibm_db.exec_immediate(conn, sql2)
    dictionary2= ibm_db.fetch_both(stmt)
    while dictionary2 != False:
        p3.append(dictionary2)
        dictionary2 = ibm_db.fetch_both(stmt)
    
    sql3="SELECT COUNT(FIRST_NAME) FROM REGISTER;"
    stmt = ibm_db.exec_immediate(conn, sql3)
    dictionary3 = ibm_db.fetch_both(stmt)
    while dictionary3 != False:
        p4.append(dictionary3)
        dictionary3 = ibm_db.fetch_both(stmt)
    
    return render_template("blog/home.html",p=p,p1=p1,p3=p3,p4=p4)


@app.route("/customer")
def customer():
    prod = []
       
    sql = "SELECT * FROM customer"
    
    
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
        

    while dictionary != False:
        prod.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)
    
    if prod:
        dictionary=[]
        return  render_template('blog/customer.html', cus= prod)
    else:
        return  render_template('blog/customer.html')




@app.route("/inventory")
def inventrory():
    invet = []
    sql = "SELECT * FROM product;"
    
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        invet.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)
    
    
       
    if invet:
        dictionary=[]
        return  render_template('blog/inventory.html', invet0= invet,)
    else:
        return  render_template('blog/inventory.html')

@app.route("/inventory/<string:name>")
def invetshow(name):
    pd= fetch(name)
    if pd:
        return  render_template('blog/inventory-view.html',prd=pd,name1=name)
    else:
        return  render_template('blog/inventory-view.html')

@app.route("/account")
def acc():
    invet = []
    sql = "SELECT * FROM REGISTER;"
    
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        invet.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)
    
    
       
    if invet:
        dictionary=[]
        return  render_template('blog/account.html', invet0= invet,)
    else:
        return  render_template('blog/account.html')
     
    

@app.route("/tranview/<string:name>")
def tranview(name):
    invet = []
    sql = f"SELECT * FROM salesadd where SUPPLIER_ID='{escape(name)}';"
    
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        invet.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)
        
    
    if invet:
        dictionary=[]
        return  render_template('blog/transcation-view-html.html', invet0= invet)
    else:
        return  render_template('blog/transcation-view-html.html')

    
    
    
@app.route("/transaction")
def transaction():
    invet = []
    sql = "SELECT DISTINCT SUPPLIER_ID FROM salesadd;"
    
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        invet.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)
        
    
    
       
    if invet:
        dictionary=[]
        return  render_template('blog/transaction.html', invet0= invet,)
    else:
        return  render_template('blog/transaction.html')

    
    

@app.route("/supplierup/<string:name>",methods = ['POST', 'GET'])
def supplierup(name):
    if request.method == 'POST':
        sname= request.form['name']
        scity= request.form['city']
        sphno = request.form['phone']
        insert_sql=f"UPDATE SUPPLIER SET COMPANY_NAME='{escape(sname)}', CITY= '{escape(scity)}', PHONE_NUMBER='{escape(sphno)}'  WHERE COMPANY_NAME = '{escape(name)}';"
        prep_stmt=ibm_db.prepare(conn, insert_sql)
        
        ibm_db.execute(prep_stmt)
    return supplier()
    
        
        

@app.route("/supplier")


def supplier():
    
    supp = []
    sql = "SELECT * FROM SUPPLIER;"
    
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        supp.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)  
    return  render_template('blog/supplier.html',supply=supp)


@app.route("/supplieredit/<string:name>")
def supplieredit(name):
    pd=fetch(name)
    sql = f"SELECT * FROM SUPPLIER WHERE COMPANY_NAME='{escape(name)}'"
    stmt = ibm_db.exec_immediate(conn, sql)  
    dict = ibm_db.fetch_both(stmt)
    
    while dict != False:
        pd.append(dict)
        dict = ibm_db.fetch_both(stmt)
    
    if pd:
        return  render_template('blog/suppileredit.html',prd=pd)
    else:
        return  render_template('blog/suppileredit.html')
        
    

@app.route("/suplierdetails/<string:name>")
def supplydetail(name):
    pd = []
    
    sql = f"SELECT * FROM supplier WHERE COMPANY_NAME='{escape(name)}'"
    
    stmt = ibm_db.exec_immediate(conn, sql)  
    dict = ibm_db.fetch_both(stmt)
     
    
    
    
    while dict != False:
      pd.append(dict)
      dict = ibm_db.fetch_both(stmt)
    
   

      
    if pd:
        dict=[]
        return render_template("blog/suplierdetails.html",prd=pd)
    else:
        dict=[]
        return  render_template('blog/suplierdetails.html')


@app.route("/account")
def account():
    return  render_template('blog/account.html')

@app.route("/sales")
def sales():
    prod2 = []    
    prod1 = []    
  
    
    sql = "SELECT DISTINCT name FROM product;" 
    stmt = ibm_db.exec_immediate(conn, sql)
    
    dictionary = ibm_db.fetch_both(stmt)
    
        
    while dictionary != False:
        prod1.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)
    
    
    
    sql1= "SELECT DISTINCT FIRST_NAME FROM CUSTOMER;"
    stmt1 = ibm_db.exec_immediate(conn, sql1)
    dictionary1 = ibm_db.fetch_both(stmt1)
    while dictionary1 != False:
        prod2.append(dictionary1)
        dictionary1 = ibm_db.fetch_both(stmt1)
    # tabel1=select()
    # i=0
    # for row in tabel1:
        
    #     for ro in row:
            
    #         print(i)
    #         i=i+int(ro['PRICE'])
    
    t,c=select()
    return  render_template('blog/sales.html',cname=prod2,detail=prod1,table=t,c=c)

@app.route("/addsale",methods = ['POST', 'GET'])
def addsale():
    if request.method == 'POST':
        prod3=[]
        pname= request.form['name']
        quan= request.form['quantity']
        cust=request.form['cname']
        sql3=f"INSERT INTO addsale(NAME, QUNATITY, CNAME) VALUES(?,?,?)"
        prep_stm=ibm_db.prepare(conn, sql3)
        ibm_db.bind_param(prep_stm, 1, pname)
        ibm_db.bind_param(prep_stm, 2, quan)
        ibm_db.bind_param(prep_stm, 3, cust)
        ibm_db.execute(prep_stm)
        return sales()

@app.route("/salesup")
def salesup():
    t,c=select()
    
    for row in t:
        for row2 in row:
            h=0
            pid=row2['PRODUCT_ID']
            pc=row2['PRODUCT_CODE']
            na=row2['NAME']
            des=row2['DESCRIPTION']
            qt=row2['QTY_STOCK']
            onh=row2['ON_HAND']
            pr=row2['PRICE']
            cat=row2['CATEGORY_ID']
            sup=row2['SUPPLIER_ID']
            da=row2['DATE_STOCK_IN']
            p=fetchqs(na)
            for row in p:
                h=int(row['QUNATITY'])
            sub(h,str(na))
                
            
            sql3="INSERT INTO salesadd(PRODUCT_ID,PRODUCT_CODE,NAME,DESCRIPTION,QTY_STOCK,PRICE,CATEGORY_ID,SUPPLIER_ID,DATE_STOCK_IN,COST) VALUES(?,?,?,?,?,?,?,?,?,?)"
            prep_stm=ibm_db.prepare(conn, sql3)
            ibm_db.bind_param(prep_stm, 1,pid )
            ibm_db.bind_param(prep_stm, 2,pc)
            ibm_db.bind_param(prep_stm, 3,na)
            ibm_db.bind_param(prep_stm, 4,des)
            ibm_db.bind_param(prep_stm, 5,qt)
            ibm_db.bind_param(prep_stm, 6,onh)
            ibm_db.bind_param(prep_stm, 7,pr)
            ibm_db.bind_param(prep_stm, 8,cat)
            ibm_db.bind_param(prep_stm, 9,sup)
            ibm_db.bind_param(prep_stm, 10,da)
            ibm_db.execute(prep_stm)
            
    print(t)
    
    
    sql='DELETE FROM ADDSALE'
    prep_stm=ibm_db.prepare(conn, sql)
    ibm_db.execute(prep_stm)
    
    return render_template('blog/account.html')
    
    

@app.route("/sales/<string:name>",methods = ['POST', 'GET'])
def bill(name):
    # prod2 = []    
    # prod1 = []    
    # sql2 = "SELECT * FROM CATEGORY;" 
    # stmt2 = ibm_db.exec_immediate(conn, sql2)
    # dictionary2 = ibm_db.fetch_both(stmt2)
        
    # while dictionary2 != False:
    #     prod2.append(dictionary2)
    #     dictionary2 = ibm_db.fetch_both(stmt2)
     
    # sql = "SELECT * FROM product;" 
    # stmt = ibm_db.exec_immediate(conn, sql)
    # dictionary = ibm_db.fetch_both(stmt)
        
    # while dictionary != False:
    #     prod1.append(dictionary)
    #     dictionary = ibm_db.fetch_both(stmt)
        
    pd= fetch(name)
    if pd:
        return render_template('blog/sales.html',bill=pd,invet1=prod2,detail=prod1)
    else:
        return render_template('blog/sales.html')
     

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)