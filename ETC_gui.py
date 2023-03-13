import tkinter as tk
from datetime import *
import csv
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkcalendar import Calendar
from PIL import ImageTk, Image
import os
import re

#
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
                messagebox.showwarning('Action failed', f"Something went wrong with writing {self.name}. Error: {err}")
            else:  # print success message
                messagebox.showinfo('Success!',f'--Employee {self.name} was successfully added to file with ID {self.emp_id}--' )

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
#user menu functions
def mark_att(emp_id,name,rank): #function will return True if writing went ok, will return false if there was un expected error
    with open('Attendance.csv', 'a', newline='') as csvfile:
        add_entry=csv.writer(csvfile)
        add_entry.writerow([datetime.now().date(), datetime.now().time(),emp_id, name, rank])
        return True
#add\delete functions
def add_manually_screen(): #propt user input for a single employee details and sends it to be written to file
    #todo - every time we add an employee sort the file by id

    global ranks, var_rank
    ranks=['Junior', 'Senior', 'Manager']
    var_rank=StringVar()
    var_rank.set('Choose employees rank')

    #built top window
    global top
    top=Toplevel()
    top.geometry('500x300')
    top.wm_transient(root)
    x = root.winfo_x()
    y = root.winfo_y()
    top.geometry("+%d+%d" % (x + 100, y + 50))

    global id_entry_add, name_entry, phone_entry, birth_entry, rank_entry

    # define window widgets
    action_label = Label(top, text=f'--Add new employee to file manually-- \nPlease insert employee details')
    empid_label=Label(top,text=f"Employee ID 4 digits): ")
    id_entry_add =Entry(top, width=35, borderwidth=5)
    name_label=Label(top,text=f'Employee name')
    name_entry=Entry(top,width=35,borderwidth=5)
    phone_label=Label(top,text=f'Phone number')
    phone_entry=Entry(top,width=35, borderwidth=5)
    birth_label=Label(top,text=f'Date of birth, YYYY-MM-DD:')
    birth_entry=Entry(top,width=35,borderwidth=5)
    rank_label=Label(top,text=f"Employees's rank:")
    rank_entry=OptionMenu(top, var_rank, *ranks )
    button_submit=Button(top, text=f"Submit", command=add_manually_func)
    button_close_top = Button(top, text='Back to Admin menu', command=top.destroy)

    #place window widgets
    action_label.grid(row=0, column=0, pady=5, columnspan=2)
    empid_label.grid(row=1,column=0, pady=5, sticky=W)
    id_entry_add.grid(row=1,column=1, pady=5, sticky=W)
    name_label.grid(row=2,column=0, pady=5, sticky=W)
    name_entry.grid(row=2,column=1, pady=5, sticky=W)
    phone_label.grid(row=3,column=0, pady=5, sticky=W)
    phone_entry.grid(row=3,column=1, pady=5, sticky=W)
    birth_label.grid(row=5,column=0, pady=5, sticky=W)
    birth_entry.grid(row=5,column=1, pady=5, sticky=W)
    rank_label.grid(row=6,column=0, pady=5, sticky=W)
    rank_entry.grid(row=6,column=1, pady=5, sticky=W)
    button_submit.grid(row=7, column=1, pady=5, sticky=W)
    button_close_top.grid(row=8,column=0, pady=5, columnspan=2)

#todo - sort employee file, show the user the next available id number

