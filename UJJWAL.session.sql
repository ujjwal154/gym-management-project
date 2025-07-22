-- CREATE TABLE classes (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     name VARCHAR(255) NOT NULL,
--     description TEXT,
--     trainer VARCHAR(100)
-- -- );

-- INSERT INTO classes(name, description, trainer)
-- VALUES('Yoga', 'good forhealth', 'john'),
-- ('Cardio', 'loose your fat ', 'john'),
-- ('Strength Training', 'Increase your strength for better performance', 'john'),
-- ('Dance', 'make your body flexible', 'john');

-- SET FOREIGN_KEY_CHECKS = 0;
-- UPDATE classes SET time ='Mon to Sat at 4PM' 
-- WHERE id=4;


-- UPDATE  classes
-- SET trainer = 'jack'
-- WHERE id = 4;

-- SET FOREIGN_KEY_CHECKS = 0;

-- ALTER TABLE enrollments
-- DROP COLUMN membership_id;

-- SET FOREIGN_KEY_CHECKS = 1;

-- CREATE TABLE enrollments (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     user_id INT,
--     class_id INT,
--     enrollment_date DATETIME,
--     UNIQUE (user_id, class_id),
--     FOREIGN KEY (user_id) REFERENCES user_details(id),
--     FOREIGN KEY (class_id) REFERENCES classes(id)
-- );

-- CREATE TABLE membership_classes (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     membership_id INT,
--     class_id INT,
--     FOREIGN KEY (membership_id) REFERENCES memberships(id),
--     FOREIGN KEY (class_id) REFERENCES classes(id)
-- );



-- SET FOREIGN_KEY_CHECKS = 0;
-- DELETE FROM memberships
-- WHERE id=8;
-- SET FOREIGN_KEY_CHECKS = 1;