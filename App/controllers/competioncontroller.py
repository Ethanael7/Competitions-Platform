import csv
from models import Competition

class CompetitionController:
    def __init__(self):
        self.competitions = []

    def view_competitions(self):
        return [comp.get_competition_info() for comp in self.competitions]
    
    def view_competition_results(self, competition_name):
        competition = self.get_competition_by_name(competition_name)
        if competition:
            return competition.get_competition_info()
        return f"No competition named {competition_name}"
    
    def get_competition_name(self, name):
        for competition in self.competitions:
            if competition.name == name:
                return competition
            return None
        
        
        

    