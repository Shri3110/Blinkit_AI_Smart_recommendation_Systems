import urllib.request
ids=['1584017911766-d451b3d0e843', '1532938911079-1b06ac7ceec7', '1576091160399-112ba8d25d1d', '1576091160550-2173dba999ef', '1498837167922-41f37c23c216']
for id in ids:
 try:
  print(id, urllib.request.urlopen(urllib.request.Request(f'https://images.unsplash.com/photo-{id}?w=400&q=80', headers={'User-Agent': 'Mozilla/5.0'})).getcode())
 except Exception as e:
  print(id, e)
