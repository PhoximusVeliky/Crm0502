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
    quantity INT NOT NULL CHECK (quantity > 0),
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
('Карточная игра');

-- Вставка данных в таблицу "Products"
INSERT INTO Products (name, description, price, quantity, age_category, difficulty) VALUES
('Монополия', 'Классическая настольная игра', 1500.00, 10, '8+', 'Средняя'),
('Каркассон', 'Игра для создания средневекового мира', 2000.00, 15, '7+', 'Легкая'),
('Манчкин', 'Юмористическая карточная игра', 1200.00, 20, '18+', 'Средняя'),
('Уно', 'Простая и веселая карточная игра', 500.00, 30, '6+', 'Легкая'),
('Колонизаторы', 'Игра о развитии и торговле', 2500.00, 8, '10+', 'Сложная');

-- Вставка данных в таблицу "Product_Genres"
INSERT INTO Product_Genres (id_product, id_genre) VALUES
(1, 1),  -- Монополия (Экономическая стратегия)
(1, 2),  -- Монополия (Стратегия)
(2, 2),  -- Каркассон (Стратегия)
(3, 3),  -- Манчкин (Карточная игра)
(4, 3),  -- Уно (Карточная игра)
(5, 1),  -- Колонизаторы (Экономическая стратегия)
(5, 2);  -- Колонизаторы (Стратегия)

-- Вставка данных в таблицу "Bonus_Cards"
INSERT INTO Bonus_Cards (card_code, issue_date, active) VALUES
('A123456789', '2023-06-15', TRUE),
('B987654321', '2023-07-20', TRUE),
('C567891234', '2023-08-10', FALSE);

-- Вставка данных в таблицу "Clients"
INSERT INTO Clients (name, phone, email, id_card) VALUES
('Иван Иванов', '89261234567', 'ivan@example.com', 1),
('Мария Петрова', '89269874567', 'maria@example.com', 2),
('Сергей Сидоров', '89265556677', 'sergey@example.com', 3),
('Елена Кузнецова', '89263334455', 'elena@example.com', NULL);

-- Вставка данных в таблицу "Sales"
INSERT INTO Sales (sale_date, id_client, payment_method) VALUES
('2024-12-01 14:30:00', 1, 'card'),
('2024-12-02 15:00:00', 2, 'cash'),
('2024-12-03 16:45:00', 3, 'card'),
('2024-12-04 17:00:00', 4, 'cash');

-- Вставка данных в таблицу "Sales_Details"
INSERT INTO Sales_Details (id_sale, id_product, quantity) VALUES
(1, 1, 2),
(1, 3, 1),
(2, 2, 2),
(3, 3, 1),
(4, 4, 1);

-- Вставка данных в таблицу "Images"
INSERT INTO Images (id_product, image_path) VALUES
(1, '/images/monopoly.jpg'),
(2, '/images/carcassonne.jpg'),
(3, '/images/munchkin.jpg'),
(4, '/images/uno.jpg'),
(5, '/images/catan.jpg');
