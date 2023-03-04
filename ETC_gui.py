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
def add_manually(): #propt user input for a single employee details and sends it to be written to file
    #todo - every time we add an employee sort the file by id
    global var_num_add
    var_num_add=IntVar()
    var_num_add.set(0)
    var_rank=StringVar()
    ranks=['Junior', 'Senior', 'Manager']

    # clear frame from previous action
    for widget in sub_action_frame.winfo_children():
        widget.grid_forget()
    var_rank.set('Choose employees rank')

    top=Toplevel()
    top.geometry('500x300')
    top.wm_transient(root)
    x = root.winfo_x()
    y = root.winfo_y()
    top.geometry("+%d+%d" % (x + 100, y + 50))

    # prepare frame for current action
    action_label = Label(top, text=f'--Add new employee to file manually-- \nPlease insert employee details')
    empid_label=Label(top,text=f"Employee ID 4 digits): ")
    id_entry =Entry(top, width=35, borderwidth=5)
    name_label=Label(top,text=f'Employee name')
    name_entry=Entry(top,width=35,borderwidth=5)
    phone_label=Label(top,text=f'Phone number')
    phone_entry=Entry(top,width=35, borderwidth=5)
    birth_label=Label(top,text=f'Date of birth, YYYY-MM-DD:')
    birth_entry=Entry(top,width=35,borderwidth=5)
    rank_label=Label(top,text=f"Employees's rank:")
    rank_entry=OptionMenu(top, var_rank,*ranks )
    button_submit=Button(top, text=f"Submit", command=lambda :submit_button('add'))
    button_close_top = Button(top, text='Back to Admin menu', command=top.destroy)


    action_label.grid(row=0, column=0, pady=5, columnspan=2)
    empid_label.grid(row=1,column=0, pady=5, sticky=W)
    id_entry.grid(row=1,column=1, pady=5, sticky=W)
    name_label.grid(row=2,column=0, pady=5, sticky=W)
    name_entry.grid(row=2,column=1, pady=5, sticky=W)
    phone_label.grid(row=3,column=0, pady=5, sticky=W)
    phone_entry.grid(row=3,column=1, pady=5, sticky=W)
    birth_label.grid(row=5,column=0, pady=5, sticky=W)
    birth_entry.grid(row=5,column=1, pady=5, sticky=W)
    rank_label.grid(row=6,column=0, pady=5, sticky=W)
    rank_entry.grid(row=6,column=1, pady=5, sticky=W)
    button_submit.grid(row=7, column=1, pady=5, sticky=W)
    # button_clear.grid(row=8,column=0, pady=5, columnspan=2)
    button_close_top.grid(row=8,column=0, pady=5, columnspan=2)

#todo - sorft employee file, show the user the next avaiable id number


    while True: #program will be stuck in this loop until all variables are valid
        button_submit.wait_variable(var_num_add)

        # emp_id input request
        emp_id=id_entry.get().strip()
        try:
            id_check, name, dob, rank =check_id(emp_id)
        except Exception as err:
            messagebox.showwarning('ID input issue', f'{err}')
            continue
        else:
            if id_check==1:
                messagebox.showwarning('ID input issue',f'ID already allocated to {name}, choose a different ID')
                continue

        # name input request
        name = name_entry.get().strip() #remes spaces from the begining and the end
        stripped = re.sub('[^a-zA-Z]', '', name)  # removes all non alphabetic chars (replaces them with '')
        if "-" in name:
            messagebox.showwarning('Name input issue', 'No dashes in name please')
            continue
        elif stripped != name:
            messagebox.showwarning('Name input issue', 'Only english alphabet please')
            continue

        # phone number input request
        phone=phone_entry.get().strip()
        if len(phone)!=11 or phone[3]!="-" or not (phone[:3]+phone[4:]).isnumeric():
            messagebox.showwarning('Phone number input issue', 'Please follow the phone number format: 05X-XXXXXXX')
            continue

        # dob input request
        birth_date=birth_entry.get().strip()
        try:
            dob=date.fromisoformat(birth_date)
        except Exception:
            messagebox.showwarning('Date input issue', f'Date not according to format. Please type again.')
            continue
        else:
            if dob>datetime.today().date():
                messagebox.showwarning('Date input issue', f'Date of Birth cannot be in the future')
                continue

        #rank input request
        rank = var_rank.get()
        if rank not in ranks:
            messagebox.showwarning('Rank input issue', 'Invalid rank input. Please choose a rank from list')
            continue
        break

