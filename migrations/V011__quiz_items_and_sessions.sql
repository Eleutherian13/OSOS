-- Level 10 Prompt 1 — Quiz item + session additive migration (V011)
-- Idempotent; preserves V001-V010; no destructive change
create table if not exists quiz_items (
    id uuid primary key default gen_random_uuid(),
    path_id uuid references paths(id) on delete cascade,
    task_id uuid references tasks(id) on delete set null,
    question text not null,
    reference_answer text not null,
    evidence_locations text[],  -- file:line references; validated at creation
    rubric_json jsonb not null default '[]',  -- 2-4 checkable facts; validated 2<=len<=4
    status text not null default 'draft' check (status in ('draft','verified','stale','retired')),
    provenance_src text not null default 'author',  -- author / generated / verified / stale
    provenance_version text,  -- code/commit version when evidence frozen
    reference_answer_version uuid,  -- version of reference answer used
    rubric_version uuid,
    created_at timestamp with time zone not null default now(),
    verified_at timestamp with time zone,
    verified_by text,
    updated_at timestamp with time zone not null default now()
);

create index if not exists idx_quiz_path on quiz_items(path_id, status);
create index if not exists idx_quiz_verified on quiz_items(status, verified_at) where status = 'verified';

create table if not exists quiz_sessions (
    id uuid primary key default gen_random_uuid(),
    quiz_item_ids uuid[] not null default '{}',
    submitted_answers jsonb not null default '{}',  -- item_id -> answer text
    rubric_version_refs uuid[],
    grader_output jsonb not null default '{}',  -- fact results + computed
    session_timestamp timestamp with time zone not null default now(),
    code_version_ref text,  -- commit or content hash
    evidence_version_refs text[],
    result text check (result in ('PASS','FAIL','UNRESOLVED')),
    pass_pct decimal(5,2),
    retry_history jsonb default '[]',
    created_at timestamp with time zone not null default now()
);

create index if not exists idx_quiz_session_time on quiz_sessions(session_timestamp desc);
