-- Удаляем старую базу данных и создаем новую
DROP DATABASE IF EXISTS CRM;
CREATE DATABASE CRM;
USE CRM;

-- Таблица "Genres" (Жанры)
CREATE TABLE Genres (
    id_genre INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Таблица "Products" (Товары)
CREATE TABLE Products (
    id_product INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    quantity INT NOT NULL CHECK (quantity >= 0),
    age_category VARCHAR(50) NOT NULL,
    difficulty VARCHAR(50) NOT NULL
);

-- Промежуточная таблица "Product_Genres" для связи многие-ко-многим
CREATE TABLE Product_Genres (
    id_product INT NOT NULL,
    id_genre INT NOT NULL,
    PRIMARY KEY (id_product, id_genre),
    FOREIGN KEY (id_product) REFERENCES Products(id_product) ON DELETE CASCADE,
    FOREIGN KEY (id_genre) REFERENCES Genres(id_genre) ON DELETE CASCADE
);

-- Таблица "Bonus_Cards" (Бонусные карты)
CREATE TABLE Bonus_Cards (
    id_card INT AUTO_INCREMENT PRIMARY KEY,
    card_code VARCHAR(50) UNIQUE NOT NULL,
    issue_date DATE NOT NULL,
    active BOOLEAN DEFAULT TRUE
);

-- Таблица "Clients" (Клиенты)
CREATE TABLE Clients (
    id_client INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255),
    id_card INT UNIQUE,
    FOREIGN KEY (id_card) REFERENCES Bonus_Cards(id_card) ON DELETE SET NULL
);

-- Таблица "Sales" (Продажи)
CREATE TABLE Sales (
    id_sale INT AUTO_INCREMENT PRIMARY KEY,
    sale_date DATETIME NOT NULL,
    id_client INT,
    payment_method ENUM('cash', 'card') NOT NULL,
    FOREIGN KEY (id_client) REFERENCES Clients(id_client) ON DELETE SET NULL
);

-- Таблица "Sales_Details" (Детали продаж)
CREATE TABLE Sales_Details (
    id_detail INT AUTO_INCREMENT PRIMARY KEY,
    id_sale INT NOT NULL,
    id_product INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity >= 0),
    FOREIGN KEY (id_sale) REFERENCES Sales(id_sale) ON DELETE CASCADE,
    FOREIGN KEY (id_product) REFERENCES Products(id_product) ON DELETE CASCADE
);

-- Таблица "Images" (Изображения)
CREATE TABLE Images (
    id_image INT AUTO_INCREMENT PRIMARY KEY,
    id_product INT NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    FOREIGN KEY (id_product) REFERENCES Products(id_product) ON DELETE CASCADE
);

-- Вставка данных в таблицу "Genres"
INSERT INTO Genres (name) VALUES
('Экономическая стратегия'),
('Стратегия'),
('Карточная игра'),
('Абстрактная игра'),
('Приключение'),
('Фэнтези'),
('Научная фантастика'),
('Детектив'),
('Ужасы'),
('Семейная игра'),
('Пати-игра'),
('Ролевая игра'),
('Военная стратегия'),
('Головоломка'),
('Кооперативная игра'),
('Детская игра'),
('Декбилдинг'),
('Игры с миниатюрами'),
('Дуэльная игра'),
('Квест');

