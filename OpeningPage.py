from tkinter import *
from PIL import Image, ImageTk
import mysql.connector as sql
from tkinter import messagebox
import time
import random


connection = sql.connect(host='localhost',password='husna123@mysql',user='root',database='stock_simulator')

root = Tk()
root.title("Stock Market Simulator")
root.geometry("1280x700+0+0")
bg_img = ImageTk.PhotoImage(file="img.jpg")
background_label = Label(root,image=bg_img).place(x=0,y=0)

def redirect_windowSignUp():
    #root.destroy()
    root_si = Toplevel(root)
    root_si.title("Sign Up")
    root_si.geometry("1280x700+0+0")

    bg_img_s = ImageTk.PhotoImage(file="BGRegister.jpg")
    background_label = Label(root_si,image=bg_img_s).place(x=0,y=0)


    frame = Frame(root_si, bg="white")
    frame.place(x=650,y=150,width=500,height=550)

    title1 = Label(frame, text="Sign Up", font=("Calibri",25,"bold"),bg="white").place(x=20, y=10)
    title2 = Label(frame, text="Join us", font=("Avenir",13),bg="white", fg="gray").place(x=20, y=50)

    f_name = Label(frame, text="First name", font=("Calibri",15,"bold"),bg="white").place(x=20, y=100)
    l_name = Label(frame, text="Last name", font=("Calibri",15,"bold"),bg="white").place(x=240, y=100)

    fname_txt = Entry(frame,font=("arial"))
    fname_txt.place(x=20, y=130, width=200)

    lname_txt = Entry(frame,font=("arial"))
    lname_txt.place(x=240, y=130, width=200)

    email = Label(frame, text="Email", font=("Calibri",15,"bold"),bg="white").place(x=20, y=180)

    email_txt = Entry(frame,font=("arial"))
    email_txt.place(x=20, y=210, width=420)


    password =  Label(frame, text="New password", font=("Calibri",15,"bold"),bg="white").place(x=20, y=260)

    password_txt = Entry(frame,font=("arial"))
    password_txt.place(x=20, y=290, width=420)

    repassword =  Label(frame, text="Re-enter password", font=("Calibri",15,"bold"),bg="white").place(x=20, y=340)

    repassword_txt = Entry(frame,font=("arial"))
    repassword_txt.place(x=20,y=370,width=420)
    

    terms = IntVar()
    terms_and_con = Checkbutton(frame,text="I Agree The Terms & Conditions",variable=terms,onvalue=1,offvalue=0,bg="white",font=("Calibri",12)).place(x=20,y=420)

    def signup_func():
        if fname_txt.get()=="" or lname_txt.get()=="" or email_txt.get()=="" or password_txt.get() == "":
            messagebox.showerror("Error!","Sorry!, All fields are required",parent=root_si)

        elif repassword_txt.get() != password_txt.get():
            messagebox.showerror("Error!","Passwords don't match, please re-enter",parent=root_si)

        elif terms.get() == 0:
            messagebox.showerror("Error!","Please Agree with our Terms & Conditions",parent=root_si)

        else:
            try:
                
                cur=connection.cursor()
                cur.execute("select * from user_signup where Email_Id like '{}';".format(email_txt.get()))
                row=cur.fetchone()

                # Check if th entered email id is already exists or not.
                if row!=None:
                    messagebox.showerror("Error!","The email id is already exists, please try again with another email id",parent=root_si)
                else:
                    cur.execute("insert into user_signup (First_Name,Last_Name,Email_Id,Password) values('{}','{}','{}','{}');".format(fname_txt.get(),lname_txt.get(),email_txt.get(),password_txt.get()))
                    cur.execute("insert into user_profile values ('{}',1000000,1000000);".format(email_txt.get()))
                    cur.execute("insert into trade_data(emailid) values('{}');".format(email_txt.get()))
                    connection.commit()
                    connection.close()
                    messagebox.showinfo("Congratulations!","Registration Successful, Please login.",parent=root_si)
                    if __name__ == "__main__":
                        redirect_windowLogin()
                    

                
            except Exception as es:
                messagebox.showerror("Error HAPPEND!",f"Error due to {es}",parent=root_si)


    signup = Button(frame,text="Sign Up",command=signup_func,font=("consolas",18, "bold"),bd=0,cursor="hand2",bg="blue",fg="white").place(x=120,y=470,width=250)

    root_si.mainloop()

