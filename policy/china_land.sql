drop database china_land;

create database china_land;
use china_land;
create table public(
    id int auto_increment primary key,
    pid varchar(20) UNIQUE,
    region varchar(50),    
    province varchar(20),
    city varchar(20),
    xian varchar(20),
    title varchar(300),
    date_out varchar(30),
    open_during varchar(50),
    content text(5000),
    url varchar(300) UNIQUE,
    update_time datetime
);
create table zongdi(
    id int auto_increment primary key,
    pid varchar(20),
    date_out varchar(30),
    zongdi varchar(200),
	region varchar(50),    
    province varchar(20),
    city varchar(20),
    xian varchar(20),
    project varchar(100),
    address varchar(200),
    useness varchar(50),
    area varchar(30),
    years varchar(20),
    price varchar(20),
    receiver varchar(100),
    tiaojian varchar(600),
    update_time datetime
);
alter table zongdi add unique index zongdi_and_date (zongdi, date_out);
use china_land;
ALTER TABLE public CONVERT TO CHARACTER SET utf8mb4;
ALTER TABLE zongdi CONVERT TO CHARACTER SET utf8mb4;

SET SQL_SAFE_UPDATES = 0;
delete from public;
delete from zongdi;
