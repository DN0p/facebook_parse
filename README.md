Проект носит исключительно обучающий характер.
Программа предназначена для получения данных с аккаунта facebook:
ссылка на пост
дата поста
локация
статус видимости
id кто прокомментировал пост
id кто поставил лайк 
id кто поделился

Требуется установка python v3 и выше
Требуется установка программной библиотеки для управления браузерами selenium версии 3.141.0, которая не входит в стандартную библиотеку python.
Требуется скачать gekodriver v0.26.0, соответствующий вашей операционной системе (можно найти по ссылке https://github.com/mozilla/geckodriver/releases).

В файле credentials.txt необходимо указать путь до файла gekodriver в переменной GECKODRIVER
	Пример для unix-подобных систем: GECKODRIVER = "/usr/local/bin/geckodriver"
	Пример для windows: GECKODRIVER = "C:\\Users\\username\\Downloads\\geckodriver-v0.26.0-win64\\geckodriver.exe"

В файле credentials.txt необходимо указать путь до исполнительного файла браузера firefox в переменной BROWSER_EXE
	Пример для unix-подобных систем: BROWSER_EXE = "/usr/bin/firefox"
	Пример для windows: BROWSER_EXE =  "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
	
в файле credentials.txt необходимо указать свой логин и пароль от страницы facebook в строки email и password

Для windows в файле credentials.txt необходимо в переменной path указать полный путь к файлу, например path = "C:\\Users\\Downloads\\geckodriver-v0.26.0-win64\\output.csv"
 
Запуск из консоли командой
	Пример для unix-подобных систем: python3 FB_parse.py
	Пример для windows: python FB_parse.py
 
Вывод данных будет распологаться в файле output.csv и будет находиться в директории с модулем FB_parse.py  