# todo complete the part of adding the subs for the manager - generate a list of employees to choose from

    if rank=='Manager':#if all the inputs were ok, the while loop didn't 'continue' and got down to here, we can write to file
            subs=[]
            emp = Manager(emp_id, name, phone, dob, 'Manager', subs)
            emp.write_new_emp_to_file()
    else:
            emp = Employee(emp_id, name, phone, dob, rank)
            emp.write_new_emp_to_file()
    # messagebox.showinfo('Success!',f'--Adding employee {name} complete--' )
    # Label(sub_action_frame,text=f'--Adding employee complete--').grid(row=9,column=0,columnspan=2)
    button_submit.config(state=DISABLED)
def add_from_file(): #add several new employees to the employee file,  reading the data from a file and sending employee data, one by one, to be written to file
    # clear frame from previous action
    for widget in sub_action_frame.winfo_children():
        widget.grid_forget()
    global var_num_browse_add
    var_num_browse_add=IntVar()
    var_num_browse_add.set(0)

    top = Toplevel()
    top.geometry('500x300')
    top.wm_transient(root)
    x = root.winfo_x()
    y = root.winfo_y()
    top.geometry("+%d+%d" % (x + 100, y + 50))


    # define widgets
    action_label = Label(top, text=f'--Add new employees by file input--')
    open_label=Label(top,text=f'Choose a file containing the \nemployees you wish to add')
    open_file_button=Button(top,text=f'Open source file', command=lambda: choose_file('add'))
    button_close_top = Button(top, text='Back to Admin menu', command=top.destroy)

    # place widgets
    action_label.grid(row=0, column=0, pady=5, columnspan=2)
    open_label.grid(row=1, column=0, pady=5)
    open_file_button.grid(row=1, column=1, pady=5)
    button_close_top.grid(row=2, column=0, pady=5, columnspan=2)


    open_file_button.wait_variable(var_num_browse_add)

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
                    messagebox.showwarning('Action aborted', f'Employee {line[0]} already exists in file')
                    continue
    except FileNotFoundError:
        Label(sub_action_frame,text=f'--File not found--').grid(row=3,column=0, columnspan=2)
    except Exception as err:
        Label(sub_action_frame,text=f"Something went wrong with opening new employees file for reading. \nError: {err}").grid(row=3,column=0, columnspan=2)
    finally:
        # Label(sub_action_frame,text=f'--Adding from file complete--').grid(row=3,column=0, columnspan=2)
        open_file_button.config(state=DISABLED)

def del_emp(emp_id,name): #delete a single employee from the employee file.
    #get confirmation from user for deletion
    sure = messagebox.askyesno('Confirm deletion', f'Are you sure you want to delete {name}?')
    # perform the deletion action according to the user input above
    if sure == 0:  # if user doesn't approve deletion
        Label(sub_action_frame, text=f'--Delete of {name} aborted--').grid(row=3, column=0, columnspan=2)
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
def del_manually():
    #clear frame from previous action
    for widget in sub_action_frame.winfo_children():
        widget.grid_forget()
    global var_num_del
    var_num_del = IntVar()
    var_num_del.set(0)

    top = Toplevel()
    top.geometry('500x300')
    top.wm_transient(root)
    x = root.winfo_x()
    y = root.winfo_y()
    top.geometry("+%d+%d" % (x + 100, y + 50))

    #define widgets
    title_label=Label(top,text=f'--Delete Employee from file--')
    id_label=Label(top,text=f'Enter the ID of the employee \nyou wish to remove from file:')
    id_entry=Entry(top,width=35,borderwidth=5)
    button_submit = Button(top, text=f"Submit", command=lambda : submit_button('del'))
    button_close_top = Button(top, text='Back to Admin menu', command=top.destroy)

    #place widgets
    title_label.grid(row=0,column=0, pady=5,columnspan=2)
    id_label.grid(row=1, column=0, pady=5)
    id_entry.grid(row=1, column=1, pady=5)
    button_submit.grid(row=2,column=0, pady=5,columnspan=2)
    button_close_top.grid(row=3,column=0, pady=5,columnspan=2)
    #validating the input by sending to 'check_id' function, only if it exists in file we can delete it
    while True:
        button_submit.wait_variable(var_num_del)
        emp_id = id_entry.get().strip()
        try:
            id_check, name, dob, rank = check_id(emp_id)
        except Exception as err:
            messagebox.showwarning('ID input issue', f'{err}')
            continue
        else:
            if id_check == 0:
                messagebox.showwarning('ID input issue', f'ID does not exist in employee file')
                return
            else: #call the deletion function
                del_emp(emp_id, name)
                break #break while loop continue to label
    # Label(sub_action_frame, text=f"Delete action complete").grid(row=4, column=0, columnspan=2)

