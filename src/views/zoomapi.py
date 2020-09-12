# http://localhost:9999/meeting.html?name=Q29saW4y&mn=91074811651&email=Y29saW4ua2luZzIwMDhAZ21haWwuY29t&pwd=S3dsT2t6SUx2TStySFVRbEJ5QzNEUT09&role=0&lang=en-US&signature=WU9VUl9BUElfS0VZLjkxMDc0ODExNjUxLjE1OTk4NzM4Mjg4MTUuMC5JcmVob2MzZGFubEg1L0p5MUVMcEpOYVREa3pJZElocjl3K3dEbUM1YjVzPQ&china=0&apiKey=YOUR_API_KEY

import http.client

conn = http.client.HTTPSConnection("api.zoom.us")

headers = {
    'authorization': "Bearer 39ug3j309t8unvmlmslmlkfw853u8",
    'content-type': "application/json"
    }

conn.request("GET", "/v2/users?status=active&page_size=30&page_number=1", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))