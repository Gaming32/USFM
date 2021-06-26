def grab(finame, chapternum, lower, upper, tag='',
        *, no_v=False, no_s=False, no_mt2=False):
    fi = open(finame, encoding='utf-8')

    content = "" # This is here in case \h cannot be found... output some stuff anyway
    for line in fi:
        # Retrives and prints book name and range
        if line.startswith(r'\h'):
            content = (line.rstrip() +' '+tag+'\n' if tag else '')  # applies any tag
            content += content.replace(r'\h','\\mt1')   # copies the line as mt2 and leaves h
            content += line.rstrip().replace("\\h","\\mt2") + f' {chapternum}'  # creates m2
            if upper < 151:
                content += f':{lower}-{upper}'
            content += '\n'
            break

    #content += "\\c " + chapternum + "\n"
    chapters = fi.read().split(r'\c ')
    chapter_dict = {}
    for chapter in chapters:
        chapter_components = chapter.split('\n',1)
        chapter_dict[chapter_components[0]] = chapter_components[1]
    try:
        chapter = r'\c ' + chapter_dict[chapternum]
        verses = chapter.split(r'\v ')
        if no_v:
            for (ix, verse) in enumerate(verses):
                if not verse[0].isdigit(): continue
                verses[ix] = verse.split(' ', 1)[1]
        content += verses[0][3:]
        if not no_v:
            content += r'\v ' + r'\v '.join(verses[lower:upper+1])
        else:
            content += ''.join(verses[lower:upper+1])
    except KeyError:
        if __name__ == '__main__':
            print("ERROR: Chapter", chapternum, "not found in this book.")
            quit()
        else: raise KeyError("Chapter %s not found in this book." % chapternum)
    else:
        split_content = content.rstrip().split('\n')
        final_content = []
        ended = False
        end_check_tuple = ['\\r', '\\p', '\\s']
        other_check_tuple = []
        if no_s:
            other_check_tuple.extend(['\\r', '\\s'])
        if no_mt2:
            other_check_tuple.append('\\mt2')
        end_check_tuple = tuple(end_check_tuple)
        other_check_tuple = tuple(other_check_tuple)
        for i in range(len(split_content)-1, -1, -1):
            line = split_content[i]
            if not ended:
                if line.startswith(end_check_tuple): continue
                else:
                    final_content.append(line)
                    ended = True
                    continue
            else:
                if line.startswith(other_check_tuple): continue
                final_content.append(line)
        return '\n'.join(reversed(final_content)) + '\n'

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
        upper = 151
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