-- MBTI backend tables for server.py (Supabase Postgres)
-- Run in Supabase SQL editor if tables do not already exist.

create table if not exists public.mbti_redeem_codes (
  code text primary key,
  self_used integer not null default 0,
  peer_used integer not null default 0,
  total_used integer not null default 0,
  assessment_id text,
  updated_at timestamptz not null default now()
);

create table if not exists public.mbti_assessment_sessions (
  assessment_id text primary key,
  code text not null,
  super boolean not null default false,
  invite_token text not null,
  self_submitted boolean not null default false,
  peer_submitted boolean not null default false,
  self_scores jsonb,
  peer_scores jsonb,
  self_type text not null default '',
  peer_type text not null default '',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_mbti_assessment_code
  on public.mbti_assessment_sessions(code);

create index if not exists idx_mbti_assessment_invite_token
  on public.mbti_assessment_sessions(invite_token);

