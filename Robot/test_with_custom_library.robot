*** Settings ***
Documentation    Test using custom Python library
Library          custom_library.CustomLibrary
Library          Collections

*** Test Cases ***
Test Custom Library Methods
    ${sum_result}    Add Numbers    15    25
    Should Be Equal As Numbers    ${sum_result}    40
    
    ${product}    Multiply Numbers    6    7
    Should Be Equal As Numbers    ${product}    42
    
    ${timestamp}    Get Current Timestamp
    Should Contain    ${timestamp}    202
