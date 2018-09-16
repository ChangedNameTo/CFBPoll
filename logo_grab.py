import requests
from bs4 import BeautifulSoup as bs

def download_logos(width=None, height=None, dirname='logos'):
    # Quick and dirty method to scrape logos from ESPN; they need minor editorial cleanup afterward
    r = requests.get('http://www.espn.com/college-football/teams')

	# Note that this finds ALL of the logos, you'll have to sort through them later
    results = bs(r.text).findAll('a', href=re.compile('^http://www.espn.com/college-football/team/_/id/'))
    if not os.path.exists('./{}/'.format(dirname)):
        os.makedirs('./{}/'.format(dirname))

    if not width:
		width = int(input('Provide an integer width: '))
	if not isinstance(width, int):
		raise TypeError('Width is not a valid integer.')	
    if not height:
		height = int(input('Provide an integer height: '))
	if not isinstance(height, int):
		raise TypeError('Heightis not a valid integer.')	

	for link in results:
        foo = link['href'].split('/')
        id = foo[5]
        name = foo[6].split('-')[0].title()
        pic_url = 'http://a.espncdn.com/combiner/i?img=/i/teamlogos/ncaa/500/{}.png&h={}&w={}'.format(id,
                                                                                                      height,
                                                                                                      width)
        with open(os.path.join('./Resources/', '{}.png'.format(name.lower())), 'wb') as handle:
            response = requests.get(pic_url, stream=True)

            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)