import os
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askdirectory
from tkinter import font
import traceback

from heimdall_cl import trace

offset = 0.5

languagefiles = os.listdir("resources/")
available_languages = [languagefile.split(".")[0] for languagefile in languagefiles]

master = Tk()

font = font.Font(family="ms sans serif",size=10)
master.title("Heidall")
master.geometry("800x800")
master.option_add("*Font",font)

inputdir = StringVar()
inputdir.set("No directory selected")

frame_io = LabelFrame(master,text="Input and Output",fg="coral3")
frame_settings = LabelFrame(master,text="Settings",fg="coral3")
frame_io.place(relwidth=1-offset-0.03,relheight=0.96,relx=0.02,rely=0.02)
frame_settings.place(relwidth=offset-0.03,relheight=0.96,relx=1-offset+0.01,rely=0.02)

frame_languages = LabelFrame(master,text="Language Options",relief=GROOVE,fg="coral2")
x_f_languages = 1-offset+0.05
y_f_languages = 0.05
height_languages = 3*0.04+0.04*(len(available_languages)-1)+0.02
frame_languages.place(relwidth=offset-0.1,relheight=height_languages,relx=x_f_languages,rely=y_f_languages)

frame_parameters = LabelFrame(master,text="Hyperparameters",relief=GROOVE,fg="coral2")
x_f_parameters = 1-offset+0.05
y_f_parameters = y_f_languages+height_languages
height_parameters = 0.04+4*0.03+4*0.07+0.04
frame_parameters.place(relwidth=offset-0.1,relheight=height_parameters,relx=x_f_parameters,rely=y_f_parameters)

frame_input = LabelFrame(master,text="Input",relief=GROOVE,fg="coral2")
x_f_input = 0.05
y_f_input = y_f_languages
height_input = 0.3
frame_input.place(relwidth=1-offset-0.09,relheight=height_input,relx=x_f_input,rely=y_f_input)

frame_output = LabelFrame(master,text="Output",relief=GROOVE,fg="coral2")
x_f_output = 0.05
y_f_output = y_f_input + 0.32
height_output = 0.2
frame_output.place(relwidth=1-offset-0.09,relheight=height_output,relx=x_f_output,rely=y_f_output)



label_input_dir = Label(master,text="Input directory:")
label_input_dir.place(relx=x_f_input+0.02,rely=y_f_input+0.04)

inputdir = StringVar()
inputdir.set("No directory selected")
input_dir_text = Entry(master,font=("courier",9))
input_dir_text.insert(0,inputdir.get())
input_dir_text.place(relx=x_f_input+0.02,rely=y_f_input+0.09,relwidth=1-offset-0.13,relheight=0.03)

def browse_input_dir():
    new_input_directory = askdirectory()
    inputdir.set(new_input_directory)
    input_dir_text.delete(0,END)
    input_dir_text.insert(0,inputdir.get())
    input_dir_text.place(relx=x_f_input+0.02,rely=y_f_input+0.09,relwidth=1-offset-0.13,relheight=0.03)

browse_button = Button(master,text="Browse files",command=browse_input_dir,bg="mint cream",relief=GROOVE)
browse_button.place(relx=x_f_input+0.18,rely=y_f_input+0.035)

label_input_format = Label(master,text="File format:")
y_f_format = y_f_input+0.13
label_input_format.place(relx=x_f_input+0.02,rely=y_f_format)

input_format = StringVar()
input_format.set("txt")

label_word_tag = Label(master,text="word tag:")
label_section_tag = Label(master,text="section tag:")
word_tag = Entry(master,font=("courier",9))
word_tag.insert(0,"w")
section_tag = Entry(master,font=("courier",9))
section_tag.insert(0,"line")
tag_files = BooleanVar()
tag_files.set(False)
tag_checkbox = Checkbutton(master,text="tag input files",variable=tag_files)

