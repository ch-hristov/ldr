import praw
import json

reddit = praw.Reddit(client_id = '',
					 client_secret = '',
					 user_agent = 'my user agent')

larry = 0.0	


mapping = {}
username_buffer = {}


count = 0

total = sum(1 for x in reddit.subreddit('longdistance').hot(limit=None))
count = total


for submission in reddit.subreddit('longdistance').hot(limit=None):
	submission.comments.replace_more(limit=0)
	comment_queue = submission.comments[:]  # Seed with top-level
	lst = []

	print(larry / (count))
	larry = larry + 1.0

	# simple BFS
	while len(comment_queue) > 0:
		comment = comment_queue.pop(0)
		flair = comment.author_flair_text
		author = None

		if comment.author is not None:
			author = comment.author.name

		try:
			if flair is not None and len(flair) > 2:
				dash = flair.split('-')
				slash = flair.split('/')


				if 'to' not in flair and 'km' not in flair and 'mi' not in flair:
					if len(dash) != 2 and len(slash) != 2:
						continue
				split = flair.split(' ')
				if len(dash) == 2:
					split = dash
				if len(slash) == 2:
					split = slash

				l = []
				for s in split:
					real = s.replace('[','').replace(']','').replace(',','').replace('.','')
					if real[0].isupper():
						l.append(real)
					if len(l) == 2:
						break
				if len(l) <= 1:
					continue

				frm = l[0]
				to = l[1]

				if author not in username_buffer:
					username_buffer[author]=1

					if frm not in mapping:
						mapping[frm] = {to : 1}
					else:
						if to not in mapping[frm]:
							mapping[frm][to] = 1
						else:
							mapping[frm][to] = mapping[frm][to] + 1

		except:
			print('Exception')

		comment_queue.extend(comment.replies)

print(larry)

with open('result.json', 'w') as fp:
    json.dump(mapping, fp)