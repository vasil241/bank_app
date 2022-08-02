from .PersonAbstract import *

class Person(PersonAbstract):

    def __init__(self, name, algorand_account):
        self.name = name
        # holds [algorand account public addr, alogrand account private key]
        self.algorand_account = algorand_account
        # holds the different roles of this person as a dictionary
        self.roles = {}

    def get_name(self):
        return self.name

    def get_account_address(self):
        return self.algorand_account[0]
    
    def get_account_pk(self):
        return self.algorand_account[1]

    def addRole(self, role, role_obj):
        if any(isinstance(x, type(role_obj)) for x in self.roles.values()):
            print("\n" + "{} already has the role {}".format(self.name, role))
            return False
        else:
            self.roles[role] = role_obj
            print("\n" + "\n" + "{} now has the role {}".format(self.name, role))
            return True
    
    def hasRole(self, role):
        if role in self.roles.keys():
            print("\n" + "{} has the role {}".format(self.name, role))
            return True
        else:
            print("\n" + "{} role was not found".format(role))
            return False

    def removeRole(self, role):
        if role in self.roles.keys():
            del self.roles[role]
            print("\n" + "The role {} was successfully removed".format(role))
            return True
        else:
            print("\n" + "Removal failed! {} has no such role".format(self.name))
            return False

    def getRole(self, role):
        if role in self.roles.keys():
            return self.roles[role]
        else:
            print("\n" + "{} has no {} role".format(self.name, role))
            return None

    def getRoles(self):
        if self.roles:
            print("\n" + "{} currently has the roles: ".format(self.name) + ", ".join(self.roles.keys()))
        else:
            print("\n" + "{} has no roles".format(self.name))
        return self.roles
