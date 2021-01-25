# Files_upload_api
api for upload\download\delete files by hash  
realised in flask  
realisation in aiohttp in progress  


###### I would greatly appreciate for your any feedback by email or tg: [arh_74](https://t.me/Arh_74)


---
#### description files: ####
##### /flask/ #####
- **application.py** - main file, which include all functions. for run: 'export FLASK_APP=application $ flask run'
- **requirments.txt** - requirments for work app
- **test_flask.py** - all tests. for run: 'python -m pytest'


##### /aio/ #####
main folder. 
for run app:  
*pip3 install -r requirements.txt*  
*python -m aiohttp.web -H localhost -P 8080 api:main*
##### /aio/api/ ##### 
- **app.py** - initialitation
- **routes.py**
- **views.py** - main functionality

##### /aio/config/ ##### 
- **aip.yaml** - configs

##### /aio/test/ ##### 
- **app_test.py** - for run: *python -m pytest*



