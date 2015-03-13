#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from time import sleep
from pync import Notifier
from wylie_utils import settings
from xml.etree import ElementTree

__title__ = 'wylie'
__version__ = '0.1'
__author__ = '@c0ding'
__repo__ = 'https://github.com/c0ding/wylie'
__license__ = 'Apache v2.0 License'

class Build():
	
	def __init__(self, attrs):
		self.name = attrs['name']
		self.number = attrs['lastBuildLabel']
		self.status = attrs['lastBuildStatus']
		
class BuildMonitor():

	def __init__(self, listener):
		self.builds = None
		self.listener = listener
		
	def loop(self):
		while True:
			try:
				self.check_for_new_builds()
			except Exception as e:
				print 'WARNING! Update failed:', e
			sleep(settings['UPDATE_INTERVAL'])
				
	def check_for_new_builds(self):
		builds = self.fetch_builds()
		if self.builds is not None:
			for build in builds.values():
				name = build.name
				if name in settings['EXCLUDE_JOBS']:
					continue
				if not self.builds.has_key(name):
					self.handle_new_build(build, None)
				elif build.number != self.builds[name].number:
					self.handle_new_build(build, self.builds[name].status)
		self.builds = builds
		
	def handle_new_build(self, build, old_status):
		transition = (old_status, build.status)
		if transition == ('Failure', 'Failure'):
			self.listener.notify(build, '☁️ Still failing')
		elif transition == ('Failure', 'Success'):
			self.listener.notify(build, '☀️ Fixed')
		elif transition == ('Success', 'Success'):
			self.listener.notify(build, '☀️ Success')
		elif build.status == 'Failure':
			self.listener.notify(build, '☁️ Failed')
			
	def fetch_builds(self):
		builds = {}
		response = requests.get(settings['JENKINS_URL'] + '/cc.xml', auth=(settings['JENKINS_USER'], settings['JENKINS_PASSWORD']))
		projects = ElementTree.fromstring(response.content)
		for project in projects.iter('Project'):
			build = Build(project.attrib)
			builds[build.name] = build
		return builds

class BuildNotifier():
	
	def __init__(self):
		self.api = Notifier
		
	def notify(self, build, event):
		url = settings['JENKINS_URL'] + '/job/' + build.name + '/' + build.number + "/"
		self.api.notify(title='Jenkins Notify', message = build.name + " "+ event, open=url)
		
if __name__ == '__main__':
	try:
		BuildMonitor(BuildNotifier()).loop()
	except KeyboardInterrupt:
		pass
