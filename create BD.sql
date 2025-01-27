-- Drop and create database
DROP DATABASE IF EXISTS CRM;
CREATE DATABASE CRM;
USE CRM;

-- Table "Genres"
CREATE TABLE Genres (
    id_genre INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Table "Products"
CREATE TABLE Products (
    id_product INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    id_genre INT NOT NULL,
    FOREIGN KEY (id_genre) REFERENCES Genres(id_genre)
);

-- Table "Bonus Cards"
CREATE TABLE Bonus_Cards (
    id_card INT AUTO_INCREMENT PRIMARY KEY,
    card_code VARCHAR(50) UNIQUE NOT NULL,
    issue_date DATE NOT NULL,
    active BOOLEAN DEFAULT TRUE
);

-- Table "Clients"
CREATE TABLE Clients (
    id_client INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255),
    id_card INT UNIQUE,
    FOREIGN KEY (id_card) REFERENCES Bonus_Cards(id_card)
);

-- Table "Sales"
CREATE TABLE Sales (
    id_sale INT AUTO_INCREMENT PRIMARY KEY,
    sale_date DATETIME NOT NULL,
    id_client INT,
    payment_method ENUM('cash', 'card') NOT NULL,
    FOREIGN KEY (id_client) REFERENCES Clients(id_client)
);

-- Table "Sales Details"
CREATE TABLE Sales_Details (
    id_detail INT AUTO_INCREMENT PRIMARY KEY,
    id_sale INT NOT NULL,
    id_product INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (id_sale) REFERENCES Sales(id_sale),
    FOREIGN KEY (id_product) REFERENCES Products(id_product)
);

-- Table "Images"
CREATE TABLE Images (
    id_image INT AUTO_INCREMENT PRIMARY KEY,
    id_product INT NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    FOREIGN KEY (id_product) REFERENCES Products(id_product) ON DELETE CASCADE
);

-- Insert data into "Genres" table
INSERT INTO Genres (name) VALUES
('Экономическая стратегия'),
('Стратегия'),
('Карточная игра');

-- Insert data into "Products" table
INSERT INTO Products (name, description, price, quantity, id_genre) VALUES
('Монополия', 'Классическая настольная игра', 1500.00, 10, 1),
('Каркассон', 'Игра для создания средневекового мира', 2000.00, 15, 2),
('Манчкин', 'Юмористическая карточная игра', 1200.00, 20, 3),
('Уно', 'Простая и веселая карточная игра', 500.00, 30, 3),
('Колонизаторы', 'Игра о развитии и торговле', 2500.00, 8, 1);

-- Insert data into "Bonus_Cards" table
INSERT INTO Bonus_Cards (card_code, issue_date, active) VALUES
('A123456789', '2023-06-15', TRUE),
('B987654321', '2023-07-20', TRUE),
('C567891234', '2023-08-10', FALSE);

-- Insert data into "Clients" table
INSERT INTO Clients (name, phone, email, id_card) VALUES
('Иван Иванов', '89261234567', 'ivan@example.com', 1),
('Мария Петрова', '89269874567', 'maria@example.com', 2),
('Сергей Сидоров', '89265556677', 'sergey@example.com', 3),
('Елена Кузнецова', '89263334455', 'elena@example.com', NULL);

-- Insert data into "Sales" table
INSERT INTO Sales (sale_date, id_client, payment_method) VALUES
('2024-12-01 14:30:00', 1, 'card'),
('2024-12-02 15:00:00', 2, 'cash'),
('2024-12-03 16:45:00', 3, 'card'),
('2024-12-04 17:00:00', 4, 'cash');

-- Insert data into "Sales_Details" table
INSERT INTO Sales_Details (id_sale, id_product, quantity) VALUES
(1, 1, 2),  -- Монополия
(1, 3, 1),  -- Манчкин
(2, 2, 2),  -- Каркассон
(3, 3, 1),  -- Манчкин
(4, 4, 1);  -- Уно

-- Insert data into "Images" table
INSERT INTO Images (id_product, image_path) VALUES
(1, '/images/monopoly.jpg'),
(2, '/images/carcassonne.jpg'),
(3, '/images/munchkin.jpg'),
(4, '/images/uno.jpg'),
(5, '/images/catan.jpg');
