import sqlite3
import time
from crypt import *
from tkinter import *
import random
import datetime

root = Tk()

root.geometry("1280x720")
root.title("Test")
root.config(bg="#5678A9")
register_page = LabelFrame(root)
sign_in_page = LabelFrame(root)
main_page_frame = LabelFrame(root)


def register_page_function():
    """ register page function"""

    global titlepagef, sign_in_page, register_page_image, back_btn_img, tnc_check, error5_img, pw_encrypted

    titlepagef.destroy()
    sign_in_page.destroy()

    username_register = StringVar()
    password_register = StringVar()
    f_name_register = StringVar()
    l_name_register = StringVar()
    e_mail_register = StringVar()
    tnc_check = IntVar()

    register_page = LabelFrame(root, width=1280, height=720)
    register_page.place(x=0, y=0)

    register_page_image = PhotoImage(file="Images/registrationpage.png")
    register_page_background = Label(
        register_page, image=register_page_image, width=1280, height=720
    )
    register_page_background.place(x=-8, y=-5)

    un_entry = Entry(
        register_page, text=username_register, bg="#5A67A8", bd=0, font=13, width=19
    )
    pw_entry = Entry(
        register_page, text=password_register, bg="#5A67A8", bd=0, font=13, width=19
    )
    f_name_entry = Entry(
        register_page, text=f_name_register, bg="#5A67A8", bd=0, font=13, width=19
    )
    l_name_entry = Entry(
        register_page, text=l_name_register, bg="#5A67A8", bd=0, font=13, width=19
    )
    e_mail_entry = Entry(
        register_page, text=e_mail_register, bg="#5A67A8", bd=0, font=13, width=19
    )

    un_entry.place(x=524, y=155)
    pw_entry.place(x=524, y=228)
    f_name_entry.place(x=524, y=298)
    l_name_entry.place(x=524, y=374)
    e_mail_entry.place(x=524, y=447)

    Checkbutton(
        register_page,
        bg="#5A67A8",
        bd=0,
        width=1,
        height=1,
        activebackground="#5A67A8",
        variable=tnc_check,
        onvalue=1,
        offvalue=0,
    ).place(x=512, y=534)

    error_frame = LabelFrame(register_page)
    error_frame.place(x=0, y=0)

    def register_btn():
        """ check eligibility for registration and update database"""

        global error5_img, error3_img, error2_img, error1_img, error4_img, success_register_img

        email_raw = str(e_mail_register.get())
        un_encrypted = str(encrypt(username_register.get(), K))
        pw_encrypted = str(encrypt(password_register.get(), K))
        f_name_encrypted = str(encrypt(f_name_register.get(), K))
        l_name_encrypted = str(encrypt(l_name_register.get(), K))
        e_mail_encrypted = str(encrypt(e_mail_register.get(), K))
        error5_img = PhotoImage(file="Images/error5reg.png")
        error3_img = PhotoImage(file="Images/error3reg.png")
        error1_img = PhotoImage(file="Images/error1reg.png")
        error2_img = PhotoImage(file="Images/error2reg.png")
        error4_img = PhotoImage(file="Images/error4reg.png")

        error1_label = Label(register_page)
        error1_label.destroy()
        error2_label = Label(register_page)
        error2_label.destroy()
        error3_label = Label(register_page)
        error3_label.destroy()
        error4_label = Label(register_page)
        error4_label.destroy()
        error5_label = Label(register_page)
        error5_label.destroy()
        if tnc_check.get() == 0:
            error5_label = Label(register_page, image=error5_img, bg="#5678A9")
            error5_label.place(x=457, y=600)
            valid1 = False
        else:
            valid1 = True

        if len(pw_encrypted) <= 7:
            error3_label = Label(register_page, image=error3_img, bg="#5678A9")
            error3_label.place(x=520, y=564)
            valid2 = False
        else:
            valid2 = True

        if "@" in email_raw and "." in email_raw:
            valid3 = True
        else:
            error2_label = Label(register_page, image=error2_img, bg="#5678A9")
            error2_label.place(x=517, y=580)
            valid3 = False

        a = sqlite3.connect("databases/user_info.db")
        c = a.cursor()
        c.execute("SELECT * FROM user_infos")
        existing_users = c.fetchall()

        valid4 = True
        for user in existing_users:
            usrname = user[0]
            if un_encrypted == usrname:
                error4_label = Label(register_page, image=error4_img, bg="#5678A9")
                error4_label.place(x=558, y=488)
                valid4 = False

        valid5 = True
        for email in existing_users:
            emial = email[4]
            if e_mail_encrypted == emial:
                error1_label = Label(register_page, image=error1_img, bg="#5678A9")
                error1_label.place(x=539, y=509)
                valid5 = False

        if valid1 == valid2 == valid3 == valid4 == valid5 == 1:
            success_register_img = PhotoImage(file="Images/registration_success.png")
            Label(register_page, image=success_register_img, bg="#5678A9").place(
                x=410, y=669
            )
            c.execute(
                "INSERT INTO user_infos VALUES (:username, :password, :first_name, :last_name, :email)",
                {
                    "username": un_encrypted,
                    "password": pw_encrypted,
                    "first_name": f_name_encrypted,
                    "last_name": l_name_encrypted,
                    "email": e_mail_encrypted,
                },
            )
            a.commit()
            a.close()
            b = sqlite3.connect(f"databases/{username_register.get()}.db")
            c = b.cursor()
            c.execute(
                """ CREATE TABLE user_records(
                  cpm integer,
                  accuracy integer,
                  record_count integer,
                  avg_cpm integer
                )"""
            )
    def back_btnnm():
        """takes user back to title page"""

        # sign_in_page.destroy()
        title_function()

    back_btn_img = PhotoImage(file="Images/backbutton.png")

    Button(
        register_page,
        image=back_btn_img,
        bd=0,
        bg="#5678A9",
        activebackground="#5678A9",
        command=back_btnnm,
    ).place(x=29, y=626)

    Button(
        register_page,
        image=register_button_image,
        bg="#5678A9",
        bd=0,
        activebackground="#5678A9",
        command=register_btn,
    ).place(x=526, y=610)


