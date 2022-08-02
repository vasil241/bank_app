from abc import ABC, abstractmethod
 
class PersonAbstract(ABC):

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_account_address(self):
        pass
    
    @abstractmethod
    def get_account_pk(self):
        pass

    @abstractmethod
    def addRole(self, role, role_obj):
        pass
    
    @abstractmethod
    def hasRole(self, role):
        pass

    @abstractmethod
    def removeRole(self, role):
        pass

    @abstractmethod
    def getRole(self, role):
        pass