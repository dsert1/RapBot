from urllib.request import urlopen as ureq
from urllib import request
import urllib
import pronouncing
from bs4 import BeautifulSoup as soup
import certifi
import requests
import prettyprinter


def get_words():
    '''reads every word on website and writes to a text file'''
    website = 'https://www.ef.edu/english-resources/english-vocabulary/top-3000-words/'
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

    # request page from server
    request = urllib.request.Request(website, headers={'User-Agent': user_agent})
    response = urllib.request.urlopen(request)

    # save page HTML
    page_html = response.read()

    # parses the HTML
    page_soup = soup(page_html, 'html.parser')

    # finds word list
    containers = page_soup.find('div', {'class': 'field-item even'})
    article = ''
    for i in containers.findAll('p'):
        article = article + '\n' + i.text

    return set(article.split('\n\t')[1:])
def write_to_file(word):
    '''adds input word to a new line of the file
    no return'''
    filename = 'words.txt'
    with open(filename, 'a+') as f:
        f.write('\n' + '\'' + word + '\'' + ',')
        f.close()

def write_all_to_file(word_set):
    '''iterates through a set and writes every word into a file'''
    for word in word_set:
        write_to_file(word)

def text_file_to_set():
    '''reads the contents off a text file and
    turns it into a set of words

    returns a set
    '''
    word_set = set()
    filename = 'words.txt'
    with open(filename, 'r') as f:
        words = f.read()
    words = words.replace(',\n', ' ')
    for word in words.split():
        stripped_word = word.strip('\'')
        word_set.add(stripped_word)
    return word_set


def create_rhyme_set(word):
    '''creates a set of rhyming words off the input word'''

    with open('resources/words2.txt') as f:
        allwords = set(f.read().splitlines())

    def is_word(x):
        return x in allwords

    return {word for word in pronouncing.rhymes(word) if is_word(word)}

def rhyme_words():
    '''
    returns a dictionary - word: {rhyming_words}
    '''
    return {word: create_rhyme_set(word) for word in text_file_to_set() if create_rhyme_set(word)}



if __name__ == '__main__':
    # write_to_file('work')
    # print(get_words())

    # write_all_to_file(get_words())
    print(rhyme_words())
