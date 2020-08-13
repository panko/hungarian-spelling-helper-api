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
- [X] Ease of deployment: we would like to see it running in our private environment and deploy it with no fuss
## deployment - docker
- $ docker build -t hsha .
- $ docker run --name hsha -d --rm -p 5000:5000 hsha  
or without
- $ FLASK_APP=hsha FLASK_ENV=development flask run
## test
- $ python3 -m pytest
## api docs
### /game
- GET /game/sample  
Returns the words from the database, all of them in json.
- GET /game/sample/<integer\>  
Returns the specified number of words from the database in json. 
- GET /game/random  
Returns one word from the db randomly, with or without the correct spelling.
- GET /game/randoms/<integer\>  
Returns the specified number of words from the db randomly, each with or without the correct spelling.
- POST /game/validate  
It's used to get our score from the sent data.
example: {"words":["hélya","borbéj","olaj","lyuhász","relyt"],"is_checked":[false,false,false,false,false]} returns correct 3  
If we have sent our cookie with our username as well, our score gets added to the db.
### /wordmanager
- PUT /wordmanager/<string\>  
We can add words to the db with this. If the word does not contain 'j' or 'ly' we should get back a 400 statuscode. If we want to add a word that is already in the db we should get back a successful 200. 
- DELETE /wordmanager/<string\>
We should be able to delete words from the db somehow, this endpoint is used for just that. If we want to delete a nonexistent word from the db, the expected behaviour is to get back a successful 200 statuscode. Thw idea is: if its not there, then there is no problem.  