def del_from_file():
    # clear frame from previous action
    for widget in sub_action_frame.winfo_children():
        widget.grid_forget()
    global file_path
    global var_num_browse_del
    var_num_browse_del= IntVar()
    var_num_browse_del.set(0)

    top = Toplevel()
    top.geometry('500x300')
    top.wm_transient(root)
    x = root.winfo_x()
    y = root.winfo_y()
    top.geometry("+%d+%d" % (x + 100, y + 50))

    # define widgets
    action_label = Label(top, text=f'--Delete employees by file input--')
    open_label=Label(top,text=f'Choose a file containing the employees \nyou wish to delete')
    open_file_button = Button(top, text=f'Browse', command=lambda: choose_file('del'))
    button_close_top = Button(top, text='Back to Admin menu', command=top.destroy)

    #place widgets
    action_label.grid(row=0, column=0, pady=5,columnspan=2)
    open_label.grid(row=1, column=0, pady=5)
    open_file_button.grid(row=1, column=1, pady=5)
    button_close_top.grid(row=2, column=1, pady=5)

    #wait for the source file input
    open_file_button.wait_variable(var_num_browse_del)

    #open source file with the employees you want to delete and get all the ids into a list
    try:
        with open(file_path, newline='') as csvfile:
            all_employees = csv.reader(csvfile)
            all_ids=[]
            next(all_employees, None)  # skip the header line
            for line in all_employees: #for each employee in the file, send it to delete function
                all_ids.append(line[0])
    except Exception as err: #error if something went wrong with reading the source file
        messagebox.showwarning('File reading error',f"Something went wrong with opening {file_path} file for reading. \nError: {err}")
        open_file_button.config(state=DISABLED)
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

    # when the function finished running print
    # Label(sub_action_frame, text=f'--Deleting from file complete--').grid(row=3,column=0, columnspan=2)
    open_file_button.config(state= DISABLED)

#reports functions
def emp_att_report():
    #clear frame from previous action
    for widget in sub_action_frame.winfo_children():
        widget.grid_forget()
    global var_num_report
    var_num_report = IntVar()
    var_num_report.set(0)

    top=Toplevel()
    top.geometry('500x300')
    top.wm_transient(root)
    x = root.winfo_x()
    y = root.winfo_y()
    top.geometry("+%d+%d" % (x + 100, y + 50))

    #define widgets
    action_label=Label(top, text=f'--Get employee attendance report--')
    input_message_label=Label(top,text=f"Please enter employee ID")
    id_entry=Entry(top, width=20, borderwidth=5)
    button_submit=Button(top, text=f"Submit", command=lambda : submit_button('report'))
    button_close_top = Button(top, text='Back to Admin menu', command=top.destroy)


    #arrange widgets
    action_label.grid(row=0, column=0, pady=5, columnspan=2)
    input_message_label.grid(row=1, column=0, pady=5)
    id_entry.grid(row=1, column=1, pady=5)
    button_submit.grid(row=2, column=0, pady=5, columnspan=2)
    button_close_top.grid(row=4, column=0, columnspan=2)

    #prompt user from emp_id
    while True:
        button_submit.wait_variable(var_num_report)
        emp_id = id_entry.get().strip()
        try:
            id_check, name, dob, rank = check_id(emp_id)
        except Exception as err:
            messagebox.showwarning('ID input issue', f'{err}')
            continue
        else:
            if id_check == 0:
                messagebox.showwarning('ID input issue', f'Employee doesnt exist in file \nAdd employees to DB via Admin menu')
                continue
        break

        #open attendance file to read it, if not existing prompt message
    try:
        with open('Attendance.csv') as csvfile:
            attendance=csv.reader(csvfile)
            # create a new list with the relevant employee's entrances. list of list
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

    button_submit.config(state=DISABLED)
    id_entry.delete(0,END)
def monthly_report():
    #clear frame from previous action
    for widget in sub_action_frame.winfo_children():
        widget.grid_forget()

    #go over attandance file print all the lines with the current date
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


