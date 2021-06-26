import sys
import os
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror
from grab2 import grab
biglen = 15
def makeFormRow(parent, label, width=None, default='', browse=False, extend=False):
    global biglen
    if not width: width = biglen
    width = max(width, len(label))
    if width > biglen: biglen = width
    var = StringVar()
    var.set(default)
    row = Frame(parent)
    lab = Label(row, text=label, relief=RIDGE, width=width)
    ent = Entry(row, relief=SUNKEN, textvariable=var)
    row.pack(fill=X)                                  # uses packed row frames
    lab.pack(side=LEFT)                               # and fixed-width labels
    ent.pack(side=LEFT, expand=YES, fill=X)           # or use grid(row, col)
    if browse:
        btn = Button(row, text='browse...')
        btn.pack(side=RIGHT)
        if not extend:
            btn.config(command=
                 lambda: var.set(askopenfilename() or var.get()) )
        else:
            btn.config(command=
                 lambda: var.set(var.get() + ' ' + askopenfilename()) )
    return var

if __name__ == '__main__':
    win = Tk()
    win.title('SFM Grabber')
    finame =  makeFormRow(win, 'File',        default='631JNRGV.SFM', browse=True)
    chapter = makeFormRow(win, 'Chapter',     default=1)
    lower =   makeFormRow(win, 'Lower Verse', default=1)
    upper =   makeFormRow(win, 'Upper Verse', default=150)
    btn = Button(win, text='Grab')
    btn.pack(expand=YES, fill=X)
    out = ScrolledText(win, state=DISABLED, bg='SystemButtonFace', wrap=WORD)
    out.pack(expand=YES, fill=BOTH)
    def grabcmd(finame=finame, chapter=chapter, lower=lower, upper=upper):
        try:
            value = grab(finame.get(), chapter.get(), int(lower.get()), int(upper.get()))
        except ValueError:
            showerror('grab2', 'ERROR: one of the arguments was not a number.')
        except IndexError:
            showerror('grab2', sys.exc_info()[1])
        else:
            out['state'] = NORMAL
            out.delete('1.0', 'end-1c')
            out.insert('1.0', value)
            out['state'] = DISABLED
    btn['command'] = grabcmd
    win.bind('<Return>', grabcmd)
    #upper.bind('<Return>', grabcmd)
    def save():
        outtxt = out.get('1.0', END)
        vix = outtxt.rfind(r'\v ') + 3
        sfiname = asksaveasfilename(defaultextension='.SFM', initialfile='%s_%s.%s-%s' % (
            os.path.splitext(os.path.basename(finame.get()))[0],
            chapter.get(),
            lower.get(),
            outtxt[vix:outtxt.find(' ', vix)]
        ))
        if sfiname:
            fi = open(sfiname, 'w', encoding='utf-8')
            fi.write(outtxt)
            fi.close()
    Button(win, text='Save', command=save).pack(expand=YES, fill=X)
    win.mainloop()