def title_function():
    """ title page function"""
    sign_in_page.destroy()

    global titlepagef, titlepageimage, sign_in_button_image, register_button_image

    titlepageimage = PhotoImage(file="Images/titlepage.png")

    sign_in_button_image = PhotoImage(file="Images/signinbutton.png")

    register_button_image = PhotoImage(file="Images/registerbutton.png")

    titlepagef = LabelFrame(root, width=1280, height=720)
    titlepagef.place(x=0, y=0)

    background = Label(titlepagef, image=titlepageimage, width=1280, height=720)
    background.place(x=-7, y=-3)

    sign_in_button = Button(
        titlepagef,
        image=sign_in_button_image,
        bg="#5678A9",
        width=252,
        height=68,
        borderwidth=0,
        activebackground="#5678A9",
        command=sign_in_page_function,
    )
    sign_in_button.place(x=512, y=262)
    register_button = Button(
        titlepagef,
        image=register_button_image,
        bg="#5678A9",
        width=252,
        height=68,
        borderwidth=0,
        activebackground="#5678A9",
        command=register_page_function,
    )
    register_button.place(x=512, y=342)


def sign_in_page_function():
    """sign in page function"""

    global titlepagef, sign_in_page_image, sign_in_page_background, back_btn_img, sign_error1, sign_error2
    global current_sign_in, username_signin

    titlepagef.destroy()

    username_signin = StringVar()
    username_signin.set("Username")

    password_signin = StringVar()
    password_signin.set("Password")

    sign_in_page = LabelFrame(root, width=1280, height=720)
    sign_in_page.place(x=0, y=0)

    sign_in_page_image = PhotoImage(file="Images/signinpage.png")
    sign_in_page_background = Label(
        sign_in_page, image=sign_in_page_image, width=1280, height=720
    )
    sign_in_page_background.place(x=-3, y=-3)

    def clear_un_sign_in(events):
        """ remove username placeholder after selection"""

        if username_signin.get() == "Username":
            username_signin.set("")

    def clear_password_signin(events):
        """ remove password placeholder after selection"""

        if password_signin.get() == "Password":
            password_signin.set("")

    un_sign_in = Entry(
        sign_in_page, text=username_signin, bg="#5A67A8", bd=0, font=13, width=17
    )
    un_sign_in.place(x=535, y=302)
    un_sign_in.bind("<Button-1>", clear_un_sign_in)

    password_sign_in = Entry(
        sign_in_page,
        text=password_signin,
        bg="#5A67A8",
        bd=0,
        font=13,
        width=17,
        show="*",
    )
    password_sign_in.place(x=535, y=372)
    password_sign_in.bind("<Button-1>", clear_password_signin)

    def back_btnn():
        """takes user back to title page"""

        sign_in_page.destroy()
        title_function()

    back_btn_img = PhotoImage(file="Images/backbutton.png")

    Button(
        sign_in_page,
        image=back_btn_img,
        bd=0,
        bg="#5678A9",
        activebackground="#5678A9",
        command=back_btnn,
    ).place(x=29, y=626)

    def submit_sign_in():
        """ verify sign in details then provide access accordingly"""

        global sign_error1, sign_error2, current_sign_in

        a = sqlite3.connect("databases/user_info.db")
        c = a.cursor()
        c.execute("SELECT * from user_infos")
        existing_users = c.fetchall()

        sign_error1 = PhotoImage(file="Images/signerror1.png")
        sign_error2 = PhotoImage(file="Images/signerror2.png")

        valid_sign_in = False
        password_not_matched = False
        for records in existing_users:
            username_rec = records[0]
            password_rec = records[1]

            if username_rec == encrypt(
                    username_signin.get(), K
            ) and password_rec == encrypt(password_signin.get(), K):
                valid_sign_in = True
                current_sign_in = username_signin.get()

            elif username_rec == encrypt(
                    username_signin.get(), K
            ) and password_rec != encrypt(password_signin.get(), K):
                password_not_matched = True

        if valid_sign_in is True:
            main_page_function()

        if password_not_matched is True and valid_sign_in is False:
            Label(sign_in_page, image=sign_error2, bg="#5678A9").place(x=532, y=442)

        if password_not_matched is False and valid_sign_in is False:
            Label(sign_in_page, image=sign_error1, bg="#5678A9").place(x=549, y=416)

    Button(
        sign_in_page,
        image=sign_in_button_image,
        bd=0,
        bg="#5678A9",
        activebackground="#5678A9",
        command=submit_sign_in,
    ).place(x=555, y=464)


