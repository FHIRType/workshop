create table test
(
    id   integer not null
        constraint test_pk
            primary key,
    name varchar
);

alter table test
    owner to postgres;

