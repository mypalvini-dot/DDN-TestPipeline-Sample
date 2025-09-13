*** Settings ***
Documentation    API testing example
Library          RequestsLibrary
Library          Collections

*** Variables ***
${BASE_URL}    https://jsonplaceholder.typicode.com

*** Test Cases ***
GET Request Test
    Create Session    jsonplaceholder    ${BASE_URL}
    
    ${response}    GET On Session    jsonplaceholder    /posts/1
    Should Be Equal As Numbers    ${response.status_code}    200
    
    ${json}    Set Variable    ${response.json()}
    Dictionary Should Contain Key    ${json}    title
    Dictionary Should Contain Key    ${json}    body
    
    Log    Title: ${json['title']}

POST Request Test
    Create Session    jsonplaceholder    ${BASE_URL}
    
    &{data}    Create Dictionary
    ...    title=Test Post
    ...    body=This is a test body
    ...    userId=1
    
    ${response}    POST On Session    jsonplaceholder    /posts    json=${data}
    Should Be Equal As Numbers    ${response.status_code}    201
    
    ${json}    Set Variable    ${response.json()}
    Should Be Equal    ${json['title']}    Test Post