def main_page_function():
    global bg_main_mage, start_button, stop_button, retry_button, stats_button, sign_out_button
    sign_in_page.destroy()
    main_page_frame = LabelFrame(root).place(x=0, y=0)
    bg_main_mage = PhotoImage(file="Images/testpage.png")
    Label(main_page_frame, image=bg_main_mage).place(x=-13, y=0)

    start_button = PhotoImage(file="Images/Start.png")
    stop_button = PhotoImage(file="Images/Stop.png")
    retry_button = PhotoImage(file="Images/Retry.png")
    stats_button = PhotoImage(file="Images/stats.png")
    sign_out_button = PhotoImage(file="Images/Sign Out.png")

    Button(
         main_page_frame,
        image=start_button,
        bd=0,
        bg="#5678A9",
        activebackground="#5678A9",
        command=start_button_click,
    ).place(x=62, y=305)
    Button(
         main_page_frame,
        image=stop_button,
        bd=0,
        bg="#5678A9",
        activebackground="#5678A9",
        command=stop_button_click,
    ).place(x=394, y=305)
    Button(
         main_page_frame,
        image=retry_button,
        bd=0,
        bg="#5678A9",
        activebackground="#5678A9",
        command=retry_button_click,
    ).place(x=695, y=305)
    Button(
         main_page_frame,
        image=stats_button,
        bd=0,
        bg="#5678A9",
        activebackground="#5678A9",
        command=stats_button_click,
    ).place(x=1025, y=305)
    Button(
         main_page_frame,
        image=sign_out_button,
        bd=0,
        bg="#5678A9",
        activebackground="#5678A9",
        command=sign_out_click,
    ).place(x=1110, y=635)


