docker stop ms.bot
docker rm ms.bot

app="ms.bot"
docker build -t ${app} .
docker run -d -p 49988:49988 \
  --name=${app} \
  -v "$PWD":/app ${app}