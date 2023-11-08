import requests

class HHresume:
    def proceessResume(uplResume):
        st_accept = "text/html" # говорим веб-серверу, 
        # что хотим получить html
        # имитируем подключение через браузер Mozilla на macOS
        st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
        # формируем хеш заголовков
        headers = {
            "Accept": st_accept,
            "User-Agent": st_useragent
        }

        
        req = requests.get("https://selectel.ru/blog/courses/", headers)
        # считываем текст HTML-документа
        src = req.text

        uplResume = "https://habr.com/ru/companies/selectel/articles/754674/"
        req1 = requests.get(uplResume, headers)
        src1 = req1.text
        
        return