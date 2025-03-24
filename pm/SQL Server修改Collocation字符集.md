由于之前创建数据库忘记了设置Collocation，数据库中插入中文字符都是乱码，于是到DataBase的Options中修改Collocation，出现了The database could not be exclusively locked to perform the operation这个错误，无法修改字符集为Chinese_PRC_90_CI_AS。

解决办法找了很久才找到，如下：

1.修改为单用户模式,执行SQL:
```sql
ALTER DATABASE db_database SET SINGLE_USER WITH ROLLBACK IMMEDIATE
```

2.然后关闭所有的查询窗口，修改Options的Collocation属性为Chinese_PRC_90_CI_AS
```sql
ALTER DATABASE db_database COLLATE Chinese_RPC_90_CI_AS
```

3.再修改为多用户模式
```sql
ALTER DATABASE db_database SET MULTI_USER
```

**总结**
```sql
ALTER DATABASE ECRS_NEW SET SINGLE_USER WITH ROLLBACK IMMEDIATE
go
ALTER DATABASE ECRS_NEW
COLLATE Chinese_PRC_CI_AS
GO
ALTER DATABASE ECRS_NEW SET MULTI_USER
```