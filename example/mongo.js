db = db.getSiblingDB('classifier')

db.classifiers.drop();

db.classifiers.insertMany([{
  "name": "USERNAME",
  "regex": [
    "^.*username.*$"
  ]
},{
  "name": "EMAIL_ADDRESS",
  "regex": [
    "^.*email.*$",
    "^.*mailbox.*$"
  ]
},{
  "name": "PASSWORD",
  "regex": [
    "^pass.*$"
  ]
},{
  "name": "CREDIT_CARD",
  "regex": [
    "^.*card((?!type).)*$"
  ]
},{
  "name": "PHONE_NUMBER",
  "regex": [
    "^.*phone.*$"
  ]
}]);

db.users.drop();

db.users.insertOne({
  "username": "admin",
  "password": "$2b$12$sGDtYKG6Mp0./jmePuoZVeDNfmWbPXZezx8IEoAVZlAOqJ/NxzJmK"
});