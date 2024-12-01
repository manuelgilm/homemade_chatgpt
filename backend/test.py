import requests

# Test the unprotected route
response = requests.get(
    "http://127.0.0.1:8000/api/v1/users/protected",
    headers={
        # 'accept': 'application/json',
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImVtYWlsIjoiam9obmRvZTEyM0Bjby5jb20iLCJ1c2VyX3VpZCI6IjcwMjU5ZDM1LTkzODEtNDQwYi04MzAyLWU3YmViNjQ3NjE2NSJ9LCJleHAiOjE3MzI5NTMxMTAsImp0aSI6ImNlYjQ1Y2IwLWI4NWMtNGQ3OC1hOGJlLTdmNzg3NTQ3YjllNiIsInJlZnJlc2giOnRydWV9.MD56ItTin4SzDZMDB_t7263u0L8dF3E-4tppV-Rjuiw"
    },
)
print(response)
# curl -X 'GET' \
#   'http://127.0.0.1:8000/api/v1/users/protected' \
#   -H 'accept: application/json'
#   -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImVtYWlsIjoiam9obmRvZTEyM0Bjby5jb20iLCJ1c2VyX3VpZCI6IjcwMjU5ZDM1LTkzODEtNDQwYi04MzAyLWU3YmViNjQ3NjE2NSJ9LCJleHAiOjE3MzI3NDM3ODIsImp0aSI6ImY2MzM3MGYyLTBiODEtNGJkNS1hMzE1LTFkOWQ1ZGI3ZDRmZiIsInJlZnJlc2giOmZhbHNlfQ.YXWlNbP4heYXKJMYrR24m0PTsmY2rPjse5_T9uSHacw'
