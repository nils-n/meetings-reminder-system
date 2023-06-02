

# TESTING 


## Table of Contents 

  * [Table of Contents](#table-of-contents)
  * [Functionality Tests](#functionality-tests)
    + [PEP8 Validation Results](#pep8-validation-results)
    + [Manual Testing Results](#manual-testing-results)
  * [Unit Testing with Pytest](#unit-testing-with-pytest)
  * [Tests of User Stories](#tests-of-user-stories)
  * [Tests For Compatibility](#tests-for-compatibility)
  * [Issues Found During Testing](#issues-found-during-testing)
  * [Add Worksheet for Unittest with Pytest](#add-worksheet-for-unittest-with-pytest)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


## Functionality Tests 

### PEP8 Validation Results 


### Manual Testing Results 

The Manual Testing document can be found here : [Numbers Testing Results](./assets/documentation/Manual-Testing-Results.numbers).

## Unit Testing with Pytest 

## Tests of User Stories 

## Tests For Compatibility

## Issues Found During Testing


-----

##  Add Worksheet for Unittest with Pytest


- If you also want to pass all unit tests you need to add a fourth sheet 'unit-test' to the sheet
- This sheet is not necessary to run the application. However, for unit testing of the methods for reading/writing, we cannot use the main sheet because the user can edit those meetings and the unit test would fail (although the read/write methods are correct). 
- There are a few strategies to mitigate this problem including mocking of the worksheet. A better option was suggested on [stackoverflow]( https://stackoverflow.com/questions/1217736/how-to-write-unit-tests-for-database-calls) to instead connect to a known database and test the code with those sheets
- I modified this idea by adding a fourth sheet 'unit-test' to our google sheet that is not used by the app, just for the unit test, but mimicks exactly the columns as the first (schedule) sheet. This sheet will never be modifed by the app. We then assume: if the function works for reading and writing to the fourth sheet, it should work for the first and second as well.
- To add this sheet:
    - Go to your sheet `Meeting-Reminders` :
        - add another sheet and name it 'unit-test'
        - Enter the exact values from the sheet from the image. This is your expectation that pytest can now reference to within the unit test 

  <table style='width:80%'>
     <tr>
       <th style='text-align:center'>Unit Test Worksheet</th>
      </tr>
       <tr>
       <td> <img src="./assets/images/sheet-unit-test.png"; alt="example of the  worksheet to test the read/write functions of the unit test" >  </td>
       </tr>
  </table>