# TESTING 

---
## Table of Contents 

- [TESTING](#testing)
  - [Table of Contents](#table-of-contents)
  - [Manual Testing](#manual-testing)
    - [Results of Syntax Validation with PEP8](#results-of-syntax-validation-with-pep8)
    - [Results of User Stories Test](#results-of-user-stories-test)
    - [Results of Functionality Tests](#results-of-functionality-tests)
    - [Results of Other Tests](#results-of-other-tests)
    - [Issues Found During Manual Testing](#issues-found-during-manual-testing)
  - [Automated Testing](#automated-testing)
    - [Setup of Automated Testing with Pytest](#setup-of-automated-testing-with-pytest)
    - [Results of Unit Testing with Pytest](#results-of-unit-testing-with-pytest)
      - [Participant Class](#participant-class)
      - [Meeting Class](#meeting-class)
      - [Schedule Class](#schedule-class)
      - [Worksheet Class](#worksheet-class)


--- 

## Manual Testing


The Manual Testing document can be found here : [Numbers Testing Results](./assets/documentation/Manual-Testing-Results.numbers).

### Results of Syntax Validation with PEP8

### Results of User Stories Test 

### Results of Functionality Tests

### Results of Other Tests

### Issues Found During Manual Testing

--- 

## Automated Testing

- This project has been implemented using a `test-driven` approach, where each bit of functionality was added incrementally using a `red-green-refactor` cycle 
- One of the advantages of this approach that code changes at a later timepoint that negatively affect other parts of the codebase are flagged early on during development while working on the function 
- While it may slightly increase the time to develop the tests in parallel to the function, ultimately it saves time by reducing the time needed for finding bugs.

The follwing section contains: 
  - Setup of the database used during Unit Testing
  - Results of Unit Tests 

### Setup of Automated Testing with Pytest

- If you also want to pass all unit tests you need to add a fourth sheet 'unit-test' to the sheet
- This sheet is not necessary to run the application. However, for unit testing of the methods for reading/writing, we cannot use the main sheet because the user can edit those meetings and the unit test would fail (although the read/write methods are correct). 
- There are a few strategies to mitigate this problem including mocking of the worksheet. A better option was suggested on [stackoverflow]( https://stackoverflow.com/questions/1217736/how-to-write-unit-tests-for-database-calls) to instead connect to a known database and test the code with those sheets
- I modified this idea by adding a fourth sheet 'unit-test' to our google sheet that is not used by the app, just for the unit test, but mimicks exactly the columns as the first (schedule) sheet. This sheet will never be modifed by the app. We then assume: if the function works for reading and writing to the fourth sheet, it should work for the first and second as well.
- This is how the unit test worksheet looks like:

<table style='width:80%'>
    <tr>
        <th style='text-align:center'>Unit Test Worksheet</th>
    </tr>
    <tr>
       <td> <img src="./assets/images/sheet-unit-test.png"; alt="example of the  worksheet to test the read/write functions of the unit test" >  </td>
    </tr>
</table>

--- 
### Results of Unit Testing with Pytest 

#### Participant Class

#### Meeting Class 

#### Schedule Class 

#### Worksheet Class 


-----