-- Вставка данных в таблицу "Products"
INSERT INTO Products (name, description, price, quantity, age_category, difficulty) VALUES
('Монополия', 'Классическая настольная игра', 1500.00, 10, '8+', 'Средняя'),
('Каркассон', 'Игра для создания средневекового мира', 2000.00, 15, '7+', 'Легкая'),
('Манчкин', 'Юмористическая карточная игра', 1200.00, 20, '18+', 'Средняя'),
('Уно', 'Простая и веселая карточная игра', 500.00, 30, '6+', 'Легкая'),
('Колонизаторы', 'Игра о развитии и торговле', 2500.00, 8, '10+', 'Сложная'),
('Шахматы', 'Классическая стратегическая игра', 2500.00, 12, '6+', 'Сложная'),
('Доминион', 'Популярная карточная игра в жанре декбилдинг', 1800.00, 20, '10+', 'Средняя'),
('Пандемия', 'Кооперативная настольная игра', 2200.00, 15, '8+', 'Средняя'),
('Диксит', 'Творческая игра с ассоциациями', 1600.00, 30, '6+', 'Легкая'),
('Эволюция', 'Игра про развитие видов', 2300.00, 10, '12+', 'Средняя'),
('7 Чудес', 'Карточная стратегия о строительстве цивилизаций', 2700.00, 14, '10+', 'Средняя'),
('Гвинт', 'Коллекционная карточная игра', 1500.00, 25, '12+', 'Легкая'),
('Зомбицид', 'Настольная игра в жанре ужасов и выживания', 4000.00, 7, '14+', 'Сложная'),
('Ticket to Ride', 'Железнодорожная стратегия', 2800.00, 9, '8+', 'Средняя'),
('Мафия', 'Классическая ролевая пати-игра', 1000.00, 40, '12+', 'Легкая'),
('Бэнг!', 'Ковбойская карточная игра', 1400.00, 18, '10+', 'Легкая'),
('Arkham Horror', 'Кооперативная игра по мотивам Лавкрафта', 3200.00, 5, '14+', 'Сложная'),
('Клуэдо', 'Детективная настольная игра', 1700.00, 16, '8+', 'Средняя'),
('Грузи и вези', 'Экономическая логистическая стратегия', 1900.00, 13, '10+', 'Средняя'),
('Детектив: Современное расследование', 'Глубокая детективная игра', 3500.00, 6, '16+', 'Сложная');

INSERT INTO Product_Genres (id_product, id_genre) VALUES
(1, 1), (1, 2),  -- Монополия
(2, 2),  -- Каркассон
(3, 3),  -- Манчкин
(4, 3),  -- Уно
(5, 1), (5, 2),  -- Колонизаторы
(6, 4),  -- Шахматы
(7, 17), -- Доминион
(8, 15), -- Пандемия
(9, 11), -- Диксит
(10, 5), -- Эволюция
(11, 2), -- 7 Чудес
(12, 3), -- Гвинт
(13, 9), -- Зомбицид
(14, 10), -- Ticket to Ride
(15, 12), -- Мафия
(16, 3), -- Бэнг!
(17, 9), -- Arkham Horror
(18, 8), -- Клуэдо
(19, 1), -- Грузи и вези
(20, 8); -- Детектив


-- Вставка данных в таблицу "Bonus_Cards"
INSERT INTO Bonus_Cards (card_code, issue_date, active) VALUES
('A123456789', '2023-06-15', TRUE),
('B987654321', '2023-07-20', TRUE),
('C567891234', '2023-08-10', FALSE),
('D123456789', '2023-09-01', TRUE),
('E987654321', '2023-09-15', TRUE),
('F567891234', '2023-10-05', FALSE),
('G123456789', '2023-10-20', TRUE),
('H987654321', '2023-11-01', TRUE),
('I567891234', '2023-11-15', FALSE),
('J123456789', '2023-12-01', TRUE),
('K987654321', '2023-12-10', TRUE),
('L567891234', '2024-01-05', FALSE),
('M123456789', '2024-01-20', TRUE),
('N987654321', '2024-02-01', TRUE),
('O567891234', '2024-02-15', FALSE),
('P123456789', '2024-03-01', TRUE),
('Q987654321', '2024-03-10', TRUE),
('R567891234', '2024-04-05', FALSE),
('S123456789', '2024-04-15', TRUE),
('T987654321', '2024-05-01', TRUE);



