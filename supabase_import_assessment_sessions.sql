-- Auto generated from assessment_sessions.json
-- Import all assessment sessions into Supabase

insert into public.mbti_assessment_sessions
(assessment_id, code, super, invite_token, self_submitted, peer_submitted, self_scores, peer_scores, self_type, peer_type, created_at, updated_at)
values
('ast_0u8RMKf5ze3pEg', 'INLIGHT', true, 'inv_YLbShIR7Bpio3Q', true, true, '{"E":2,"I":5,"S":1,"N":6,"T":7,"F":0,"J":4,"P":3}'::jsonb, '{"E":4,"I":3,"S":0,"N":7,"T":0,"F":7,"J":0,"P":7}'::jsonb, 'INTJ', 'ENFP', '2026-02-18T05:35:52.835269+00:00'::timestamptz, '2026-02-18T07:34:15.194696+00:00'::timestamptz),
('ast_-k45C4OWc2XnYw', 'INLIGHT', true, 'inv_yQ0Zfe0e5Hyv7A', true, true, '{"E":5,"I":2,"S":2,"N":5,"T":4,"F":3,"J":2,"P":5}'::jsonb, '{"E":1,"I":6,"S":4,"N":3,"T":3,"F":4,"J":5,"P":2}'::jsonb, 'ENTP', 'ISFJ', '2026-02-18T05:42:04.430182+00:00'::timestamptz, '2026-02-18T06:43:22.337358+00:00'::timestamptz),
('ast__RA6LqvZX7UsXA', 'INLIGHT', true, 'inv_QG_RrMw5bUxBSw', true, true, '{"E":4,"I":3,"S":3,"N":4,"T":3,"F":4,"J":4,"P":3}'::jsonb, '{"E":5,"I":2,"S":4,"N":3,"T":4,"F":3,"J":3,"P":4}'::jsonb, 'ENFJ', 'ESTP', '2026-02-18T05:44:34.366965+00:00'::timestamptz, '2026-02-18T05:45:25.597985+00:00'::timestamptz),
('ast__dNjIjI5vjAcfw', 'INLIGHT', true, 'inv_Xo5rmra_jOvTxQ', false, false, NULL, NULL, '', '', '2026-02-18T05:45:54.492681+00:00'::timestamptz, '2026-02-18T05:45:54.492714+00:00'::timestamptz),
('ast_NwMD1oKFcmgS-Q', 'INLIGHT', true, 'inv_jS4vjsL3u8I4Jw', true, true, '{"E":7,"I":0,"S":1,"N":6,"T":5,"F":2,"J":3,"P":4}'::jsonb, '{"E":7,"I":0,"S":3,"N":4,"T":3,"F":4,"J":6,"P":1}'::jsonb, 'ENTP', 'ENFJ', '2026-02-18T05:48:53.105725+00:00'::timestamptz, '2026-02-18T05:49:40.732043+00:00'::timestamptz),
('ast_KixiEibct75XDg', 'INLIGHT', true, 'inv_hnPJx0e-hLK3Eg', true, true, '{"E":5,"I":2,"S":7,"N":0,"T":1,"F":6,"J":6,"P":1}'::jsonb, '{"E":6,"I":1,"S":2,"N":5,"T":4,"F":3,"J":2,"P":5}'::jsonb, 'ESFJ', 'ENTP', '2026-02-18T05:50:40.938082+00:00'::timestamptz, '2026-02-18T05:51:26.393030+00:00'::timestamptz),
('ast_lJoo9rVjuCuVmA', 'INLIGHT', true, 'inv_1E6aQQTEu_uYRw', true, true, '{"E":3,"I":4,"S":4,"N":3,"T":3,"F":4,"J":3,"P":4}'::jsonb, '{"E":3,"I":4,"S":1,"N":6,"T":4,"F":3,"J":3,"P":4}'::jsonb, 'ISFP', 'INTP', '2026-02-18T06:20:17.008777+00:00'::timestamptz, '2026-02-18T06:22:15.476405+00:00'::timestamptz),
('ast_N9ittEBdb69LAg', 'DJIBL781', false, 'inv_X15eCtnBHhQbsw', true, true, '{"E":4,"I":3,"S":4,"N":3,"T":6,"F":1,"J":3,"P":4}'::jsonb, '{"E":5,"I":2,"S":1,"N":6,"T":3,"F":4,"J":1,"P":6}'::jsonb, 'ESTP', 'ENFP', '2026-02-18T06:29:37.081127+00:00'::timestamptz, '2026-02-18T06:31:03.223649+00:00'::timestamptz),
('ast_4qJh7-ngXDoxkA', 'INLIGHT', true, 'inv_-r60OkgkW_w-vA', true, true, '{"E":2,"I":5,"S":0,"N":7,"T":0,"F":7,"J":2,"P":5}'::jsonb, '{"E":1,"I":6,"S":4,"N":3,"T":0,"F":7,"J":1,"P":6}'::jsonb, 'INFP', 'ISFP', '2026-02-18T06:39:38.206223+00:00'::timestamptz, '2026-02-18T06:40:24.101978+00:00'::timestamptz),
('ast_eEtX9wwXpwCmaA', 'INLIGHT', true, 'inv_Ko6Y9Byn49C09Q', true, true, '{"E":1,"I":6,"S":3,"N":4,"T":7,"F":0,"J":1,"P":6}'::jsonb, '{"E":7,"I":0,"S":7,"N":0,"T":2,"F":5,"J":0,"P":7}'::jsonb, 'INTP', 'ESFP', '2026-02-18T07:08:09.068489+00:00'::timestamptz, '2026-02-18T07:08:52.857556+00:00'::timestamptz),
('ast_v8kR4hsPSY3lIA', 'INLIGHT', true, 'inv_AYEkXCd6NDc9Sg', true, true, '{"E":7,"I":0,"S":7,"N":0,"T":7,"F":0,"J":7,"P":0}'::jsonb, '{"E":7,"I":0,"S":2,"N":5,"T":0,"F":7,"J":3,"P":4}'::jsonb, 'ESTJ', 'ENFP', '2026-02-18T07:14:26.601651+00:00'::timestamptz, '2026-02-18T07:15:24.603325+00:00'::timestamptz),
('ast_te8uKtVaUPlRiw', 'INLIGHT', true, 'inv_eunIKv7Flh2Ukw', true, true, '{"E":6,"I":1,"S":7,"N":0,"T":1,"F":6,"J":0,"P":7}'::jsonb, '{"E":7,"I":0,"S":7,"N":0,"T":0,"F":7,"J":6,"P":1}'::jsonb, 'ESFP', 'ESFJ', '2026-02-18T07:25:10.173397+00:00'::timestamptz, '2026-02-18T07:26:02.936112+00:00'::timestamptz),
('ast_Ctcphas99TkREg', 'INLIGHT', true, 'inv_Ieflmlh-qicneg', true, true, '{"E":1,"I":6,"S":0,"N":7,"T":7,"F":0,"J":6,"P":1}'::jsonb, '{"E":6,"I":1,"S":6,"N":1,"T":0,"F":7,"J":5,"P":2}'::jsonb, 'INTJ', 'ESFJ', '2026-02-18T07:48:53.687963+00:00'::timestamptz, '2026-02-18T07:49:53.316048+00:00'::timestamptz),
('ast_mEeB6WqQygYZsQ', 'INLIGHT', true, 'inv_uw6GAmQz0nWKkg', false, false, NULL, NULL, '', '', '2026-02-18T08:00:31.827102+00:00'::timestamptz, '2026-02-18T08:00:31.827156+00:00'::timestamptz),
('ast_GFrfVhaumqiSig', 'INLIGHT', true, 'inv_p6vIxR4AsAbluQ', true, true, '{"E":7,"I":0,"S":7,"N":0,"T":7,"F":0,"J":7,"P":0}'::jsonb, '{"E":7,"I":0,"S":7,"N":0,"T":7,"F":0,"J":7,"P":0}'::jsonb, 'ESTJ', 'ESTJ', '2026-02-18T08:00:51.120044+00:00'::timestamptz, '2026-02-18T08:01:36.597426+00:00'::timestamptz),
('ast_NmbnFfmUn2QYCA', 'INLIGHT', true, 'inv_Fm3IdSsmDgJ1OQ', true, true, '{"E":6,"I":1,"S":2,"N":5,"T":3,"F":4,"J":3,"P":4}'::jsonb, '{"E":0,"I":7,"S":7,"N":0,"T":0,"F":7,"J":6,"P":1}'::jsonb, 'ENFP', 'ISFJ', '2026-02-18T09:06:32.978490+00:00'::timestamptz, '2026-02-18T11:41:05.388540+00:00'::timestamptz),
('ast_8qrstAwSxr5Fig', 'INLIGHT', true, 'inv_I5SibpEsm7krpw', true, true, '{"E":6,"I":1,"S":1,"N":6,"T":4,"F":3,"J":3,"P":4}'::jsonb, '{"E":5,"I":2,"S":7,"N":0,"T":1,"F":6,"J":0,"P":7}'::jsonb, 'ENTP', 'ESFP', '2026-02-18T09:09:10.819856+00:00'::timestamptz, '2026-02-18T09:10:11.692405+00:00'::timestamptz)
on conflict (assessment_id) do update set
  code = excluded.code,
  super = excluded.super,
  invite_token = excluded.invite_token,
  self_submitted = excluded.self_submitted,
  peer_submitted = excluded.peer_submitted,
  self_scores = excluded.self_scores,
  peer_scores = excluded.peer_scores,
  self_type = excluded.self_type,
  peer_type = excluded.peer_type,
  created_at = excluded.created_at,
  updated_at = excluded.updated_at;
