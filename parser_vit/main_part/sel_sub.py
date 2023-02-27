from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import datetime
from .models import app_user

url_for_token = 'https://oauth.vk.com/authorize?client_id=51434932&redirect_uri=https%3A%2F%2Foauth.vk.com%2Fblank.html&display=page&scope=wall%2Coffline%2Cgroups%2Cfriends&response_type=token&v=5.131'


def get_user_token(user, url_for_token):

	last_token_date = user.app_user.token_date.timestamp()

	if datetime.datetime.now().timestamp() - last_token_date > 60 * 60 * 23:

		print('сообщение 1')

		options = Options()
		options.add_argument("start-maximized")
		#chrome_browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
		print('сообщение 2')

		chrome_browser = webdriver.Chrome()

		#try:
		print('сообщение 3')
		chrome_browser.get(url_for_token)
		wait = WebDriverWait(chrome_browser, 300)
		wait.until(lambda driver: driver.current_url != url_for_token)
		url = chrome_browser.current_url
		token = url.split('#access_token=')[1].split('&expires_in')[0]
		changing_user = app_user.objects.get(user=user.pk)
		changing_user.token = token
		changing_user.token_date = datetime.datetime.now()
		changing_user.save()
		print('сообщение 4')
		return token
		#except:
			#print(Exception)

	else:
		return user.app_user.token


#get_user_token(url_for_token)