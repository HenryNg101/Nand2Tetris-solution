#This module is used for creating and using symbol table`

class Table:
    def __init__(self):
        self.startSubroutine()

    def startSubroutine(self):
        self.table = {'Name':[], 'Type':[], 'Kind':[], '#':[]}

    def define(self, name, type, kind):
        self.table['Name'].append(name)
        self.table['Type'].append(type)
        self.table['Kind'].append(kind)
        self.table['#'].append(self.varcount(kind)-1)

    def varcount(self, kind):
        return self.table['Kind'].count(kind)

    def kindof(self, name):
        if name in self.table['Name']:
            return self.table['Kind'][self.table['Name'].index(name)]
        else:
            return None

    def typeof(self, name):
        if name in self.table['Name']:
            return self.table['Type'][self.table['Name'].index(name)]
        else:
            return None

    def indexof(self, name):
        if name in self.table['Name']:
            return self.table['#'][self.table['Name'].index(name)]
        else:
            return None