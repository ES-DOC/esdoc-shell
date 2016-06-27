/* Grant schema permissions */
GRANT USAGE ON SCHEMA docs, facets TO esdoc_db_user;

/* Grant table permissions */
GRANT INSERT, UPDATE, DELETE, SELECT ON ALL TABLES IN SCHEMA docs TO esdoc_db_user;
GRANT INSERT, UPDATE, DELETE, SELECT ON ALL TABLES IN SCHEMA facets TO esdoc_db_user;

/* Grant sequence permissions */
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA docs TO esdoc_db_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA facets TO esdoc_db_user;
