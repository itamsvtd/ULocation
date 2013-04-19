drop table if exists entries;
create table location (
  id integer primary key autoincrement,
  lat string not null,
  lng string not null,
  address string not null,
  name string not null
);
