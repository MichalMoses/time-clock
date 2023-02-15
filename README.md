# time-clock
Managing your employees' attendance<br>

A simple app for managing employees attendance - enables users to log in once arriving to work, enables admin to generate reports of login time of all the user. <br>
I built this app using Python and Tkinter as a final project of my basic python class at She-Codes. Data is stored in csv files. <br>

The app contains the following screens:<br>

1. Log in screen<br>
   input employee id and click login for clocking in<br>
   input admin id and click 'admin menu' to access the admin menu (admin id currently set to 8888)<br>
![image](https://user-images.githubusercontent.com/119158314/218956775-e6f32a20-49ff-4f10-ac80-eca5074ff52f.png)
    <br>

2. Admin menu <br>
Options divided to two group: <br>
"Actions in employees file" - enbales admin to add new employees or delete employees<br>
"Generate addendance reports" - enables admin to generate attendance reports for the employees.<br>
![image](https://user-images.githubusercontent.com/119158314/218957521-ad1fe0a3-b0d0-496f-91f7-b7c0efd5a1ec.png)
    <br>

2.1. Actions in employee file - <br>
  2.1.1. Add employee manually - manually input all the employees detail to create a new employee in file<br>
  ![image](https://user-images.githubusercontent.com/119158314/218957836-5deddf25-3bec-44a0-8720-b3eb4d64fa0c.png)<br>
  2.1.2. Add employee from file - add a new employee or a group of employees by getting their data from a csv file with the specific format<br>
  ![image](https://user-images.githubusercontent.com/119158314/218958148-9165b85d-fea5-4c7a-bb78-9a7b50e7ba76.png)<br>
  2.1.3. Delete employee manually- delete an employee from file by the employee id.<br>
  ![image](https://user-images.githubusercontent.com/119158314/218958332-882f6c59-b52c-496d-981e-80ce77113ae1.png)<br>
  2.1.4. Delete a single or multiple employees by getting their data from a csv file <br>
  ![image](https://user-images.githubusercontent.com/119158314/218959065-ecfaeebe-67fd-4b30-a1a2-0483eb067bb0.png)<br>
2.2. Generate attendance reports - <br>
  2.2.1. Attendance report for a single employee - will generate a csv file under dir "/reports" containing all the employee's registered entries
  ![image](https://user-images.githubusercontent.com/119158314/218959930-9f9d23c1-cfb7-4177-9a86-421e1ac05c60.png)<br>
  2.2.2. Current month report for all employees - will create a csv file with all the registered log ins of the current month.<br>
  2.2.3. Late employees report - will create a csv file wtih all the log-ins later than 9:30 ('late time' can be changed in code')<br>
  2.2.4. Custom attendance report - will create a csv file with all the log-ins in for a spefic emplyee ranks and specific date range<br>
  ![image](https://user-images.githubusercontent.com/119158314/218960593-10d3c90e-bbfc-460e-bd2f-41d573e20c1d.png)<br>
  
  

  

    

  
  
