from abc import abstractmethod
from .PersonAbstract import *
 
class RoleAbstract(PersonAbstract):

    @abstractmethod
    def __init__(self, person):
        self.person = person

    def get_name(self):
        return self.person.get_name()

    def get_account_address(self):
        return self.person.get_account_address()
    
    def get_account_pk(self):
        return self.person.get_account_pk()

    def addRole(self, role, role_obj):
        self.person.addRole(role, role_obj)
    
    def hasRole(self, role):
        return self.person.hasRole(role)

    def removeRole(self, role):
        self.person.removeRole(role)

    def getRole(self, role):
        return self.person.getRole(role)