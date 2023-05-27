# Meetings reminder system 

This python-based terminal app is designed to organize meeting reminders. The goal is to free the user of low-level attention tasks that are associated with organizing meetings and keeping track that participants show up to the meeting. This is achieved by automatizing the process of sending meeting invitations and reminder emails.

Link to the live terminal : TO DO 

![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)


--- 

## Table of Contents



----
## User Experience (UX)


### User Stories 

As a user of this terminal application...
<ol>
    <li> I want to see all my scheduled meetings on a first glance.</li>
    <li> I want to be able to create, read, update, delete a meeting.</li>
    <li> I want to be able to add or delete participants from a particular meeting.</li>
    <li> I want to be able to update information of a meeting, such as: time, place or the meeting notes.</li>
    <li> I want every participant to receive a reminder email at least 24hrs before the meeting.</li>
    <li> I want to have the option to turned notification off for individual participants or entire meetings (opt-out principle)</li>
    <li> I want to ensure that a reminder email is sent only once per participant.</li>
     <li> If I did not send the reminder email manually 24hrs before the meeting, i want the system to send an automatic reminder email instead.</li>
    <li> When a meeting is in the past, i do not want to have it displayed with the other meetings</li>
</ol>

### Website Aims

<ul>
    <li> add an automation task that requires low-level attention to organzing an event or meetings </li>
    <li> reduce likelihood that meetings are missed, or that participants do not attend a meeting </li>
</ul>


### How these needs are addressed

- Item 1
- Item 2


### Opportunities 


<table  style="margin: 0 auto; width: 80%">
    <tr >
        <th > Description </th>
        <th> Impact </th>
        <th> Feasibility </th>
    </tr>
    <tr>
        <td> Create,Read ,Update or Delete a meeting  </td>
        <td> 5  </td>
        <td> 5  </td>
    </tr>
     <tr>
        <td> Create, Read, Update and Delete a participant of a meeting   </td>
        <td> 5  </td>
        <td> 5  </td>
    </tr>
    <tr>
        <td >  Add, remove and update notes attached to the reminder email   </td>
        <td> 5  </td>
        <td> 5  </td>
    </tr>
     <tr>
        <td style="max-width:200px"> Send a reminder to participants with a button press  </td>
        <td> 5  </td>
        <td> 5  </td>
    </tr>
    <tr>
        <td style="max-width:200px"> Send automatic reminder to participants who have not received a manual reminder email 24hrs before meeting   </td>
        <td> 5  </td>
        <td> 5  </td>
    </tr>
  <tr>
        <td> Display list of upcoming meetings and allow to browse details </td>
        <td> 5  </td>
        <td> 5  </td>
    </tr>
     <tr>
        <td> allow to turn on/off notifications for each meeting and participant </td>
        <td> 3  </td>
        <td> 4  </td>
    </tr>

    

</table>


--- 

### Feature selection

----- 

## Design


### Imagery


--- 

### Data Structures

The information about meetings and participants will be stored using Google sheets: 

<table style='max-width:80%; text-align: center'>
    <tr>
        <th style='text-align:center'> Python Class</th>
        <th style='text-align:center'> Flow Chart - Python</th>
    </tr>
    <tr>
        <td> Meeting Data </td>
        <td> <img src="./assets/images/google-sheet-example-1.png"; alt="example data of thr meetings as stored in google sheets " >  </td>
    </tr>
   <tr>
        <td> Particiant Data </td>
        <td> <img src="./assets/images/google-sheet-example-2.png"; alt="example data of the participants as stored in google sheets " >  </td>
    </tr>
</table>

--- 

### Implementation in Python  

The implementation will be divided into two Apps:
-  TerminalApp : User Terminal Application where the user can interact with the Meeting schedule
-  ReminderApp : A small worker application that sends reminders based on the Meeting schedule

These are the classes that will model the behaviour:
- Meeting Class: to describe details of the meeting (that consists of participants)
- Participant Class: to describe details of the participant
- Worksheet Class : describes interaction with Google Sheets (read/write)
- Schedule Class : to store and handle all scheduled Meetings 

<table style='max-width:70%'>
    <tr>
        <th style='text-align:center'> Python : Classes</th>
    </tr>
    <tr>
        <td> <img src="./assets/images/classes-python.png"; alt="outline of python classes for this project" >  </td>
    </tr>
</table>

----- 



## Wireframes


### Program Flow Chart

