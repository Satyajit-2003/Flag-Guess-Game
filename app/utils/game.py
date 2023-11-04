from app.models import get_random_country, set_high_score
import string

class Game:
    def __init__(self, user_id):
        self.user_id = user_id
        self.score = 0
        self.country = None

    def __del__(self):
        set_high_score(self.user_id, self.score)

    def cmp_ans(self, str1, str2):
        translator = str.maketrans('', '', string.whitespace + string.punctuation)
        str1_clean = str1.translate(translator)
        str2_clean = str2.translate(translator)

        return str1_clean.lower() == str2_clean.lower()
    
    def refresh_country(self):
        self.country = get_random_country()
    
    def get_country(self):
        if self.country is None:
            self.refresh_country()
        return self.country
    
    def check_answer(self, answer):
        if self.cmp_ans(answer, self.country.name):
            self.score += 10
            return (True, self.country.name)
        else:
            self.score -= 5
            return (False, self.country.name)
        
    def get_score(self):
        return self.score
    

    
    


    
