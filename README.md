Ответ на задание https://github.com/eshmargunov/tech_intreview_task/blob/main/README.md

## От автора:
Не смог ограничиться лишь 10 недочетами, все найденные кажутся критичными.
Неточеты отсортированы в порядке от более критичных к менее критичным.

## Найденные недочеты:
- Нет ожидания загрузки картинок на яндекс диск. Отправив POST запрос на адрес https://cloud-api.yandex.net/v1/disk/resources/upload в ответ приходит ссылка, по которой можно следить за прогрессом загрузки файла.
- Файлы и папки после теста не удаляются.
- В тесте идет проверка 2 тестовых случаев, когда у породы есть нет подпороды и когда есть. 
- [Использование случайных данных](https://github.com/eshmargunov/tech_intreview_task/blob/b8ede7b7f4334d56a9d570af29614ad4ef0eaf96/test_dogs.py#L51C62-L51C83) может привести к непрогнозируемым результатам.
- Подготовка данных идет в самом тесте.
- Нет проверок, что запросы прошли успешно. Что помешает понять причину падения теста, когда будем получать информацию о ресурсе.
- Лишняя проверка в тесте [assert True](https://github.com/eshmargunov/tech_intreview_task/blob/b8ede7b7f4334d56a9d570af29614ad4ef0eaf96/test_dogs.py#L60)
- Некорректное имя для функции [u(breed)](https://github.com/eshmargunov/tech_intreview_task/blob/b8ede7b7f4334d56a9d570af29614ad4ef0eaf96/test_dogs.py#L40-L48). Из названия должно быть очевидно что делает данная функция.
- В названии тестовой функции используется транслит.
- В классе YaUploader нет необходимости в [пустом конструкторе](https://github.com/eshmargunov/tech_intreview_task/blob/b8ede7b7f4334d56a9d570af29614ad4ef0eaf96/test_dogs.py#L8-L9). Как в целом выделении функциональности в отдельный класс, методы можно вынести из класса или сделать статическими.
- Нет необходимости в явном сравнении списка подпород с [пустым списком](https://github.com/eshmargunov/tech_intreview_task/blob/b8ede7b7f4334d56a9d570af29614ad4ef0eaf96/test_dogs.py#L61). Выполниться автоматическое приведение списка к логическому типу.
- Базовые части всех адресов, как и формирование заголовков, лучше вынести в отдельные поля или методы. Чтобы в случае необходимости изменить в одном месте, что понизит вероятность ошибки.
- Название метода upload_photos_to_yd слишком обманчивое, т.к. скачивает только одно фото. Так же лишняя приписка to_yd, из класса понятно куда данные загружаются.
- В методе create_folder присваивается значение переменной [response](https://github.com/eshmargunov/tech_intreview_task/blob/b8ede7b7f4334d56a9d570af29614ad4ef0eaf96/test_dogs.py#L14), которое потом не используется. В методе [upload_photos_to_yd](https://github.com/eshmargunov/tech_intreview_task/blob/b8ede7b7f4334d56a9d570af29614ad4ef0eaf96/test_dogs.py#L20) та же самая ошибка.
- При [вызове метода put](https://github.com/eshmargunov/tech_intreview_task/blob/b8ede7b7f4334d56a9d570af29614ad4ef0eaf96/test_dogs.py#L14C62-L14C79) в методе create_folder есть лишние пробелы при использовании именованного аргумента headers.

