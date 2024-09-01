# haha.learn("Video Database/Hello/ASL_Hello.mp4")
# print(haha.getKeyPoints()[0])

'''
{
'dataset' : 
			{
			'word' : 	{
						
						}
			}

}

'''
# with open("data_file.json", "w") as write_file:
#     json.dump(data, write_file)
# a = json.dumps(data, indent=4)
# a = json.loads(JSONstring)

# for temporary json writing
'''
import json
import numpy

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

f1 = open('dataset.txt','r')
for ss in f1:
	sad = ss
f1.close()
data = json.loads(sad)
if 'you' not in data.keys():
	data['you'] = [haha.getKeyPoints()]
else:
	data['you'].append(haha.getKeyPoints())

stss = json.dumps(data, cls=MyEncoder)


f = open('dataset.txt','w')
f.write(stss)
f.close()
'''