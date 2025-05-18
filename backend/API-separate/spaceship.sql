create table spaceship(
id int unsigned auto_increment primary key,
maxweight float(30),
captainid int unsigned,
FOREIGN KEY(captainid) references captain(id)
)

select* from spaceship