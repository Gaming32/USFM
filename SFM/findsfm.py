import grab2
from books import malbookdict

bookdict = {
    '01-GEN': 'Genesis',
    '02-EXO': 'Exodus',
    '03-LEV': 'Leviticus',
    '19-PSA': 'Psalm',
    '23-ISA': 'Isaiah',
    '40-MAT': 'Matthew',
    '41-MRK': 'Mark',
    '42-LUK': 'Luke',
    '43-JHN': 'John',
    '44-ACT': 'Acts',
    '45-ROM': 'Romans',
}

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('book_name', metavar='BOOK')
    parser.add_argument('chapter_verses', metavar='CHAPTER[:LOWER_VERSE[-UPPER_VERSE]]')
    parser.add_argument('tag', metavar='TAG', nargs='?', default='')
    parser.add_argument('-f', '--filename', action='store_true', dest='do_filename', help='Provide a filename instead of a book name')
    parser.add_argument('--no-mt2-headings', action='store_true', dest='no_mt2', help='Do not output \\mt2 headings')
    parser.add_argument('--no-section-headings', action='store_true', dest='no_s', help='Do not output section headings')
    parser.add_argument('--no-v-markings', action='store_true', dest='no_v', help='Do not output \\v markings')
    args = parser.parse_args()

    if not args.do_filename:
        des = args.book_name.lower()
    if ':' in args.chapter_verses:
        chapter, other = args.chapter_verses.split(':')
        if '-' in other:
            lverse, uverse = other.split('-')
            if uverse == '': uverse = 151
        else:
            lverse = uverse = other
    else:
        chapter = args.chapter_verses
        lverse, uverse = 1, 151
    chapter, lverse, uverse = chapter, int(lverse), int(uverse)
    if not args.do_filename:
        for (sfm, real) in bookdict.items():
            if real.lower().startswith(des):
                break
    fname = args.book_name if args.do_filename else '%s.sfm'%sfm
    print(grab2.grab(fname, chapter, lverse, uverse, args.tag,
                     no_mt2=args.no_mt2, no_s=args.no_s, no_v=args.no_v))