-- Вставка данных в таблицу "Clients"
INSERT INTO Clients (name, phone, email, id_card) VALUES
('Иван Иванов', '89261234567', 'ivan@example.com', 1),
('Мария Петрова', '89269874567', 'maria@example.com', 2),
('Сергей Сидоров', '89265556677', 'sergey@example.com', 3),
('Елена Кузнецова', '89263334455', 'elena@example.com', 4),
('Алексей Смирнов', '89261112233', 'alexey@example.com', 5),
('Татьяна Орлова', '89262221144', 'tanya@example.com', 6),
('Дмитрий Козлов', '89263335566', 'dmitry@example.com', 7),
('Ольга Васильева', '89264446677', 'olga@example.com', 8),
('Антон Захаров', '89265557788', 'anton@example.com', 9),
('Наталья Морозова', '89266668899', 'natalia@example.com', 10),
('Владимир Соколов', '89267779900', 'vladimir@example.com', 11),
('Екатерина Лебедева', '89268881122', 'ekaterina@example.com', 12),
('Максим Воронов', '89269992233', 'maxim@example.com', 13),
('Анастасия Михайлова', '89261113344', 'anastasia@example.com', 14),
('Георгий Павлов', '89262224455', 'georgiy@example.com', 15),
('Людмила Романова', '89263335566', 'liudmila@example.com', 16),
('Кирилл Тихонов', '89264446677', 'kirill@example.com', 17),
('Виктория Ковалева', '89265557788', 'viktoria@example.com', 18),
('Артур Гаврилов', '89266668899', 'artur@example.com', 19),
('Дарья Фролова', '89267779900', 'daria@example.com', NULL);


-- Вставка данных в таблицу "Sales"
INSERT INTO Sales (sale_date, id_client, payment_method) VALUES
('2024-12-01 14:30:00', 1, 'card'),
('2024-12-02 15:00:00', 2, 'cash'),
('2024-12-03 16:45:00', 3, 'card'),
('2024-12-04 17:00:00', 4, 'cash'),
('2024-12-05 18:15:00', 5, 'card'),
('2024-12-06 19:30:00', 6, 'cash'),
('2024-12-07 12:00:00', 7, 'card'),
('2024-12-08 13:45:00', 8, 'cash'),
('2024-12-09 14:15:00', 9, 'card'),
('2024-12-10 15:30:00', 10, 'cash'),
('2024-12-11 16:45:00', 11, 'card'),
('2024-12-12 17:30:00', 12, 'cash'),
('2024-12-13 18:00:00', 13, 'card'),
('2024-12-14 19:15:00', 14, 'cash'),
('2024-12-15 20:30:00', 15, 'card'),
('2024-12-16 21:45:00', 16, 'cash'),
('2024-12-17 10:30:00', 17, 'card'),
('2024-12-18 11:45:00', 18, 'cash'),
('2024-12-19 12:15:00', 19, 'card'),
('2024-12-20 13:30:00', 20, 'cash');



-- Вставка данных в таблицу "Sales_Details"
INSERT INTO Sales_Details (id_sale, id_product, quantity) VALUES
(1, 1, 2),
(1, 3, 1),
(2, 2, 2),
(2, 5, 1),
(3, 4, 3),
(3, 6, 2),
(4, 7, 1),
(4, 8, 2),
(5, 9, 1),
(5, 10, 3),
(6, 11, 1),
(6, 12, 2),
(7, 13, 1),
(7, 14, 2),
(8, 15, 3),
(8, 16, 1),
(9, 17, 2),
(9, 18, 1),
(10, 19, 3),
(10, 20, 1);



-- Вставка данных в таблицу "Images"
INSERT INTO Images (id_product, image_path) VALUES
(1, 'images\\Без названия (0).jpeg'),
(2, 'images\\Без названия (1).jpeg'),
(3, 'images\\Без названия (2).jpeg'),
(4, 'images\\Без названия (3).jpeg'),
(5, 'images\\Без названия (4).jpeg'),
(6, 'images\\Без названия (5).jpeg'),
(7, 'images\\Без названия (6).jpeg'),
(8, 'images\\Без названия (7).jpeg'),
(9, 'images\\Без названия (8).jpeg'),
(10, 'images\\Без названия (9).jpeg'),
(11, 'images\\Без названия (10).jpeg'),
(12, 'images\\Без названия (11).jpeg'),
(13, 'images\\Без названия (12).jpeg'),
(14, 'images\\Без названия (13).jpeg'),
(15, 'images\\Без названия (14).jpeg'),
(16, 'images\\Без названия (15).jpeg'),
(17, 'images\\Без названия (16).jpeg'),
(18, 'images\\Без названия (17).jpeg'),
(19, 'images\\Без названия (18).jpeg'),
(20, 'images\\Без названия (19).jpeg');
