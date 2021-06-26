def grab(finame, chapternum, lower, upper):
    fi = open(finame, encoding='utf-8')

    content = "" # This is here in case \h cannot be found... output some stuff anyway
    for cnt,line in enumerate(fi):
        # Retrives and prints book name
        if line.find(r'\h') == 0:
            content = line
            break

    content += "\\c " + str(chapternum) + "\n"

    try:
        chapter = r'\c ' + fi.read().split(r'\c ')[chapternum]
        content += r'\v ' + r'\v '.join(
            chapter.split(r'\v ')[lower:upper + 1])
    except IndexError:
        if __name__ == '__main__':
            print("ERROR: Chapter", chapternum, "not found in this book.")
            quit()
        else: raise IndexError("ERROR: Chapter %s not found in this book." % chapternums)
    else: return content

if __name__ == '__main__':
    import sys

    def syntax():
        print('Usage:\n\t%s <chapter> [[start-verse] [end-verse]] [file]' % sys.argv[0])
        print('Examples:')
        print('\tTo get all of Chapter 1:')
        print('\t  %s 1\n' % sys.argv[0])
        print('\tTo get Chapter 1, verses 1 through 10:')
        print('\t  %s 1 1 10' % sys.argv[0])
        quit()

    if len(sys.argv) < 2:
        syntax()
    elif len(sys.argv) < 4:
        lower = 1
        upper = 150
    else:
        try:
            lower      = int(sys.argv[2])
            upper      = int(sys.argv[3])
        except:
            print("ERROR: one of the arguments was not a number.\n")
            syntax()

    try:
        chapternum = int(sys.argv[1])
    except:
        print("ERROR: one of the arguments was not a number.\n")
        syntax()

    finame = (len(sys.argv) > 4 and sys.argv[4]) or '631JNRGV.SFM'
    content = grab(finame, chapternum, lower, upper)
    print(content)
    