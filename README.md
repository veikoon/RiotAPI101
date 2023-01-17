# RIOTAPI101

## Installation

Clone the repository and install python required libraries:
```Bash
git clone https://github.com/veikoon/RiotAPI101.git
cd RiotAPI101/
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Install riot assets dependecies:
```Bash
mkdir -p static/assets/dragontail
cd static/assets/dragontail
wget https://ddragon.leagueoflegends.com/cdn/dragontail-13.1.1.tgz
tar xvf dragontail-13.1.1.tgz
rm dragontail-13.1.1.tgz
```

## Start

```Bash
export RIOT_API=""
source venv/bin/activate
python3 manage.py runserver
```