def check_xml():
    if input_format.get()== "xml":
        label_word_tag.place(relx=x_f_input+0.06,rely=y_f_input+0.20)
        label_section_tag.place(relx=x_f_input+0.06,rely=y_f_input+0.23)
        word_tag.place(relx=x_f_input+0.18,rely=y_f_input+0.2,relwidth=0.21)
        section_tag.place(relx=x_f_input+0.18,rely=y_f_input+0.23,relwidth=0.21)
        tag_checkbox.place(relx=x_f_input+0.06,rely=y_f_input+0.45)
    else:
        label_word_tag.place_forget()
        label_section_tag.place_forget()
        word_tag.place_forget()
        section_tag.place_forget()
        tag_checkbox.place_forget()

for i,f in enumerate(["txt","xml"]):
    b = Radiobutton(master,text=f,variable=input_format,value=f,command=check_xml)
    x_b_def = x_f_input+ 0.15
    y_b_def = y_f_format+i*0.03
    b.place(relx=x_b_def,rely=y_b_def)

label_output_dir = Label(master,text="Output directory:")
label_output_dir.place(relx=x_f_output+0.02,rely=y_f_output+0.04)

outputdir = StringVar()
outputdir.set("No directory selected")
output_dir_text = Entry(master,font=("courier",9))
output_dir_text.insert(0,outputdir.get())
output_dir_text.place(relx=x_f_output+0.02,rely=y_f_output+0.09,relwidth=1-offset-0.13,relheight=0.03)


def browse_output_dir():
    new_output_directory = askdirectory()
    outputdir.set(new_output_directory)
    output_dir_text.delete(0,END)
    output_dir_text.insert(0,outputdir.get())
    output_dir_text.place(relx=x_f_output+0.02,rely=y_f_output+0.09,relwidth=1-offset-0.13,relheight=0.03)

browse_button = Button(master,text="Browse files",command=browse_output_dir,bg="mint cream",relief=GROOVE)
browse_button.place(relx=x_f_output+0.18,rely=y_f_output+0.035)

#################################

label_default_language = Label(master,text="Default language:")
label_default_language.place(relx=x_f_languages+0.02,rely=y_f_languages+0.04)
        
uppercase_languages = [lang.capitalize() for lang in available_languages]
default_lang = StringVar()
default_lang.set(uppercase_languages[0])
b = OptionMenu(master,default_lang,*tuple(uppercase_languages))
#b = apply(OptionMenu, (master,default_lang) + tuple(available_languages))
#for i,language in enumerate(available_languages):
#    w = OptionMenu(master,default_lang,)
#    b = Radiobutton(master,text=language.capitalize(),variable=default_lang,value=language)
#    x_b_def = x_f_languages+0.25
#    y_b_def = y_f_languages+0.04+i*0.03
#    b.place(relx=x_b_def,rely=y_b_def)
x_b_def = x_f_languages+0.19
y_b_def = y_f_languages+0.03
b.place(relx=x_b_def,rely=y_b_def)

label_languages_to_detect = Label(master,text="Languages to detect:")
label_languages_to_detect.place(relx=x_f_languages+0.02,rely=y_b_def+0.05)

active_languages = {}
for i,language in enumerate(available_languages):
    v = IntVar()
    v.set(0)
    c = Checkbutton(master,text=language.capitalize(),variable=v)
    x_c = x_f_languages+0.1
    y_c = y_b_def+0.08+i*0.03
    active_languages[language]=v
    c.place(relx=x_c,rely=y_c)

label_minconf = Label(master,text="Minimum confidence level:")
label_minconf.place(relx=x_f_parameters+0.02,rely=y_f_parameters+0.04)
minconf = DoubleVar()
minconf.set(0.6)
scale_minconf = Scale(master,variable=minconf,from_=0.5,to=0.9,orient="horizontal",resolution=0.05)
scale_minconf.place(relx=x_f_parameters+0.02, rely=y_f_parameters+0.04+1*0.03,relwidth=offset-0.14)

