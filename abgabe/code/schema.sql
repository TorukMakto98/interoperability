DROP TABLE IF EXISTS cpee_requests;
DROP TABLE IF EXISTS production_requests;

CREATE TABLE cpee_requests (
    Cpee_Callback_id TEXT PRIMARY KEY,
    created TEXT NOT NULL,
    Cpee_Callback_url TEXT NOT NULL,
    Cpee_Activity TEXT NOT NULL,
    Cpee_uuid TEXT NOT NULL,
    Cpee_instance TEXT NOT NULL,
    Process_finished INTEGER,
    pid TEXT NOT NULL
);

CREATE TABLE production_requests (
    pid TEXT,
    created TEXT NOT NULL,
    completion INTEGER NOT NULL,
    progress_state TEXT NOT NULL
);
