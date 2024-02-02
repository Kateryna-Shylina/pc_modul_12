from collections import UserDict
from datetime import datetime
import pickle

class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value
    
    def __str__(self):
        return str(self.__value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        required = True
 

class Phone(Field):
    def __init__(self, value):    
        super().__init__(value)
        required = False
            
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Wrong phone number")
        else: 
            self.__value = value
               

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        required = False

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value != "":
            try:
                birthday_day = datetime.strptime(value, '%d.%m.%Y')
                self.__value = value
            except:
                raise ValueError("Wrong date format")


class Record:
    def __init__(self, name, birthday = ""):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)
        
    def edit_phone(self, old_phone, new_phone):   
        for phone in self.phones:
            if phone.value == old_phone:
                self.add_phone(new_phone)
                self.remove_phone(old_phone)                
                break
        else:
            raise ValueError
        
    def remove_phone(self, phone_number):
        index = -1
        for phone in self.phones:
            index += 1
            if phone.value == phone_number:
                break
        else:
            raise ValueError

        self.phones.pop(index)

    def days_to_birthday(self):
        if self.birthday.value == "":
            return None
        
        current_day = datetime.now().date()
        birthday_day = datetime.strptime(self.birthday.value, '%d.%m.%Y')
        birthday_day = datetime(year=current_day.year, month=birthday_day.month, day=birthday_day.day, hour=0).date()
        if birthday_day >= current_day:
            days = birthday_day - current_day
        else:
            birthday_day = datetime(year=current_day.year+1, month=birthday_day.month, day=birthday_day.day, hour=0).date()
            days = birthday_day - current_day
        
        return days

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"



class AddressBook(UserDict):
    def __init__(self, filename=""):
        self.data = {}
        self.filename = filename
        if self.filename != "":
            self.load_from_file(filename)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.filename == "":
            self.filename = "SomeAddressBook.bin"
        self.save_to_file(self.filename)

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, str):
        records = []
        for key, record in self.data.items():
            if str in key.lower():
                records.append(record.__str__())
            else:
                for phone in record.phones:
                    if str in phone.value:
                        records.append(record.__str__())          
        return '\n'.join(records) 
        
    def delete(self, name):
        for key, record in self.data.items():
            if key == name:
                del self.data[name]
                break

    def iterator(self, n):
        values = list(self.data.values())
        for i in range(0, len(values), n):
            yield '\n'.join(map(str, values[i:i+n]))

    def save_to_file(self, filename):
        with open(filename, "wb") as fh:
            pickle.dump(self, fh)
        
    def load_from_file(self, filename):
        with open(filename, "rb") as fh:
            self.data = pickle.load(fh)
            


if __name__ == '__main__':
    filename = 'AddressBook.bin'    
    
    #creating of new file
    with AddressBook() as addrbook:
        record1 = Record("Kate")
        record1.add_phone("1234567890")
        addrbook.add_record(record1)

        record2 = Record("Kacy")
        record2.add_phone("1122334455")
        addrbook.add_record(record2)

        record3 = Record("Jhon")
        record3.add_phone("1111111111")
        addrbook.add_record(record3)

        record4 = Record("Jhonatan")
        record4.add_phone("2222222222")
        addrbook.add_record(record4)

        record5 = Record("Jeck")
        record5.add_phone("1973824650")
        addrbook.add_record(record5)

        record6 = Record("Don")
        record6.add_phone("1236547890")
        addrbook.add_record(record6)

        addrbook.save_to_file(filename)

    #Loading from existing file in __init__ method
    with AddressBook(filename) as book:
        iter = book.iterator(4)
        for i in iter:
            print(i)

        print('-----------------------------')
        print(book.find("kate"))
        print('-----------------------------')
        print(book.find("22"))
        print('-----------------------------')
        print(book.find("111"))
        print('-----------------------------')
        print(book.find("0"))
        print('-----------------------------')
        print(book.find("jh"))
        print('-----------------------------')

    #Loading from existing file using load_from_file method
    with AddressBook() as book_new:
        book_new.load_from_file(filename)
    
        record_new = Record("Kate_new")
        record_new.add_phone("0000000000")
        book_new.add_record(record_new)
    
        iter = book_new.iterator(4)
        for i in iter:
            print(i)


    #book.save_to_file(filename)
    #book_new.save_to_file('AddressBook_new.bin')
     
    