def add_manually_func():
    global id_entry_add, name_entry, phone_entry, birth_entry, rank_entry, var_rank, ranks, top

    while True: #program will be stuck in this loop until all variables are valid

        # emp_id input request
        emp_id=id_entry_add.get().strip()
        try:
            id_check, name, dob, rank =check_id(emp_id)
        except Exception as err:
            messagebox.showwarning('ID input issue', f'{err}')
            return
        else:
            if id_check==1:
                messagebox.showwarning('ID input issue',f'ID already allocated to {name}, choose a different ID')
                return

        # name input request
        name = name_entry.get().strip() #removes spaces from the beginning and the end
        stripped = re.sub('[^a-zA-Z]', '', name)  # removes all non-alphabetic chars (replaces them with '')
        if "-" in name:
            messagebox.showwarning('Name input issue', 'No dashes in name please')
            return
        elif stripped != name:
            messagebox.showwarning('Name input issue', 'Only english alphabet please')
            return

        # phone number input request
        phone=phone_entry.get().strip()
        if len(phone)!=11 or phone[3]!="-" or not (phone[:3]+phone[4:]).isnumeric():
            messagebox.showwarning('Phone number input issue', 'Please follow the phone number format: 05X-XXXXXXX')
            return

        # dob input request
        birth_date=birth_entry.get().strip()
        try:
            dob=date.fromisoformat(birth_date)
            type(dob)
        except Exception:
            messagebox.showwarning('Date input issue', f'Date not according to format. Please type again.')
            return
        else:
            if dob>datetime.today().date():
                messagebox.showwarning('Date input issue', f'Date of Birth cannot be in the future')
                return

        #rank input request
        rank = var_rank.get()
        if rank not in ranks:
            messagebox.showwarning('Rank input issue', 'Invalid rank input. Please choose a rank from list')
            return
        break

# todo complete the part of adding the subs for the manager - generate a list of employees to choose from

    if rank=='Manager':#if all the inputs were ok, the while loop didn't 'continue' and got down to here, we can write to file
            subs=[]
            emp = Manager(emp_id, name, phone, str(dob), 'Manager', subs)
            emp.write_new_emp_to_file()
    else:
            emp = Employee(emp_id, name, phone, str(dob), rank)
            emp.write_new_emp_to_file()

    top.destroy()
def add_from_file_screen(): #add several new employees to the employee file,  reading the data from a file and sending employee data, one by one, to be written to file
    #todo validate file format (that all the required columns exist) before calling write_new_emp_to_file

    global top

    top = Toplevel()
    top.geometry('500x300')
    top.wm_transient(root)
    x = root.winfo_x()
    y = root.winfo_y()
    top.geometry("+%d+%d" % (x + 100, y + 50))


    # define widgets
    action_label = Label(top, text=f'--Add new employees by file input--')
    open_label=Label(top,text=f'Choose a file containing the \nemployees you wish to add')
    # open_file_button=Button(top,text=f'Open source file', command=lambda: choose_file('add'))
    open_file_button=Button(top,text=f'Open source file', command=add_from_file_func)
    button_close_top = Button(top, text='Back to Admin menu', command=top.destroy)

    # place widgets
    action_label.grid(row=0, column=0, pady=5, columnspan=2)
    open_label.grid(row=1, column=0, pady=5)
    open_file_button.grid(row=1, column=1, pady=5)
    button_close_top.grid(row=2, column=0, pady=5, columnspan=2)

def add_from_file_func():
    global top
    file_path = choose_file()
    #open the source file with the new employees, read it, for each line validate id and send wrtitten to file
    try:
        with open(file_path) as csvfile:
            all_employees = csv.reader(csvfile)
            next(all_employees, None)  # skip the header line
            for line in all_employees: #run over each line and send it to add function
                cells = len(line)
                while cells <= 6:
                    line.append("")
                    cells += 1
                if not check_id(line[0])[0]: #if id not in file, add it
                    emp = Employee(line[0], line[1], line[2], line[3], line[4], line[5])
                    emp.write_new_emp_to_file()
                else:
                    messagebox.showwarning('Action aborted', f'Employee ID {line[0]} already exists in file, belongs to {line[1]}')
                    continue
    except FileNotFoundError:
        messagebox.showwarning('Error', f'--File not found--')
        return
    except Exception as err:
        messagebox.showwarning('Error', f"Something went wrong with opening new employees file for reading. \nError: {err}")
        return
    finally:
        top.destroy()

def del_emp(emp_id,name): #delete a single employee from the employee file.
    #get confirmation from user for deletion
    sure = messagebox.askyesno('Confirm deletion', f'Are you sure you want to delete {name}?')
    # perform the deletion action according to the user input above
    if sure == 0:  # if user doesn't approve deletion
        messagebox.showinfo('Abort', f'--Delete of {name} aborted--')
    else:  # if user approves deletion, in order to delete from file need to copy only the data we want to keep to a new file.
        with open('Employees.csv') as csvfile:  # reopen file and get all the data
            all_employees = csv.reader(csvfile)
            all_employees_lines = [line for line in all_employees]
        # create new file and paste all data except from emp_id
        with open('Employees.csv', 'w', newline='') as csvfile:
            file_writer = csv.writer(csvfile)
            for line in all_employees_lines:
                if line[0] == emp_id:
                    continue #skip the line that we don't want to copy to the new file
                else:
                    file_writer.writerow(line) #write all lines to a new file
        # print user message that action completed
        messagebox.showinfo('Delete employee', f'-- {name} was successfully deleted from file!--') # print a message to user with data of the action


