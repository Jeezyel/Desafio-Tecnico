O que o projeto faz: o projeto ele efetua uma concção com um Netbox local da rede não localhost

Como configurar o ambiente e instalar as dependências

  instalação necessarias (docker, python, postman, vscode, git) instalação com o py (flask, rich, requests, json)
  
Como executar a aplicação 

   passo 1: crie uma instacia do netbox 
   
      comandos usado : ls
       1231  cd Área\ de\ trabalho/
       1232  ls
       1233  mkdri gitNetBox
       1234  mkdir gitNetBox
       1235  ls
       1236  cd gitNetBox/
       1237  ls
       1238  git --version
       1239  git clone https://github.com/netbox-community/netbox-docker.git
       1240  ls
       1241  cd netbox-docker/
       1242  ls
       1243  docker compose up -d
       1244  docker --version
       1245  sudo apt install --only-upgrade docker-ce docker-ce-cli containerd.io -y
       1246  sudo apt install --only-upgrade git -y
       1247  git --version
       1248  sudo docker compose up -d
       1249  sudo docker-compose up -d
       1250  docker compose version
       1251  docker-compose version
       1252  sudo apt install docker-compose-plugin -y
       1253  docker pull netboxcommunity/netbox:snapshot-3.4.1
       1254  docker ps
       1255  docker ps -a
       1256  docker imagens
       1257  docker imagen
       1258  docker image
       1259  docker help
       1260  docker image
       1261  sudo docker image
       1262  docker image ps
       1263  docker image
       1264  docker image --help
       1265  docker images
       1266  docker run -p 8000:8080 netboxcommunity/netbox:latest
       1267  ls
       1268  nano docker-compose.yml
       1269  docker-compose up
       1270  python --version
       1271  sudo apt install python3 -y
       1272  python3 --version
       1273  sudo apt install python3-pip -y
       1274  pip3 --version
       1275  docker-compose up -d
       1276  docker ps
       1277  docker-compose restart netbox-worker
       1278  docker exec -it netbox-docker_postgres_1 psql -U netbox -d netbox
       1279  docker logs netbox-docker_netbox-worker_1
       1280  docker ps -a
       1281  ls
       1282  nano docker-compose.yml
       1283  docker-compose run --rm netbox python3 /opt/netbox/netbox/manage.py rqworker
       1284  docker ps
       1285  ls
       1286  nano docker-compose.override.yml
       1287  docker-compose pull
       1288  docker-compose up -d
       1289  docker ps
       1290  docker stop ce
       1291  docker stop 2d
       1292  docker stop b4
       1293  docker ps
       1294  docker-compose up -d
       1295  docker images
       1296  docker rmi netbox
       1297  docker rmi netboxcommunity/netbox:
       1298  docker rmi 3a
       1299  docker rmi db
       1300  docker rmi netboxcommunity/netbox:v4.4-3.4.1
       1301  docker rmi netboxcommunity/netbox   latest
       1302  docker rmi -f db62a0e6b4ca
       1303  docker images
       1304  docker rmi d741b3768746
       1305  docker rmi e2b92b9c8261
       1306  docker rmi -f e2b92b9c8261
       1307  docker ps
       1308  docker stop ce
       1309  docker stop 2d
       1310  docker stop b4
       1311  docker ps
       1312  docker rmi d741b3768746
       1313  docker rm 2dcc62e1cdbd
       1314  docker rmi d741b3768746
       1315  docker ps
       1316  docker images
       1317  docker ps
       1318  docker rmi e2b92b9c8261
       1319  docker rm b4acb0c82a01
       1320  docker rmi e2b92b9c8261
       1321  docker ps
       1322  docker ps -a
       1323  docker rm ce0
       1324  docker rmi e2b92b9c8261
       1325  docker ps -a
       1326  docker rm 191
       1327  docker rm 61
       1328  docker ps -a
       1329  docker images
       1330  docker-compose up -d
       1331  docker ps -a
       1332  docker ps
       1333  docker-compose up -d netbox-worker
       1334  docker ps
       1335  ls
       1336  nano README.md
       1337  docker-compose exec netbox /bin/bash
       quando tiver dentro do conteiner use os comando para criar um super usuario
       pode ser que vc não use todos mas so os principais que esta no repositorio https://github.com/netbox-community/netbox-docker.git
       
   passo 2: depos acesse o netbox atraves de um navegador e faça login e senha admin
   
   passo 3: va em adiministrativo e crie um token pra usar na api
   
   passo 4: va na aplicação e subistitua o meu token pelo seu e a url do netbox
   
Como usar a API: no postman usaremos o get e post o get para coleta de dados e o post pra o tratamento de erro as url usada no postman pode variar de a cordo com o que vc fez ate agora mas a base e o seginte get http://localhost:5000/All e post http://localhost:5000/api/v1/discover passando o intervalos de ips 
  {
    "ips": ["192.168.1.1", "10.0.0.20"]
  }
