import PySide2, json, os, random

vidExts = ['.mp4','.mov']

class mediaItem:

	def __init__(self, imgData):
		self.path = imgData['imgPath']
		self.url = imgData['imgURL']
		self.status = imgData['status']
		if (self.status == 'Unfiltered'):
			self.status = 0
		if (self.status == 'Filtered'):
			self.status = 1
		if (self.status == 'Sorted'):
			self.status = 2
		self.subs = imgData['subs']
		self.tags = imgData['tags']

		if (os.path.splitext(self.path)[1] in vidExts):
			self.tags.append('animated')
			self.tags.append('movie')

		if (os.path.splitext(self.path)[1] == '.gif'):
			self.tags.append('animated')
			self.tags.append('gif')


	def merge(self, other):
		self.status = max(self.status, other.status)
		self.subs.extend(w for w in other.subs if w not in self.subs)
		self.tags.extend(w for w in other.tags if w not in self.tags)
		other.status = -1


class Library:

	def __init__(self, datapath: str):
		data = json.load(open(datapath))

		self.all = []
		for img in data['images']:
			self.all.append(mediaItem(img))

		self.unfiltered = [w for w in self.all if w.status == 0]
		self.filtered = [w for w in self.all if w.status == 1]
		self.sorted = [w for w in self.all if w.status == 2]

	def queueFromString(self, source: str):
		self.queue = self.all
		self.queryList = source.split(' ')
		if ('' in self.queryList):
			self.queryList.remove('')
		self.subList = [w for w in self.queryList if w[0] == '-']
		self.addList = list(set(self.queryList) - set(self.subList))
		if len(self.addList) > 0:
			self.queue = [w for w in self.queue if all(x in w.tags for x in self.addList)]
			print(self.addList)
		if len(self.subList) > 0:
			self.queue = [w for w in self.queue if all(x not in w.tags for x in self.subList)]
			print(self.subList)

	def randomFromQueue(self):
		i = random.randint(0, len(self.queue))
		return self.queue[i]
