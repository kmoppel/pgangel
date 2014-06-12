select datname
  from pg_databases
 where not datistemplate;