def del_manually_screen():


    global top, id_entry_del
    top = Toplevel()
    top.geometry('500x300')
    top.wm_transient(root)
    x = root.winfo_x()
    y = root.winfo_y()
    top.geometry("+%d+%d" % (x + 100, y + 50))

    #define widgets
    title_label=Label(top,text=f'--Delete Employee from file--')
    id_label=Label(top,text=f'Enter the ID of the employee \nyou wish to remove from file:')
    id_entry_del=Entry(top,width=35,borderwidth=5)
    button_submit = Button(top, text=f"Submit", command=del_manually_func)
    button_close_top = Button(top, text='Back to Admin menu', command=top.destroy)

    #place widgets
    title_label.grid(row=0,column=0, pady=5,columnspan=2)
    id_label.grid(row=1, column=0, pady=5)
    id_entry_del.grid(row=1, column=1, pady=5)
    button_submit.grid(row=2,column=0, pady=5,columnspan=2)
    button_close_top.grid(row=3,column=0, pady=5,columnspan=2)

def del_manually_func():
    global id_entry_del
    #validating the input by sending to 'check_id' function, only if it exists in file we can delete it
    emp_id = id_entry_del.get().strip()
    id_entry_del.delete(0,END)
    try:
        id_check, name, dob, rank = check_id(emp_id)
    except Exception as err:
        messagebox.showwarning('ID input issue', f'{err}')
        return
    else:
        if id_check == 0:
            messagebox.showwarning('ID input issue', f'ID does not exist in employee file')
            return
        else: #call the deletion function
            del_emp(emp_id, name)
            top.destroy()


def del_from_file_screen():
    #todo validate the file format (at list the first column) before calling del_emp

    # clear frame from previous action

    # global file_path
    global top

    top = Toplevel()
    top.geometry('500x300')
    top.wm_transient(root)
    x = root.winfo_x()
    y = root.winfo_y()
    top.geometry("+%d+%d" % (x + 100, y + 50))

    # define widgets
    action_label = Label(top, text=f'--Delete employees by file input--')
    open_label=Label(top,text=f'Choose a file containing the employees \nyou wish to delete')
    # open_file_button = Button(top, text=f'Browse', command=lambda: choose_file('del'))
    open_file_button = Button(top, text=f'Browse', command=del_from_file_func)
    button_close_top = Button(top, text='Back to Admin menu', command=top.destroy)

    #place widgets
    action_label.grid(row=0, column=0, pady=5,columnspan=2)
    open_label.grid(row=1, column=0, pady=5)
    open_file_button.grid(row=1, column=1, pady=5)
    button_close_top.grid(row=2, column=1, pady=5)

def del_from_file_func():

    global top
    file_path = choose_file()

    #open source file with the employees you want to delete and get all the ids into a list
    try:
        with open(file_path, newline='') as csvfile:
            all_employees = csv.reader(csvfile)
            all_ids=[]
            next(all_employees, None)  # skip the header line
            for line in all_employees: #for each employee in the file, add it to the list of IDs to be deleted
                all_ids.append(line[0])
    except Exception as err: #error if something went wrong with reading the source file
        messagebox.showwarning('File reading error',f"Something went wrong with opening {file_path} file for reading. \nError: {err}")
        return

    # take the list of ids, send each one to be validated and then to be deleted.
    for employee in all_ids:
        try: #send employee to be validated
            id_check, name, dob, rank = check_id(employee)
        except Exception as err: #can't validate employee, print error and move to next employee
            messagebox.showwarning('employee ID error', f'{err}')
            continue
        else: #employee id validated
            if id_check == 0:
                messagebox.showwarning('ID input issue', f'ID {employee} does not exist in employee file')
                continue
            else:  # call the deletion function
                del_emp(employee, name)

    top.destroy()

