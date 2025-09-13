*** Settings ***
Documentation    Example test suite demonstrating Robot Framework structure
Library          Collections
Library          OperatingSystem
Library          String

*** Variables ***
${BROWSER}      chrome
${URL}          https://example.com
${TIMEOUT}      10s

*** Test Cases ***
Simple Arithmetic Test
    [Documentation]    Test basic arithmetic operations
    ${result}    Evaluate    5 + 3
    Should Be Equal As Numbers    ${result}    8
    
    ${result}    Evaluate    10 * 2
    Should Be Equal As Numbers    ${result}    20

String Manipulation Test
    [Documentation]    Test string operations
    ${text}    Set Variable    Hello World
    ${upper}    Convert To Upper Case    ${text}
    Should Be Equal    ${upper}    HELLO WORLD
    
    ${length}    Get Length    ${text}
    Should Be Equal As Numbers    ${length}    11

File Operation Test
    [Documentation]    Test file operations
    Create File    test_file.txt    This is test content
    File Should Exist    test_file.txt
    
    ${content}    Get File    test_file.txt
    Should Contain    ${content}    test content
    
    [Teardown]    Remove File    test_file.txt

List Operations Test
    [Documentation]    Test list operations
    @{fruits}    Create List    apple    banana    orange
    Length Should Be    ${fruits}    3
    Should Contain    ${fruits}    banana

*** Keywords ***
Log Custom Message
    [Arguments]    ${message}
    Log    Custom message: ${message}
    Return From Keyword    Message processed: ${message}

Calculate Sum
    [Arguments]    ${a}    ${b}
    ${result}    Evaluate    ${a} + ${b}
    [Return]    ${result}
