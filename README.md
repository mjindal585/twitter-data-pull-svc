# twitter-data-pull-svc

Demo: https://twitter-data-pull-svc.vercel.app/get_sentiments
</br>
Sample CURL request: </br>
curl --location --request POST 'https://twitter-data-pull-svc.vercel.app/get_sentiments' \
--header 'Content-Type: application/json' \
--data-raw '{
    "query": "bollywood",
    "count": 1000
}'
