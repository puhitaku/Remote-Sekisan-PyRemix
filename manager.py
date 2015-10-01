class AcquireManager:
    def __init__(self):
        self.user_using = ''

    def set_user_list(self, user_list):
        self.user_list = user_list

    def acquire(self, ip):
        if   self.user_using != '':
            return False
        elif ip in self.user_list:
            self.user_using = self.user_list[ip]
            return True
        else:
            return False

    def free(self, ip):
        if self.user_list[ip] == self.user_using:
            self.user_using = ''
            return True
        else:
            return False
