# Магазин цифровых товаров для Telegram
***

В боте реализован магазин цифровых товаров с гибкой административной панелью, есть возможность создавать подкатегории товаров, база данных построенна на MongoDB.

### Пользователь может:

* Просматривать категории и товары:

![юзер_категории_товары](https://user-images.githubusercontent.com/83144447/132414098-18b1153d-8a23-4268-8472-a30921fb3e8d.gif)

* Удобно управлять кол-вом аккаунов:

![юзер_управление_колво_покупка](https://user-images.githubusercontent.com/83144447/132414700-273d6acf-fbf2-424e-8862-bcd425788e90.gif)

* Участвовать в рулетке на бонусы (чем выше сложность, тем больше кнопок в игре):

![юзер_бонусы_игра](https://user-images.githubusercontent.com/83144447/132414526-fe5e2e27-431e-4fa0-9a43-e99b16e162c4.gif)

* Просматривать ранее купленные аккаунты:

![мои покупки](https://user-images.githubusercontent.com/83144447/132414583-38e4cec6-4ac8-4b53-8386-c0ab88003701.gif)

### Администратор может:

* Добавить новый товар/катеогрию/подкатегорию и заполнить витрину:

![админ_добавить товар и аккаунты](https://user-images.githubusercontent.com/83144447/132415791-511cbc61-0ce0-4521-a250-ace7ff58f49b.gif)

* Изменить товар/катеогрию/подкатегорию:

![админ_изменить_товар](https://user-images.githubusercontent.com/83144447/132415866-dada3d29-fd38-427b-be5e-ab8c356847fa.gif)

* Удалить товар/катеогрию/подкатегорию:

![админ_удалить_товар](https://user-images.githubusercontent.com/83144447/132415907-bb0f60fa-f81e-42d6-b437-3bd9580224b5.gif)

* Главный администатор может назначать других админов:

![админ_назначить_админа](https://user-images.githubusercontent.com/83144447/132415957-f5b7bde6-329d-4579-82af-e95d1619b3d6.gif)


# Установка
***
1. Клонируйте репозиторий с github
2. Создайте виртуальное окружение
3. Установите зависимости `pip install -r requirements.txt`
4. Пропишите в файле `settings.py`:
   * `TELEGRAM_KEY` - ключ телеграм бота;
   * `MONGO_DB_LINK` - ссылка на кластер Mongo;
   * `MONGO_DB` - название базы данных Mongo;
   * `QIWI TOKEN` - токен QIWI кошелька
   * `TEST_BUY` - для тестового режима (True - включает кнопку покупки аккаунтов без оплаты)
5. Запустите бота командой:

`python3 main.py`

# Пример бота
***

https://t.me/FUAShop_bot - тестовый функционал при котором можно купить товар без оплаты (аккаунты в товарах фейковые)

