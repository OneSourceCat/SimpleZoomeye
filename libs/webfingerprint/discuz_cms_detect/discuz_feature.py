#coding=utf-8
'''
Powered By:ChongRui
web-fingerprint plugin
1. robots.txt detecting
2. Powered by DedeCMS detecting
'''
matches = {
	'robots_for_Xx':
		   ["Disallow: /forum.php?mod=redirect*",
			"Disallow: /forum.php?mod=post*",
			"Disallow: /home.php?mod=spacecp*",
			"Disallow: /userapp.php?mod=app&*",
			"Disallow: /*?mod=misc*",
			"Disallow: /*?mod=attachment*",
			"Disallow: /*mobile=yes*"],
	'robots_for_xx':
			["Disallow: /forumdata/",
			 "Disallow: /ipdata/",
			 "Disallow: /modcp/",
			 "Disallow: /wap/",
			 "Disallow: /ajax.php",
			 "Disallow: /logging.php",
			 "Disallow: /memcp.php",
			 "Disallow: /my.php",
			 "Disallow: /pm.php",
			 "Disallow: /post.php",
			 "Disallow: /rss.php",
			 "Disallow: /seccode.php",
			 "Disallow: /topicadmin.php",
			 "Disallow: /space.php",
			 "Disallow: /modcp.php"],
	'intext':['<p>Powered by <strong><a href="http://www.discuz.net" target="_blank">Discuz!</a></strong> <em></em></p>',
			  '<p class="xs0">&copy; 2001-2013 <a href="http://www.comsenz.com" target="_blank">Comsenz Inc.</a></p>'],
	'meta':['Discuz!','Comsenz']
}