*** Settings ***
Documentation    Web testing example
Library          SeleniumLibrary

*** Variables ***
${BROWSER}      chrome
${URL}          https://robotframework.org

*** Test Cases ***
Open Robot Framework Website
    Open Browser    ${URL}    ${BROWSER}
    Title Should Be    Robot Framework
    Capture Page Screenshot
    
    ${title}    Get Title
    Log    Page title: ${title}
    
    [Teardown]    Close Browser

*** Keywords ***
Setup Browser
    Open Browser    about:blank    ${BROWSER}
    Maximize Browser Window

Teardown Browser
    Close All Browsers
