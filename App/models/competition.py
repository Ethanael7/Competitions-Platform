from App.database import db  

class Competition(db.Model):
        id = db.Column(db.Integer,primary_key=True)
        name = db.Column(db.String,nullable=False,unique=True)
        date = db.Column(db.DateTime, default=datetime.now)
        paticipants = db.Column(db.String,nullable = False)

        def __init__(self,name,date,participants=None):
            self.name = name
            self.date = datetime.strptime(date,"%d-%m-%Y")
            self.participants = participants or []

        def add_participant(self, participant_name):
            self.participant.append(participant_name)

        def get_competition_info(self):
            return{
                'name':self.name,
                'date':self.date.strptime("%d-%m-%Y"),
                'participants': self.participants
            }
