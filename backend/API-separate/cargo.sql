create table if not exists cargo (
id int unsigned auto_increment primary key,
weight float(30) not null,
cargotype varchar(30),
departure date,
arrival date,
shipid int unsigned,
FOREIGN KEY(shipid) references spaceship(id)
)

select * from cargo;



