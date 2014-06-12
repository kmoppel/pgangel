select nspname
  from (select nspname, row_number() over (partition by regexp_replace(nspname, '_r[0-9_]+$', '') order by nspname desc) ord
          from pg_namespace
         where nspname not like 'pg_%'
           and nspname <> 'public'
        ) nsp
 where ord = 1;
