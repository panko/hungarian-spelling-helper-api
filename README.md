# Hungarian spelling helper API
## Description
In the Hungarian language there are words with "J" and with "LY". Phonetically they are the same, however there is no rule which should be used where. During learning Hungarian this is challenging to learn for every students.  
So, lets create a RESTFUL API for helping the students to learn where to use "J" or "LY".
## Technical requirements
- Python3, Flask
- Persistent storage (sqlite3)
- Proper encodeing, Utf-8
## Must have features
- [X] Predefined list of words containing J or Ly
- [X] Ask for username, and store results
- [X] Ask user the desired number of asked words every round
- [X] Ask words randomly, change the spelling randomly, ask if its correct or not
- [X] Show round result at the end
- [X] Simple GUI
## Optional features
- [X] Expand predefined wordlist
- [ ] Ask the wrong answers again until we send back the number of the failures
## What will be checked
- [ ] Existence and quality of tests
- [ ] API whether it is clear, rest like
- [ ] Quality of code: naming, clarity, adherence to Clean Coding
- [ ] Correctness (Hopefully reviewing the tests will suffice)
- [ ] Ease of deployment: we would like to see it running in our private environment and deploy it with no fuss
