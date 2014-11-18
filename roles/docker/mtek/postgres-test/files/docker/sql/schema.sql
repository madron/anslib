CREATE USER test WITH ENCRYPTED PASSWORD 'test' ;
CREATE DATABASE test WITH OWNER test;
\c test;
SET ROLE test;

CREATE TABLE log (
    id              SERIAL,
    insert_time     timestamp   not null default CURRENT_TIMESTAMP,
    data            text        default repeat('1234567890ABCDEF', 64)
);
CREATE TABLE bytea (
    id              SERIAL,
    insert_time     timestamp   not null default CURRENT_TIMESTAMP,
    bytea           bytea
);

create or replace function bytea_import(p_path text, p_result out bytea)
                   language plpgsql as $$
declare
  l_oid oid;
  r record;
begin
  p_result := '';
  select lo_import(p_path) into l_oid;
  for r in ( select data
             from pg_largeobject
             where loid = l_oid
             order by pageno ) loop
    p_result = p_result || r.data;
  end loop;
  perform lo_unlink(l_oid);
end;$$;
