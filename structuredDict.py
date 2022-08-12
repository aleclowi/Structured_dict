#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 00:00:00 2022

@author: Alec Lowi
"""


class StructuredDict:
    def __init__(self, d):
        self.__check(d) # UNCOMMENT THIS
        self.__d = d

    def __str__(self):
        return str(self.__d)

    def __repr__(self):
        return repr(self.__d)

    def __len__(self):
        return len(self.__d)

    # DEFINE THIS
    def __contains__(self, item):
        for j in self.__d:
            if j == item:
                return True
        return False

    # DEFINE THIS
    def __iter__(self):
        return iter(self.__d) 

    def __getitem__(self, key):
        return self.__d[key]

    # FIX THIS
    def __delitem__(self, key):
        raise DeleteError

    # FIX THIS
    def __setitem__(self, key, value):
        if isinstance(key, str) and isinstance(value,float):
            print(self.__class__.key_to_type)
            self.__d[key] = value
        else:
            raise UpdateValueError(key,value, self.__class__.key_to_type)

    # FIX THIS
    def __check(self, d):
        type_dict = self.__class__.key_to_type
        type_dict_keys = set(type_dict.keys())
        d_keys = set(d.keys())
        error_keys = set()
        missing_keys = set()
        error_type = []

        missing_keys = type_dict_keys.difference(d_keys)
        error_keys = d_keys.difference(type_dict_keys)
        matching = list(d_keys.intersection(type_dict_keys))

        for key in matching:
            if type(d[key]) != type_dict[key]:
                error_type.append(key)

        if len(error_keys) > 0 or len(missing_keys) > 0 or len(error_type) > 0:
            raise InitializationError(d, type_dict, missing_keys, error_keys, error_type)
    
class StructuredDictError(Exception):
    pass

# FIX THIS
class DeleteError(StructuredDictError):
    def __str__(self):
        return 'You cannot delete from a StructuredDict'

# FIX THIS
class UpdateValueError(StructuredDictError):
    def __init__(self, key, value, key_to_type):
        self.key = key
        self.value = value
        self.key_to_type = key_to_type
        
    def __str__(self):
        f = self.key_to_type
        return "The type of %s is %s, but the value corresponding to the key '%s' should have type %s" % (self.value , type(self.value) , self.key, f[self.key])

# FIX THIS
class InitializationError(StructuredDictError):
    def __init__(self, d, key_to_type, mis, add, typ):
        self.d = d
        self.key_to_type = key_to_type
        self.mis = mis
        self.add = add
        self.typ = typ
    def __str__(self):
        out = ''
        if len(self.mis) > 0:
            out += f'The following keys are missing from d: {self.mis};\n'
        if len(self.add) > 0:
            out += f'The following keys were supplied in error: {self.add};\n'
        if len(self.typ) > 0:
            for self.key in self.typ:
                out += "the type of d[%s] is %s, but it should be %s;\n" %(repr(self.key), type(self.d[self.key]),self.key_to_type[self.key])
        return out
            

class Rectangle(StructuredDict):
    key_to_type = {'len1': float, 'len2': float}

    def __init__(self, len1, len2):
        d = {'len1' : len1, 'len2' : len2}
        super().__init__(d)

    def area(self):
        return self['len1'] * self['len2']


class Student(StructuredDict):
    key_to_type = {'first name': str, 'last name': str, 'GPA': float}

    def __init__(self, first, last, gpa):
        d = {'first name': first, 'last name': last, 'GPA': gpa}
        super().__init__(d)

    def __str__(self):
        name = 'Name: ' + self['first name'] + ' ' + self['last name'] + ', '
        gpa = 'GPA: ' + str(self['GPA'])

        return name + gpa



if __name__ == '__main__':
    r = Rectangle(2.0, 4.0)
    print('area =', r.area())

    def f1():
        r = Rectangle(2.0, 4.0)
        del r['len1']

    def f2():
        r = Rectangle(2.0, 4.0)
        r['len1'] = 2

    def f3():
        r = Rectangle(2, '4')
        return r

    def f4():
        class C(StructuredDict):
            key_to_type = {0:int, 1:int, 2:int, 3:float, 4:str}

        c = C({2:2, 3:3, 4:4, 5:5, 6:6})
        return c

    L = [f1, f2, f3, f4]

    for f in L:
        try:
            print('')
            f()
        except DeleteError as e:
            print('DeleteError:', e)
        except UpdateValueError as e:
            print('UpdateValueError:', e)
        except InitializationError as e:
            print('InitializationError:', e)


# MY OUTPUT
# area = 8.0

# DeleteError: You cannot delete from a StructuredDict

# UpdateValueError: The type of 2 is <class 'int'>, but the value corresponding to the key 'len1' should have type <class 'float'>

# InitializationError: the type of d['len1'] is <class 'int'>, but it should be <class 'float'>;
# the type of d['len2'] is <class 'str'>, but it should be <class 'float'>;

# InitializationError: the following keys are missing from d: {0, 1};
# the following keys were supplied in error: {5, 6};
# the type of d[3] is <class 'int'>, but it should be <class 'float'>;
# the type of d[4] is <class 'int'>, but it should be <class 'str'>;