label_maxnoise = Label(master,text="Maximum number of intervening words:")
label_maxnoise.place(relx=x_f_parameters+0.02,rely=y_f_parameters+0.04+1*0.03+1*0.07)
maxnoise = IntVar()
maxnoise.set(1)
scale_maxnoise = Scale(master,variable=maxnoise,from_=0,to=5,orient="horizontal",resolution=1)
scale_maxnoise.place(relx=x_f_parameters+0.02,rely=y_f_parameters+0.04+2*0.03+1*0.07,relwidth=offset-0.14)

label_minseq = Label(master,text="Minimal sequence length:")
label_minseq.place(relx=x_f_parameters+0.02,rely=y_f_parameters+0.04+2*0.03+2*0.07)
minseq = IntVar()
minseq.set(5)
scale_minseq = Scale(master,variable=minseq,from_=3,to=10,orient="horizontal",resolution=1)
scale_minseq.place(relx=x_f_parameters+0.02,rely=y_f_parameters+0.04+3*0.03+2*0.07,relwidth=offset-0.14)

label_logprob = Label(master,text="Logprob threshold:")
label_logprob.place(relx=x_f_parameters+0.02,rely=y_f_parameters+0.04+3*0.03+3*0.07)
logprob = DoubleVar()
logprob.set(2.5)
scale_logprob = Scale(master,variable=logprob,from_=1,to=5,orient="horizontal",resolution=0.5)
scale_logprob.place(relx=x_f_parameters+0.02,rely=y_f_parameters+0.04+4*0.03+3*0.07,relwidth=offset-0.14)


def start():
    settings = {
        "TAG_FILES": tag_files.get(),
        "INPUTDIR": inputdir.get(),
        "OUTPUTDIR": outputdir.get(),
        "RESOURCEDIR": "resources/",
        "INPUT_TYPE": input_format.get(),
        "WORD_MARKER": word_tag.get(),
        "SECTION_MARKER": section_tag.get(),
        "DEFAULT_LANGUAGE": default_lang.get().lower(),
        "LANGUAGES":[language.lower() for (language,activation_var) in active_languages.items() if activation_var.get() == 1],
        "MIN_CONFIDENCE": minconf.get(),
        "MAX_NOISE": maxnoise.get(),
        "MIN_SEQUENCE": minseq.get(),
        "LOGPROB_THRESHOLD": logprob.get(),
        "NORMALIZE": False,
    }
    t = Text(master,font=("courier",9))
    if (settings["DEFAULT_LANGUAGE"] in settings["LANGUAGES"]) or (len(settings["LANGUAGES"]) == 0) :
        t.insert(END,"ERROR: You need to specify at least one language to detect, and none of them can be the default language.")
        t.place(relx=x_start_button,rely=y_start_button+0.1,relheight=height_start_button,relwidth=1-offset-0.09)
    elif (settings["INPUTDIR"] == "No directory selected") or (settings["OUTPUTDIR"] == "No directory selected"):
        t.insert(END,"ERROR: no input or output directory specified.") 
        t.place(relx=x_start_button,rely=y_start_button+0.1,relheight=height_start_button,relwidth=1-offset-0.09)
    else:
        t.insert(END,"Start processing...\n")
        t.place(relx=x_start_button,rely=y_start_button+0.1,relheight=height_start_button,relwidth=1-offset-0.09)
        try:
            trace(settings)
            t.insert(END,"Finished.")
        except Exception as e:
            t.insert(END,"ERROR. Execution stopped.\n")
            t.insert(END,traceback.format_exc())
            t.insert(END, "Error message: %s" % (e))

start_button = Button(master,text="GO!",command=start,bg="steelblue3",relief=GROOVE)
x_start_button = 0.05
y_start_button = y_f_input + 0.55
height_start_button = 0.08
start_button.place(relx=x_start_button,rely=y_start_button,relheight=height_start_button,relwidth=1-offset-0.09)

master.mainloop()