def custom_att_report():
    # clear frame from previous action
    for widget in sub_action_frame.winfo_children():
        widget.grid_forget()
    var_rank=StringVar()
    var_rank.set("Choose a rank    ")
    ranks=['Junior', 'Senior', 'Manager', 'All']
    global var_start_date,  var_end_date, var_num_report_custom
    var_start_date=StringVar()
    var_start_date.set('Choose start date')
    var_end_date=StringVar()
    var_end_date.set('Choose end date')
    var_num_report_custom = IntVar()
    var_num_report_custom.set(0)

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
    button_submit=Button(top, text=f'Submit', command=lambda : submit_button('report_custom'))
    # result_label=Label(top,text=f"")

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
    # result_label.grid(row=8,column=0, columnspan=5,sticky=W, pady=5)

    button_close_top.grid(row=9, column=0, columnspan=5,sticky=W, pady=5)


    #get input and validate
    while True:
        button_submit.wait_variable(var_num_report_custom)
        #get user input for rank
        rank=var_rank.get()
        if rank not in ranks:
            messagebox.showwarning('Rank input error', 'Please choose a rank from list')
            continue
        #get user input for time range
        start_date_str=start_date_entry.get()
        end_date_str=end_date_entry.get()
        try:
            start_date=date.fromisoformat(start_date_str)
            end_date=date.fromisoformat(end_date_str)
            if start_date>datetime.today().date():
                messagebox.showwarning('Date input error', 'Start date cannot be in the future')
                continue
            if end_date<start_date:
                messagebox.showwarning('Date input error', 'End date cannot be before start date')
                continue
        except Exception as err:
            messagebox.showwarning('Date input error', f'Invalid date input, please try again. \nError: {err} ')
            continue
        break
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
        # result_label.config(text= f'--Report created successfully! \nSaved as "Att report {start_date} to {end_date} {rank} ranks.csv"--')
    button_submit.config(state=DISABLED)
def late_report():
    # clear frame from previous action
    for widget in sub_action_frame.winfo_children():
        widget.grid_forget()



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
def submit_button(option):
    global var_num_login, var_num_add, var_num_del, var_num_report, var_num_report_custom
    #several buttons call this function, we check which button called it and update the variable accordingly
    if option=='login':
        var_num_login.set(not var_num_login.get())
    elif option=='add':
        var_num_add.set(not var_num_add.get())
    elif option =='del':
        var_num_del.set(not var_num_del.get())
    elif option=='report':
        var_num_report.set(not var_num_report.get())
    elif option=='report_custom':
        var_num_report_custom.set(not var_num_report_custom.get())
def back_button():
    main_menu()
    return
def choose_file(option):
    global file_path, var_num_browse_add, var_num_browse_del
    current_dir = os.getcwd()
    root.filename=filedialog.askopenfilename(initialdir=current_dir, title='Select a file', filetypes=(('csv files','*.csv'),('all files','*.*')))
    file_path=root.filename
    if option=='add':
        var_num_browse_add.set(1)
    elif option == 'del':
        var_num_browse_del.set(1)
    return
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
def clear_subaction():
    # for widget in sub_action_frame.winfo_children():
    #     widget.grid_forget()
    # sub_action_frame.grid_forget()
    admin_menu()
    return
def validate_admin(emp_id):
    if emp_id.strip()=='8888':
        admin_menu()
        return
    try:
        id_check, name, dob, rank = check_id(emp_id)
    except Exception as err:
        messagebox.showwarning('Permission issue', f'{err}')
        return
    else:
        if rank=='Manager':
            admin_menu()
        else:
            messagebox.showwarning('Permission issue', 'Only managers have permission to perform this action')
    return

def grab_date(cal_start, cal_end):
    global var_start_date
    global var_end_date
    var_start_date.set(cal_start.get_date())
    var_end_date.set(cal_end.get_date())
    return

# top level functions
def admin_menu():

    # clear frame from previous action
    for widget in main_frame.winfo_children():
        widget.grid_forget()
    main_frame.place_forget()
    for widget in sub_action_frame.winfo_children():
        widget.grid_forget()
    sub_action_frame.grid_forget()

    label_welcome=Label(admin_menu_frame,text=f'---Administrator portal---')
    label_welcome.config(font=('Helvatical bold',12))


    #Admin menu frames
    button_back = Button(admin_menu_frame, text=f"<<back to main", command=back_button)
    # button_clear = Button(admin_menu_frame, text=f'Clear form', command=clear_subaction)
    frame_add_remove = LabelFrame(admin_menu_frame, pady=10, padx=20, text=f'Actions in employees file')
    frame_admin_reports = LabelFrame(admin_menu_frame, pady=10, padx=20, text=f'Generate attendance reports')

    # widgets in add\remove frame
    button_add_manually = Button(frame_add_remove, text=f'Add employee manually', width=30, command=add_manually)
    button_add_from_file = Button(frame_add_remove, text=f'Add employee from file', width=30, command=add_from_file)
    button_delete_manually = Button(frame_add_remove, text=f'Delete employee manually', width=30, command=del_manually)
    button_delete_from_file = Button(frame_add_remove, text=f'Delete Employee from file', width=30, command=del_from_file)

    # widgets in reports frame
    button_attendance_report_employee = Button(frame_admin_reports, text=f'Attendance report for a single employee', width=30, command=emp_att_report)
    button_attendance_this_month = Button(frame_admin_reports, text=f'Current month report for all employees', width=30, command=monthly_report)
    button_late_report = Button(frame_admin_reports, text=f'Late employees report', width=30, command=late_report)
    button_custom_report = Button(frame_admin_reports, text=f'Custom attendance report', width=30, command=custom_att_report)

    admin_menu_frame.place(x=350, y=0, anchor=N)
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

    sub_action_frame.grid(row=2,column=0,columnspan=2)
    # button_clear.grid(row=3, column=0, sticky=W)
    button_back.grid(row=4,column=0, sticky= W)