#reports functions
def emp_att_report_screen():
    global top
    global id_entry_att

    top=Toplevel()
    top.geometry('500x300')
    top.wm_transient(root)
    x = root.winfo_x()
    y = root.winfo_y()
    top.geometry("+%d+%d" % (x + 100, y + 50))

    #define widgets
    action_label=Label(top, text=f'--Get employee attendance report--')
    input_message_label=Label(top,text=f"Please enter employee ID")
    id_entry_att=Entry(top, width=20, borderwidth=5)
    button_submit=Button(top, text=f"Submit", command=emp_att_report_func)
    button_close_top = Button(top, text='Back to Admin menu', command=top.destroy)


    #arrange widgets
    action_label.grid(row=0, column=0, pady=5, columnspan=2)
    input_message_label.grid(row=1, column=0, pady=5)
    id_entry_att.grid(row=1, column=1, pady=5)
    button_submit.grid(row=2, column=0, pady=5, columnspan=2)
    button_close_top.grid(row=4, column=0, columnspan=2)

def emp_att_report_func():
    global id_entry_att, top

    #valideate the id entry
    emp_id = id_entry_att.get().strip()
    try:
        id_check, name, dob, rank = check_id(emp_id)
    except Exception as err:
        messagebox.showwarning('ID input issue', f'{err}')
        id_entry_att.delete(0,END)
        return
    else:
        if id_check == 0:
            messagebox.showwarning('ID input issue', f'Employee doesnt exist in file \nAdd employees to DB via Admin menu')
            id_entry_att.delete(0, END)
            return


        #open attendance file to read it, if not existing prompt message
    try:
        with open('Attendance.csv') as csvfile:
            attendance=csv.reader(csvfile)
            # create a new list with the relevant employee's entrances. list of lists
            emp_att = []
            for line in attendance:
                    if str(emp_id) == line[2]:
                        emp_att.append(line)
            if len(emp_att)==0:
                    messagebox.showwarning('Action aborted', f'No log entries for this employee\nReport was not generated')
                    return
    except FileNotFoundError:
            messagebox.showwarning('Action aborted', f'No log entries history exist yet\nReport was not generated')
            return
    except Exception as err:
            messagebox.showwarning('Action aborted', f"Something went wrong with opening attendance file for reading. \nError: {err}\nReport was not generated'")
            return

    #open attendance file and write the entry
    try:
        os.mkdir('Reports')
    except Exception as err:
        pass

    try:
            with open(f'Reports/Employee {name} attendance report.csv', 'w', newline='') as csvfile:
                add_entry = csv.writer(csvfile)
                add_entry.writerow(['Date', 'Time', 'Employee ID','Name','Rank'])
                add_entry.writerows(emp_att)
    except Exception as err :
        messagebox.showwarning('Action aborted',f'something went wrong with opening employee attendance report for writing. \nError: {err}\nReport was not generated' )
    else:
        messagebox.showinfo('Success',f'--Action complete-- \nYour report name is "Employee {name} attendance report {datetime.today().date()}.csv"' )

    id_entry_att.delete(0,END)

def monthly_report():

    #go over attandance file get all the lines with the current month
    today=datetime.today().date()
    try:
        with open('Attendance.csv') as csvfile:
            attendances=csv.reader(csvfile)
            monthly_lines=[]
            next(attendances,None)
            for line in attendances:
                log_date=date.fromisoformat(line[0])
                if log_date.month==today.month and log_date.year==today.year:
                    monthly_lines.append(line)
    except FileNotFoundError:
        messagebox.showwarning('Action aborted', f'No log entries history exist yet\nReport was not generated')

    except Exception as err:
        messagebox.showwarning('Action aborted', f'Something went wrong with opening attendance file for reading.\nError: {err}\nReport was not generated')

    else:
        with open(f'Reports/Monthly report {today.month} {today.year}.csv', 'w', newline='') as csvfile:
            add_entry=csv.writer(csvfile)
            add_entry.writerow(['Date', 'Time', 'Employee ID'])
            add_entry.writerows(monthly_lines)
        messagebox.showinfo('Success', f'--Report created successfully!--\n Saved as "Monthly report {today.month} {today.year}.csv"')

