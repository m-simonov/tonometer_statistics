CREATE TABLE users(
   tid INTEGER PRIMARY KEY,
   username VARCHAR(255),
   first_name VARCHAR(25),
   last_name VARCHAR(25)
);

CREATE TABLE meterings(
    id INTEGER PRIMARY KEY,
    user INTEGER NOT NULL,
    date DATE NOT NULL,
    morning VARCHAR(11),
    afternoon VARCHAR(11),
    evening VARCHAR(11),
    FOREIGN KEY(user) REFERENCES users(tid)
);

CREATE TABLE access_rights(
    id INTEGER PRIMARY KEY,
    user INTEGER NOT NULL,
    open_for INTEGER,
    FOREIGN KEY(user) REFERENCES users(tid),
    FOREIGN KEY(open_for) REFERENCES users(tid) 
);