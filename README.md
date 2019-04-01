# QA_using_spacy_and_nmslib
Search based English **Question Answering** model based on **Spacy** english vectors 

- max_distance - threshold for cosine distance for finding neighbours in vector space. Use values in range 0.05 - 0.15 for good search results 
## Request 
```bash
curl --request POST --url http://localhost:5000/ --header 'Content-Type: application/json' --header 'Postman-Token: 22d20dbd-1f8c-4bbd-844a-2e4e3afb6229'  --header 'cache-control: no-cache' --data '{"questions":[{"id":0, "question":"Carl and the Passions day changed band name to what"},{"id":1, "question":"Where in your body is your patella"},{"id":2, "question":"Can you answer to all of my questions?"}],"max_distance":0.05}'
```
## Response:
```json
[
  {
    "answer": "Beach Boys", 
    "id": 0, 
    "question": "Carl and the Passions day changed band name to what"
  }, 
  {
    "answer": "Knee ( it's the kneecap )", 
    "id": 1, 
    "question": "Where in your body is your patella"
  }, 
  {
    "answer": "N/A", 
    "id": 2, 
    "question": "Can you answer to all of my questions?"
  }
]
```
