from .exceptions import *
from random import choice

class GuessAttempt(object):
    def __init__(self, letter, hit= False, miss= False):
        if hit == miss:
            raise InvalidGuessAttempt()
        
        self.letter = letter
        self.hit = hit
        self.miss = miss
            
    def is_hit(self):
        return self.hit
        
    def is_miss(self):
        return self.miss


class GuessWord(object):
    def __init__(self, answer):
        self.answer = answer
        self.masked = '*' * len(answer)
        
        if not self.answer:
            raise InvalidWordException()
    
    def perform_attempt(self, character):
        if len(character) > 1:
            raise InvalidGuessedLetterException()
        
        if character.lower() in self.answer.lower():
            masked_list = [char for char in self.masked] 
            
            for index, char in enumerate(self.answer):
                if char.lower() == character.lower():
                    masked_list[index] = character.lower()
            
            self.masked = ''.join(masked_list)
            
            return GuessAttempt(character, hit=True)
        
        return GuessAttempt(character, miss= True)

class HangmanGame(object):
    
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list= WORD_LIST, number_of_guesses=5):
        self.word_list = word_list
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.word = GuessWord(self.select_random_word(word_list))
    
    @classmethod
    def select_random_word(cls, list_of_words):
        if not list_of_words:
            raise InvalidListOfWordsException()
        
        return choice(list_of_words)
    
    def guess(self, character):
        """
        1st: Keep track of previous_guesses
        2nd: self.word is a GuessWord obj that calls the perform_attempt
        method. That method returns a GuessAttempt obj.
        3rd: If guess is incorrect, deduct from remaining_misses
        4th: Check if the game is lossed or won"""
        if self.is_finished():
            raise GameFinishedException()
        
        self.previous_guesses.append(character.lower())
        
        guess_object = self.word.perform_attempt((character)) 
        if self.word.perform_attempt(character).is_miss():
            self.remaining_misses -= 1
            
        if self.is_finished():
            if self.is_won():
                raise GameWonException()
            if self.is_lost():
                raise GameLostException()
            
        return guess_object 
        
    def is_finished(self):
        if self.word.masked == self.word.answer or self.remaining_misses == 0:
            return True
        
    def is_won(self):
        if self.word.masked == self.word.answer:
            return True
        return False
    
    def is_lost(self):
        if self.remaining_misses == 0:
            return True
        return False
