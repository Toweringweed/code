drop database house;
create database house;
use house;
create table basis(
	id int auto_increment primary key,
    uid varchar(20),
    pici int(6),
    k int(6),
    title varchar(80),
	zongjia varchar(20),
    price_i varchar(20),
	huxing varchar(20),
	mianji varchar(20),
	chaoxiang varchar(10),
    jianzhuniandai varchar(20),
	cengji varchar(10),
	zongcenggao int(5),	
	xiaoqu varchar(50),
	quyu varchar(30),
	jiedao varchar(50),
    tags varchar(80),
    date_time varchar(20)  
);
create index basis_uid on basis(uid);
create table price(
	id int auto_increment primary key,
    uid varchar(20),
    zongjia varchar(20),
    price_i varchar(20),
    date_time varchar(20)     
	
);
create index price_uid on price(uid);

