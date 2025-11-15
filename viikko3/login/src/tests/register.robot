*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  Testi
    Set Password1  Testi123
    Set Password2  Testi123
    Click Button  Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  T
    Set Password1  Testi123
    Set Password2  Testi123
    Click Button  Register
    Register Should Fail With Message  Username must be atleast 3 characters long

Register With Valid Username And Too Short Password
    Set Username  Testi
    Set Password1  Testi
    Set Password2  Testi
    Click Button  Register
    Register Should Fail With Message  Password must be atleast 8 characters long

Register With Valid Username And Invalid Password
    Set Username  Testi
    Set Password1  Testinen
    Set Password2  Testinen
    Click Button  Register
    Register Should Fail With Message  Password must contain at least one number

Register With Nonmatching Password And Password Confirmation
    Set Username  Testi
    Set Password1  Testi123
    Set Password2  Testi456
    Click Button  Register
    Register Should Fail With Message  Passwords must match

Register With Username That Is Already In Use
    Set Username  kalle
    Set Password1  kalle123
    Set Password2  kalle123
    Click Button  Register
    Register Should Fail With Message  User with username kalle already exists

*** Keywords ***
Register Should Succeed
    Welcome Page Should Be Open

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password1
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password2
    [Arguments]  ${password}
    Input Password  password_confirmation  ${password}

*** Keywords ***
Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page