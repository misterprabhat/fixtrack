-- 3. USERS  (IDs 1-4 students, 5-7 staff, 8 admin)
INSERT INTO USERS (FULL_NAME, EMAIL, PHONE, USER_ROLE) VALUES ('Aarav Sharma',   'aarav.sharma.cse@gmail.com',  '9876500001', 'STUDENT');
INSERT INTO USERS (FULL_NAME, EMAIL, PHONE, USER_ROLE) VALUES ('Riya Verma',     'riya.verma.ece@gmail.com',    '9876500002', 'STUDENT');
INSERT INTO USERS (FULL_NAME, EMAIL, PHONE, USER_ROLE) VALUES ('Karan Singh',    'karan.singh.mech@gmail.com',  '9876500003', 'STUDENT');
INSERT INTO USERS (FULL_NAME, EMAIL, PHONE, USER_ROLE) VALUES ('Simran Kaur',    'simran.kaur.bba@gmail.com',   '9876500004', 'STUDENT');
INSERT INTO USERS (FULL_NAME, EMAIL, PHONE, USER_ROLE) VALUES ('Rahul Mehta',    'rahul.mehta.electric@gmail.com', '9876500005', 'STAFF');
INSERT INTO USERS (FULL_NAME, EMAIL, PHONE, USER_ROLE) VALUES ('Suresh Kumar',   'suresh.kumar.plumber@gmail.com', '9876500006', 'STAFF');
INSERT INTO USERS (FULL_NAME, EMAIL, PHONE, USER_ROLE) VALUES ('Neha Kapoor',    'neha.kapoor.facility@gmail.com', '9876500007', 'STAFF');
INSERT INTO USERS (FULL_NAME, EMAIL, PHONE, USER_ROLE) VALUES ('Priya Malhotra', 'priya.malhotra.admin@gmail.com',  '9876500008', 'ADMIN');

-- 4. CATEGORIES (IDs 1-5)
INSERT INTO CATEGORIES (CATEGORY_NAME, DESCRIPTION) VALUES ('Electrical', 'Lights, fans, projectors, sockets and power issues');
INSERT INTO CATEGORIES (CATEGORY_NAME, DESCRIPTION) VALUES ('Plumbing',   'Water leakage, taps, drainage and water coolers');
INSERT INTO CATEGORIES (CATEGORY_NAME, DESCRIPTION) VALUES ('Furniture',  'Damaged desks, chairs, benches and cupboards');
INSERT INTO CATEGORIES (CATEGORY_NAME, DESCRIPTION) VALUES ('Cleaning',   'Classroom, washroom, canteen and hall cleanliness');
INSERT INTO CATEGORIES (CATEGORY_NAME, DESCRIPTION) VALUES ('Internet',   'Wi-Fi and network connectivity problems');

COMMIT;


SELECT * FROM USERS;

SELECT * FROM CATEGORIES;