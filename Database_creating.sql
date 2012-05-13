create table categories (
       cat_id serial primary key,
       cat_name varchar(20) not null,
       parent_cat_id integer references categories(cat_id)
);
create table characteristics (
       ch_id serial primary key,
       ch_name varchar(50) not null,
       ch_type varchar(5) not null
);
create table categories_characteristics (
       cat_id integer references categories(cat_id),
       ch_id integer references characteristics(ch_id),
       primary key (cat_id, ch_id)
);
create table commodities (
       com_id serial primary key,
       com_name varchar(40) not null,
       cat_id integer references categories(cat_id),
       price_p integer check (price_p>1 OR price_p<1000000),
       price_r integer check (price_r>1 OR price_r<1000000)
);
create table commodities_characteristics (
       com_id integer references commodities(com_id),
       ch_id integer references characteristics(ch_id),
       value varchar(30),
       primary key (com_id, ch_id)
);
create user reader with password '000000';
grant select on categories,characteristics,categories_characteristics,
                commodities,commodities_characteristics to reader;



       