The functionality of the python program is displayed below. 

<table>
    <tr>
        <th style='text-align:center'> Flow Chart - Python</th>
    </tr>
    <tr>
        <td> <img src="./assets/images/flowchart-reminder-system.png"; alt="flowchart of the python objects" >  </td>
    </tr>
</table>

-----

## Features

### General Features 

### Future Implementations

- Add option for recurring meetings 
- Add option to connect to a calendar (Gmail, Outlook) to check for availability of participants
- send a calender invite (for simplicity, this project sends currently only emails) 
- create options for virutal meetings (i.e. add options for zoom)

### Accessibility

--- 



## Technologies Used 

-  Git / [Github](https://github.com/)  for Version Control 
- [VS Code ](https://code.visualstudio.com/) as local IDE  
- [ Code Anywhere ](.codeanywhere.com) as cloud IDE 
- [Figma](https://www.figma.com/) for the Flowchart 
- [W3 Validation Tools](https://validator.w3.org/) for Testing
- [Shields.io](https://shields.io/) for Readme badges
- [Markdown Beautifier](https://markdownbeautifier.com/#)  to format tables in this Readme
- convert markdown tables to html via [HTML Table Converter](https://tableconvert.com/markdown-to-html)
- Markdown [TOC Generator](https://ecotrust-canada.github.io/markdown-toc/)
- [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode) VS Code formatter 
- [Pseudo](https://marketplace.visualstudio.com/items?itemName=willumz.generic-pseudocode) VS Code plugin to write pseudocode


### Languages 

- HTML 
- Python

### Frameworks 

- 

### Python Packages 


<table style='max-width:70%'>
    <tr>
        <th style='text-align:center'>  Name</th>
        <th> Purpose </th>
    </tr>
        <tr>
        <td> textual / rich </td>
        <td> to create a terminal user interface</td>
    </tr>
    <tr>
        <td> email / ezgmail  </td>
        <td>  to send emails from python  </td>
    </tr>
     <tr>
        <td> pytest </td>
        <td>   for unit tests  </td>
    </tr>  
       <tr>
        <td> email_validator </td>
        <td>   to validate that email has correct form  </td>
    </tr>  
    
</table>



----- 

## Deployment and Local Development 

Most of the features of this application run fine on a local computer (any interactions with the schedule such as read/delete/update meetings etc.).
However, deploying on Heroku has the advantage that the meeting reminders will also be sent automatically on a scheduled basis.

#### How to Fork

- Log into GitHub and navigate to this repository  
- Click on the "Main" Branch button and type the name of the forked branch
- Click on "Create Branch" to confirm

#### How to Clone

- Click on the "Code" button and copy the link to this repository
- open terminal on your machine and navigate to the folder you want to store a local copy
- in the terminal, type 'git clone ' followed by the link you copied
- press enter to confirm

### Deployment on Heroku 

- Heroku will requires public access to the `reminding` package inside your forked repository. Basically i wsee [this explanation from Heroku](https://devcenter.heroku.com/articles/python-pip) 
- Create an account on [Heroku](https://dashboard.heroku.com/apps)
- Log into Heroku 
- Go to Dashboard and click on `New` > `New App`
- Choose a name i.e. my-meetings and region (EU) then click on `Create App`
- Connect with your forked repository on github
- Switch to `Settings` Tab
    - Config Vars and add `PORT` with value `8000`
    -  `NOTE FOR LATER` add here more credentials when adding config vars
    - On `Buildpacks` choose in that order (the order matters)
        -  `heroku/python` 
        -  `heroku/nodejs`
-   Switch to to `Deploy` Tab 
    - If you want to deploy just once, `Manual deply` section > Click on `Deploy Branch` 
    - If you want to deploy automatically after each commit to your repository, choose `Enable Automatic Deploys` on `Automatic Deploys` section

--- 

## Testing 

### Testing Procedure 
The website was tested extensively for several apsects , and the results were documented in [---TO DO ---TESTING.md](./TESTING.md) 

- Functionality
- User Stories
- Usability and Accessibility 
- Compatibility and Responsiveness 

Also, this website was developed using a `test-driven development` (TDD) approach using the `pytest` framework for python. Results of of the unit tests are documented in same document above. The reasons for TDD is to 
- ... ensure core functionality
- ... better code re-usability 
- ... better code readibility by enforcing smaller functions.

(clean code principles).

---

### Solved Bugs 

- After packaging the python code into an installable package ( so that we can use classes via `from reminding.meeting import Meeting`), the app would not deploy  on Heroku: 
    <table style='max-width:80%; text-align: left'>

    <tr>
    <td> Error Message</td>
    <td> <img src="./assets/images/heroku-build-error.png"; alt="
    image of heroku error message caused by python dependencies. Here the message on the image: 
        Running command git clone --filter=blob:none --quiet https://github.com/nils-n/meetings-reminder-system.git /app/.heroku/src/reminding
        fatal: could not read Username for 'https://github.com': No such device or address
        error: subprocess-exited-with-error
        × git clone --filter=blob:none --quiet https://github.com/nils-n/meetings-reminder-system.git /app/.heroku/src/reminding did not run successfully.
        │ exit code: 128 " >   </td>
    </tr>
    <tr>
    <td> Solution</td>
    <td> 
    Setting the visibility of the repository from `private` to `public`. In this way, the `reminding` dependency from this repository could be installed successfully. There are other options for private repositories (see [Heroku Devcenter](https://devcenter.heroku.com/articles/python-pip) or [Stackoverflow ](https://stackoverflow.com/questions/21297755/heroku-python-dependencies-in-private-repos-without-storing-my-password)) but none of these were deemed safe or good practice (i.e. storing private SSH-KEYs as environment variable). Being mindful about the scope of this project, it was chosen to follow the easier and safer approach by setting visibility to 'public'. 
    </td>
    </tr>
    </table>

### Open Bugs 



---- 

## Credits 

### Code Used

- How to write emails from python [Link](https://towardsdatascience.com/how-to-easily-automate-emails-with-python-8b476045c151)
- How to schedule a python task on Heroku [Link](https://www.youtube.com/watch?v=qn3Obj56wfA)
- Textual Tutorial : Stopwatch Application [Link](https://textual.textualize.io/tutorial/)
- Starting point for pyproject.toml file [Link](https://github.com/tiangolo/fastapi/tree/master);


### Content 

- All of the content was written by myself.
- Externally used code (such as code snippets from stackoverflow or from tutorials) in this project are referenced in this Readme and inside the html or python source code. 

## Acknowledgements

- Teaching and Support from Code Insitute [Code Insitute](https://codeinstitute.net/)
- How to setup python packages that are testable with pytest 
    - Good Integration Practices for pytest [Link](https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html)
    - Packaging Python Projects [Link](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
    - James' Murphys Yotube Tutorial for unit testing with python [Link](https://youtu.be/DhUpxWjOhME)
    - Effective Python Testing with Pytest [Link](https://realpython.com/pytest-python-testing/)
    - Okken, Brian. "Python Testing with pytest." Pragmatic Bookshelf, 2022.
- Console-based Terminal User Interface by William McGugan [GitHub Textual](https://github.com/textualize/textual/)
- Example Readme from Kera Cudmore [Kera's Github](https://github.com/kera-cudmore/readme-examples/blob/main/milestone1-readme.md)
- Images from  [Pexels](https://pexels.com/)  in case you use a BG image (check this!)
- examples from pytest about parametrized tests [pytest docs](https://docs.pytest.org/en/7.1.x/example/parametrize.html) 
- tutorials for unit python unit testing with pytest (update this once you started using it) 
    - Pytest Unit Testing Tutorial - How to test your Python code [pixegami (Youtube)](https://www.youtube.com/watch?v=YbpKMIUjvK8)
    - why to use dataclass decorators [mCoding (Youtube)](https://www.youtube.com/watch?v=vBH6GRJ1REM)
    - Automated Testing in Python with pytest, tox, and GitHub Actions [mCoding (Youtube) ](https://www.youtube.com/watch?v=DhUpxWjOhME)
    - Pytest: How to use fixtures as arguments in parametrize [Article](https://engineeringfordatascience.com/posts/pytest_fixtures_with_parameterize/)
- Talks from Dylan Israel about Unit Testing: [Clean Code (Youtube)](https://youtu.be/YQsU2Zq2Zis) 
- Last but not least : Thanks to my mentor Ronan (Code Institute) for his advices and clear feedback 


--



<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

Welcome,

This is the Code Institute student template for deploying your third portfolio project, the Python command-line project. The last update to this file was: **March 14, 2023**

## Reminders

- Your code must be placed in the `run.py` file
- Your dependencies must be placed in the `requirements.txt` file
- Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

---

Happy coding!