def custom_att_report_screen():

    global var_rank, ranks, top
    var_rank=StringVar()
    var_rank.set("Choose a rank    ")
    ranks=['Junior', 'Senior', 'Manager', 'All']
    global var_start_date,  var_end_date
    global start_date_entry, end_date_entry
    var_start_date=StringVar()
    var_start_date.set('Choose start date')
    var_end_date=StringVar()
    var_end_date.set('Choose end date')


    top=Toplevel()
    top.geometry('600x500')
    top.wm_transient(root)
    x = root.winfo_x()
    y = root.winfo_y()
    top.geometry("+%d+%d" % (x + 50, y + 50))


    #define widgets
    action_label = Label(top, text=f'--Generate a specific attendance report--')
    label_rank=Label(top,text=f"Employees rank:")
    rank_entry=OptionMenu(top,var_rank,*ranks)
    label_time_range=Label(top, text=f'Date range:')

    label_start_date=Label(top,text=f'Start date')
    start_date_entry=Entry(top, textvariable=var_start_date ,width=20, borderwidth=5)
    cal_start_date=Calendar(top, selectmode='day',date_pattern='yyyy-mm-dd',year=datetime.today().year, month=datetime.today().month, day=datetime.today().day)

    label_end_date=Label(top,text=f'End date')
    end_date_entry=Entry(top, textvariable=var_end_date, width=20, borderwidth=5)
    cal_end_date=Calendar(top, selectmode='day',date_pattern='yyyy-mm-dd',year=datetime.today().year, month=datetime.today().month, day=datetime.today().day)

    button_select_date=Button(top,text=f'Get calendar selection', command=lambda : grab_date(cal_start_date,cal_end_date))
    button_submit=Button(top, text=f'Submit', command=custom_att_report_func)

    button_close_top = Button(top, text='Back to Admin menu', command=top.destroy)


    #Place widgets
    action_label.grid(row=0,column=0, columnspan=2, pady=5)
    label_rank.grid(row=1, column=0,sticky=W, pady=5)
    rank_entry.grid(row=1, column=1, columnspan=2,sticky=W, pady=5)
    label_time_range.grid(row=2, column=0,sticky=W, pady=5)

    label_start_date.grid(row=3,column=0,sticky=W, pady=5)
    cal_start_date.grid(row=4, column=0, sticky=W, pady=5, padx=5)
    start_date_entry.grid(row=5, column=0,sticky=W, pady=5)

    label_end_date.grid(row=3, column=1,sticky=W, pady=5)
    cal_end_date.grid(row=4, column=1, sticky=W, pady=5, padx=5)
    end_date_entry.grid(row=5,column=1, sticky=W, pady=5)

    button_select_date.grid(row=6, column=0,sticky=W, pady=5)
    button_submit.grid(row=7, column=0,sticky=W, pady=5)

    button_close_top.grid(row=9, column=0, columnspan=5,sticky=W, pady=5)

def custom_att_report_func():
    global var_rank, ranks, top
    global var_start_date,  var_end_date
    global start_date_entry, end_date_entry


    #get input and validate
        #get user input for rank
    rank=var_rank.get()
    if rank not in ranks:
        messagebox.showwarning('Rank input error', 'Please choose a rank from list')
        return
    #get user input for time range
    start_date_str=start_date_entry.get()
    end_date_str=end_date_entry.get()
    try:
        start_date=date.fromisoformat(start_date_str)
        end_date=date.fromisoformat(end_date_str)
        if start_date>datetime.today().date():
            messagebox.showwarning('Date input error', 'Start date cannot be in the future')
            return
        if end_date<start_date:
            messagebox.showwarning('Date input error', 'End date cannot be before start date')
            return
    except Exception as err:
        messagebox.showwarning('Date input error', f'Invalid date input, please try again. \nError: {err} ')
        return

    #go over attandance file and collect all the lines with the required values
    try:
        with open('Attendance.csv') as csvfile:
            attendances=csv.reader(csvfile)
            report_lines=[]
            next(attendances,None) #skip header line
            for line in attendances:
                log_date=date.fromisoformat(line[0])
                if log_date>=start_date and log_date<=end_date and (rank.lower()==line[4].lower() or rank.lower()=='all'):
                    report_lines.append(line)
            if len(report_lines)==0:
                messagebox.showwarning('No Data', 'There are no log entries for these dates and rank')
                return
    except FileNotFoundError:
        messagebox.showwarning('No Data', 'No log entries history exist yet')
    except Exception as err:
        messagebox.showwarning('No Data', f'Something went wrong with opening attendance file for reading.\nError: {err}')
    else:
        with open(
                f'Reports/Att report {start_date} to {end_date} {rank} ranks.csv', 'w', newline='') as csvfile:
            add_entry=csv.writer(csvfile)
            add_entry.writerow(['Date', 'Time', 'Employee ID', 'Name', 'Rank'])
            add_entry.writerows(report_lines)
        messagebox.showinfo('Success', f'--Report created successfully!-- \nSaved as "Att report {start_date} to {end_date} {rank} ranks.csv"')

    top.destroy()

