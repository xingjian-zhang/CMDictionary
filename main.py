import argparse
import cmd

from rich import print
from rich.emoji import Emoji
from rich.panel import Panel

from myDict import myDictionary

print("Starting...")
d = myDictionary()
welcome = Panel(
    """
        :100: Memorize thousands of english words in [blink]command line[/blink]!
        :sleeping: [blue]Author: jimmyzxj[/blue]

        :fuelpump: Type 'help' for more details on avaliable commands.
        :computer: Visit my [link=https://github.com/xingjian-zhang]Github Page[/link]!
        """,
    title="[red]CM[rgb(255,165,0)]D[rgb(255,255,0)]ictionary",
    width=80
)
print(
    welcome
)

d = myDictionary()


class DictShell(cmd.Cmd):
    prompt = "📚 "

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.n = 0

    def do_ls(self, args):
        """List recent added/updated words.

Usage: ls [options]
Options:
    -l, --length,   <int> Number of words to list.
    -t, --time,     <int> Only list the words added/updated in how many HOURS.
        """
        args = args.split()
        parser = argparse.ArgumentParser()
        parser.add_argument('-l', '--length', type=int, default=None)
        parser.add_argument('-t', '--time', type=int, default=None)
        args = parser.parse_args(args)
        if args.length is None and args.time is None:
            d.list_words(9999999)
        elif args.length is not None and args.time is None:
            d.list_words(9999999, n=args.length)
        elif args.length is None and args.time is not None:
            d.list_words(args.time, n=9999999)
        else:
            d.list_words(args.time, n=args.length)

    def do_rm(self, args):
        """Remove a certain word.

Usage: rm [options]
Options:
    doc_id          <int> Document index of some word to be removed, which can be found in command 'ls'.
    word            <str> Word to be removed.
Notes:
    If neither of 'doc_id' and 'word' are specified, the latest added word will be removed.
    This is equivalent to 'rm -1'.
        """
        if args is not None:
            args = args.split()
            if len(args) == 1:
                d.remove_word(args[0])
            elif len(args) == 0:
                d.remove_word(-1)
            else:
                print(":astonished: rm args number > 1")
                print(self.do_rm.__doc__)

    def do_cr(self, args):
        """Activate card review mode.

Usage: cr [options]
Options:
    -l, --length,   <int> Number of words to be reviewed.
    -t, --time,     <int> Only review the words added/updated in how many HOURS.
    -s, --sleep,    <int> Time interval in seconds before showing next card.
Note:
    Type '^C' to exit the card review mode.
        """
        args = args.split()
        parser = argparse.ArgumentParser()
        parser.add_argument('-l', '--length', type=int, default=None)
        parser.add_argument('-t', '--time', type=int, default=None)
        parser.add_argument('-s', '--sleep', type=int, default=5)
        args = parser.parse_args(args)
        if args.length is None and args.time is None:
            d.card_review(3600, n=9999999, sleep_time=args.sleep)
        elif args.length is not None and args.time is None:
            d.card_review(9999999, n=args.length, sleep_time=args.sleep)
        elif args.length is None and args.time is not None:
            d.card_review(args.time, n=9999999, sleep_time=args.sleep)
        else:
            d.card_review(args.time, n=args.length, sleep_time=args.sleep)

    def do_add(self, args):
        """Add a new word to the dataset.
Usage: add <word> [options]
Arguments:
    word            <str> The word to be added.
Options:
    -f, --force     If flagged, ignore testing the existence of word in English.
        """
        args = args.split()
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--force', action="store_true")
        parser.add_argument('word', type=str)
        args = parser.parse_args(args)
        d.save_word(args.word, args.force)
        self.n += 1
        # add prompt

    def do_whatis(self, args):
        """Search the meaning of a word.
Usage: whatis <word>
Arguments:
    word            <str> The word to be searched.
        """
        args = args.split()
        if len(args) > 0:
            word = args[0]
            d.get_meaning(word)
        # add prompt

    def do_clear(self, args):
        """Clear the screen.
Usage: clear
        """
        d.console.clear()

    def cmdloop(self, intro=None):
        while True:
            try:
                super(DictShell, self).cmdloop(intro="")
                break
            except KeyboardInterrupt:
                print(f"^C\nAdded/Updated {self.n} new words. :running:")
                print("End. Good luck! :thumbs_up::clap::tada:")
                break

    def do_help(self, arg):
        if arg == "":
            print(
                """
    ls      List recent added/updated words.
    rm      Remove a certain word.
    add     Add a new word to the dataset.
    cr      Activate card review mode.
    whatis  Search the meaning of a word.
    clear   Clear the screen.
    ^C      Exit.

    Type 'help <command>' for details on <command>. e.g. 'help cr'.
        """
            )
        else:
            try:
                print(eval(f"self.do_{arg}.__doc__"))
            except AttributeError:
                self.do_whatis(arg)

    def default(self, arg):
        # print(f":astonished: Not supported command: [red]{arg}")
        self.do_add(arg)


shell = DictShell()
shell.cmdloop()