def redirect_windowLogin():
    #root.destroy()
    root_lo = Toplevel(root)
    root_lo.title("Log In - Stock Market Simulatork")
    root_lo.geometry("1280x800+0+0")
    bg_img_l = ImageTk.PhotoImage(file="BGLogin.jpg")
    background_label = Label(root_lo,image=bg_img_l).place(x=0,y=0)


    frame2 = Frame(root_lo, bg = "gray95")
    frame2.place(x=650,y=200,width=600,height=550)
    frame3 = Frame(frame2, bg="white")
    frame3.place(x=40,y=50,width=500,height=450)

    email_label = Label(frame3,text="Email Address", font=("helvetica",20,"bold"),bg="white", fg="gray").place(x=50,y=40)
    email_entry = Entry(frame3,font=("calibri",15,"bold"),bg="white",fg="gray")
    email_entry.place(x=50, y=80, width=300)

    password_label = Label(frame3,text="Password", font=("helvetica",20,"bold"),bg="white", fg="gray").place(x=50,y=120)
    password_entry = Entry(frame3,font=("calibri",15,"bold"),bg="white",fg="gray",show="*")
    password_entry.place(x=50, y=160, width=300)

    def login_func():
        if email_entry.get()=="" or password_entry.get()=="":
            messagebox.showerror("Error!","All fields are required",parent=root_lo)
        else:
            try:
                cur = connection.cursor()
                while True:
                    cur.execute("select * from user_signup where Email_Id like '{}';".format(email_entry.get()))
                    user_data_row = cur.fetchone()
                    if user_data_row == None:
                        messagebox.showerror("Error!","The EMAILID does not exist",parent=root_lo)
                        break
                    cur.execute("select * from user_signup where Email_Id like '{}' and Password like '{}'".format(email_entry.get(),password_entry.get()))
                    user_data_row = cur.fetchone()
                    if user_data_row == None:
                        messagebox.showerror("Error!","EMAILID and PASSWORD don't match!",parent=root_lo)
                        break
                    else:
                        messagebox.showinfo("Success","Login Successful",parent=root_lo)

    #attach code for home here
                        #importing modules
                    
                        from tkinter import ttk
                        from tkinter.ttk import Button,Style
                        import webbrowser

                #making a connection
                        conn = sql.connect(host='localhost',password='husna123@mysql',user='root',database='stock_simulator')
                        if conn.is_connected():
                            print("connection successful")

            #making root window
                        root_h = Toplevel(root_lo)
                        root_h.geometry("1280x700")
                        root_h.title("Home Page")

            #making styles
                        style_button = Style()
                        style_button.configure("B.TButton",font=("consolas",13),bg="white", fg="black",width=12,height=1)
                        style_quit = Style()
                        style_quit.configure("Q.TButton",font=("consolas",10))

                        #making function for quit
                        def quit_page():
                            root_s.destroy()
                        #making function for user_info
                        def user_info_page():
  
                            mycur = connection.cursor()
                            mycur.execute("select * from user_profile where Email_Id like '{}';".format(email_entry.get()))
                            data_alle = mycur.fetchall()
                            data_all = list(data_alle[0])
                            mycur.execute("select * from user_signup where Email_Id like '{}';".format(email_entry.get()))
                            data_profe = mycur.fetchall()
                            data_prof = list(data_profe[0])

                            #making a window
                            root_u = Toplevel(root_h)
                            root_u.geometry("1280x700")
                            root_u.title("Profile Info")

                            #editing the bg
                            img_bge_u = Image.open("user_info_bg.jpg")
                            resize_img_bg_u = img_bge_u.resize((1280,700))
                            img_bg_u = ImageTk.PhotoImage(resize_img_bg_u)

                            #making widgets
                            label_bg_u = Label(root_u,image=img_bg_u)
                            label_bg_u.place(x=0,y=0)

                            name_label_c = Label(root_u,text="Welcome,",fg="black",bg="#EEEEE6",font=("Calibri",20))
                            name_label_c.place(x=150,y=260)
                            name_label = Label(root_u,text=data_prof[0],fg="black",bg="#EEEEE6",font=("Calibri",20))
                            name_label.place(x=270,y=260)

                            current_balance_c = Label(root_u,text="Cash",fg="black",bg="#CDCDB3",font=("Calibri",14))
                            current_balance_c.place(x=150,y=460)
                            current_balance_label = Label(root_u,text=data_all[1],fg="black",bg="#EEEEE6",font=("Calibri",20))
                            current_balance_label.place(x=150,y=490)

                            networth_c = Label(root_u,text="Networth",fg="black",bg="#CDCDB3",font=("calibri",14))
                            networth_c.place(x=150,y=330)
                            networth_label = Label(root_u,text=data_all[2],fg="black",bg="#EEEEE6",font=("calibri",20))
                            networth_label.place(x=150,y=360)

                            #ranking
                            mycur.execute("select Email_Id from user_profile order by Networth;")
                            rank_data = mycur.fetchall()
                            rank=0
                            for i in range (0,len(rank_data)):
                                j = list(rank_data[i])
                                if j[0] == email_entry.get():
                                    rank = i + 1
                                    break
                                else:
                                    continue
                            mycur.execute("select First_Name from user_signup where Email_Id like '{}';".format(email_entry.get())) 

                            label_rank_title = Label(root_u,text=" YOUR RANK",font=(15)).place(x=700,y=270)
                            label_rank = Label(root_u,text=rank,font=(15)).place(x=700,y=300)
                            
                            root_u.mainloop()

                            
                        #making function for trade
                        def trade_page():

                            from tkinter.ttk import Button,Style

                            connection=sql.connect(user="root",host="localhost",password="husna123@mysql",database="stock_simulator")
                            if connection.is_connected:
                                print("connected successfully")

                            mycur=connection.cursor(buffered=True)
                            mycur.execute("Select company_name from company_data;")
                            search_list_data=mycur.fetchall()
                            print(search_list_data)

                            root_t=Toplevel(root_h)
                            root_t.geometry("1280x700+0+0")
                            root_t.title("Trade page")

                            #making a function to get string from the tuple
                            def tup_to_str(a):
                                i = ""
                                for x in range(2,len(a)):
                                    i += a[x]
                                irev = i[::-1]
                                j = ""
                                for x in range (3,len(irev)):
                                    j += irev[x]
                                result = j[::-1]
                                return result

                            #making a function to get string from tuple of another type
                            def tupn_to_str(a):
                                i=""
                                for x in range(1,len(a)):
                                    i += a[x]
                                irev = i[::-1]
                                j = ""
                                for x in range(2,len(irev)):
                                        j += irev[x]
                                result = j[::-1]
                                return result

