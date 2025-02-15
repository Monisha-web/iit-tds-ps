This project is the submission for IIT DS Project in TDS (phase 1 and phase 2).

Email - 23f2000136@ds.study.iitm.ac.in

Docker Image URL - https://hub.docker.com/r/monisha195/iit-tds-ps

Github URL - https://github.com/Monisha-web/iit-tds-ps

# Instructions to run code locally:
uv run datagen.py 23f2000136@ds.study.iitm.ac.in

uv run app.py

uv run evaluate.py --email=23f2000136@ds.study.iitm.ac.in --log-level=INFO

# Instructions to build docker locally:
docker build -t monisha195/iit-tds-ps .

docker push monisha195/iit-tds-ps 

# Instructions to run podman locally:
podman machine init

podman machine start

podman run -e AIPROXY_TOKEN=$env:AIPROXY_TOKEN -p 8000:8000 monisha195/iit-tds-ps