def start_button_click():
    global bg_main_mage, start_button, stop_button, retry_button, stats_button, sign_out_button, entry_entered_texts
    global t_start_time, g_rand_text, entry_entered_text
    main_page_frame = LabelFrame(root)
    main_page_frame.destroy()
    main_page_frame = LabelFrame(root).place(x=0, y=0)
    bg_main_mage = PhotoImage(file="Images/testpage.png")
    Label(main_page_frame, image=bg_main_mage).place(x=-13, y=0)

    start_button = PhotoImage(file="Images/Start.png")
    stop_button = PhotoImage(file="Images/Stop.png")
    retry_button = PhotoImage(file="Images/Retry.png")
    stats_button = PhotoImage(file="Images/stats.png")
    sign_out_button = PhotoImage(file="Images/Sign Out.png")

    Button(
         main_page_frame,
        image=start_button,
        bd=0,
        bg="#5678A9",
        activebackground="#5678A9",
        command=start_button_click,
    ).place(x=62, y=305)
    Button(
         main_page_frame,
        image=stop_button,
        bd=0,
        bg="#5678A9",
        activebackground="#5678A9",
        command=stop_button_click,
    ).place(x=394, y=305)
    Button(
         main_page_frame,
        image=retry_button,
        bd=0,
        bg="#5678A9",
        activebackground="#5678A9",
        command=retry_button_click,
    ).place(x=695, y=305)
    Button(
         main_page_frame,
        image=stats_button,
        bd=0,
        bg="#5678A9",
        activebackground="#5678A9",
        command=stats_button_click,
    ).place(x=1025, y=305)
    Button(
         main_page_frame,
        image=sign_out_button,
        bd=0,
        bg="#5678A9",
        activebackground="#5678A9",
        command=sign_out_click,
    ).place(x=1110, y=635)


    def clear_entry(events):
        """ remove placeholder after selection"""

        if entry_entered_text.get() == "Type Here!":
            entry_entered_text.set("")

    t_start_time = time.time()
    a = "abcdefghijklmnopqrstuvwxyz"
    rand_text = ""
    entry_entered_text = StringVar()
    entry_entered_text.set("Type Here!")
    for i in range(0, 30):
        zz = a[random.randint(0, 25)]
        rand_text = rand_text + zz
    g_rand_text = rand_text
    Label(main_page_frame, text=rand_text, width=85, font=30, bg="#FFF3F3", bd=0, anchor=W).place(x=77, y=175)
    entry_rands = Entry(main_page_frame, text=entry_entered_text, bg="#FFF3F3", bd=0, width=85, font=22)
    entry_rands.place(x=77, y=225)
    entry_rands.bind("<Button-1>", clear_entry)



def stop_button_click():
    global bg_main_mage, start_button, stop_button, retry_button, stats_button, sign_out_button, entry_entered_texts
    global g_rand_text, entry_entered_text
    main_page_frame = LabelFrame(root)
    main_page_frame.destroy()
    main_page_frame = LabelFrame(root).place(x=0, y=0)
    bg_main_mage = PhotoImage(file="Images/testpage.png")
    Label(main_page_frame, image=bg_main_mage).place(x=-13, y=0)

    start_button = PhotoImage(file="Images/Start.png")
    stop_button = PhotoImage(file="Images/Stop.png")
    retry_button = PhotoImage(file="Images/Retry.png")
    stats_button = PhotoImage(file="Images/stats.png")
    sign_out_button = PhotoImage(file="Images/Sign Out.png")

    def entry_text_assign():
        global entry_entered_texts
        entry_entered_texts = entry_entered_text.get()
    entry_text_assign()

    Button(
         main_page_frame,
        image=start_button,
        bd=0,
        bg="#5678A9",
        activebackground="#5678A9",
        command=start_button_click,
    ).place(x=62, y=305)
    Button(
         main_page_frame,
        image=stop_button,
        bd=0,
        bg="#5678A9",
        activebackground="#5678A9",
        command=stop_button_click,
    ).place(x=394, y=305)
    Button(
         main_page_frame,
        image=retry_button,
        bd=0,
        bg="#5678A9",
        activebackground="#5678A9",
        command=retry_button_click,
    ).place(x=695, y=305)
    Button(
         main_page_frame,
        image=stats_button,
        bd=0,
        bg="#5678A9",
        activebackground="#5678A9",
        command=stats_button_click,
    ).place(x=1025, y=305)
    Button(
         main_page_frame,
        image=sign_out_button,
        bd=0,
        bg="#5678A9",
        activebackground="#5678A9",
        command=sign_out_click,
    ).place(x=1110, y=635)
    t_stop_time = time.time()
    time_for_completion = t_stop_time - t_start_time
    characters_per_minute = int((30/time_for_completion)*60)
    error_count = 0
    if len(entry_entered_texts) < 30:
        entry_char_count = len(entry_entered_texts)
        entry_entered_texts = entry_entered_texts + " "*(30-entry_char_count)
    elif len(entry_entered_texts) > 30:
        entry_entered_texts = entry_entered_texts[0:30]
    print(entry_entered_texts)
    print(g_rand_text)
    for lr in range(0, 29):
        if g_rand_text[lr] != entry_entered_texts[lr]:
            error_count += 1
    error_percentage = int((error_count*100)/30)
    accuracy = int(100 - error_percentage)
    a = sqlite3.connect(f'databases/{current_sign_in}.db')
    b = a.cursor()
    b.execute("SELECT * FROM user_records")
    c = b.fetchall()
    if c == []:
        rec_count = 1
        avg_cpm = characters_per_minute
    else:
        g = c[-1]
        rec_count = int(g[2]) + 1
        avg_cpm = int((int(g[3]) + characters_per_minute)/2)
    a.close()
    a = sqlite3.connect(f'databases/{current_sign_in}.db')
    b = a.cursor()
    b.execute(
        "INSERT INTO user_records VALUES(:cpm, :accuracy, :record_count, :avg_cpm)",
        {
            "cpm": characters_per_minute,
            "accuracy": accuracy,
            "record_count": rec_count,
            "avg_cpm": avg_cpm,
        },
    )
    a.commit()
    a.close()
