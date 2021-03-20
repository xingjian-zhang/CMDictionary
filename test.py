from time import sleep
from myDict import myDictionary

d = myDictionary()
for i in range(10):
    d.save_word(str(i))
    sleep(1)

d.list_words(1000)

d.remove_word(-1)

d.list_words(1000)
