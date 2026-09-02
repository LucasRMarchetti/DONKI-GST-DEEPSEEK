-- Criação da tabela de eventos solares
CREATE TABLE IF NOT EXISTS eventos_solares (
    id BIGSERIAL PRIMARY KEY,
    gst_id TEXT UNIQUE NOT NULL,
    start_time TIMESTAMP,
    kp_index FLOAT,
    source TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_eventos_start_time ON eventos_solares (start_time);
ALTER TABLE eventos_solares ENABLE ROW LEVEL SECURITY;
CREATE POLICY select_all_policy ON eventos_solares FOR SELECT USING (true);
CREATE POLICY insert_authenticated_policy ON eventos_solares FOR INSERT WITH CHECK (auth.role() = 'authenticated');
GRANT SELECT ON eventos_solares TO anon, authenticated;
GRANT ALL ON eventos_solares TO service_role;
