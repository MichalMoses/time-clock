import csv
from tkinter import *
from tkinter import messagebox
from ETC_gui import *



class Employee:
    def __init__(self, emp_id, name, phone, dob, rank, subs=None, manager=None):
        self.emp_id=emp_id
        self.name=name
        self.phone=phone
        self.dob=dob
        self.rank=rank
        self.subs=subs
        self.manager=manager

    def write_new_emp_to_file(self):
        #we always call this function after we validated id. so no need to validate id again.
        #now we have an existing file, we can check if employee already exists in id list, if not we can add it to file
            try:
                with open('Employees.csv', 'a', newline='') as csvfile:
                    all_employees = csv.writer(csvfile)
                    # create one input row
                    all_employees.writerow([self.emp_id] + [self.name] + [self.phone] + [self.dob]+[self.rank]+[self.subs]+[self.manager])
            except Exception as err:
                messagebox.showwarning('Adding new employee issues', f"Something went wrong with writing {self.name}. Error: {err}")
            else:  # print success message
                messagebox.showinfo('Success!',f'--Employee {self.name} was successfully added to file with ID {self.emp_id}!--' )

    #todo - this function is currently not in use. After i implement manager input need to test this function
    def update_manager(self, new_manager):
        self.manager=new_manager


    def __repr__(self):
        return "Employee('{}','{}','{}','{}')".format(self.emp_id, self.name, self.phone, self.dob)

    def __str__(self):
        return f'  Employee ID: {self.emp_id} \n  Employee name: {self.name}\n  phone number: {self.phone}\n  Date of Birth: {self.dob}'
class Manager(Employee):
    rank = "Manager"
    def __init__(self,emp_id, name, phone, dob, rank, subs=None, manager=None):
        super().__init__(emp_id, name, phone, dob, rank, subs, manager)
    #todo - run the following function and make sure they work
    def add_sub (self, employee):
        if employee not in self.subs:
            self.subs.append(employee)
    def remove_sub (self, emp):
        if emp in self.subs:
            self.subs.remove(emp)
    def print_subs (self):
        for emp in self.subs:
            print(f'-->{emp}')