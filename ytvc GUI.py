from tkinter import *
import tkinter.messagebox as ms
from tkinter.font import Font
from PIL import ImageTk, Image
from bs4 import BeautifulSoup
import urllib.request
from pytube import YouTube
import time

def SearchVid(search):

    global main_data

    main_data = {}
    vid_id = 0

    search.replace(" ", "+")
    responce = urllib.request.urlopen('https://www.youtube.com/results?search_query='+search+'&gl=GB')

    soup = BeautifulSoup(responce,'html.parser')    
    divs = soup.find_all("div", { "class" : "yt-lockup-content"})

    if len(divs)==0:
        return 'failed to request'

    for i in divs:
        href= i.find('a', href=True)
        if len(list(href.text))>30:
            href2 = ''.join(list(i.find('a', href=True).text)[:30])+'...'
        else:
            href2 = ''.join(list(i.find('a', href=True).text))
        uploader= i.find('a', { "class" : "yt-uix-sessionlink spf-link"}, href=True)
        desc = i.find('div', { "class" : "yt-lockup-description yt-ui-ellipsis yt-ui-ellipsis-2"})
        if len("https://www.youtube.com"+href['href'])==43 :
            try:
                main_data[str(vid_id)] = {
                    'url' : "https://www.youtube.com"+href['href'],
                    'title' : href2,
                    'uploader' : uploader.text,
                    'description' :desc.text,
                    }
                vid_id +=1
            except:
                pass

def download_vid(vidid_to_download, result):

    if int(vidid_to_download)<=len(result):
        url_to_download = result[vidid_to_download]['url']
        yt = YouTube(url_to_download).streams.first()
        yt.download()
        ms.showinfo('video download','Video download completed')
        root.destroy()
        quit

root = Tk()
root.geometry('450x300')
root.config(bg='#252525')
root.resizable(False,False)
root.title('YouTube Video Downloader')
root.iconbitmap('icon.ico')

global titlefont
global inputfont
global buttonfont
global framefont
global instrufont

frameFont = Font(size=20, family='Bahnschrift Light')
inputfont = Font(size=20, family='Bahnschrift Light')
titlefont = Font(size=20, family='Consolas')
buttonfont = Font(size=15, family='Bahnschrift SemiBold')
instrufont = Font(size=20, family='Bahnschrift SemiLight')

mainicon = ImageTk.PhotoImage(Image.open("mainicon.png"))

def searchvideo():

    def proceed():
        
        proceedid = str(int(id_search_input.get()))
        download_vid(proceedid, main_data)
    
    search_keyword = search_input.get()
    print(search_keyword)
    if search_keyword == '' or search_keyword == 'keyword here':
        ms.showwarning('WARNING', 'Don\'t left the search box blank!')
    else:
        try:
            SearchVid(search_keyword)
            searchframe.place_forget()
            search_input.place_forget()
            submitbuttoninputframe.place_forget()
            submit_button.place_forget()
            quitbuttoninputframe.place_forget()
            quit_button.place_forget()

            root.geometry('920x500')

            def id_on_click(event):
                id_search_input.configure(state=NORMAL)
                id_search_input.delete(0, END)
                id_search_input.unbind('<Button-1>', id_on_click_id)

            def limiturlinput(*args):
                value = id_search_input.get()
                if value == 'ID':
                    proceed_btn.place_forget()
                    proceed_btn.config(state=DISABLED)
                    proceed_btn.place(x=361,y=401)
                if len(value) < 2:
                    proceed_btn.place_forget()
                    proceed_btn.config(state=DISABLED)
                    proceed_btn.place(x=361,y=401)
                if len(value) >= 2:
                    videoinput_id.set(value[:2])
                    proceed_btn.place_forget()
                    proceed_btn.config(state=NORMAL)
                    proceed_btn.place(x=361,y=401)
                if value != '' and value != 'ID':
                    try: videoinput_id.set(str(len(main_data)-1)) if int(value) > len(main_data) else videoinput_id
                    except: videoinput_id.set(value[:0])
                else:
                    proceed_btn.place_forget()
                    proceed_btn.config(state=DISABLED)
                    proceed_btn.place(x=361,y=401)

            def pbutton_on_enter(e):
                proceed_btn['background'] = '#565656'
                proceed_btn['fg'] = 'white'

            def pbutton_on_leave(e):
                proceed_btn['background'] = '#252525'
                proceed_btn['fg'] = 'white'

            videoinput_id = StringVar()
            videoinput_id.trace('w', limiturlinput)

            title.place_forget()
            titleicon.place_forget()
            scrollbar = Scrollbar(root)
            titleshowframe = Frame(root, width=876, height=108,background = '#00FFFF', borderwidth = 1, relief = FLAT)
            mylist = Listbox(root, yscrollcommand=scrollbar.set, selectmode=BROWSE, highlightthickness=0, selectbackground='#252525',selectborderwidth=0, width=58, fg='white', relief=FLAT, height=3, font=frameFont, bg='#252525')
            scrollbar.config(command=mylist.yview)

            try:
                for i in range(len(main_data)-1):
                    if i <10:
                        mylist.insert(END, ('  ID:                 '+'0'+str(i)))
                    else:
                        mylist.insert(END, ('  ID:                 '+str(i)))
                    mylist.insert(END, ('  title:              '+main_data[str(i)]['title']))
                    mylist.insert(END, ('  uploader:     '+main_data[str(i)]['uploader']))
                    mylist.insert(END,'\n')
                mylist.insert(END, ('  ID:                 '+str(len(main_data)-1)))
                mylist.insert(END, ('  title:              '+main_data[str(len(main_data)-1)]['title']))
                mylist.insert(END, ('  uploader:     '+main_data[str(len(main_data)-1)]['uploader']))
            except:
                ms.showwarning('ERROR', 'some error happened. Please restart your program')
                root.destroy()

            instrulabel = Label(root, font = instrufont, bg='#252525', fg='white', text='Scroll on the listbox above to explore the search results\nEnter the video id into entry below and press proceed')
            id_searchframe = Frame(root, width=409, height=62,background='#00FFFF', borderwidth=1)
            id_search_input = Entry(root, textvariable=videoinput_id, disabledbackground='#252525', font=inputfont, borderwidth=0, fg='white', bg='#252525', relief=FLAT, justify=CENTER, width=27)
            id_search_input.config(insertbackground='white')
            pbuttoninputframe = Frame(root, width=204.45, height=52.45, background='#00FFFF', borderwidth=1.45)


            proceed_btn = Button(root,
                activebackground='#565656',
                command=proceed,
                activeforeground='white',
                fg='white',
                text='PROCEED',
                state=DISABLED,
                font=buttonfont,
                padx=50,
                pady=5,
                bg='#252525',
                relief=FLAT)

            titleicon.place(x=245,y=15)
            title.place(x=295,y=20)
            titleshowframe.place(x=20, y=79)
            mylist.place(x=22,y=81)
            instrulabel.place(x=110, y=210)
            id_searchframe.place(x=255,y=300)
            id_search_input.place(x=256,y=301, height=60)
            id_search_input.insert(0, 'ID')
            id_search_input.configure(state=DISABLED)
            id_on_click_id = id_search_input.bind('<Button-1>', id_on_click)
            pbuttoninputframe.place(x=360,y=400)
            proceed_btn.place(x=361,y=401)
            proceed_btn.bind("<Enter>", pbutton_on_enter)
            proceed_btn.bind("<Leave>", pbutton_on_leave)
        except:
            raise
            ms.showwarning('KEYWORD ERROR','Invalid Keyword!')