#making a function to display the name of the company chosen
                            def chosen_show_name():
                                company_name_tup = str(clicked_search.get())
                                company_name = tup_to_str(company_name_tup)
                                name_label.config(text = company_name)

                            def user_input(a):
                                word=str(a)
                                word_s=tup_to_str(word)
                                return word_s
    
#making a function to display the price per stock of the company chosen
                            def chosen_show_price():
                                company_name_tup = str(clicked_search.get())
                                company_name = tup_to_str(company_name_tup)
                                st_price = "select stock_price from company_data where company_name like '{}';"
                                mycur.execute(st_price.format(company_name))
                                com_price = mycur.fetchall()
                                price_label.config(text = tupn_to_str(str(com_price[0])))

#making a function to display the amount of stocks in the company
                            def chosen_show_volume():
                                company_name_tup = str(clicked_search.get())
                                company_name = tup_to_str(company_name_tup)
                                st_volume = "select max_stock from company_data where company_name like '{}';"
                                mycur.execute(st_volume.format(company_name))
                                com_volume = mycur.fetchall()
                                volume_label.config(text = tupn_to_str(str(com_volume[0])))

#making a function to display the cost for all the stocks in the company
                            def chosen_show_volume_price():
                                company_name_tup = str(clicked_search.get())
                                company_name = tup_to_str(company_name_tup)
                                st_volume_price = "select maxstock_price from company_data where company_name like '{}';"
                                mycur.execute(st_volume_price.format(company_name))
                                com_volume_price = mycur.fetchall()
                                volume_price_label.config(text = tupn_to_str(str(com_volume_price[0])))

