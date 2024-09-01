
from . import getKeyPoints
vids = [
		'Sign Language Videos/Are you okay/You Okay 1/You 1.mp4',
		'Sign Language Videos/Are you okay/You Okay 1/Okay 1.mp4',
		'Sign Language Videos/Are you okay/You Okay 2/You 2.mp4',
		'Sign Language Videos/Are you okay/You Okay 2/Okay 2.mp4',
		'Sign Language Videos/Are you okay/You Okay 3/You 3.mp4',
		'Sign Language Videos/Are you okay/You Okay 3/Okay 3.mp4',
		'Sign Language Videos/Are you okay/You Okay 4/You 4.mp4',
		'Sign Language Videos/Are you okay/You Okay 4/Okay 4.mp4'
		]
haha = getKeyPoints()
haha.learn(vids[6],showDisplay=False)
haha.removeUselessFrames()

datasetString = json.dumps(haha.getKeyPoints(), cls=MyEncoder)

f = open('try.json','w')
f.write(datasetString)
f.close()
# print(haha.getKeyPoints())
# haha.writeJSON('you')
# haha.learn(vids[1],showDisplay=False)
# haha.removeUselessFrames()
# haha.writeJSON('okay')
# haha.learn(vids[2],showDisplay=False)
# haha.removeUselessFrames()
# haha.writeJSON('you')
# haha.learn(vids[3],showDisplay=False)
# haha.removeUselessFrames()
# haha.writeJSON('okay')
# haha.learn(vids[4],showDisplay=False)
# haha.removeUselessFrames()
# haha.writeJSON('you')
# haha.learn(vids[5],showDisplay=False)
# haha.removeUselessFrames()
# haha.writeJSON('okay')


# keypoints = haha.getKeyPoints()
# for i in range(len(keypoints)):
# 	sampX = []
# 	sampY = []
# 	for k,v in keypoints[i].items():
# 		sampX.append(v[0])
# 		sampY.append(v[1])
# 	sss = "AFTER"+str(i+1)
# 	plt.title(sss)
# 	plt.plot(sampX, sampY, 'ro')
# 	plt.axis([-125,125,-125,125])
# 	plt.show()

# f = open(vids[5]+'.txt','w')
# f.write("{'You'" + str(haha.getKeyPoints()) + "}" )
