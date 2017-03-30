import Calculator
from Constants import VERSION


class CommandList(object):
    """
        A auxiliary class to get fitting commands.
        Interface: lookup(text): Get the commands that begin with text.
                                 The text include cmd args.
    """

    def __init__(self, cmdlist):
        self.lst = cmdlist

    def lookup(self, text):
        ans = reduce(lambda l, s: s.find(text) and l or l + [s],
                     self.lst, [None])
        return ans[1:]


class CommandRunner(object):
    """
        Used to run commands.
        Interface: runcmd(cmdstr): Run the cmd.
    """

    def CMD_help(self, args):
        print('Test help')

    def CMD_version(self, args):
        print('version ' + VERSION)

    def CMD_print(self, args):
        print(args[0])

    def CMD_showall(self, args):
        if Calculator.Calculator.varValue:
            length = 0
            for k in Calculator.Calculator.varValue:
                length = max(length, len(k))
            for (k, v) in Calculator.Calculator.varValue.items():
                print('%s : %g' % ((length - len(k) + 1) * ' ' + k, v))
        else:
            print('No variables.')

    def CMD_init(self, args):
        Calculator.Calculator.varValue.clear()
        print('Ok. All variables are deleted.')

    def __init__(self, cmds):
        self.cmd_list = cmds
        self.last = None

    def runcmd(self, text):
        if len(text) == 1:
            text = self.last
        args = text.split()
        text = args[0]
        args = args[1:]
        if text == None:
            print('There is no last command to perfrom.')
            print('Enter ":help" for help.')
            return
        lst = self.cmd_list.lookup(text[1:])
        if not lst:
            self.last = None
            print('Unknown commend"' + text + '".')
            print('Enter ":help" for help.')
            return
        self.last = text
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
            getattr(self, 'CMD_' + lst[0])(args)
