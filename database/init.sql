CREATE TABLE IF NOT EXISTS reservations (
    id VARCHAR PRIMARY KEY,
    nom TEXT NOT NULL,
    date TEXT NOT NULL,
    personnes TEXT NOT NULL,
    telephone TEXT NOT NULL,
    commentaire TEXT
);
