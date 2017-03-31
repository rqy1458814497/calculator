from Constants import VERSION
import Parser
import ASTVisiter
cmd_list = ['help', 'version', 'showall', 'init', 'showfunc']

variable_table = {}
functions = {}
last = None


def CMD_help(args):
    print('Test help')


def CMD_version(args):
    print('version ' + VERSION)


def CMD_print(args):
    print(args[0])


def CMD_showall(args):
    if variable_table:
        length = 0
        for k in variable_table:
            length = max(length, len(k))
        for (k, v) in variable_table.items():
            print('%s : %s' % ((length - len(k) + 1) * ' ' + k, v))
    else:
        print('No variables.')


def CMD_showfunc(args):
    if functions:
        length = 0
        ans = []
        for k in functions:
            s = k + '('
            if functions[k].arglist:
                s += functions[k].arglist[0]
                for t in functions[k].arglist[1:]:
                    s += ', ' + t
            s += ')'
            length = max(length, len(s))
            ans.append(s)
        for s in ans:
            print(s)
    else:
        print('No functions.')


def CMD_init(args):
    variable_table.clear()
    print('Ok. All variables are deleted.')


def runcmd(text):
    if len(text) == 1:
        text = last
    args = text.split()
    text = args[0]
    args = args[1:]
    if text == None:
        print('There is no last command to perfrom.')
        print('Enter ":help" for help.')
        return
    lst = reduce(lambda l, s: s.find(text[1:]) and l or l + [s],
                 cmd_list, [None])[1:]
    if not lst:
        last = None
        print('Unknown command"' + text + '".')
        print('Enter ":help" for help.')
        return
    last = text
    if len(lst) > 1:
        print('Ambiguous command. You may want:')
        ans = ''
        for i in range(0, len(lst)):
            ans += ' ' + lst[i]
            if len(ans) >= 50:
                print(ans)
                ans = ''
        print(ans)
    else:
        globals()['CMD_' + lst[0]](args)


def main():
    print('A calculator written by RQY at Mar 31, 2017.')
    print('version ' + VERSION)
    try:
        while True:
            try:
                text = raw_input('>>> ')
            except NameError:
                text = input('>>> ')
            if text and not text.isspace():
                text.strip()
                if text[0] == ':':
                    runcmd(text)
                else:
                    try:
                        p = Parser.Parser(text)
                        i = ASTVisiter.Interpreter(p, variable_table, functions)
                        ans = i.interpret()
                        # if ans is not None:
                        # print(ans)
                        # print(p.parse())
                    except Exception, e:
                        print(e.message)
    except EOFError:
        print('')


if __name__ == '__main__':
    main()
