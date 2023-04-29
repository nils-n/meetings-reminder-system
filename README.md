# Meetings reminder system 

This python-based web app is designed to keep track of open meetings, send reminder meetings to participants, and reminder to oneself if the meeting itself, or one of the participants, has not confirmed his or her assistance.

Link to the live terminal : TO DO 


![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)


--- 

## Table of Contents



----
## User Experience (UX)


### User Stories 

As a first-time user...
<ol>
    <li> I want to be able to create and delete meetings </li>
    <li> I want to be able to see all my upcoming meetings in the following week or day</li>
    <li> I want to be able to modify meetings details of an upcoming meeting</li>
    <li> I want to to be able to add and remove particpants from the meeting </li>
    <li> I want to to be able to turn on and off notifications for a meeting </li>
    <li> I want to automatically receive a notification email if the meeting itself has not been confirmed (24h prior meeting)  </li>
    <li> I want to automatically receive a notification email if a participant has not confirmed his assistance (24h prior meeting)  </li>
    <li> I want to automatically send reminder emails to all particpants who have confirmed assistance (24h prior meeting)</li>
</ol>

### Website Aims

<ul>
    <li> add an automation task that requires low-level attention to repeating events or meetings </li>
    <li>  reduce likelihood that meetings are missed, or that participants do not attend a meeting </li>
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
        <td> Create a new meeting  </td>
        <td> 5  </td>
        <td> 5  </td>
    </tr>
    <tr>
        <td> Delete a meeting  </td>
        <td> 5  </td>
        <td> 5  </td>
    </tr>
     <tr>
        <td> Add participants to meeting   </td>
        <td> 5  </td>
        <td> 5  </td>
    </tr>
        <tr>
        <td>  Remove participants from meeting   </td>
        <td> 5  </td>
        <td> 5  </td>
    </tr>
    <tr>
        <td > Send reminders to participants who have confirmed assistance (24hrs before meeting)   </td>
        <td> 5  </td>
        <td> 5  </td>
    </tr>
    <tr>
        <td style="max-width:200px"> send reminders to oneself if participant has not confirmed  (24hrs before meeting)   </td>
        <td> 5  </td>
        <td> 5  </td>
    </tr>
     <tr>
        <td>Send reminders to oneself if meeting itself has not been confirmed  (24hrs before meeting)  </td>
        <td> 5  </td>
        <td> 5  </td>
    </tr>
  <tr>
        <td> Display list upcoming meetings and allow to browse details </td>
        <td> 5  </td>
        <td> 5  </td>
    </tr>
     <tr>
        <td> allow to turn on/off notifications for each meeting and/or participant </td>
        <td> 3  </td>
        <td> 4  </td>
    </tr>
     <tr>
        <td> connect to a web app that checks Microsoft Outlook Calender </td>
        <td> 2 </td>
        <td> 4 </td>
    </tr>

</table>


--- 

### Feature selection

----- 

## Design


### Imagery


---

## Wireframes

### Program Flow Chart


----- 

## Features

### General Features 

### Future Implementations

### Accessibility

--- 

## Technologies Used 

-  Git / [Github](https://github.com/)  for Version Control 
- [VS Code ](https://code.visualstudio.com/) as IDE for local devlopment  
- [Figma](https://www.figma.com/) for the Flowchart 
- [W3 Validation Tools](https://validator.w3.org/) for Testing
- [Shields.io](https://shields.io/) for Readme badges
- [Markdown Beautifier](https://markdownbeautifier.com/#)  to format tables in this Readme
- convert markdown tables to html via [HTML Table Converter](https://tableconvert.com/markdown-to-html)
- Markdown [TOC Generator](https://ecotrust-canada.github.io/markdown-toc/)
- [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode) VS Code formatter 



### Languages Used

- HTML 
- Python

### Frameworks Used

- [pytest](https://docs.pytest.org/en/7.3.x/) for unit tests 


----- 

## Deployment and Local Development 

### Deployment on Heroku 


#### How to Fork


#### How to Clone

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

### Open Bugs 


---- 

## Credits 

### Code Used

### Content 

- All of the content was written by myself.
- Externally used code (such as code snippets from stackoverflow) in this project are referenced in this Readme and inside the html or python source code. 

## Acknowledgements

- Teaching and Support from Code Insitute [Code Insitute](https://codeinstitute.net/)
- Example Readme from Kera Cudmore [Kera's Github](https://github.com/kera-cudmore/readme-examples/blob/main/milestone1-readme.md)
- Images from  [Pexels](https://pexels.com/)  in case you use a BG image (check this!)
- tutoria;s for unit python unit testing with pytest (update this once you started using it) 
- Talks from Dylan Israel about Unit Testing: [Link - Clean Coding](https://youtu.be/YQsU2Zq2Zis) 
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
