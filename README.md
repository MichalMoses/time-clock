# time-clock
Managing your employees' attendance<br>

A simple app for managing employees attendance - enables users to log in once arriving to work, enables admin to generate reports of login time of all the user. <br>
I built this app using Python and Tkinter as a final project of my basic python class at She-Codes. Data is stored in csv files. <br>

The app contains the following screens:<br>

## Log in screen<br>
input employee id and click login for clocking in<br>
input admin id and click 'admin menu' to access the admin menu (admin id currently set to 8888)<br>
<img src="https://user-images.githubusercontent.com/119158314/224833046-1bb897cc-7246-4016-afed-1e608ed19702.png" width="700"><br>


## Admin menu <br>
Options divided to two group: <br>
"Actions in employees file" - enbales admin to add new employees or delete employees<br>
"Generate addendance reports" - enables admin to generate attendance reports for the employees.<br>
  <img src="https://user-images.githubusercontent.com/119158314/224833185-3840b2d1-db46-4364-aa81-13a876e7bb45.png" width="700"><br>  

## Actions in employee file<br>
### Add employee manually
Manually input all the employees detail to create a new employee in file<br>
  <img src="https://user-images.githubusercontent.com/119158314/224833526-e2d4289f-bf40-4790-8c96-e80ce47999c5.png" width="500"><br>  

### Add employee from file
Add a new employee or a group of employees by getting their data from a csv file of the same format as the emloyees file<br>
  <img src="https://user-images.githubusercontent.com/119158314/224833670-c85302ae-cb95-4671-aae8-585f297a4397.png" width="500"><br>  

### Delete employee manually
Delete an employee from file by the employee id.<br>
  <img src="https://user-images.githubusercontent.com/119158314/224833780-6c245165-8ecc-449f-9c34-df2b2b577160.png" width="500"><br>  

### Delete employee from file 
Delete a single or multiple employees by getting their data from a csv file of the same format as the emloyees file <br>
  <img src="https://user-images.githubusercontent.com/119158314/224833814-05d09ed4-e5e8-4509-b29a-e40a290e00c3.png" width="500"><br>  

## Generate attendance reports<br>
All reports are saved under under dir "/Reports" 
<img src="https://user-images.githubusercontent.com/119158314/222112774-e290367d-7f20-4de6-ac18-c21762ac9c7e.png" width="700"><br>

### Attendance report for a single employee
Will generate a csv file containing all the employee's registered entries<br>
### Current month report for all employees
Will create a csv file with all the registered log ins of the current month.<br>
### Late employees report
Will create a csv file wtih all the log-ins later than 9:30 ('late time' can be changed in code')<br>
### Custom attendance report
Will create a csv file with all the log-ins in for a spefic emplyee ranks and specific date range<br>
    <img src="https://user-images.githubusercontent.com/119158314/224834084-4bb865e6-bd6c-4033-8f19-948cb5b0d5a1.png" width="600"><br>  


  

    

  
  
