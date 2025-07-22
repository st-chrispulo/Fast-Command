CREATE TABLE tbl_job_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID NOT NULL,
    job_type TEXT NOT NULL CHECK (job_type IN ('queued', 'scheduled')),
    command TEXT NOT NULL,
    payload JSONB NOT NULL,
    output_directory TEXT,
    result JSONB,
    error_message TEXT,
    status TEXT NOT NULL CHECK (status IN ('processing', 'done', 'failed')),
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    finished_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_queued_job FOREIGN KEY (job_id) REFERENCES tbl_queued_jobs(id)
);
