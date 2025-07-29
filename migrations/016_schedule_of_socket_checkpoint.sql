INSERT INTO tbl_scheduled_jobs (
    command,
    payload,
    cron_expression,
    output_directory,
    enabled,
    last_run_at,
    next_run_at
)
VALUES (
    'socket_event_checkpoint',
    '{}'::jsonb,
    '*/5 * * * *',
    NULL,
    true,
    NULL,
    NOW()
);