def main_menu():
    global mainicon
    global search_input
    global searchframe
    global search_input
    global submitbuttoninputframe
    global submit_button
    global quitbuttoninputframe
    global quit_button
    global title
    global titleicon

    def button_on_enter(e):
        submit_button['background'] = '#565656'
        submit_button['fg'] = 'white'

    def button_on_leave(e):
        submit_button['background'] = '#252525'
        submit_button['fg'] = 'white'

    def quitbutton_on_enter(e):
        quit_button['background'] = '#565656'
        quit_button['fg'] = 'white'

    def quitbutton_on_leave(e):
        quit_button['background'] = '#252525'
        quit_button['fg'] = 'white'

    def on_click(event):
        search_input.configure(state=NORMAL)
        search_input.delete(0, END)
        search_input.unbind('<Button-1>', on_click_id)

    def quitmenu():
        root.destroy()
        quit()
    
    titleicon = Label(root, image=mainicon,bg = '#252525')
    title = Label(root, text='Youtube Video Downloader', fg='white', bg='#252525', font=titlefont)
    searchframe = Frame(root, width=409, height=47,background='#00FFFF', borderwidth=1)
    search_input = Entry(root, disabledbackground='#252525', font=inputfont, borderwidth=0, fg='white', bg='#252525', relief=FLAT, justify=CENTER, width=27)
    search_input.config(insertbackground='white')
    submitbuttoninputframe = Frame(root, width=193.45, height=52.45, background='#00FFFF', borderwidth=1.45)
    submit_button = Button(
        root,
        command=searchvideo,
        activebackground='#565656',
        activeforeground='white',
        fg='white',text='SEARCH',
        font=buttonfont,
        padx=50,
        pady=5,
        bg='#252525',
        relief=FLAT)
    
    quitbuttoninputframe = Frame(root, width=193.45, height=52.45, background='#00FFFF', borderwidth=1.45)
    quit_button = Button(
        root,
        activebackground='#565656',
        activeforeground='white',
        command=quitmenu,
        fg='white',
        text='QUIT',
        font=buttonfont,
        padx=67,
        pady=5,
        bg='#252525',
        relief=FLAT)

    titleicon.place(x=10,y=15)
    title.place(x=70,y=20)
    searchframe.place(x=20,y=100)
    search_input.place(x=21,y=101, height=45)
    submitbuttoninputframe.place(x=125,y=170)
    submit_button.place(x=126.45,y=171.45)
    quitbuttoninputframe.place(x=125,y=230)
    quit_button.place(x=126.45,y=231.45)
    submit_button.bind("<Enter>", button_on_enter)
    submit_button.bind("<Leave>", button_on_leave)
    search_input.insert(0, 'keyword here')
    search_input.configure(state=DISABLED)
    on_click_id = search_input.bind('<Button-1>', on_click)
    quit_button.bind("<Enter>", quitbutton_on_enter)
    quit_button.bind("<Leave>", quitbutton_on_leave)
    
main_menu()

root.mainloop()
