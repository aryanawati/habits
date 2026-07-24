class Task:
    def __init__(self, name):
        self.name = name #task name
        self.row = None
        self.taskframe = None
        self.checkbox = None
        self.checkboxlabel = None #task name label
        self.streak = 0
        self.streaklabel = None
        self.streakStartDate = None
        self.lastStreakUpdateDate = None
        self.streakImgLabel = None
        self.streakImgNotLabel = None
        self.completedToday = False
        self.taskMenu = None
        self.isPinned = False
