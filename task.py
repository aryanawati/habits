class Task:
    def __init__(self, name):
        self.name = name #task name
        self.row = None
        self.checkbox = None
        self.streak = 0
        self.streaklabel = None
        self.streakStartDate = None
        self.lastStreakUpdateDate = None
        self.streakImgLabel = None
        self.streakImgNotLabel = None
        self.completedToday = False
        self.taskMenu = None