def late_report():


    # open attendance report, go over all the entries, create a local list with all the entries which were recorded after 9:30
    try:
        with open('Attendance.csv') as csvfile:
            att_data=csv.reader(csvfile)
            late_entries=[]
            late_time=time(9,30,00) #hour, minute, seconds
            for line in att_data:
                if line[0]=='Date':
                    continue
                log_time=time.fromisoformat(line[1])
                if log_time>=late_time:
                    late_entries.append(line)
    except FileNotFoundError:
        messagebox.showwarning('Action failed', f'No log entries history exists yet\nReport not created')

    except Exception as err:
        messagebox.showwarning('Action failed', f"Something went wrong with opening attendance file for reading. \nError: {err}")


    else: #open 'late report' as w (if already exist we can override it), and write the list of the relevant entries that we created into this file.
        with  open(f'Reports/Late report {datetime.today().date()}.csv', 'w', newline='') as csvfile:
            write_file=csv.writer(csvfile)
            write_file.writerow(['Date', 'Time', 'Employee ID']) #it's a new file so we always write the title
            write_file.writerows(late_entries)
        messagebox.showinfo('Success!', f'--Late log create successfully!--\nFile name: Late report {datetime.today().date()}.csv')
#utility functions
def mark_att_all(): #helping function to fill up the log file for testing
    with open('Employees.csv') as csvfile:
        all_employees=csv.reader(csvfile)
        next(all_employees,None)
        for line in all_employees:
            mark_att(line[0],line[1],line[4])
#button functions
def choose_file():
    current_dir = os.getcwd()
    root.filename=filedialog.askopenfilename(initialdir=current_dir, title='Select a file', filetypes=(('csv files','*.csv'),('all files','*.*')))
    file_path = root.filename
    return file_path

def check_id(emp_id):#received emp_id, validates it, returns emp details
    if emp_id == '8888':
        raise Exception (f'{emp_id} is a reserved system number, please insert a different four digit number')
    elif not emp_id.isnumeric():
        raise Exception('Employee ID must contain numbers only')
    elif len(emp_id) != 4:
        raise Exception(f'Employee ID must be 4 digits long')

    else:
        try:
            with open('Employees.csv') as csvfile:
                all_employees=csv.reader(csvfile)
                next(all_employees,None)
                for line in all_employees:
                    if emp_id==line[0]:
                        name=line[1]
                        dob=line[3]
                        rank=line[4]
                        id_check=True
                        return(id_check, name, dob,rank)
                id_check=False
                return (id_check,"", "" ,"")
        except FileNotFoundError : #if file doesn't exist create new file and write into it only the header
            try:
                with open('Employees.csv', 'w' , newline='') as csvfile:
                    all_employees = csv.writer(csvfile)
                    #create a header row
                    all_employees.writerow(["Employee ID"] + ['Employee name']+['Employee Phone number']+['Employee DOB']+['Rank']+['Subs']+['Manager'])
                    id_check = False
                    return (id_check, "", "", "")
            except Exception as err:
                raise Exception(f"Something went wrong with generating new employee file for writing. Error: {err}")
        except Exception as err:
            raise (f"Something went wrong with opening employees file for reading. \nError: {err}")

def grab_date(cal_start, cal_end):
    global var_start_date
    global var_end_date
    var_start_date.set(cal_start.get_date())
    var_end_date.set(cal_end.get_date())
    return