def main_menu():
    # clear frame from previous action
    for widget in admin_menu_frame.winfo_children():
        widget.grid_forget()
    admin_menu_frame.place_forget()

    global var_num_login
    var_num_login=IntVar()
    var_num_login.set(0)

    # Define main screen labels and buttons
    label_welcome = Label(main_frame, text=f'Welcome to employee time clock')
    label_welcome.config(font=('Helvatical bold', 12))
    button_admin = Button(main_frame, text=f'Admin menu', width=10, command=lambda : validate_admin(id_entry.get()))
    input_message_label = Label(main_frame, text=f"Eenter your employee ID to log in \n click 'admin menu' for more options")
    id_entry = Entry(main_frame, width=20, borderwidth=5)
    button_log_in = Button(main_frame, text=f'Log in', command=lambda : submit_button('login'))
    label_action_result = Label(main_frame, text=f"")
    bday_image = ImageTk.PhotoImage(Image.open('../bday.png'))

    # place main screen labels on root
    main_frame.place(x=350, y=0, anchor=N)
    label_welcome.grid( row=0, column=0, columnspan=3)
    input_message_label.grid(row=2, column=0,columnspan=3, pady=5)
    id_entry.grid(row=3, column=0, pady=5, padx=2, sticky=W)
    button_log_in.grid(row=3, column=1, padx=2, sticky=W)
    button_admin.grid(row=3,column=2, padx=2)
    label_action_result.grid(row=4, column=0, columnspan=3)

    while True:
        button_log_in.wait_variable(var_num_login)
        emp_id = id_entry.get().strip()
        id_entry.delete(0, END)
        try: #find the employee in employee file and get their details
            id_check, name, dob, rank = check_id(emp_id)
        except Exception as err: #error in the input validity
            messagebox.showwarning('ID input issue', f'{err}')
            continue #wait for the user to correct their input
        else: #we didn't get exception from employee file
            if id_check == 1:#means the employee exists and we got all their details
                #check if it's their birthday
                if datetime.fromisoformat(dob).month==datetime.today().date().month and datetime.fromisoformat(dob).day==datetime.today().date().day:
                    bday_image_label=Label(main_frame, image=bday_image, text=f"Congratulations {name}, it's your birthday!!!")
                    bday_image_label.grid(row=6,column=0,columnspan=2)
                    messagebox.showinfo('HAPPY BIRTHDAY', f"Congratulations {name}, it's your birthday!!!")
                # open attendance file to check if employee already checked in today.
                response=1
                try:
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
                    label_action_result.config(text=f"Something went wrong with opening attendance file for writing. \nError: {err}")
                    response=0
                    break #no need to keep waiting for correct input because there is somekind of error with the file
                finally:  # update the log according to 'response'
                    if response==0:# if they don't want to check in again
                        label_action_result.config(text=f'--{name} your current entry was not registered--')
                    else: #check the employee in
                        if mark_att(emp_id, name, rank) == True:
                            label_action_result.config(text=f'--{name}, your log in is registered-- \n --Date: {datetime.now().date().__str__()}, Time: {datetime.now().time().__str__()[:5]}--')
            else:
                label_action_result.config(text=f'--user does not appear in user list--')

root = Tk()
root.title('Employee Management System')
root.geometry('700x300')
var_num = IntVar()

global file_path
# mark_att_all()

# Define label common to all screens
main_frame=LabelFrame(root, width=600, height=600) #, relief='flat'
admin_menu_frame=LabelFrame(root,padx=20, pady=10)
sub_action_frame = LabelFrame(admin_menu_frame, pady=10, padx=20)

main_menu()

root.mainloop()




