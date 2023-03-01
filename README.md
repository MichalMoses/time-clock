# time-clock
Managing your employees' attendance<br>

A simple app for managing employees attendance - enables users to log in once arriving to work, enables admin to generate reports of login time of all the user. <br>
I built this app using Python and Tkinter as a final project of my basic python class at She-Codes. Data is stored in csv files. <br>

The app contains the following screens:<br>

## Log in screen<br>
input employee id and click login for clocking in<br>
input admin id and click 'admin menu' to access the admin menu (admin id currently set to 8888)<br>
<img src="https://user-images.githubusercontent.com/119158314/222097654-43fb81be-f511-44c1-b57d-546d1ac4c564.png" width="700"><br>


## Admin menu <br>
Options divided to two group: <br>
"Actions in employees file" - enbales admin to add new employees or delete employees<br>
"Generate addendance reports" - enables admin to generate attendance reports for the employees.<br>
<img src="https://user-images.githubusercontent.com/119158314/222098221-0e2e9d44-ecdf-4c16-b4e2-8853baac736d.png" width="700"><br>

## Actions in employee file<br>
### Add employee manually
Manually input all the employees detail to create a new employee in file<br>
  <img src="https://user-images.githubusercontent.com/119158314/222098377-dbdf6e8b-f132-447e-b78a-16b5800f7a74.png" width="700"><br>  
  
### Add employee from file
Add a new employee or a group of employees by getting their data from a csv file of the same format as the emloyees file<br>
  <img src="https://user-images.githubusercontent.com/119158314/222098575-78484d91-49f7-4bfc-8f4f-1171c5ddc3d5.png" width="700"><br>  

### Delete employee manually
Delete an employee from file by the employee id.<br>
  <img src="https://user-images.githubusercontent.com/119158314/222098813-4a35c8cd-e867-4d2c-941f-f99caeec08d8.png" width="700"><br>  

### Delete employee from file 
Delete a single or multiple employees by getting their data from a csv file of the same format as the emloyees file <br>
  <img src="https://user-images.githubusercontent.com/119158314/222099107-17a6e16f-ec07-481b-98aa-3b81a9ecb90a.png" width="700"><br>  


## Generate attendance reports<br>
All reports are saved under under dir "/Reports" 
  <img src="https://user-images.githubusercontent.com/119158314/222100702-5c2649be-a1a8-4bd0-9310-4e5d3b5a89ac.png" width="700"><br>  

### Attendance report for a single employee
Will generate a csv file containing all the employee's registered entries<br>
### Current month report for all employees
Will create a csv file with all the registered log ins of the current month.<br>
### Late employees report
Will create a csv file wtih all the log-ins later than 9:30 ('late time' can be changed in code')<br>
### Custom attendance report
Will create a csv file with all the log-ins in for a spefic emplyee ranks and specific date range<br>
    <img src="https://user-images.githubusercontent.com/119158314/222099631-117dcfdc-5131-4952-a661-39d8c0c934af.png" width="700"><br>  


  

    

  
  
