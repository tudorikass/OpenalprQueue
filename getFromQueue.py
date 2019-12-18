import beanstalkc
import json
import requests
import shutil
beanstalk=beanstalkc.Connection(host='localhost',port=11300)

TUBE_NAME='alprd'

print beanstalk.tubes()

print(beanstalk.stats_tube(TUBE_NAME))


beanstalk.watch(TUBE_NAME)
a=3
while True:
    job=beanstalk.reserve(timeout=1)
    if job is None:
        print "no plates"
    else:
        plates_info=json.loads(job.body)
        #print(plates_info)
        uuid=""
        linkForm=""
        if plates_info['data_type']=='alpr_results':
            print(plates_info['uuid'])
            uuid=plates_info['uuid']
        if plates_info['data_type']=='alpr_group':
            print(plates_info['best_uuid'])
            uuid=plates_info['best_uuid']
        if uuid !="":
            linkForm="http://localhost:8355/img/"+uuid+".jpg"
            print(linkForm)
            response=requests.get(linkForm,stream=True)
            with open('img.jpg', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response


        job.delete()