#making a function for command to run all these functions together
                            def chosen_show_search():
                                name = chosen_show_name()
                                price = chosen_show_price()
                                volume = chosen_show_volume()
                                volume_price = chosen_show_volume_price()

                                return name,price,volume,volume_price

                            def quit_page():
                                root_t.destroy()


                            #making styles
                            style_search = Style()
                            style_search.configure("S.TButton",font=("consolas",10))

                            style_quit = Style()
                            style_quit.configure("Q.TButton",font=("consolas",10))
                            
                            #editing the image
                            img_bge_t = Image.open("trade_bg.png")
                            resize_img_bg_t = img_bge_t.resize((1280,700))
                            img_bg_t = ImageTk.PhotoImage(resize_img_bg_t)

                            #making widgets in root window

                            label_bg = Label(root_t,image=img_bg_t).place(x=0,y=0)
                            drop_down_options_search = search_list_data

                            clicked_search = StringVar()

                            clicked_search.set("Choose the company")

                            drop_menu_search = OptionMenu(root_t,clicked_search,*drop_down_options_search)
                            drop_menu_search.place(x=160,y=251)
                            drop_menu_search.config(width=20)

                            name_title = Label(root_t,text="Name of the company",font=("Calibri",10,"italic"))
                            name_title.place(x=160,y=320)
                            name_label = Label(root_t,text = "Name of the company",background="#BDBDB7",height=1,width=20)
                            name_label.place(x=160,y=350)

                            price_title = Label(root_t,text="Price per stock",font=("Calibri",10,"italic"))
                            price_title.place(x=160,y=410)
                            price_label = Label(root_t,text = "Price per stock",font=("Calibri",10),background="#BDBDB7",height=1,width=15)
                            price_label.place(x=160,y=440)

                            volume_title = Label(root_t,text="Number of stocks",font=("Calibri",10,"italic"))
                            volume_title.place(x=160,y=500)
                            volume_label = Label(root_t,text = "Number of stocks",font=("Calibri",10),background="#BDBDB7",height=1,width=15)
                            volume_label.place(x=160,y=530)

                            volume_price_title = Label(root_t,text="Total stock value",font=("Calibri",10,"italic"))
                            volume_price_title.place(x=160,y=590)
                            volume_price_label = Label(root_t,text = "Total stock value",font=("Calibri",10),background="#BDBDB7",height=1,width=15)
                            volume_price_label.place(x=160,y=620)

                            search_button = Button(root_t,text = "search",command = chosen_show_search,style="S.TButton")
                            search_button.place(x=360,y=255)

                            quit_button = Button(root_t,text="Quit",command = quit_page,style="Q.TButton")
                            quit_button.place(x=1190,y=670)
                            ########################################### 
                            def showSelected():
                                show.config(text=lb.get(ANCHOR))

                            def show_option(a):
                                return a

                            def Confirm_change():
                                name = int(name_Tf.get())
                                mycur.execute("select*from company_data where company_name like '{}';".format(user_input(clicked_search.get())))
                                price_stock = mycur.fetchall()
                                price_stock1 = list(price_stock[0])
                                price = price_stock1[1]
                                name = int(name_Tf.get())
                                money = name*price

                                #BUY BLOCK
                                if show_option(lb.get(ANCHOR))=="BUY":
                                    mycur.execute("update company_data set max_stock = max_stock - {} where company_name like '{}' ; ".format(name,user_input(clicked_search.get())))
                                    print(user_input(clicked_search.get()))
                                    mycur.execute("update user_profile set Current_Balance = Current_Balance - {} where Email_Id like '{}';".format(money,email_entry.get()))
                                    if user_input(clicked_search.get()) == "Apple":
                                        mycur.execute("update trade_data set Apple = Apple + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Microsoft":
                                        mycur.execute("update trade_data set Microsoft = Microsoft + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Google":
                                        mycur.execute("update trade_data set Google = Google + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Amazon":
                                        mycur.execute("update trade_data set Amazon = Amazon + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Tesla":
                                        mycur.execute("update trade_data set Tesla = Tesla + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Johnson&Johnson":
                                        mycur.execute("update trade_data set JohnsonJohnson = JohnsonJohnson + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Visa Inc":
                                        mycur.execute("update trade_data set VisaInc = VisaInc + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Walmart":
                                        mycur.execute("update trade_data set Walmart = Walmart + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Nvidia Corp":
                                        mycur.execute("update trade_data set NvidiaCorp = NvidiaCorp + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Mastercard Incorporated":
                                        mycur.execute("update trade_data set MastercardIncorporated = MastercardIncorporated + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "META platform":
                                        mycur.execute("update trade_data set METAplatform = METAplatform + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Pfizer":
                                        mycur.execute("update trade_data set Pfizer = Pfize + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Pepsico":
                                        mycur.execute("update trade_data set Pepsico = Pepsico + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Costco":
                                        mycur.execute("update trade_data set Costco = Costco + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Oracle Corp":
                                        mycur.execute("update trade_data set OracleCorp = OracleCorp + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Alibaba":
                                        mycur.execute("update trade_data set Alibaba = Alibaba + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Cisco":
                                        mycur.execute("update trade_data set Cisco =Cisco + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Accenture":
                                        mycur.execute("update trade_data set Accenture = Accenture + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Walt Disney Co.":
                                        mycur.execute("update trade_data set WaltDisneyCo = WaltDisneyCo + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Nike":
                                        mycur.execute("update trade_data set Nike = Nike + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Adobe INC":
                                        mycur.execute("update trade_data set AdobeINC = AdobeINC+ {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Morgen Stanley":
                                        mycur.execute("update trade_data set MorgenStanley = MorgenStanley + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Ford Mtr CO":
                                        mycur.execute("update trade_data set FordMtrCO = FordMtrCO + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Qualcomm Incorp":
                                        mycur.execute("update trade_data set QualcommIncorp = QualcommIncorp + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "International Business Machines Corp":
                                        mycur.execute("update trade_data set InternationalBusinessMachinesCorp = InternationalBusinessMachinesCorp + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Netflix":
                                        mycur.execute("update trade_data set Netflix= Netflix + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Intel":
                                        mycur.execute("update trade_data set Intel = Intel + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Starbucks":
                                        mycur.execute("update trade_data set Starbucks = Starbucks + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Boeing":
                                        mycur.execute("update trade_data set Boeing = Boeing + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Citigroup":
                                        mycur.execute("update trade_data set Citigroup = Citigroup + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Paypal":
                                        mycur.execute("update trade_data set Paypal = Paypal + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Target":
                                        mycur.execute("update trade_data set Target = Target + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Airbnb INC ":
                                        mycur.execute("update trade_data set AirbnbINC = AirbnbINC + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Uber Inc":
                                        mycur.execute("update trade_data set UberInc = UberInc + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Monster Corp":
                                        mycur.execute("update trade_data set MonsterCorp = MonsterCorp + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Hershey":
                                        mycur.execute("update trade_data set Hershey = Hershey + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Heinz CO.":
                                        mycur.execute("update trade_data set HeinzCO = HeinzCO + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "Fedex Corp":
                                        mycur.execute("update trade_data set FedexCorp = FedexCorp + {} where emailid like '{}';".format(name,email_entry.get()))
                                    elif user_input(clicked_search.get()) == "McDonalds":
                                        mycur.execute("update trade_data set McDonalds = McDonalds + {} where emailid like '{}';".format(name,email_entry.get()))
                                    connection.commit()
                                #connection.commit()

                                #SELL BLOCK
                                elif show_option(lb.get(ANCHOR))=="SELL":
                                    mycur.execute("update company_data set max_stock = max_stock + {} where company_name like '{}' ; ".format(name,user_input(clicked_search.get())))
                                    mycur.execute("update user_profile set Current_Balance = Current_Balance + {} where Email_Id like '{}';".format(money,email_entry.get()))
                                    
                                    if user_input(clicked_search.get()) == "Apple":
                                        mycur.execute("select Apple from trade_data where emailid like '{}';".format(email_entry.get()))
                                        limit = mycur.fetchone()
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks",parent=root_t)
                                            
                                        else:
                                            mycur.execute("update trade_data set Apple = Apple - {} where emailid like '{}';".format(name,email_entry.get()))
                                            
                                    elif user_input(clicked_search.get()) == "Microsoft":
                                        limit = mycur.execute("select Microsoft from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set Microsoft = Microsoft - {} where emailid like '{}';".format(name,email_entry.get()))
                                    
                                    elif user_input(clicked_search.get()) == "Google":
                                        limit = mycur.execute("select Google from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set Google = Google - {} where emailid like '{}';".format(name,email_entry.get()))
                                            
                                    elif user_input(clicked_search.get()) == "Amazon":
                                        limit = mycur.execute("select Amazon from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set Amazon = Amazon - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Tesla":
                                        limit = mycur.execute("select Tesla from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set Tesla = Tesla - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Johnson&Johnson":
                                        limit = mycur.execute("select Johnson&Johnson from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set Johnson&Johnson = Johnson&Johnson - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Visa Inc":
                                        limit = mycur.execute("select VisaInc from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set VisaInc = VisaInc - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Walmart":
                                        limit = mycur.execute("select Walmart from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set Walmart = Walmart - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Nvidia Corp":
                                        limit = mycur.execute("select NvidiaCorp from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set NvidiaCorp = NvidiaCorp - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Mastercard Incorporated":
                                        limit = mycur.execute("select MastercardIncorporated from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set MastercardIncorporated = MastercardIncorporated - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "META platform":
                                        limit = mycur.execute("select METAplatform from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set METAplatform = METAplatform - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Pfizer":
                                        limit = mycur.execute("select Pfizer from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set Pfizer = Pfizer - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Pepsico":
                                        limit = mycur.execute("select Pepsico from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set Pepsico = Pepsico - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Costco":
                                        limit = mycur.execute("select Costco from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set Costco = Costco - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Oracle Corp":
                                        limit = mycur.execute("select OracleCorp from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set OracleCorp = OracleCorp - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Alibaba":
                                        limit = mycur.execute("select Alibaba from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set Alibaba = Alibaba - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Cisco":
                                        limit = mycur.execute("select Cisco from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set Cisco = Cisco - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Accenture":
                                        limit = mycur.execute("select Accenture from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set Accenture = Accenture - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Walt Disney Co.":
                                        limit = mycur.execute("select WaltDisneyCo from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set WaltDisneyCo = WaltDisneyCo - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Nike":
                                        limit = mycur.execute("select Nike from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set Nike = Nike - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Adobe INC":
                                        limit = mycur.execute("select AdobeINC from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set AdobeINC = AdobeINC - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Morgen Stanley":
                                        limit = mycur.execute("select MorgenStanley from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set MorgenStanley = MorgenStanley - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Ford Mtr CO":
                                        limit = mycur.execute("select FordMtrCO from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set FordMtrCO = FordMtrCO - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Qualcomm Incorp":
                                        limit = mycur.execute("select QualcommIncorp from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set QualcommIncorp = QualcommIncorp - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "International Business Machines Corp":
                                        limit = mycur.execute("select InternationalBusinessMachinesCorp from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set InternationalBusinessMachinesCorp = InternationalBusinessMachinesCorp - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Netflix":
                                        limit = mycur.execute("select Netflix from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set Netflix = Netflix - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Intel":
                                        limit = mycur.execute("select Intel from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set Intel = Intel - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Starbucks":
                                        limit = mycur.execute("select Starbucks from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set Starbucks = Starbucks - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Boeing":
                                        limit = mycur.execute("select Boeing from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set Boeing = Boeing - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Citigroup":
                                        limit = mycur.execute("select Citigroup from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set Citigroup = Citigroup - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Paypal":
                                        limit = mycur.execute("select Paypal from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set Paypal = Paypal - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Target":
                                        limit = mycur.execute("select Target from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set Target = Target - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Airbnb INC":
                                        limit = mycur.execute("select AirbnbINC from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set AirbnbINC = AirbnbINC - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Uber Inc":
                                        limit = mycur.execute("select UberInc from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set UberInc = UberInc - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Monster Corp":
                                        limit = mycur.execute("select MonsterCorp from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set MonsterCorp = MonsterCorp - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Hershey":
                                        limit = mycur.execute("select Hershey from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set Hershey = Hershey - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Heinz CO.":
                                        limit = mycur.execute("select HeinzCO. from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set HeinzCO. = HeinzCO. - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "Fedex Corp":
                                        limit = mycur.execute("select FedexCorp from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set FedexCorp = FedexCorp - {} where emailid like '{}';".format(name,email_entry.get()))

                                    elif user_input(clicked_search.get()) == "McDonalds":
                                        limit = mycur.execute("select McDonalds from trade_data where emailid like '{}';".format(email_entry.get()))
                                        if limit[0] < name:
                                            messagebox.showerror("ERROR","You don't have so many stocks")
                                        else:
                                            mycur.execute("update trade_data set McDonalds = McDonalds - {} where emailid like '{}';".format(name,email_entry.get()))

                                    connection.commit()
                                else:
                                    return messagebox.showerror("ERROR","Choose the activity")
                                mycur.execute("update company_data set maxstock_price=max_stock*stock_price where company_name like '{}';".format(user_input(clicked_search.get())))
                                connection.commit()
                                if clicked_search.get() != "Choose the company":
                                    return messagebox.showinfo('MESSAGE','Your order has been confirmed',parent=root_t)
                                else:
                                    return messagebox.showerror("ERROR","Choose the company")

                            lb = Listbox(root_t)
                            lb.configure(font=("calibri",14),width=8,height=2)
                            lb.place(x=700,y=320)
                            lb.insert(0, 'BUY')
                            lb.insert(1, 'SELL')

                            confirm_button_activity=Button(root_t, text='confirm',style="S.TButton", command=showSelected,width=8)
                            confirm_button_activity.place(x=700,y=440)
                            show = Label(root_t,font=("calibri",14))
                            show.place(x=700,y=400)
                               
                            label_idk=Label(root_t, text="Enter the quantity of stock you want to trade",font=("calibri",14))
                            label_idk.place(x=700,y=490)
                            name_Tf = Entry(root_t)
                            name_Tf.place(x=700,y=520)


                            confirm_trade=Button(root_t, text="confirm",style="S.TButton", command=Confirm_change)
                            confirm_trade.place(x=700,y=570)

                            root_t.mainloop()

                        #making function for search
                        def search_page():

                            #cursor object
                            mycur = conn.cursor()
                            st_name_of_companies = "select company_name from company_data"
                            mycur.execute(st_name_of_companies)
                            data_name = mycur.fetchall()

                            #making window in tk
                            root_s = Toplevel(root_h)
                            root_s.geometry("1280x700")
                            root_s.title("Search page")

                            #making a function to get string from the tuple
                            def tup_to_str(a):
                                i = ""
                                for x in range(2,len(a)):
                                    i += a[x]
                                irev = i[::-1]
                                j = ""
                                for x in range (3,len(irev)):
                                    j += irev[x]
                                result = j[::-1]
                                return result

                            #making a function to get string from tuple of another type
                            def tupn_to_str(a):
                                i=""
                                for x in range(1,len(a)):
                                    i += a[x]
                                irev = i[::-1]
                                j = ""
                                for x in range(2,len(irev)):
                                    j += irev[x]
                                result = j[::-1]
                                return result

    #making a function to display the name of the company chosen
                            def chosen_show_name():
                                company_name_tup = str(clicked_search.get())
                                company_name = tup_to_str(company_name_tup)
                                name_label.config(text = company_name)
        
    #making a function to display the price per stock of the company chosen
                            def chosen_show_price():
                                company_name_tup = str(clicked_search.get())
                                company_name = tup_to_str(company_name_tup)
                                st_price = "select stock_price from company_data where company_name like '{}';"
                                mycur.execute(st_price.format(company_name))
                                com_price = mycur.fetchall()
                                price_label.config(text = tupn_to_str(str(com_price[0])))

    #making a function to display the amount of stocks in the company
                            def chosen_show_volume():
                                company_name_tup = str(clicked_search.get())
                                company_name = tup_to_str(company_name_tup)
                                st_volume = "select max_stock from company_data where company_name like '{}';"
                                mycur.execute(st_volume.format(company_name))
                                com_volume = mycur.fetchall()
                                volume_label.config(text = tupn_to_str(str(com_volume[0])))

    #making a function to display the cost for all the stocks in the company
                            def chosen_show_volume_price():
                                company_name_tup = str(clicked_search.get())
                                company_name = tup_to_str(company_name_tup)
                                st_volume_price = "select maxstock_price from company_data where company_name like '{}';"
                                mycur.execute(st_volume_price.format(company_name))
                                com_volume_price = mycur.fetchall()
                                volume_price_label.config(text = tupn_to_str(str(com_volume_price[0])))

    #making a function for command to run all these functions together
                            def chosen_show_search():
                                name = chosen_show_name()
                                price = chosen_show_price()
                                volume = chosen_show_volume()
                                volume_price = chosen_show_volume_price()

                                return name,price,volume,volume_price

    #making a function for going back to home screen
                            def quit_page_s():
                                root_s.destroy()

    #making styles
                            style_search = Style()
                            style_search.configure("S.TButton",font=("consolas",10))

                            style_quit = Style()
                            style_quit.configure("Q.TButton",font=("consolas",10))

        #resizing image
                            img_bge_s = Image.open("search_bg.jpg")
                            resize_img_bg_s = img_bge_s.resize((1280,700))
                            img_bg_s = ImageTk.PhotoImage(resize_img_bg_s)


        #making widgets in root window
                            label_bg = Label(root_s,image=img_bg_s).place(x=0,y=0)

                            drop_down_options_search = data_name

                            clicked_search = StringVar()

                            clicked_search.set("Choose the company")

                            drop_menu_search = OptionMenu(root_s,clicked_search,*drop_down_options_search)
                            drop_menu_search.place(x=160,y=251)
                            drop_menu_search.config(width=50)

                            name_title = Label(root_s,text="Name of the company",font=("Calibri",10,"italic"))
                            name_title.place(x=200,y=370)
                            name_label = Label(root_s,text = "Name of the company",background="#BDBDB7",height=1,width=30)
                            name_label.place(x=200,y=400)

                            price_title = Label(root_s,text="Price per stock",font=("Calibri",10,"italic"))
                            price_title.place(x=700,y=370)
                            price_label = Label(root_s,text = "Price per stock",font=("Calibri",10),background="#BDBDB7",height=1,width=15)
                            price_label.place(x=700,y=400)

                            volume_title = Label(root_s,text="Number of stocks",font=("Calibri",10,"italic"))
                            volume_title.place(x=200,y=520)
                            volume_label = Label(root_s,text = "Number of stocks",font=("Calibri",10),background="#BDBDB7",height=1,width=15)
                            volume_label.place(x=200,y=550)

                            volume_price_title = Label(root_s,text="Total stock value",font=("Calibri",10,"italic"))
                            volume_price_title.place(x=700,y=520)
                            volume_price_label = Label(root_s,text = "Total stock value",font=("Calibri",10),background="#BDBDB7",height=1,width=15)
                            volume_price_label.place(x=700,y=550)

                            search_button = Button(root_s,text = "search",command = chosen_show_search,style="S.TButton")
                            search_button.place(x=550,y=255)

                            quit_button = Button(root_s,text="Quit",command = quit_page_s,style="Q.TButton")
                            quit_button.place(x=1190,y=670)
                            

                            root_s.mainloop()

#making a function for learn
                        def learn_page():
    #creating window
                            root_l = Toplevel(root_h)
                            root_l.geometry("1280x700")

    #making a function
                            def callback_learn(url):
                                webbrowser.open_new_tab(url)

                            def quit_page_s():
                                root_l_s.destroy()

    #editing the image
                            img_bge_l = Image.open("learn_bg.png")
                            resize_img_bg_l = img_bge_l.resize((1280,700))
                            img_bg_l = ImageTk.PhotoImage(resize_img_bg_l)

                            #making widgets in window
                            label_bg_l = Label(root_l,image=img_bg_l)
                            label_bg_l.place(x=0,y=0)

                            #intro batch
                            link_label_intro1 = Label(root_l,text="Introduction to stocks",font=("Calibri",15),fg="black",bg="#FFFFDA")
                            link_label_intro1.place(x=8,y=200)

                            link_label1 = Label(root_l, text="The Stock Market",font=("consolas",12),fg="blue",bg="#FFFFF8", cursor="hand2")
                            link_label1.place(x=8,y=240)
                            link_label1.bind("<Button-1>",lambda e:callback_learn("https://www.investopedia.com/terms/s/stockmarket.asp"))

                            link_label2 = Label(root_l, text="How does the Stock Market work",font=("consolas",12),fg="blue",bg="#FFFFF8", cursor="hand2")
                            link_label2.place(x=8,y=270)
                            link_label2.bind("<Button-1>",lambda e:callback_learn("https://www.investopedia.com/articles/investing/082614/how-stock-market-works.asp"))

                            link_label3 = Label(root_l, text="Getting to know the Stock exchanges",font=("consolas",12),fg="blue",bg="#FFFFF8", cursor="hand2")
                            link_label3.place(x=8,y=300)
                            link_label3.bind("<Button-1>",lambda e:callback_learn("https://www.investopedia.com/articles/basics/04/092404.asp"))

                            link_label4 = Label(root_l, text="How to buy and sell Stocks",font=("consolas",12),fg="blue",bg="#FFFFF8", cursor="hand2")
                            link_label4.place(x=8,y=330)
                            link_label4.bind("<Button-1>",lambda e:callback_learn("https://www.investopedia.com/ask/answers/108.aspp"))

                            link_label5 = Label(root_l, text="What owning a stock means",font=("consolas",12),fg="blue",bg="#FFFFF8", cursor="hand2")
                            link_label5.place(x=8,y=360)
                            link_label5.bind("<Button-1>",lambda e:callback_learn("https://www.investopedia.com/investing/what-owning-stock-actually-means/"))

                            link_label6 = Label(root_l, text="What is a Penny Stock",font=("consolas",12),fg="blue",bg="#FFFFF8", cursor="hand2")
                            link_label6.place(x=8,y=390)
                            link_label6.bind("<Button-1>",lambda e:callback_learn("https://www.investopedia.com/terms/p/pennystock.asp"))

                            #trading batch
                            link_label_intro2 = Label(root_l,text="Stock Trading Basics",font=("Calibri",15),fg="black",bg="#FFFFDA")
                            link_label_intro2.place(x=600,y=200)

                            link_label7 = Label(root_l, text="When to sell a stock",font=("consolas",12),fg="blue",bg="#FFFFF8", cursor="hand2")
                            link_label7.place(x=600,y=240)
                            link_label7.bind("<Button-1>",lambda e:callback_learn("https://www.investopedia.com/articles/stocks/10/when-to-sell-stocks.asp"))

                            link_label8 = Label(root_l, text="Investing Vs. Trading",font=("consolas",12),fg="blue",bg="#FFFFF8", cursor="hand2")
                            link_label8.place(x=600,y=270)
                            link_label8.bind("<Button-1>",lambda e:callback_learn("https://www.investopedia.com/ask/answers/12/difference-investing-trading.asp"))

                            link_label9 = Label(root_l, text="Income,Value and Growth of Stocks",font=("consolas",12),fg="blue",bg="#FFFFF8", cursor="hand2")
                            link_label9.place(x=600,y=300)
                            link_label9.bind("<Button-1>",lambda e:callback_learn("https://www.investopedia.com/articles/investing/080113/income-value-and-growth-stocks.asp"))

                            link_label10 = Label(root_l, text="Short Selling",font=("consolas",12),fg="blue",bg="#FFFFF8", cursor="hand2")
                            link_label10.place(x=600,y=330)
                            link_label10.bind("<Button-1>",lambda e:callback_learn("https://www.investopedia.com/terms/s/shortselling.asp"))

                            link_label11 = Label(root_l, text="Basics of Order types",font=("consolas",12),fg="blue",bg="#FFFFF8", cursor="hand2")
                            link_label11.place(x=600,y=360)
                            link_label11.bind("<Button-1>",lambda e:callback_learn("https://www.investopedia.com/investing/basics-trading-stock-know-your-orders/"))

                            link_label12 = Label(root_l, text="Executing trades",font=("consolas",12),fg="blue",bg="#FFFFF8", cursor="hand2")
                            link_label12.place(x=600,y=390)
                            link_label12.bind("<Button-1>",lambda e:callback_learn("https://www.investopedia.com/ask/answers/073015/how-do-i-place-order-buy-or-sell-shares.asp"))

                            #research batch
                            link_label_intro3 = Label(root_l,text="Stock Research",font=("Calibri",15),fg="black",bg="#FFFFDA")
                            link_label_intro3.place(x=8,y=450)

                            link_label13 = Label(root_l, text="Stock Fundamentals",font=("consolas",12),fg="blue",bg="#FFFFF8", cursor="hand2")
                            link_label13.place(x=8,y=490)
                            link_label13.bind("<Button-1>",lambda e:callback_learn("https://www.investopedia.com/articles/fundamental/03/022603.asp"))

                            link_label14 = Label(root_l, text="How to become your own stack analyst",font=("consolas",12),fg="blue",bg="#FFFFF8", cursor="hand2")
                            link_label14.place(x=8,y=520)
                            link_label14.bind("<Button-1>",lambda e:callback_learn("https://www.investopedia.com/articles/basics/09/become-your-own-stock-analyst.asp"))

                            link_label15 = Label(root_l, text="Essentials of Analysing stocks",font=("consolas",12),fg="blue",bg="#FFFFF8", cursor="hand2")
                            link_label15.place(x=8,y=550)
                            link_label15.bind("<Button-1>",lambda e:callback_learn("https://www.investopedia.com/financial-edge/0411/5-essential-things-you-need-to-know-about-every-stock-you-buy.aspx"))

                            link_label16 = Label(root_l, text="Fundamental analysis",font=("consolas",12),fg="blue",bg="#FFFFF8", cursor="hand2")
                            link_label16.place(x=8,y=580)
                            link_label16.bind("<Button-1>",lambda e:callback_learn("https://www.investopedia.com/terms/f/fundamentalanalysis.asp"))

                            #options batch
                            link_label_intro3 = Label(root_l,text="Introduction to Options",font=("Calibri",15),fg="black",bg="#FFFFDA")
                            link_label_intro3.place(x=600,y=450)

                            link_label17 = Label(root_l, text="What is an Option",font=("consolas",12),fg="blue",bg="#FFFFF8", cursor="hand2")
                            link_label17.place(x=600,y=490)
                            link_label17.bind("<Button-1>",lambda e:callback_learn("https://www.investopedia.com/terms/o/option.asp"))

                            link_label18 = Label(root_l, text="Essential Options trading guide",font=("consolas",12),fg="blue",bg="#FFFFF8", cursor="hand2")
                            link_label18.place(x=600,y=520)
                            link_label18.bind("<Button-1>",lambda e:callback_learn("https://www.investopedia.com/options-basics-tutorial-4583012"))

                            link_label19 = Label(root_l, text="Basics of Option prices",font=("consolas",12),fg="blue",bg="#FFFFF8", cursor="hand2")
                            link_label19.place(x=600,y=550)
                            link_label19.bind("<Button-1>",lambda e:callback_learn("https://www.investopedia.com/articles/optioninvestor/09/buying-options.asp"))

                            link_label20 = Label(root_l, text="Basics of Options Probability",font=("consolas",12),fg="blue",bg="#FFFFF8", cursor="hand2")
                            link_label20.place(x=600,y=580)
                            link_label20.bind("<Button-1>",lambda e:callback_learn("https://www.investopedia.com/articles/active-trading/091714/basics-options-profitability.asp"))

                            quit_button = Button(root_l,text="Quit",command = quit_page,style="Q.TButton")
                            quit_button.place(x=1000,y=600)

                            root_l.mainloop()


                        #editing image for home
                        bge_img = Image.open("Home.jpeg")
                        resize_bg_img = bge_img.resize((1280,700))
                        bg_img = ImageTk.PhotoImage(resize_bg_img)
                        background_label = Label(root_h,image=bg_img).place(x=0,y=0)
                        imge = Image.open("home_page_pic.jpg")
                        resize_image = imge.resize((375,400))
                        img_pic = ImageTk.PhotoImage(resize_image)

                        #home page frame
                        frame = Frame(root_h, bg="#C2C2C2")
                        frame.place(x=150,y=200,width=950,height=450)

                        cap_label = Label(frame,text="") #da quote

                        title1 = Button(frame, text="User Info",style="B.TButton",command=user_info_page).place(x=20, y=150)
                        title2 = Button(frame, text="Trade",style="B.TButton",command=trade_page).place(x=20, y=200)
                        title3 = Button(frame, text="Search",style="B.TButton",command=search_page)
                        title3.place(x=20, y=250)
                        title4 = Button(frame, text="Learn",style="B.TButton",command=learn_page)
                        title4.place(x=20, y=300)

                        img_label = Label(frame, image = img_pic)
                        img_label.place(x=400,y=25)

                        quit_button = Button(root_h,text="Quit",command = quit_page,style="Q.TButton")
                        quit_button.place(x=1000,y=600)

                        root.mainloop()


            except Exception as e:
                messagebox.showerror("Error!",f"Error due to {str(e)}",parent=root_lo)
                
#================Buttons===================
    login_button = Button(frame3,text="Log In",command=login_func,font=("consolas",15, "bold"),bd=0,cursor="hand2",bg="blue",fg="white").place(x=50,y=200,width=300)
     
    root_lo.mainloop()

frame1 = Frame(root, bg="white")
frame1.place(x=400,y=400,width=150,height=50)
frame2 = Frame(root, bg="white")
frame2.place(x=900,y=400,width=100,height=50)
title1 = Button(frame1, text="Register",command=redirect_windowSignUp, font=("consolas",14),bg="white",fg="black",width=13,height=1,bd=1).place(x=6, y=6)
title2 = Button(frame2, text="Login", command=redirect_windowLogin, font=("consolas",14),bg="white", fg="black",width=8,height=1,bd=2).place(x=5, y=6)
     
root.mainloop()
