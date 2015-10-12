import sublime, sublime_plugin, re, os, os.path, mmap

class snippetxCommand(sublime_plugin.TextCommand):


	def maybe(self, dict, key):
		if key in dict:
			return dict[key]
		else:
			return None

	def getFields(self, lines):
		for line in lines:
			yield line.split(",")


	def notEmpty(self, line):
		if line not in ['\n', '\r\n', '']:
			return line


	def findFiles(self, path, type=".sublime-snippet"):
		for root, dirs, files in os.walk(path):
			for file in files:
				if file.endswith(type):
					yield os.path.join(root, file)


	def matchFile(self, path, pattern):
		f = open(path)
		s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
		if s.find(pattern.encode('utf-8')) != -1:
			return s.read(s.size()).decode("utf-8")


	def findSnippetContent(self, snippet):
		return re.search(r'CDATA\[[\n\r]{0,2}(.*?)\]\]', snippet, re.DOTALL).group(1) if snippet else ''


	def zipSnip(self, snippet, content, indent=''):
		for idx, field in enumerate(content):
			snippet = re.sub(r'(?<!\\)\${{{0}:.*?}}|\${0}'.format(str(idx+1)) ,field, snippet)
		snippet = re.sub(r'(?<!\\)\$\{\d+:(.+?)\}', '\\1', snippet)
		snippet = re.sub(r'(?<!\\)\$\d+', '', snippet)
		return indent + snippet


	def findMatch(self, view, pattern, num):
		return view.substr(view.find(pattern, num))


	def getData(self, patterns):

		data = {}

		data['+metaRegion']     = self.view.find(patterns['+metaRegion'], 0)

		data['asString']        = self.findMatch(self.view, patterns['+metaRegion'], 0)

		data['asLines']         = data['asString'].splitlines()

		if (re.search(r'sx:', data['asLines'][0])):
			data['snippetName']     = re.search(r'(?<=sx:).+', data['asLines'].pop(0)).group(0)
		elif (re.search(r'sx:', data['asLines'][-1])):
			data['snippetName']     = re.search(r'(?<=sx:).+', data['asLines'].pop(-1)).group(0)
		else: data['snippetName'] = ''

		data['indent']          = re.search(r'[\t ]*', data['asLines'][0]).group(0)

		data['asLinesMassaged'] = [re.sub(r'(^[\t ]*|["]*)*', '', content) for content in list(filter(self.notEmpty, data['asLines']))]

		return data


	def getSnippet(self, name=None):

		snippet = {}

		snippet['name']             = name

		snippet['match']            = '<tabTrigger>' + snippet['name'] + '</tabTrigger>'

		snippet['filenames']        = list(self.findFiles(sublime.packages_path()))

		snippet['matchedFiles']     = [self.matchFile(x, snippet['match']) for x in snippet['filenames']]
		
		snippet['filteredFiles']    = list(filter(None.__ne__, snippet['matchedFiles']  ))

		snippet['asString']         = [self.findSnippetContent(x) for x in snippet['filteredFiles']]

		snippet['asStringMassaged'] = [re.sub(r'[\r]', '', content) for content in snippet['asString']]

		return snippet


	def run(self, edit):

		patterns = {'+metaRegion': r"([\t ]*sx:.*[\n\r]*)(.+[\n\r]?)*|(?<=[\n\r])?(.+[\n\r])+([\t ]*sx:.+)" }

		data = self.getData(patterns)

		if (data['+metaRegion'].a >= 0 and data['+metaRegion'].b > 0):
			snippet = self.getSnippet(data['snippetName'])

			if (len(snippet['asStringMassaged'])):
				self.view.replace(edit, data['+metaRegion'], '')

				for snippet in snippet['asStringMassaged']:
					snips = ''
					for fields in self.getFields(data['asLinesMassaged']):
						snips += self.zipSnip(snippet,fields, data['indent'])
					self.view.insert(edit, data['+metaRegion'].a, snips)
			else:
				sublime.status_message("Can't find snippet named " + snippet['name'])
		else:
			sublime.status_message("Can't find region.")