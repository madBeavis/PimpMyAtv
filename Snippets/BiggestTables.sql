SELECT table_schema, table_name,
  ROUND((data_length+index_length)/POWER(1024,2),2) AS tablesize_mb
FROM information_schema.tables
ORDER BY tablesize_mb DESC LIMIT 20;
