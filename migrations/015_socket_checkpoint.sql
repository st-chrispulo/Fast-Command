CREATE TABLE tbl_socket_event_log (
    id SERIAL PRIMARY KEY,
    room TEXT,
    event_type TEXT,
    data JSONB,
    timestamp TIMESTAMP NOT NULL
);