def retry_button_click():
    start_button_click()

def stats_button_click():
    global bg_main_mage, start_button, stop_button, retry_button, stats_button, sign_out_button, back_button_stats, last_rec_noo, last_rec_no
    sign_in_page.destroy()
    main_page_frame = LabelFrame(root).place(x=0, y=0)
    bg_main_mage = PhotoImage(file="Images/stats_page.png")
    back_button_stats = PhotoImage(file="Images/back.png")
    Label(main_page_frame, image=bg_main_mage).place(x=0, y=0)
    Button(
         main_page_frame,
        image=sign_out_button,
        bd=0,
        bg="#5678A9",
        activebackground="#5678A9",
        command=sign_out_click,
    ).place(x=1103, y=31)
    Button(
         main_page_frame,
        image=back_button_stats,
        bd=0,
        bg="#5678A9",
        activebackground="#5678A9",
        command=main_page_function,
    ).place(x=950, y=32)

    file_call = sqlite3.connect(f'databases/{current_sign_in}.db')
    g = file_call.cursor()
    g.execute("SELECT * FROM user_records")
    fetched = g.fetchall()
    n =fetched[-1]
    rec_count = n[2]

    graph_details_label = LabelFrame(main_page_frame, bg="#5678A9").place(x=141, y=220)
    canvas_display = Canvas(graph_details_label, bg="#5678A9", highlightthickness=0)
    canvas_display.place(x=141, y=220, width=1087, height=185)
    canvas_display.config(bg='#5678A9')
    graph_details_label2 = LabelFrame(main_page_frame, bg="#5678A9").place(x=141, y=524)
    canvas_display2 = Canvas(graph_details_label2, bg="#5678A9", highlightthickness=0)
    canvas_display2.place(x=141, y=524, width=1087, height=173)
    canvas_display2.config(bg='#5678A9')
    accur=0
    zzz = fetched[-1]
    avg_cpm=zzz[3]
    if rec_count > 100:
        n = fetched[-100:-1]
        for j in range(0,99):
            curr_rec = n[j]
            canvas_display.create_rectangle((j*10), 173, ((j*10)+3), (185-(curr_rec[0]*0.925)),
                                            outline="#0f0", fill="#0f0")
            canvas_display2.create_rectangle((j*10), 173, ((j*10)+3), (185-(curr_rec[1]*1.85)),
                                            outline="#0f0", fill="#0f0")
            accur += curr_rec[1]
            last_rec_no = curr_rec[2]
        accur = int(accur / last_rec_no)

    else:
        n = fetched
        for i in range(0, rec_count):
            curr_reco = n[i]
            canvas_display.create_rectangle((i*10), 173, ((i*10)+3), (185-(curr_reco[0]*0.925)),
                                            outline="#0f0", fill="#0f0")
            canvas_display2.create_rectangle((i*10), 173, ((i*10)+3), (185-(curr_reco[1]*1.85)),
                                            outline="#0f0", fill="#0f0")
            accur += curr_reco[1]
            last_rec_noo = curr_reco[2]
        accur = int(accur / last_rec_noo)

    Label(main_page_frame, text=accur, bg="#5678A9", font=("Unispace",18)).place(x=204, y=85)
    Label(main_page_frame, text=avg_cpm, bg="#5678A9", font=("Unispace",18)).place(x=157, y=139)


def sign_out_click():
    title_function()



title_function()

root.mainloop()
