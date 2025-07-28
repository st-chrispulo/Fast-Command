CREATE TABLE tbl_user_avatars (
    id SERIAL PRIMARY KEY,
    user_id SERIAL NOT NULL,
    filename TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_user_avatar FOREIGN KEY (user_id) REFERENCES tbl_users(id) ON DELETE CASCADE
);
