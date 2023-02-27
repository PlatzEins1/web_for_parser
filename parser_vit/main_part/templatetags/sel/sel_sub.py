from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

url_for_token = 'https://oauth.vk.com/authorize?client_id=51434932&redirect_uri=https%3A%2F%2Foauth.vk.com%2Fblank.html&display=page&scope=wall%2Coffline%2Cgroups%2Cfriends&response_type=token&v=5.131'


def get_user_token(url_for_token):

	options = Options()
	options.add_argument("start-maximized")
	chrome_browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

	#schrome_browser = webdriver.Chrome('./chromedriver')
	try:
		chrome_browser.get(url_for_token)
		wait = WebDriverWait(chrome_browser, 300)
		wait.until(lambda driver: driver.current_url != url_for_token)
		url = chrome_browser.current_url
		token = url.split('#access_token=')[1].split('&expires_in')[0]
		return token
	except:
		pass


#get_user_token(url_for_token)