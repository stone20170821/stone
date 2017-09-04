drop database :database_name;
create database :database_name with template :template_name owner :owner_name;
grant all PRIVILEGES on database :database_name to :owner_name;
