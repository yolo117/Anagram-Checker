import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from snippets import Words
# from Tkinter import *


JINJA_ENVIRONMENT=jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True
)

class Add(webapp2.RequestHandler):
    def split(self, word):
        return [char for char in word]
    def merge(self, word):
        new=''
        for x in word:
            new += x
        return new
    def sort(self, word):
        split_data =self.split(word)
        # print(split_data)
        sorted_alphabets = sorted(split_data)
        # print(sorted_alphabets)
        merged_word = self.merge(sorted_alphabets)
        return merged_word
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        action= self.request.get('search_button')
        message = ''
        Anagram = ''

        user = users.get_current_user()

        searched_string=self.request.get('search_word')
        # print(searched_string)
        lex_word = self.sort(searched_string.lower())
        # sorted_alphabets = sorted(self.split(searched_string.lower()))
        # print(lex_word)
        key_word=user.user_id() + lex_word
        # print(key_word)
        word_key= ndb.Key('Words', key_word)
        word=word_key.get()
        if word == None:
            message= 'Anagram not found'
        else:
            message=''
            Anagram = word.wordsList
        Template_values ={
        'message': message,
        'word': Anagram
        }
        template = JINJA_ENVIRONMENT.get_template('add.html')
        self.response.write(template.render(Template_values))


        # else:
        #     message='enter an anagram and click search'
        #     Template_values ={
        #     'message': message
        #     }
        #     template = JINJA_ENVIRONMENT.get_template('add.html')
        #     self.response.write(template.render(Template_values))





    def post(self):
        action = self.request.get('add_button')
        # print (action)
        user = users.get_current_user()
        add_string=self.request.get('word_input')
        # print(add_string)
        sorted_alphabets = sorted(self.split(add_string.lower()))
        keyword=user.user_id() + self.merge(sorted_alphabets)
        key = ndb.Key('Words', keyword)
        word = key.get()
        if word ==None:
            word = Words(id=keyword)
            word.count_of_words=0

            word.put()

        if action == 'Add':
            string = keyword
            if string == '' or string == None or len(string)<3:
                self.redirect('/add')
                return
            word_doesnt_exists = True
            List = []
            for i in word.wordsList:
                print(i)
                List.append(i)
            print(List.count(add_string))
            if List.count(add_string.lower())>0:
                word_doesnt_exists=False
                print('word exists')
            if(word_doesnt_exists):
                word.wordsList.append(add_string.lower())
                word.count_of_words=word.count_of_words+1
                word.alphabet_no_List.append(len(add_string))
                word.put()

        # Code to read from text document
        # root = Tk()
        # root.fileName = filedialog.askopenfilename(filetypes =(("All text file", "*.txt")))
        dict = []
        f = open("words.txt", "r")
        for line in f.readlines():
            # sorted_word_from_text = self.merge(sorted(self.split(line.strip())))
            #
            if(line.rstrip()):
            #     print (sorted_word_from_text)
                dict.append(line.rstrip())

        print(dict)
        # user = users.get_current_user()
        file_action = self.request.get('add_from_files')
        print (file_action)
        if file_action=='Add':
            print(len(dict))
            for i in dict:
                keyword1=user.user_id() + self.sort(i)
                print(keyword1)
                key = ndb.Key('Words', keyword1)
                word = key.get()
                # print(word)
                new_word = False
                if word!=None:
                    if word.wordsList.count(i)==0:
                        word.wordsList.append(i)
                        word.count_of_words=word.count_of_words+1
                        word.alphabet_no_List.append(len(i))
                        word.put()

                    # word.wordsList.append(i)
                    # word.count_of_words=word.count_of_words+1
                    # word.alphabet_no_List.append(len(i))
                    # word.put()
                else:
                    new_word=True
                if(new_word):
                    word = Words(id=keyword1)
                    print(i + " word is added")
                    word.wordsList.append(i)
                    word.count_of_words=1
                    word.alphabet_no_List.append(len(i))
                    word.put()
                    print(i)
                self.redirect('/add')



        self.redirect('/add')
        # raw_word =self.request.get('word_input')
        # sorted_alphabets = sorted(self.split(raw_word.lower()))
        # user = users.get_current_user()
        # # used as a key to display only certain content to certain
        # keyword =user.user_id()+merge(sorted_alphabets)
        # print(keyword)
        # # if action =='Add':
        #
        #
        #     # use user_id()+ keyword as the key.
        # word_key = ndb.Key('Words', keyword)
        # word = word_key.get()
        #
        # if word==None:
        #     # word = Word(id=keyword)
        #     word.word = raw_word
        #     word.count_of_alphabets = len(raw_word)
        #     word.count_of_words = 1
        #     word.put()
        #     word.word.append(raw_word)
        #     word.put()
        #     self.redirect('/add')
        #
        # else:
        #     word.word.append(raw_word)
        #     word.count_of_alphabets = len(raw_word)
        #     countOfWords = word.count_of_words
        #     word.count_of_words=countOfWords+1
        #     word.put()
        #     self.redirect('/add')