# top level functions

def admin_menu(emp_id):
    #check permission
    while True:
        if emp_id.strip() == '8888':
            break
        else:
            try:
                id_check, name, dob, rank = check_id(emp_id)
            except Exception as err:
                messagebox.showwarning('Permission issue', f'{err}')
                return
            else:
                if rank!='Manager':
                    messagebox.showwarning('Permission issue', f'{emp_id} is not a valid admin ID')
                    return
                else:
                    break

    # clear frame from previous action
    for widget in main_frame.winfo_children():
        widget.grid_forget()
    main_frame.place_forget()

    label_welcome=Label(admin_menu_frame,text=f'---Administrator portal---')
    label_welcome.config(font=('Helvatical bold',12))

    #Admin menu frames
    button_back = Button(admin_menu_frame, text=f"<<back to main", command=back_to_main)
    frame_add_remove = LabelFrame(admin_menu_frame, pady=10, padx=20, text=f'Actions in employees file')
    frame_admin_reports = LabelFrame(admin_menu_frame, pady=10, padx=20, text=f'Generate attendance reports')

    # widgets in add\remove frame
    button_add_manually = Button(frame_add_remove, text=f'Add employee manually', width=30, command=add_manually_screen)
    button_add_from_file = Button(frame_add_remove, text=f'Add employee from file', width=30, command=add_from_file_screen)
    button_delete_manually = Button(frame_add_remove, text=f'Delete employee manually', width=30, command=del_manually_screen)
    button_delete_from_file = Button(frame_add_remove, text=f'Delete Employee from file', width=30, command=del_from_file_screen)

    # widgets in reports frame
    button_attendance_report_employee = Button(frame_admin_reports, text=f'Attendance report for a single employee', width=30, command=emp_att_report_screen)
    button_attendance_this_month = Button(frame_admin_reports, text=f'Current month report for all employees', width=30, command=monthly_report)
    button_late_report = Button(frame_admin_reports, text=f'Late employees report', width=30, command=late_report)
    button_custom_report = Button(frame_admin_reports, text=f'Custom attendance report', width=30, command=custom_att_report_screen)

    admin_menu_frame.place(x=350, y=30, anchor=N)
    label_welcome.grid(row=0, column=0, columnspan=2)

    #add/delet frame
    frame_add_remove.grid(row=1, column=0)
    button_add_manually.grid(pady=5, row=0, column=0, sticky=W)
    button_add_from_file.grid(pady=5, row=1, column=0, sticky=W)
    button_delete_manually.grid(pady=5, row=2, column=0, sticky=W)
    button_delete_from_file.grid(pady=5, row=3, column=0, sticky=W)

    # reports frame
    frame_admin_reports.grid(row=1, column=1)
    button_attendance_report_employee.grid(pady=5, row=0, column=0, sticky=W)
    button_attendance_this_month.grid(pady=5, row=1, column=0, sticky=W)
    button_late_report.grid(pady=5, row=2, column=0, sticky=W)
    button_custom_report.grid(pady=5, row=3, column=0, sticky=W)
    button_back.grid(row=4,column=0, sticky= W)

def back_to_main():
    # clear frame from previous action
    for widget in admin_menu_frame.winfo_children():
        widget.grid_forget()
    admin_menu_frame.place_forget()
    id_entry_main.delete(0,END)

    #place main screen labels back on root
    main_frame.place(x=350, y=30, anchor=N)
    label_welcome.grid( row=0, column=0, columnspan=2, padx=100)
    input_message_label.grid(row=2, column=0,columnspan=2, pady=5)
    id_entry_main.grid(row=3, column=0, pady=5, padx=2, columnspan=2)
    button_log_in.grid(row=4, column=0, padx=2, sticky=E)
    button_admin.grid(row=4,column=1, padx=2, sticky=W)
    label_action_result.grid(row=5, column=0, columnspan=2)

