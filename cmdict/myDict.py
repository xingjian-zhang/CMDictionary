import os
import re
import time
from random import shuffle

from bs4 import BeautifulSoup
from urllib3 import PoolManager

import arrow
from rich.panel import Panel
from rich import print, box
from rich.console import Console
from rich.table import Table
from tinydb import Query, TinyDB, operations


class myDictionary:
    def __init__(self, width=50):
        self.dir, _ = os.path.split(__file__)
        self.console = Console()
        self.width = width
        self.data_dir = os.path.join(self.dir, ".db")
        os.makedirs(self.data_dir, exist_ok=True)
        self.db = TinyDB(os.path.join(self.data_dir, "db.json"))
        self.q = Query()
        self.load_words()
        self.http = PoolManager()
        self.c = ["n.", "v.", "adj.", "adv.",
                  "prep.", "conj.", "interj.", "vt.", "vi."]

    def load_words(self):
        self.words = set()
        words_file = os.path.join(self.dir, "data", "words.txt")
        with open(words_file) as fp:
            for word in fp.readlines():
                self.words.add(word.strip())

    def get_meaning(self, word):
        # reuse if saved in dataset
        try:
            word_info = self.db.search(self.q.word == word)[0]
            if "meaning" in word_info:
                print(Panel(word_info["meaning"],
                            title=f"[red]{word}", title_align="left", height=20))
                return
        except IndexError:
            pass

        api_url = "http://apii.dict.cn/mini.php?q="
        response = self.http.request('GET', api_url + word.strip())
        soup = BeautifulSoup(response.data, features="html.parser")

        # chinese
        translation = soup.find('div', attrs={'id': 'e'})
        # tense
        tense = soup.find('div', attrs={'id': 't'})
        # sentences
        sentences = soup.find('div', attrs={'id': 's'})

        print_string = "\n"
        if translation:
            tran_text = translation.text
            for t in self.c:
                tran_text = tran_text.replace(t, f"\n[blue]{t}[/blue]")
            print_string += tran_text.strip()
            print_string += "\n\n"
        if tense:
            tense_text = tense.text
            tense_text = re.sub(r'(: [a-zA-Z]+)', r'\1\n', tense_text)
            tense_text = "\n".join([_.strip() for _ in tense_text.split("\n")])
            print_string += tense_text + "\n\n"
        if sentences:
            sentences = re.sub(r'[1-9]. ', '\n', sentences.text).split('\n')
            for sentence in sentences[1:]:
                sentence = sentence.replace(word,
                                            f"[red]{word}[/red]").strip() + "\n\n"
                sentence = re.sub(r'([!\?\.])', r'\1\n', sentence, count=1)
                print_string += sentence
        print_string += "\n" * 20
        self.db.update(operations.set(
            'meaning', print_string), self.q.word == word)
        print(Panel(print_string,
                    title=f"[red]{word}", title_align="left", height=20))

    def save_word(self, word, force=False):
        word = word.strip().lower()
        if force or word in self.words:
            self.get_meaning(word)
            if self.db.search(self.q.word == word):
                self.db.update(operations.set(
                    'time', time.time()), self.q.word == word)
                print(f"[green]{word}[/green] updated.")
                return True
            else:
                self.db.insert({"word": word, "time": time.time()})
                print(f"[green]{word}[/green] saved.")
                return True
        else:
            print(
                f":astonished: [red]{word}[/red] seems not a English word. Type `add {word} -f` to force to save.")
            return False

    def list_words(self, time_delta, n=10):
        time_delta *= 3600
        words = self.db.search((time.time() - time_delta) < self.q.time)
        words = list(map(lambda x: (x.doc_id, x['word'], x['time']), sorted(
            words, key=lambda x: x['time'])))
        table = Table(show_header=True,
                      header_style="bold blue",
                      title="Word List",
                      show_lines=False,
                      box=box.ROUNDED)
        table.add_column("Doc ID", style="dim", width=6)
        table.add_column("Word", width=21, justify="center")
        table.add_column("Last Update", width=20)
        for i, word, timestamp in words[-n:]:
            table.add_row(str(i), word, arrow.get(timestamp).humanize())
        self.console.print(table)

    def remove_word(self, word):
        if type(word) is int:
            try:
                victim = self.db.all()[word]
                self.db.remove(doc_ids=[victim.doc_id])
                print(f"[red]{victim['word']}[/red] removed.")
            except IndexError:
                print(f"#{word} Not Found.")
        elif type(word) is str:
            try:
                victim = self.db.search(self.q.word == word)
                self.db.remove(doc_ids=[victim[0].doc_id])
                print(f"[red]{victim[0]['word']}[/red] removed.")
            except IndexError:
                print(f"[red]{word}[/red] Not Found.")

    def card_review(self, time_delta, n=10, repeat=True, sleep_time=5):
        time_delta *= 3600
        words = self.db.search(
            (time.time() - time_delta) < self.q.time)
        words = list(map(lambda x: x['word'], sorted(
            words, key=lambda x: x['time'])))[-n:]
        try:
            while True:
                shuffle(words)
                for word in words:
                    self.get_meaning(word)
                    time.sleep(sleep_time)
                    print("\n")
                if not repeat:
                    return
        except KeyboardInterrupt:
            print("\n")
            return