def main_menu():
    global root
    global main_frame, admin_menu_frame, button_exit
    global label_welcome, input_message_label, button_log_in, button_admin, label_action_result
    global id_entry_main

    root = Tk()
    root.title('Employee Management System')
    root.geometry('700x400')

    # Define label common to all screens
    main_frame = LabelFrame(root, padx=20, pady=10)
    admin_menu_frame = LabelFrame(root, padx=20, pady=10)
    button_exit = Button(root, text='Exit', command=lambda: terminate(root))
    button_exit.pack(pady=20, ipady=10, ipadx=20, side=tk.BOTTOM)
    button_exit.configure(bg='#CDCDCD')
    root.configure(bg='#E3E4DB')

    # Define main screen labels and buttons
    label_welcome = Label(main_frame, text=f'Welcome to employee time clock')
    label_welcome.config(font=('Helvatical bold', 12))
    input_message_label = Label(main_frame, text=f"Eenter your employee ID to log in \n Enter admin ID and click 'admin menu' for more options")
    id_entry_main = Entry(main_frame, width=20, borderwidth=5)
    button_log_in = Button(main_frame, text=f'Log in', width=10, command=login)
    button_admin = Button(main_frame, text=f'Admin menu', width=10, command=lambda : admin_menu(id_entry_main.get()))
    label_action_result = Label(main_frame, text=f"")

    # place main screen labels on root
    main_frame.place(x=350, y=30, anchor=N)
    label_welcome.grid( row=0, column=0, columnspan=2, padx=100)
    input_message_label.grid(row=2, column=0,columnspan=2, pady=5)
    id_entry_main.grid(row=3, column=0, pady=5, padx=2, columnspan=2)
    button_log_in.grid(row=4, column=0, padx=2, sticky=E)
    button_admin.grid(row=4,column=1, padx=2, sticky=W)
    label_action_result.grid(row=5, column=0, columnspan=2)

    root.mainloop()

def login():
    global id_entry_main
    emp_id=id_entry_main.get()
    id_entry_main.delete(0, END)
    bday_image = ImageTk.PhotoImage(Image.open('../bday.png'))
    try: #find the employee in employee file and get their details
        id_check, name, dob, rank = check_id(emp_id)
    except Exception as err: #error in the input validity
        messagebox.showwarning('ID input issue', f'{err}')
        return
        # continue #wait for the user to correct their input
    else: #we didn't get exception from employee file
        if id_check == 1:#means the employee exists and we got all their details
            #check if it's their birthday
            if datetime.fromisoformat(dob).month==datetime.today().date().month and datetime.fromisoformat(dob).day==datetime.today().date().day:
                bday_image_label=Label(main_frame, image=bday_image, text=f"Congratulations {name}, it's your birthday!!!")
                bday_image_label.grid(row=6,column=0,columnspan=2)
                messagebox.showinfo('HAPPY BIRTHDAY', f"Congratulations {name}, it's your birthday!!!")
            response=1
            try: #todo - improve search, i don't need to go over the entire list of attendance logs to see if the user logged in today
                with open('Attendance.csv') as csvfile:  # check if the file exists and if an entry for today already exists
                    attendance = csv.reader(csvfile)
                    for line in attendance:
                        if str(datetime.now().date()) == line[0] and emp_id == line[2]:  # if the employee already checked in we ask them if they want to check in again
                            response=messagebox.askyesno('Continue?', f'Hi {name}, you already checked in today. Do you wish to check in again?')
                            break
            except FileNotFoundError:  # if the file doesn't exist create it
                with open('Attendance.csv', 'w', newline='') as csvfile:
                    add_entry = csv.writer(csvfile)
                    add_entry.writerow(['Date', 'Time', 'Employee ID', 'Employee name', 'Rank'])
            except Exception as err: #if there is some kind of error display it, and update response so we don't write to file
                messagebox.showwarning('Error', f'Something went wrong with opening attendance file for writing. \nError: {err}')
                return
            finally:  # update the log according to 'response'
                if response==0:# if they don't want to check in again
                    messagebox.showwarning('Error', f'--{name} your current entry was not registered--')
                    return
                else: #check the employee in
                    if mark_att(emp_id, name, rank) == True:
                        messagebox.showinfo('Error',f'--{name}, your log in is registered-- \n --Date: {datetime.now().date().__str__()}, Time: {datetime.now().time().__str__()[:5]}--')
                        return
        else:
            messagebox.showwarning('Error',f'--user does not appear in user list--' )
            return

def terminate(root):
    root.destroy()
    exit()

if __name__ == "__main__":
    main_menu()






